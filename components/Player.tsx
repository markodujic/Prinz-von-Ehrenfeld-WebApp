import React, {useEffect, useRef, useState} from 'react';
import {View, StyleSheet, Pressable, Text, Image} from 'react-native';

type GamePlatform = {
  x: number;
  y: number;
  width: number;
  height: number;
  solid?: boolean;
};

type CollectibleHit = {
  id: string;
  x: number;
  y: number;
  size: number;  // Breite & Höhe des Collectibles
};

type Props = {
  startX?: number;
  groundY?: number;
  containerWidth?: number;
  platforms?: GamePlatform[];
  collectibles?: CollectibleHit[];
  onCollectItem?: (id: string) => void;
  onTakeDamage?: () => void;
  onPositionChange?: (pos: { x: number; y: number }) => void;
  onJump?: () => void;
};

const SIZE = 64;      // Sprite-Größe (unveränderlich für Rendering)

// Hitbox: bündig zum Körper (ohne Rucksack und Randbereich)
// Gemessen am generierten Sprite: Körper bei x≈22–38, y≈13–61
const HIT_OFFSET_X = 20; // px vom Sprite-Linksrand bis Hitbox-Linksrand
const HIT_OFFSET_Y = 12; // px vom Sprite-Obenrand bis Kopf
const HIT_W        = 18; // Körperbreite
const HIT_H        = 49; // Körperhöhe (bis Fußsohle bei y=61)

const GRAVITY      = 1500; // px/s^2
const MOVE_SPEED   = 300;  // px/s
const JUMP_VELOCITY = -650; // px/s
const RUN_FPS  = 12; // Frames pro Sekunde der Lauf-Animation
const IDLE_FPS =  8; // Frames pro Sekunde der Idle-Animation

// Alle 8 Run-Frames vorgeladen
const RUN_FRAMES = [
  require('../assets/sprites/Kev_run_1.png'),
  require('../assets/sprites/Kev_run_2.png'),
  require('../assets/sprites/Kev_run_3.png'),
  require('../assets/sprites/Kev_run_4.png'),
  require('../assets/sprites/Kev_run_5.png'),
  require('../assets/sprites/Kev_run_6.png'),
  require('../assets/sprites/Kev_run_7.png'),
  require('../assets/sprites/Kev_run_8.png'),
];

// 6 Idle-Frames (Atemanimation + Blinzeln)
const IDLE_FRAMES = [
  require('../assets/sprites/Kev_idle_1.png'),
  require('../assets/sprites/Kev_idle_2.png'),
  require('../assets/sprites/Kev_idle_3.png'),
  require('../assets/sprites/Kev_idle_4.png'),
  require('../assets/sprites/Kev_idle_5.png'),
  require('../assets/sprites/Kev_idle_6.png'),
];

// Für Sprung nehmen wir vorerst Frame 3 (Beine auseinander)
const JUMP_FRAME = require('../assets/sprites/Kev_run_3.png');

export default function Player({
  startX = 100, groundY = 500, containerWidth = 800,
  platforms = [],
  collectibles = [],
  onCollectItem,
  onTakeDamage,
  onPositionChange,
  onJump,
}: Props) {
  // pos = Sprite-Top-Left; Hitbox = pos + HIT_OFFSET_*
  const initY = groundY - HIT_OFFSET_Y - HIT_H;
  const [pos, setPos] = useState({x: startX, y: initY});
  const [spriteFrame, setSpriteFrame] = useState<number>(100);
  const [facingLeft, setFacingLeft] = useState(false);
  const posRef = useRef({x: startX, y: initY});
  const vel = useRef({x: 0, y: 0});
  const onGroundRef = useRef(true);
  const platformsRef = useRef(platforms);
  const collectiblesRef = useRef(collectibles);
  const onCollectItemRef = useRef(onCollectItem);
  const onTakeDamageRef  = useRef(onTakeDamage);
  const onPositionChangeRef = useRef(onPositionChange);
  const onJumpRef = useRef(onJump);
  const frameTimeRef = useRef(0); // akkumulierte Zeit für Frame-Wechsel
  const frameIdxRef  = useRef(0); // aktueller Run-Frame-Index
  const idleTimeRef  = useRef(0); // akkumulierte Zeit für Idle-Frame-Wechsel
  const idleIdxRef   = useRef(0); // aktueller Idle-Frame-Index
  const keys = useRef<{[k: string]: boolean}>({});
  const rafRef = useRef<number | null>(null);
  const lastRef = useRef<number | null>(null);

  // keep refs in sync without restarting the RAF loop
  useEffect(() => { platformsRef.current = platforms; }, [platforms]);
  useEffect(() => { collectiblesRef.current = collectibles; }, [collectibles]);
  useEffect(() => { onCollectItemRef.current = onCollectItem; }, [onCollectItem]);
  useEffect(() => { onTakeDamageRef.current = onTakeDamage; }, [onTakeDamage]);
  useEffect(() => { onPositionChangeRef.current = onPositionChange; }, [onPositionChange]);
  useEffect(() => { onJumpRef.current = onJump; }, [onJump]);

  useEffect(() => {
    function down(e: KeyboardEvent) {
      keys.current[e.code] = true;
    }
    function up(e: KeyboardEvent) {
      keys.current[e.code] = false;
    }
    window.addEventListener('keydown', down);
    window.addEventListener('keyup', up);
    return () => {
      window.removeEventListener('keydown', down);
      window.removeEventListener('keyup', up);
    };
  }, []);

  useEffect(() => {
    // Single RAF loop; do not re-create on every position change.
    const step = (t: number) => {
      if (lastRef.current == null) lastRef.current = t;
      const dt = (t - lastRef.current) / 1000; // seconds
      lastRef.current = t;

      // input
      const left = keys.current['ArrowLeft'] || keys.current['KeyA'] || keys.current['TouchLeft'];
      const right = keys.current['ArrowRight'] || keys.current['KeyD'] || keys.current['TouchRight'];
      const jump = keys.current['Space'];

      vel.current.x = 0;
      if (left) vel.current.x = -MOVE_SPEED;
      if (right) vel.current.x = MOVE_SPEED;

      // jump (only from ground or platform)
      if (jump && onGroundRef.current) {
        vel.current.y = JUMP_VELOCITY;
        onGroundRef.current = false;
        onJumpRef.current?.();
      }

      // physics
      vel.current.y += GRAVITY * dt;
      // X: Sprite bleibt so, dass Hitbox im Spielfeld bleibt
      const nextX = Math.max(
        -HIT_OFFSET_X,
        Math.min(containerWidth - HIT_OFFSET_X - HIT_W, posRef.current.x + vel.current.x * dt)
      );
      let nextY = posRef.current.y + vel.current.y * dt;

      let landed = false;

      // platform collision
      for (const p of platformsRef.current) {
        const hbX     = nextX + HIT_OFFSET_X;
        const overlapX = hbX + HIT_W > p.x && hbX < p.x + p.width;

        // top collision
        const feetY   = nextY + HIT_OFFSET_Y + HIT_H;
        const prevFeetY = posRef.current.y + HIT_OFFSET_Y + HIT_H;
        const feetReach = feetY >= p.y;
        const wasAbove  = prevFeetY <= p.y + 6;
        if (overlapX && feetReach && wasAbove && vel.current.y >= 0) {
          nextY = p.y - HIT_OFFSET_Y - HIT_H;
          vel.current.y = 0;
          landed = true;
          break;
        }

        // bottom collision (solid platforms only)
        if (p.solid) {
          const headY        = nextY + HIT_OFFSET_Y;
          const prevHeadY    = posRef.current.y + HIT_OFFSET_Y;
          const headHitsBottom   = headY <= p.y + p.height;
          const wasBelowPlatform = prevHeadY >= p.y + p.height - 6;
          if (overlapX && headHitsBottom && wasBelowPlatform && vel.current.y < 0) {
            nextY = p.y + p.height - HIT_OFFSET_Y;
            vel.current.y = 0;
          }
        }
      }

      // ground collision
      if (nextY + HIT_OFFSET_Y + HIT_H >= groundY) {
        nextY = groundY - HIT_OFFSET_Y - HIT_H;
        vel.current.y = 0;
        landed = true;
      }

      onGroundRef.current = landed;

      // Animations-State bestimmen
      const isMoving = vel.current.x !== 0;
      let newFrame: number;
      if (!landed) {
        newFrame = -2; // Sprung
      } else if (isMoving) {
        frameTimeRef.current += dt;
        if (frameTimeRef.current >= 1 / RUN_FPS) {
          frameTimeRef.current = 0;
          frameIdxRef.current = (frameIdxRef.current + 1) % 8;
        }
        idleTimeRef.current = 0;
        newFrame = frameIdxRef.current;
      } else {
        // Idle-Animation
        frameTimeRef.current = 0;
        frameIdxRef.current  = 0;
        idleTimeRef.current += dt;
        if (idleTimeRef.current >= 1 / IDLE_FPS) {
          idleTimeRef.current = 0;
          idleIdxRef.current = (idleIdxRef.current + 1) % 6;
        }
        newFrame = 100 + idleIdxRef.current; // 100–105 = Idle-Frames
      }

      // Collectible-Kollision prüfen
      const hbX2 = nextX + HIT_OFFSET_X;
      const hbY2 = nextY + HIT_OFFSET_Y;
      for (const c of collectiblesRef.current) {
        // Einfache AABB-Kolision: Spieler-Hitbox gegen Collectible-Box
        const overlapCX = hbX2 + HIT_W > c.x && hbX2 < c.x + c.size;
        const overlapCY = hbY2 + HIT_H > c.y - c.size && hbY2 < c.y;
        if (overlapCX && overlapCY) {
          onCollectItemRef.current?.(c.id);
        }
      }

      // update refs and state
      const newPos = {x: nextX, y: nextY};
      posRef.current = newPos;
      setPos(newPos);
      setSpriteFrame(newFrame);
      onPositionChangeRef.current?.(newPos);
      if (left) setFacingLeft(true);
      if (right) setFacingLeft(false);
      rafRef.current = requestAnimationFrame(step);
    };

    rafRef.current = requestAnimationFrame(step);
    return () => {
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
      lastRef.current = null;
    };
    // groundY and containerWidth affect physics bounds; re-run if they change.
  }, [groundY, containerWidth]);

  // simple on-screen controls for touch
  const pressLeft = () => (keys.current['TouchLeft'] = true);
  const releaseLeft = () => (keys.current['TouchLeft'] = false);
  const pressRight = () => (keys.current['TouchRight'] = true);
  const releaseRight = () => (keys.current['TouchRight'] = false);
  const pressJump = () => (keys.current['Space'] = true);
  const releaseJump = () => (keys.current['Space'] = false);

  const currentSource =
    spriteFrame === -2          ? JUMP_FRAME :
    spriteFrame >= 100          ? IDLE_FRAMES[spriteFrame - 100] :
    RUN_FRAMES[spriteFrame] ?? IDLE_FRAMES[0];

  return (
    <View style={styles.wrapper} pointerEvents="box-none">
      <Image
        source={currentSource}
        style={[
          styles.player,
          {left: pos.x, top: pos.y},
          facingLeft && styles.flipped,
        ]}
        resizeMode="contain"
      />

      {/* touch controls (visible on mobile / web) */}
      <View style={styles.controls} pointerEvents="box-none">
        <Pressable
          onPressIn={pressLeft}
          onPressOut={releaseLeft}
          style={styles.controlButton}
          accessibilityLabel="Left"
        >
          <Text style={styles.controlText}>◀</Text>
        </Pressable>
        <Pressable
          onPressIn={pressRight}
          onPressOut={releaseRight}
          style={styles.controlButton}
          accessibilityLabel="Right"
        >
          <Text style={styles.controlText}>▶</Text>
        </Pressable>
        <Pressable
          onPressIn={pressJump}
          onPressOut={releaseJump}
          style={[styles.controlButton, styles.jumpButton]}
          accessibilityLabel="Jump"
        >
          <Text style={styles.controlText}>↑</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    position: 'absolute',
    left: 0,
    top: 0,
    right: 0,
    bottom: 0,
  },
  player: {
    position: 'absolute',
    width: SIZE,
    height: SIZE,
    backgroundColor: 'transparent',
    borderRadius: 6,
    borderWidth: 0,
    borderColor: 'transparent',
    zIndex: 50,
  },
  flipped: {
    transform: [{scaleX: -1}],
  },
  controls: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    flexDirection: 'row',
    alignItems: 'center',
    zIndex: 60,
  } as any,
  controlButton: {
    width: 56,
    height: 56,
    backgroundColor: 'rgba(0,0,0,0.35)',
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 8,
  },
  jumpButton: {
    backgroundColor: 'rgba(0,0,0,0.45)'
  },
  controlText: {
    color: 'white',
    fontSize: 20,
    fontWeight: '700'
  }
});

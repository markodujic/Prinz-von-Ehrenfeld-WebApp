import React, { useEffect, useRef, useState } from 'react';
import { View, Image, StyleSheet } from 'react-native';
import type { EnemyDef, Platform } from '../constants/level1';

type Props = EnemyDef & {
  defeated: boolean;
  groundY: number;
  platforms: Platform[];
  onDamagePlayer: (enemyId: string) => void;
  onDefeated: (enemyId: string) => void;
  playerPos: { x: number; y: number };  // Sprite-Position des Spielers
};

// Physik-Konstanten (Tourist ist langsamer als Kev)
const GRAVITY       = 1500;
const WALK_SPEED    = 80;   // px/s
const FOTO_INTERVAL_MIN = 3.0;   // Sekunden zwischen Foto-Stops
const FOTO_INTERVAL_MAX = 6.0;
const FOTO_DURATION     = 1.8;   // Sekunden Foto-Stop

// Kev-Hitbox-Konstanten (müssen zum Player.tsx passen)
const KEV_HIT_OFFSET_X = 20;
const KEV_HIT_OFFSET_Y = 12;
const KEV_HIT_W        = 18;
const KEV_HIT_H        = 49;

// Tourist-Sprite-Größe
const SPRITE_W = 48;
const SPRITE_H = 64;
// Tourist-Hitbox (relativ zum Sprite)
const T_HIT_OFFSET_X = 10;
const T_HIT_OFFSET_Y = 10;
const T_HIT_W        = 28;
const T_HIT_H        = 50;

const WALK_FPS = 8;
const FOTO_FPS = 3;

const WALK_FRAMES = [
  require('../assets/sprites/Tourist_walk_1.png'),
  require('../assets/sprites/Tourist_walk_2.png'),
  require('../assets/sprites/Tourist_walk_3.png'),
  require('../assets/sprites/Tourist_walk_4.png'),
  require('../assets/sprites/Tourist_walk_5.png'),
  require('../assets/sprites/Tourist_walk_6.png'),
];
const FOTO_FRAMES = [
  require('../assets/sprites/Tourist_foto_1.png'),
  require('../assets/sprites/Tourist_foto_2.png'),
  require('../assets/sprites/Tourist_foto_3.png'),
];

type AIState = 'wander' | 'foto_stop';

export default function Enemy({
  id, x: startX, patrolMin, patrolMax,
  defeated, groundY, platforms,
  onDamagePlayer, onDefeated, playerPos,
}: Props) {
  const initY = groundY - T_HIT_OFFSET_Y - T_HIT_H;
  const [spritePos, setSpritePos] = useState({ x: startX, y: initY });
  const [frameIdx, setFrameIdx] = useState(0);
  const [aiState, setAIState] = useState<AIState>('wander');
  const [facingLeft, setFacingLeft] = useState(false);

  const posRef    = useRef({ x: startX, y: initY });
  const velY      = useRef(0);
  const dirRef    = useRef<1 | -1>(1);               // 1 = rechts, -1 = links
  const stateRef  = useRef<AIState>('wander');
  const fotoTimer = useRef(randomFotoInterval());
  const fotoElapsed = useRef(0);
  const frameTimeRef = useRef(0);
  const frameIdxRef  = useRef(0);
  const platformsRef = useRef(platforms);
  const playerPosRef = useRef(playerPos);
  const defeatedRef  = useRef(defeated);
  const damagedCooldown = useRef(0);  // Schaden-Cooldown (Sekunden)

  const rafRef  = useRef<number | null>(null);
  const lastRef = useRef<number | null>(null);

  useEffect(() => { platformsRef.current = platforms; }, [platforms]);
  useEffect(() => { playerPosRef.current = playerPos; }, [playerPos]);
  useEffect(() => { defeatedRef.current = defeated; }, [defeated]);

  function randomFotoInterval() {
    return FOTO_INTERVAL_MIN + Math.random() * (FOTO_INTERVAL_MAX - FOTO_INTERVAL_MIN);
  }

  useEffect(() => {
    if (defeated) {
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
      return;
    }

    const step = (t: number) => {
      if (defeatedRef.current) return;
      if (lastRef.current == null) lastRef.current = t;
      const dt = Math.min((t - lastRef.current) / 1000, 0.05);
      lastRef.current = t;

      const pos = posRef.current;
      const pp  = playerPosRef.current;

      // ----- Schaden-Cooldown -----
      if (damagedCooldown.current > 0) damagedCooldown.current -= dt;

      // ----- KI-Logik -----
      let vx = 0;

      if (stateRef.current === 'wander') {
        vx = dirRef.current * WALK_SPEED;

        // Umkehren an Patrol-Grenzen
        const spriteX = pos.x;
        if (spriteX <= patrolMin && dirRef.current === -1) dirRef.current = 1;
        if (spriteX + SPRITE_W >= patrolMax && dirRef.current === 1) dirRef.current = -1;

        // Foto-Stop-Timer
        fotoTimer.current -= dt;
        if (fotoTimer.current <= 0) {
          stateRef.current = 'foto_stop';
          setAIState('foto_stop');
          fotoElapsed.current = 0;
          fotoTimer.current = randomFotoInterval();
        }
      } else {
        // foto_stop: stehen bleiben
        vx = 0;
        fotoElapsed.current += dt;
        if (fotoElapsed.current >= FOTO_DURATION) {
          stateRef.current = 'wander';
          setAIState('wander');
        }
      }

      // ----- Physik (Y) -----
      velY.current += GRAVITY * dt;
      let nextX = pos.x + vx * dt;
      let nextY = pos.y + velY.current * dt;

      // Boden
      if (nextY + T_HIT_OFFSET_Y + T_HIT_H >= groundY) {
        nextY = groundY - T_HIT_OFFSET_Y - T_HIT_H;
        velY.current = 0;
      }

      // Plattform-Kollision (nur Top)
      for (const p of platformsRef.current) {
        const hbX = nextX + T_HIT_OFFSET_X;
        const overlapX = hbX + T_HIT_W > p.x && hbX < p.x + p.width;
        const feetY = nextY + T_HIT_OFFSET_Y + T_HIT_H;
        const prevFeetY = pos.y + T_HIT_OFFSET_Y + T_HIT_H;
        if (overlapX && feetY >= p.y && prevFeetY <= p.y + 6 && velY.current >= 0) {
          nextY = p.y - T_HIT_OFFSET_Y - T_HIT_H;
          velY.current = 0;
          break;
        }
      }

      // X-Begrenzung
      nextX = Math.max(patrolMin, Math.min(patrolMax - SPRITE_W, nextX));

      posRef.current = { x: nextX, y: nextY };
      setSpritePos({ x: nextX, y: nextY });

      if (vx > 0) setFacingLeft(false);
      if (vx < 0) setFacingLeft(true);

      // ----- Animation -----
      const frames = stateRef.current === 'wander' ? WALK_FRAMES : FOTO_FRAMES;
      const fps    = stateRef.current === 'wander' ? WALK_FPS : FOTO_FPS;
      const numFrames = frames.length;
      frameTimeRef.current += dt;
      if (frameTimeRef.current >= 1 / fps) {
        frameTimeRef.current = 0;
        frameIdxRef.current = (frameIdxRef.current + 1) % numFrames;
        setFrameIdx(frameIdxRef.current);
      }

      // ----- Kollision mit Kev -----
      if (damagedCooldown.current <= 0) {
        // Kev-Hitbox
        const kevHbX = pp.x + KEV_HIT_OFFSET_X;
        const kevHbY = pp.y + KEV_HIT_OFFSET_Y;
        // Tourist-Hitbox
        const tHbX = nextX + T_HIT_OFFSET_X;
        const tHbY = nextY + T_HIT_OFFSET_Y;

        const overlapX2 = kevHbX + KEV_HIT_W > tHbX && kevHbX < tHbX + T_HIT_W;
        const overlapY2 = kevHbY + KEV_HIT_H > tHbY && kevHbY < tHbY + T_HIT_H;

        if (overlapX2 && overlapY2) {
          // Stomp: Kev-Füße oberhalb der Tourist-Mitte, und Kev fällt
          const kevFeetY = kevHbY + KEV_HIT_H;
          const tMidY    = tHbY + T_HIT_H * 0.45;
          if (kevFeetY < tMidY + 10) {
            // Stomp-Kill
            onDefeated(id);
          } else {
            // Seitliche Kollision → Schaden
            onDamagePlayer(id);
            damagedCooldown.current = 1.5;
          }
        }
      }

      rafRef.current = requestAnimationFrame(step);
    };

    rafRef.current = requestAnimationFrame(step);
    return () => {
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
      lastRef.current = null;
    };
  }, [defeated, groundY, id, onDamagePlayer, onDefeated, patrolMax, patrolMin]);

  if (defeated) return null;

  const frames = aiState === 'wander' ? WALK_FRAMES : FOTO_FRAMES;
  const clampedIdx = Math.min(frameIdx, frames.length - 1);

  return (
    <View
      style={[
        styles.wrapper,
        { left: spritePos.x, top: spritePos.y },
      ]}
      pointerEvents="none"
    >
      <Image
        source={frames[clampedIdx]}
        style={[styles.sprite, facingLeft && styles.flipped]}
        resizeMode="contain"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    position: 'absolute',
    width: SPRITE_W,
    height: SPRITE_H,
  },
  sprite: {
    width: SPRITE_W,
    height: SPRITE_H,
  },
  flipped: {
    transform: [{ scaleX: -1 }],
  },
});

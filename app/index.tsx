import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import Player from '../components/Player';
import Collectible from '../components/Collectible';
import Enemy from '../components/Enemy';
import GameBackground from '../components/GameBackground';
import LevelComplete from '../components/LevelComplete';
import { useSound } from '../hooks/useSound';
import type { PlayerSnapshot } from '../components/Player';
import {
  LEVEL1_PLATFORMS,
  LEVEL1_COLLECTIBLES,
  LEVEL1_ENEMIES,
  LEVEL1_START_X,
  LEVEL1_GROUND_Y,
  LEVEL1_WIDTH,
  LEVEL1_SCORE_KOELSCH,
  LEVEL1_SCORE_STICKER,
} from '../constants/level1';

const COLLECTIBLE_SIZE = 32;
const INITIAL_LIVES = 3;
const BOTTLE_SPEED = 640;
const BOTTLE_ARC_HEIGHT = 28;
const BOTTLE_LIFETIME_MS = 860;
const BOTTLE_THROW_SPRITE = require('../assets/sprites/Bottle_throw.png');
const BOTTLE_SHATTER_SPRITE = require('../assets/sprites/Bottle_shatter.png');
const BOTTLE_SHATTER_LIFETIME_MS = 220;

type BottleThrow = {
  id: number;
  startX: number;
  startY: number;
  direction: 1 | -1;
  spawnTime: number;
};

type ActiveBottleThrow = BottleThrow & {
  x: number;
  y: number;
  rotationDeg: number;
  opacity: number;
};

type BottleBurst = {
  id: number;
  x: number;
  y: number;
  spawnTime: number;
};

type ActiveBottleBurst = BottleBurst & {
  opacity: number;
};

type DebugEvent = {
  id: number;
  label: string;
  detail: string;
};

function buildCollectibleHits(collectedIds: Set<string>) {
  return LEVEL1_COLLECTIBLES
    .filter(c => !collectedIds.has(c.id))
    .map(c => ({ id: c.id, x: c.x, y: c.y, size: COLLECTIBLE_SIZE }));
}

export default function Page() {
  const groundY        = LEVEL1_GROUND_Y;
  const containerWidth = LEVEL1_WIDTH;

  const [collectedIds, setCollectedIds]     = useState<Set<string>>(new Set());
  const [defeatedIds,  setDefeatedIds]      = useState<Set<string>>(new Set());
  const [lives,        setLives]            = useState(INITIAL_LIVES);
  const [score,        setScore]            = useState(0);
  const [levelComplete, setLevelComplete]   = useState(false);
  const [resetKey,     setResetKey]         = useState(0);   // Level neu starten
  const [playerSnapshot, setPlayerSnapshot] = useState<PlayerSnapshot | null>(null);
  const [debugEvents, setDebugEvents]       = useState<DebugEvent[]>([]);
  const [bottleThrows, setBottleThrows]     = useState<BottleThrow[]>([]);
  const [bottleBursts, setBottleBursts]     = useState<BottleBurst[]>([]);
  const [projectileNow, setProjectileNow]   = useState(() => Date.now());

  // Spieler-Position für Enemy-Kollisionscheck
  const playerPosRef = useRef({ x: LEVEL1_START_X, y: 0 });
  const playerSnapshotRef = useRef<PlayerSnapshot | null>(null);
  const defeatedIdsRef = useRef(defeatedIds);
  const [playerPos,  setPlayerPos]          = useState({ x: LEVEL1_START_X, y: 0 });
  const debugEventIdRef = useRef(1);
  const bottleIdRef = useRef(1);
  const bottleBurstIdRef = useRef(1);
  const consumedBottleIdsRef = useRef<Set<number>>(new Set());

  const { play } = useSound();

  // Damit onCollectItem keine unnötigen Re-Renders via dep-Array auslöst
  const collectedIdsRef = useRef(collectedIds);
  collectedIdsRef.current = collectedIds;
  defeatedIdsRef.current = defeatedIds;

  useEffect(() => {
    let raf = 0;
    const tick = () => {
      setProjectileNow(Date.now());
      raf = requestAnimationFrame(tick);
    };

    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  useEffect(() => {
    setBottleThrows(prev => {
      const next = prev.filter(bottle => projectileNow - bottle.spawnTime <= BOTTLE_LIFETIME_MS);
      return next.length === prev.length ? prev : next;
    });
    setBottleBursts(prev => {
      const next = prev.filter(burst => projectileNow - burst.spawnTime <= BOTTLE_SHATTER_LIFETIME_MS);
      return next.length === prev.length ? prev : next;
    });
  }, [projectileNow]);

  const activeBottleThrows: ActiveBottleThrow[] = useMemo(() => {
    return bottleThrows.flatMap(bottle => {
      const age = projectileNow - bottle.spawnTime;
      if (age < 0 || age > BOTTLE_LIFETIME_MS) return [];

      const progress = age / BOTTLE_LIFETIME_MS;
      const travel = BOTTLE_SPEED * (age / 1000);
      const spin = (progress * 540) + 24;
      return [{
        ...bottle,
        x: bottle.startX + bottle.direction * travel,
        y: bottle.startY - Math.sin(progress * Math.PI) * BOTTLE_ARC_HEIGHT,
        rotationDeg: bottle.direction === 1 ? spin : -spin,
        opacity: Math.max(0.25, 1 - progress * 0.22),
      }];
    });
  }, [bottleThrows, projectileNow]);

  const activeBottleBursts: ActiveBottleBurst[] = useMemo(() => {
    return bottleBursts.flatMap(burst => {
      const age = projectileNow - burst.spawnTime;
      if (age < 0 || age > BOTTLE_SHATTER_LIFETIME_MS) return [];

      const progress = age / BOTTLE_SHATTER_LIFETIME_MS;
      return [{
        ...burst,
        opacity: Math.max(0, 1 - progress),
      }];
    });
  }, [bottleBursts, projectileNow]);

  const pushDebugEvent = useCallback((label: string, detail: string) => {
    setDebugEvents(prev => {
      const next = [{ id: debugEventIdRef.current++, label, detail }, ...prev];
      return next.slice(0, 4);
    });
  }, []);

  const handleCollect = useCallback((id: string) => {
    if (collectedIdsRef.current.has(id)) return;
    const def = LEVEL1_COLLECTIBLES.find(c => c.id === id);
    pushDebugEvent('collect', `${id}${def ? ` (${def.type})` : ''}`);
    setCollectedIds(prev => {
      const next = new Set(prev);
      next.add(id);
      // Level-Ende prüfen
      if (next.size === LEVEL1_COLLECTIBLES.length) {
        setLevelComplete(true);
        play('level_complete');
      }
      return next;
    });
    if (def) {
      setScore(s => s + (def.type === 'koelsch' ? LEVEL1_SCORE_KOELSCH : LEVEL1_SCORE_STICKER));
      play(def.type === 'sticker' ? 'collect_sticker' : 'collect_koelsch');
    }
  }, [play, pushDebugEvent]);

  const handleTakeDamage = useCallback((_enemyId: string) => {
    pushDebugEvent('damage', `from ${_enemyId}`);
    setLives(l => Math.max(0, l - 1));
    play('damage');
  }, [play, pushDebugEvent]);

  const handleEnemyDefeated = useCallback((id: string) => {
    pushDebugEvent('defeat', id);
    setDefeatedIds(prev => {
      const next = new Set(prev);
      next.add(id);
      defeatedIdsRef.current = next;
      return next;
    });
    setScore(s => s + 25);
    play('stomp');
  }, [play, pushDebugEvent]);

  const handleBottleThrow = useCallback(() => {
    const snapshot = playerSnapshotRef.current;
    if (!snapshot) return;

    const direction: 1 | -1 = snapshot.facingLeft ? -1 : 1;
    const startX = snapshot.position.x + (direction === 1 ? 42 : -6);
    const startY = snapshot.position.y + 18;
    const id = bottleIdRef.current++;

    pushDebugEvent('throw', `bottle ${id}`);
    setBottleThrows(prev => [
      ...prev,
      {
        id,
        startX,
        startY,
        direction,
        spawnTime: Date.now(),
      },
    ]);
    play('throw_bottle');
  }, [play, pushDebugEvent]);

  const handleBottleHit = useCallback((enemyId: string, bottleId: string) => {
    const numericBottleId = Number(bottleId);
    if (consumedBottleIdsRef.current.has(numericBottleId)) return;
    consumedBottleIdsRef.current.add(numericBottleId);

    if (defeatedIdsRef.current.has(enemyId)) return;

    const bottle = activeBottleThrows.find(item => item.id === numericBottleId);
    if (bottle) {
      setBottleBursts(prev => [
        ...prev,
        {
          id: bottleBurstIdRef.current++,
          x: bottle.x,
          y: bottle.y,
          spawnTime: Date.now(),
        },
      ]);
    }

    pushDebugEvent('bottle', `${bottleId} -> ${enemyId}`);
    setBottleThrows(prev => prev.filter(bottle => bottle.id !== numericBottleId));
    setDefeatedIds(prev => {
      if (prev.has(enemyId)) return prev;
      const next = new Set(prev);
      next.add(enemyId);
      defeatedIdsRef.current = next;
      return next;
    });
    setScore(s => s + 25);
    play('bottle_hit');
  }, [activeBottleThrows, play, pushDebugEvent]);

  const handlePositionChange = useCallback((pos: { x: number; y: number }) => {
    playerPosRef.current = pos;
    setPlayerPos(pos);
  }, []);

  const handlePlayerSnapshot = useCallback((snapshot: PlayerSnapshot) => {
    playerSnapshotRef.current = snapshot;
    setPlayerSnapshot(snapshot);
  }, []);

  const handleRestart = useCallback(() => {
    pushDebugEvent('restart', 'reset level state');
    setCollectedIds(new Set());
    setDefeatedIds(new Set());
    defeatedIdsRef.current = new Set();
    setBottleThrows([]);
    consumedBottleIdsRef.current = new Set();
    playerSnapshotRef.current = null;
    setPlayerSnapshot(null);
    setLives(INITIAL_LIVES);
    setScore(0);
    setLevelComplete(false);
    setResetKey(k => k + 1);
  }, [pushDebugEvent]);

  const collectibleHits = useMemo(
    () => buildCollectibleHits(collectedIds),
    [collectedIds],
  );

  const kronenTotal  = LEVEL1_COLLECTIBLES.filter(c => c.type === 'koelsch').length;
  const stickerTotal = LEVEL1_COLLECTIBLES.filter(c => c.type === 'sticker').length;
  const kronenCollected  = [...collectedIds].filter(id => id.startsWith('k')).length;
  const stickerCollected = [...collectedIds].filter(id => id.startsWith('s')).length;

  return (
    <View style={styles.container}>
      <View style={styles.gameArea}>
        {/* Hintergrund */}
        <GameBackground />

        {/* Boden (semi-transparent, damit Hintergrund-Asphalt durchscheint) */}
        <View style={[styles.ground, { top: groundY }]} />

        {/* Plattformen */}
        {LEVEL1_PLATFORMS.map((p, i) => (
          <View
            key={i}
            style={[
              p.solid ? styles.platformSolid : styles.platform,
              { left: p.x, top: p.y, width: p.width, height: p.height },
            ]}
          />
        ))}

        {/* Collectibles */}
        {LEVEL1_COLLECTIBLES.map(c => (
          <Collectible
            key={`${c.id}-${resetKey}`}
            {...c}
            collected={collectedIds.has(c.id)}
            onCollect={handleCollect}
          />
        ))}

        {/* Gegner */}
        {LEVEL1_ENEMIES.map(e => (
          <Enemy
            key={`${e.id}-${resetKey}`}
            {...e}
            defeated={defeatedIds.has(e.id)}
            groundY={groundY}
            platforms={LEVEL1_PLATFORMS}
            playerPos={playerPos}
            bottleThrows={activeBottleThrows}
            onDamagePlayer={handleTakeDamage}
            onDefeated={handleEnemyDefeated}
            onBottleHit={handleBottleHit}
          />
        ))}

        {activeBottleThrows.map(bottle => (
          <Image
            key={`bottle-${bottle.id}`}
            source={BOTTLE_THROW_SPRITE}
            style={[
              styles.bottleSprite,
              {
                left: bottle.x,
                top: bottle.y,
                opacity: bottle.opacity,
                transform: [{ rotate: `${bottle.rotationDeg}deg` }],
              },
            ]}
            pointerEvents="none"
            resizeMode="contain"
          />
        ))}

        {activeBottleBursts.map(burst => (
          <Image
            key={`bottle-burst-${burst.id}`}
            source={BOTTLE_SHATTER_SPRITE}
            style={[
              styles.bottleBurst,
              {
                left: burst.x - 4,
                top: burst.y - 4,
                opacity: burst.opacity,
              },
            ]}
            pointerEvents="none"
            resizeMode="contain"
          />
        ))}

        {/* Spieler */}
        <Player
          key={`player-${resetKey}`}
          startX={LEVEL1_START_X}
          groundY={groundY}
          containerWidth={containerWidth}
          platforms={LEVEL1_PLATFORMS}
          collectibles={collectibleHits}
          onCollectItem={handleCollect}
          onTakeDamage={() => handleTakeDamage('player')}
          onPositionChange={handlePositionChange}
          onJump={() => play('jump')}
          onThrowBottle={handleBottleThrow}
          onSnapshot={handlePlayerSnapshot}
        />

        {playerSnapshot && (
          <View style={styles.debugOverlay}>
            <Text style={styles.debugTitle}>Debug</Text>
            <Text style={styles.debugText}>
              pos: {Math.round(playerSnapshot.position.x)}, {Math.round(playerSnapshot.position.y)}
            </Text>
            <Text style={styles.debugText}>
              frame: {playerSnapshot.spriteFrame} · {playerSnapshot.grounded ? 'grounded' : 'air'}
            </Text>
            <Text style={styles.debugText}>
              vel: {Math.round(playerSnapshot.velocity.x)}, {Math.round(playerSnapshot.velocity.y)}
            </Text>
            <Text style={[styles.debugText, styles.debugSeparator]}>events:</Text>
            {debugEvents.map(event => (
              <Text key={event.id} style={styles.debugText}>
                {event.label}: {event.detail}
              </Text>
            ))}
          </View>
        )}

        {/* Level-Complete-Overlay */}
        {levelComplete && (
          <LevelComplete
            score={score}
            kronenCollected={kronenCollected}
            kronenTotal={kronenTotal}
            stickerCollected={stickerCollected}
            stickerTotal={stickerTotal}
            onRestart={handleRestart}
          />
        )}
      </View>

      {/* HUD */}
      <View style={styles.hud}>
        <Text style={styles.hudText}>🍺 {kronenCollected}/{kronenTotal}</Text>
        <Text style={styles.hudText}>📍 {stickerCollected}/{stickerTotal}</Text>
        <Text style={styles.hudText}>{'❤️ '.repeat(Math.max(0, lives)).trim() || '💀'}</Text>
        <Text style={[styles.hudText, styles.scoreText]}>Score: {score}</Text>
        <Text style={styles.hudHint}>Pfeiltasten / A D · Leertaste zum Springen · F zum Flaschenwerfen</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#0d0d1a',
  },
  gameArea: {
    width: 960,
    height: 600,
    backgroundColor: '#5a8fcf',
    overflow: 'hidden',
    position: 'relative',
    borderWidth: 2,
    borderColor: '#ffc84a',
    borderRadius: 4,
  },
  bottleSprite: {
    position: 'absolute',
    width: 32,
    height: 32,
    zIndex: 55,
  },
  bottleBurst: {
    position: 'absolute',
    width: 32,
    height: 32,
    zIndex: 56,
  },
  ground: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: 100,
    backgroundColor: 'rgba(80,65,45,0.5)',
  },
  platform: {
    position: 'absolute',
    backgroundColor: 'rgba(100,75,50,0.85)',
    borderRadius: 3,
    borderBottomWidth: 3,
    borderBottomColor: 'rgba(50,30,10,0.9)',
  },
  platformSolid: {
    position: 'absolute',
    backgroundColor: 'rgba(110,105,95,0.85)',
    borderRadius: 3,
    borderTopWidth: 2,
    borderTopColor: 'rgba(180,175,165,0.8)',
    borderBottomWidth: 3,
    borderBottomColor: 'rgba(60,55,50,0.9)',
  },
  hud: {
    marginTop: 10,
    flexDirection: 'row',
    gap: 20,
    alignItems: 'center',
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  hudText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  scoreText: {
    color: '#ffc84a',
  },
  hudHint: {
    color: '#888',
    fontSize: 12,
  },
  debugOverlay: {
    position: 'absolute',
    top: 12,
    right: 12,
    paddingVertical: 8,
    paddingHorizontal: 10,
    borderRadius: 8,
    backgroundColor: 'rgba(0,0,0,0.72)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.2)',
    maxWidth: 220,
  },
  debugTitle: {
    color: '#ffc84a',
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 4,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  debugText: {
    color: '#fff',
    fontSize: 11,
    lineHeight: 15,
  },
  debugSeparator: {
    marginTop: 6,
    color: '#ffc84a',
  },
});

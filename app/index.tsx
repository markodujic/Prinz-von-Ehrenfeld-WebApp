import React, { useCallback, useMemo, useRef, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
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

  // Spieler-Position für Enemy-Kollisionscheck
  const playerPosRef = useRef({ x: LEVEL1_START_X, y: 0 });
  const [playerPos,  setPlayerPos]          = useState({ x: LEVEL1_START_X, y: 0 });
  const debugEventIdRef = useRef(1);

  const { play } = useSound();

  // Damit onCollectItem keine unnötigen Re-Renders via dep-Array auslöst
  const collectedIdsRef = useRef(collectedIds);
  collectedIdsRef.current = collectedIds;

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
      return next;
    });
    setScore(s => s + 25);
    play('stomp');
  }, [play, pushDebugEvent]);

  const handlePositionChange = useCallback((pos: { x: number; y: number }) => {
    playerPosRef.current = pos;
    setPlayerPos(pos);
  }, []);

  const handleRestart = useCallback(() => {
    pushDebugEvent('restart', 'reset level state');
    setCollectedIds(new Set());
    setDefeatedIds(new Set());
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
            onDamagePlayer={handleTakeDamage}
            onDefeated={handleEnemyDefeated}
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
          onSnapshot={setPlayerSnapshot}
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
        <Text style={styles.hudHint}>Pfeiltasten / A D · Leertaste zum Springen</Text>
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

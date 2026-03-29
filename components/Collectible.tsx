import React, { useEffect, useRef, useState } from 'react';
import { Image, StyleSheet, Animated } from 'react-native';
import type { CollectibleDef } from '../constants/level1';

type Props = CollectibleDef & {
  collected: boolean;
  onCollect: (id: string) => void;
};

const KRONE_FRAMES = [
  require('../assets/sprites/Krone_spin_1.png'),
  require('../assets/sprites/Krone_spin_2.png'),
  require('../assets/sprites/Krone_spin_3.png'),
  require('../assets/sprites/Krone_spin_4.png'),
];
const STICKER_IMG = require('../assets/sprites/Sticker.png');

const KRONE_SIZE  = 32;
const STICKER_SIZE = 32;
const SPIN_FPS = 6; // Frames pro Sekunde

export default function Collectible({ id, x, y, type, collected, onCollect }: Props) {
  const [frameIdx, setFrameIdx] = useState(0);
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const opacityAnim = useRef(new Animated.Value(1)).current;
  const rafRef = useRef<number | null>(null);
  const lastRef = useRef<number | null>(null);
  const accRef = useRef(0);
  const frameRef = useRef(0);
  const wasCollected = useRef(false);

  // Animations-Loop für Krone
  useEffect(() => {
    if (type !== 'koelsch') return;
    const step = (t: number) => {
      if (lastRef.current == null) lastRef.current = t;
      const dt = (t - lastRef.current) / 1000;
      lastRef.current = t;
      accRef.current += dt;
      if (accRef.current >= 1 / SPIN_FPS) {
        accRef.current = 0;
        frameRef.current = (frameRef.current + 1) % 4;
        setFrameIdx(frameRef.current);
      }
      rafRef.current = requestAnimationFrame(step);
    };
    rafRef.current = requestAnimationFrame(step);
    return () => {
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
      lastRef.current = null;
    };
  }, [type]);

  // Pop-Animation wenn eingesammelt
  useEffect(() => {
    if (collected && !wasCollected.current) {
      wasCollected.current = true;
      Animated.parallel([
        Animated.timing(scaleAnim, {
          toValue: 1.6,
          duration: 120,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
        }),
      ]).start();
    }
  }, [collected, scaleAnim, opacityAnim]);

  if (collected && wasCollected.current) {
    // Nach der Animation komplett ausblenden
  }

  const size = type === 'koelsch' ? KRONE_SIZE : STICKER_SIZE;
  const source = type === 'koelsch' ? KRONE_FRAMES[frameIdx] : STICKER_IMG;

  return (
    <Animated.View
      style={[
        styles.wrapper,
        {
          left: x,
          top: y - size,
          width: size,
          height: size,
          transform: [{ scale: scaleAnim }],
          opacity: opacityAnim,
        },
      ]}
      pointerEvents="none"
    >
      <Image source={source} style={{ width: size, height: size }} resizeMode="contain" />
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    position: 'absolute',
  },
});

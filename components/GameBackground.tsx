import React from 'react';
import { Image, StyleSheet } from 'react-native';

export default function GameBackground() {
  return (
    <Image
      source={require('../assets/sprites/Bg_venloer.png')}
      style={styles.bg}
      resizeMode="cover"
      pointerEvents="none"
    />
  );
}

const styles = StyleSheet.create({
  bg: {
    position: 'absolute',
    left: 0,
    top: 0,
    width: 960,
    height: 500,
  },
});

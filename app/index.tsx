import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Player from '../components/Player';

const PLATFORMS = [
  // braune Einweg-Plattformen (nur von oben betretbar)
  { x: 100, y: 390, width: 150, height: 20 }, // unten-links
  { x: 650, y: 390, width: 150, height: 20 }, // unten-rechts
  { x: 280, y: 280, width: 150, height: 20 }, // mitte-links
  { x: 520, y: 280, width: 150, height: 20 }, // mitte-rechts
  { x: 150, y: 170, width: 150, height: 20 }, // oben-links
  { x: 620, y: 170, width: 150, height: 20 }, // oben-rechts
  // graue solide Plattformen (blockieren auch von unten)
  { x: 390, y: 360, width: 130, height: 20, solid: true }, // mitte-boden
  { x:  40, y: 250, width: 130, height: 20, solid: true }, // ganz-links
  { x: 760, y: 250, width: 130, height: 20, solid: true }, // ganz-rechts
  { x: 385, y: 140, width: 130, height: 20, solid: true }, // mitte-oben
];

export default function Page() {
  const groundY = 500;
  const containerWidth = 960;

  return (
    <View style={styles.container}>
      <View style={styles.gameArea}>
        <View style={[styles.ground, {top: groundY}]} />
        {PLATFORMS.map((p, i) => (
          <View
            key={i}
            style={[
              p.solid ? styles.platformSolid : styles.platform,
              { left: p.x, top: p.y, width: p.width, height: p.height },
            ]}
          />
        ))}
        <Player groundY={groundY} containerWidth={containerWidth} platforms={PLATFORMS} />
      </View>
      <View style={styles.hud}>
        <Text style={styles.hudText}>Benutze Pfeiltasten / A D zum Laufen, Leertaste zum Springen.</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    padding: 12,
  },
  gameArea: {
    width: 960,
    height: 600,
    backgroundColor: '#cfe9ff',
    overflow: 'hidden',
    position: 'relative'
  },
  ground: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: 80,
    backgroundColor: '#5b8a3c'
  },
  platform: {
    position: 'absolute',
    backgroundColor: '#8B5E3C',
    borderRadius: 4,
    borderBottomWidth: 4,
    borderBottomColor: '#5a3a1a',
  },
  platformSolid: {
    position: 'absolute',
    backgroundColor: '#888',
    borderRadius: 4,
    borderTopWidth: 3,
    borderTopColor: '#aaa',
    borderBottomWidth: 4,
    borderBottomColor: '#555',
  },
  hud: {
    marginTop: 12
  },
  hudText: {
    color: '#333'
  }
});

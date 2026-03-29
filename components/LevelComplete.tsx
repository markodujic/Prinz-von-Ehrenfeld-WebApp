import React from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';

type Props = {
  score: number;
  kronenCollected: number;
  kronenTotal: number;
  stickerCollected: number;
  stickerTotal: number;
  onRestart: () => void;
};

export default function LevelComplete({
  score, kronenCollected, kronenTotal,
  stickerCollected, stickerTotal,
  onRestart,
}: Props) {
  const allKronen  = kronenCollected === kronenTotal;
  const allSticker = stickerCollected === stickerTotal;

  return (
    <View style={styles.overlay}>
      <View style={styles.panel}>
        <Text style={styles.title}>Klasse Veedel! 🍺</Text>
        <Text style={styles.subtitle}>Level 1 – Venloer Straße</Text>

        <View style={styles.statsRow}>
          <Text style={styles.statItem}>
            🍺 {kronenCollected}/{kronenTotal} Kölsch-Kronen
            {allKronen ? '  ✓' : ''}
          </Text>
          <Text style={styles.statItem}>
            📍 {stickerCollected}/{stickerTotal} Veedel-Sticker
            {allSticker ? '  ✓' : ''}
          </Text>
        </View>

        <Text style={styles.score}>Score: {score}</Text>

        {allKronen && allSticker && (
          <Text style={styles.bonus}>🏆 Perfekt! Alle Collectibles gefunden!</Text>
        )}

        <Pressable style={styles.button} onPress={onRestart}>
          <Text style={styles.buttonText}>Nochmal spielen</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    left: 0, top: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.65)',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 100,
  },
  panel: {
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    borderWidth: 3,
    borderColor: '#ffc84a',
    padding: 36,
    alignItems: 'center',
    minWidth: 340,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffc84a',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#aaa',
    marginBottom: 24,
  },
  statsRow: {
    marginBottom: 16,
    gap: 8,
    alignItems: 'flex-start',
  },
  statItem: {
    fontSize: 18,
    color: '#fff',
  },
  score: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 12,
  },
  bonus: {
    fontSize: 15,
    color: '#ffc84a',
    marginBottom: 16,
    textAlign: 'center',
  },
  button: {
    marginTop: 12,
    backgroundColor: '#ffc84a',
    paddingHorizontal: 32,
    paddingVertical: 12,
    borderRadius: 8,
  },
  buttonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1a1a2e',
  },
});

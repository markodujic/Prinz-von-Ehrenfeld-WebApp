import { useRef, useCallback } from 'react';

export type SoundName =
  | 'jump'
  | 'collect_koelsch'
  | 'collect_sticker'
  | 'stomp'
  | 'damage'
  | 'level_complete';

function getCtx(
  ctxRef: React.MutableRefObject<AudioContext | null>,
): AudioContext | null {
  if (typeof window === 'undefined') return null;
  if (!ctxRef.current) {
    ctxRef.current = new (
      window.AudioContext ||
      (window as unknown as { webkitAudioContext: typeof AudioContext })
        .webkitAudioContext
    )();
  }
  return ctxRef.current;
}

function tone(
  ctx: AudioContext,
  type: OscillatorType,
  freq1: number,
  freq2: number,
  duration: number,
  vol = 0.25,
  startOffset = 0,
) {
  const osc  = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.type = type;
  const t = ctx.currentTime + startOffset;
  osc.frequency.setValueAtTime(freq1, t);
  if (freq2 !== freq1) {
    osc.frequency.exponentialRampToValueAtTime(freq2, t + duration);
  }
  gain.gain.setValueAtTime(vol, t);
  gain.gain.exponentialRampToValueAtTime(0.001, t + duration);
  osc.start(t);
  osc.stop(t + duration);
}

export function useSound() {
  const ctxRef = useRef<AudioContext | null>(null);

  const play = useCallback((name: SoundName) => {
    const ctx = getCtx(ctxRef);
    if (!ctx) return;
    // Browser-Policy: AudioContext nach User-Interaktion entsperren
    if (ctx.state === 'suspended') ctx.resume();

    switch (name) {
      case 'jump':
        tone(ctx, 'square', 280, 560, 0.12, 0.2);
        break;

      case 'collect_koelsch':
        tone(ctx, 'sine', 523, 1047, 0.18, 0.3);
        tone(ctx, 'sine', 1047, 1047, 0.1, 0.15, 0.18);
        break;

      case 'collect_sticker':
        tone(ctx, 'sine', 523,  784,  0.1,  0.3,  0.0);
        tone(ctx, 'sine', 784,  1047, 0.1,  0.3,  0.1);
        tone(ctx, 'sine', 1047, 1568, 0.15, 0.25, 0.2);
        break;

      case 'stomp':
        tone(ctx, 'square', 200, 60, 0.12, 0.35);
        tone(ctx, 'sine',   150, 40, 0.08, 0.2,  0.04);
        break;

      case 'damage':
        tone(ctx, 'sawtooth', 440, 110, 0.08, 0.3,  0.0);
        tone(ctx, 'sawtooth', 330, 80,  0.1,  0.25, 0.08);
        tone(ctx, 'sawtooth', 220, 55,  0.12, 0.2,  0.18);
        break;

      case 'level_complete': {
        // C5 E5 G5 C6 E6 — Fanfare
        const notes = [523, 659, 784, 1047, 1319];
        notes.forEach((f, i) => tone(ctx, 'sine', f, f, 0.15, 0.3, i * 0.13));
        // abschließendes Glissando
        tone(ctx, 'sine', 523, 2093, 0.6, 0.2, notes.length * 0.13);
        break;
      }
    }
  }, []);

  return { play };
}

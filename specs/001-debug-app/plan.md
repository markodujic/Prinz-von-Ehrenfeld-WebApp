# Implementation Plan: App Debugging and Stabilization

**Branch**: `[001-debug-app]` | **Date**: 2026-06-14 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-debug-app/spec.md`

**Note**: This plan focuses on reproducing, isolating, and verifying app failures in the existing Expo app.

## Summary

Stabilize the current web app by tightening the debugging workflow around the live gameplay loop, especially the single-frame loop in `components/Player.tsx`, so failures can be reproduced, isolated, and verified without broad refactors.

## Technical Context

**Language/Version**: TypeScript 5.9 on Expo SDK 54 / React Native 0.81 / React 19

**Primary Dependencies**: Expo Router, React Navigation, Reanimated, Expo runtime, existing app components

**Storage**: N/A for this feature

**Testing**: Expo lint, browser-based local repro in `npm run web`, targeted manual validation of known failure paths

**Target Platform**: Expo web app first; existing Expo runtime remains available for mobile targets

**Project Type**: Expo web/mobile app

**Performance Goals**: Keep the current gameplay loop responsive while debugging; no new perf target is defined yet

**Constraints**: Preserve existing gameplay behavior unless the bug fix explicitly changes it; stay within the current Expo/TypeScript stack; avoid broad refactors

**Scale/Scope**: Current single-screen platformer flow and the player/collision loop

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Spec-first workflow is already in place and must stay intact.
- Expo and TypeScript remain the baseline stack.
- The smallest possible change should be preferred over architectural cleanup.
- Debugging must be validated through focused repro and verification steps.
- No constitution conflicts identified for this feature.

## Project Structure

### Documentation (this feature)

```text
specs/001-debug-app/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md
```

### Source Code (repository root)

```text
app/
├── index.tsx

components/
├── Player.tsx
├── Enemy.tsx
├── Collectible.tsx
├── GameBackground.tsx
└── LevelComplete.tsx

hooks/
└── useSound.ts

constants/
└── level1.ts

assets/
└── sprites/
```

**Structure Decision**: Keep the plan centered on the existing Expo Router app. The highest-risk debugging surface is `components/Player.tsx` because it owns physics, collision, and animation state in a single requestAnimationFrame loop.

## Complexity Tracking

No constitution violations need justification for this feature.

# Implementation Plan: App Debugging and Stabilization

**Branch**: `[001-debug-app]` | **Date**: 2026-06-14 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-debug-app/spec.md`

**Note**: This plan focuses on reproducing, isolating, and verifying app failures in the existing Expo app.

## Summary

Stabilize the current web app by tightening the debugging workflow around the live gameplay loop, especially the single-frame loop in `components/Player.tsx`, so failures can be reproduced, isolated, and verified without broad refactors.

## Research

### Key Findings

- The app is an Expo Router web/mobile project with the main gameplay loop concentrated in `components/Player.tsx`, `components/Enemy.tsx`, and `app/index.tsx`.
- The most efficient debugging workflow for this codebase is to capture the visible failure, the exact repro path, and the runtime evidence from the browser, then validate with `expo lint` and the local web run.
- The current app already has a compact single-screen structure, so the plan should avoid introducing new abstractions and instead preserve the smallest possible reproduction and verification surface.

### Decisions

- Use the browser web build as the primary debugging target because it is already the fastest local feedback loop for this repository.
- Keep the debug workflow centered on observable behavior and the smallest affected code path rather than global cleanup.
- Treat screenshots or screen recordings as optional evidence that strengthens the reproduction case, not as a hard requirement.

## Data Model

### Issue Report

- `id`: Unique issue identifier.
- `title`: Short human-readable description.
- `severity`: Relative impact level.
- `userImpact`: What the user can observe.
- `steps`: Ordered repro steps.
- `environment`: Relevant runtime context such as browser or local build state.
- `evidence`: Console output, runtime errors, screenshots, or recordings.

### Reproduction Case

- `issueId`: Link to the originating issue.
- `preconditions`: State required before reproduction.
- `steps`: Minimal step list that triggers the problem.
- `expected`: Normal behavior.
- `actual`: Observed failing behavior.

### Debug Session

- `id`: Unique session identifier.
- `issueId`: Linked issue.
- `hypothesis`: Current suspected root cause.
- `scope`: Files or surfaces under investigation.
- `findings`: Notes from reproduction and isolation.
- `status`: Open, narrowed, fixed, or verified.

### Verification Result

- `sessionId`: Linked debug session.
- `fixValidated`: Whether the original failure is gone.
- `regressionCheck`: Whether the normal flow still works.
- `evidence`: Lint output, local runtime confirmation, or other proof.

## Quickstart

### Prerequisites

- Node.js dependencies installed for the workspace.
- The web app can be started locally with the existing Expo script.

### Validate the Debug Flow

1. Start the app with `npm run web`.
2. Reproduce the visible failure in the browser.
3. Record the minimal repro steps and the exact runtime evidence.
4. Narrow the issue to the smallest likely code path.
5. Apply the fix and confirm the same steps no longer fail.
6. Run `npm run lint` before concluding the session.

### Expected Outcome

- The issue can be reproduced from the recorded context without guessing.
- The failing surface can be isolated to a small part of the app.
- The fix can be verified against the original failure without breaking the normal flow.

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

## Constitution Check Revisited

- Spec-first workflow remains intact after design artifact generation.
- Expo and TypeScript are still the baseline stack for the repository.
- The plan still prefers the smallest reproducible and verifiable change.
- No new constitution conflicts were introduced by the design artifacts.

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

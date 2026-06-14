# Research: App Debugging and Stabilization

## Decision 1: Work against the existing Expo web app, not a new diagnostic layer

Decision: Keep the feature scoped to the current Expo/TypeScript app and its existing runtime.

Rationale: The repository already exposes a clear local reproduction path through `npm run web`, and the debugging problem is inside the current gameplay loop rather than in a missing infrastructure layer.

Alternatives considered: Adding a separate debugging service, a new logging backend, or a replay system. Those would increase scope without fixing the immediate need to reproduce and isolate failures in the live app.

## Decision 2: Treat `components/Player.tsx` as the primary investigation surface

Decision: Focus initial debugging effort on `components/Player.tsx` and the nearby render path in `app/index.tsx`.

Rationale: The architecture documents show a single `requestAnimationFrame` loop that owns physics, collision, input, and animation state. That concentration makes it the highest-value place to reproduce and isolate defects.

Alternatives considered: Spreading investigation across all components immediately. That would dilute the debugging effort and make root-cause identification slower.

## Decision 3: Use local browser repro and linting as the validation baseline

Decision: Validate fixes with local web repro (`npm run web`) and Expo lint, then confirm the original failure no longer occurs.

Rationale: The feature is about user-visible failure recovery, so the cheapest reliable proof is a repeatable local repro plus a clean validation pass.

Alternatives considered: Adding automated end-to-end coverage first or introducing a more formal test harness. Those are useful later, but they are not necessary to start narrowing the current debugging scope.

## Decision 4: Keep debugging state conceptual, not persisted

Decision: Model issue reports, reproduction cases, debug sessions, and verification results as planning concepts only; do not add new storage.

Rationale: The feature spec focuses on stabilization workflow rather than data persistence. New storage would add implementation overhead without changing the immediate debugging path.

Alternatives considered: Building a persistent issue database or telemetry pipeline. That would be useful for larger-scale operations, but it is out of scope for this pass.
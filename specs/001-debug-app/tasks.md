---

description: "Task list template for feature implementation"
---

# Tasks: App Debugging and Stabilization

**Input**: Design documents from `/specs/001-debug-app/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: No standalone automated test suite is requested for this feature. Validation tasks are included as manual repro and lint checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Preparation)

**Purpose**: Capture the current debugging baseline before changing behavior

- [ ] T001 Document the current reproduction baseline and failure notes in `specs/001-debug-app/quickstart.md`
- [ ] T002 [P] Record the current investigation scope and issue model in `specs/001-debug-app/research.md` and `specs/001-debug-app/data-model.md`

---

## Phase 2: Foundational (Blocking Debugging Primitives)

**Purpose**: Add the shared debug surface needed by all three user stories

**⚠️ CRITICAL**: No story-specific verification should start until this shared debug surface exists

- [X] T003 [P] Add a lightweight player-state snapshot helper in `components/Player.tsx` for position, velocity, grounded state, and collision contact
- [X] T004 [P] Surface the snapshot in a minimal debug overlay in `app/index.tsx` so the live repro can be inspected during play
- [X] T005 Extract the collision and reset logic into named helper functions in `components/Player.tsx` so the failing path is easier to isolate

**Checkpoint**: The app exposes enough live state to reproduce and inspect a failure without guessing

---

## Phase 3: User Story 1 - Reproduce Critical Issues (Priority: P1)

**Goal**: Make the current failure path repeatable from a clean start

**Independent Test**: Start the app, follow the recorded steps, and reach the same failure state consistently

- [ ] T006 [US1] Wire a deterministic restart and replay path through `app/index.tsx` and `components/Player.tsx` so the same issue can be triggered from a clean state
- [ ] T007 [US1] Update `specs/001-debug-app/quickstart.md` with the exact reproduction steps and the expected failure signature
- [ ] T008 [US1] Validate the reproduction path with `npm run web` and record the observed failure behavior in `specs/001-debug-app/quickstart.md`

**Checkpoint**: The problem can now be reproduced repeatedly without additional context

---

## Phase 4: User Story 2 - Isolate Root Cause (Priority: P2)

**Goal**: Narrow the failing behavior to the smallest responsible code path

**Independent Test**: Use the debug surface to distinguish the failing path from the working path and identify one likely cause

- [ ] T009 [P] Add focused debug markers or logging around movement, collision, collectible pickup, damage, and reset transitions in `components/Player.tsx`
- [ ] T010 [P] Expand the debug overlay in `app/index.tsx` to show only the state needed to compare expected versus failing frames
- [ ] T011 [US2] Use the added debug surface to isolate the smallest failing path and capture the root-cause hypothesis in `specs/001-debug-app/research.md`

**Checkpoint**: The failure is narrowed to a specific branch of the player/game loop

---

## Phase 5: User Story 3 - Confirm the Fix (Priority: P3)

**Goal**: Fix the isolated issue and prove that the original failure is gone

**Independent Test**: Re-run the recorded reproduction path and confirm the failure no longer occurs while the normal flow still works

- [ ] T012 [US3] Implement the smallest fix in `components/Player.tsx`, `app/index.tsx`, or `constants/level1.ts` based on the isolated root cause
- [ ] T013 [US3] Re-run the exact reproduction steps with `npm run web` and confirm the issue no longer appears
- [ ] T014 [US3] Update `specs/001-debug-app/quickstart.md` with the post-fix verification result and any regression checks

**Checkpoint**: The fix is verified against the original failure and the core gameplay flow still works

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Remove temporary diagnostics and align the feature notes with the verified result

- [ ] T015 [P] Remove or gate temporary debug output in `components/Player.tsx` and `app/index.tsx` so only intentional diagnostics remain
- [ ] T016 Clean up `specs/001-debug-app/research.md` and `specs/001-debug-app/data-model.md` so they reflect the final verified debugging workflow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Stories (Phase 3+)**: Depend on the shared debug surface from Phase 2
- **Polish (Final Phase)**: Depends on the fix being implemented and verified

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 - no dependency on later stories
- **User Story 2 (P2)**: Can start after Phase 2 - builds on the same debug surface as US1
- **User Story 3 (P3)**: Can start after US2 has narrowed the issue enough to implement the fix

### Within Each User Story

- Repro steps and baseline notes before root-cause work
- Debug surface before diagnosis
- Diagnosis before the fix
- Fix before verification
- Verification before cleanup

### Parallel Opportunities

- `T002` can run in parallel with `T001`
- `T003` can run in parallel with `T004`
- `T009` can run in parallel with `T010`
- `T015` can run in parallel with `T016`

---

## Parallel Example: User Story 1

```bash
# Once the shared debug surface exists, these can be worked in parallel:
Task: "Wire a deterministic restart and replay path through app/index.tsx and components/Player.tsx"
Task: "Update specs/001-debug-app/quickstart.md with the exact reproduction steps and the expected failure signature"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational debug surface
3. Complete Phase 3: Reproduce the issue reliably
4. Stop and validate the reproduction path

### Incremental Delivery

1. Make the issue reproducible
2. Add instrumentation to isolate the cause
3. Implement the smallest fix
4. Verify the fix against the original failure
5. Remove temporary diagnostics

### Parallel Team Strategy

With more than one developer:

1. One person captures the reproduction baseline and quickstart notes
2. One person builds the debug overlay and state snapshot in the app
3. One person works on the root-cause isolation and verification notes

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to a specific user story for traceability
- The feature is intentionally narrow: debug the current app first, then lock in the fix and cleanup
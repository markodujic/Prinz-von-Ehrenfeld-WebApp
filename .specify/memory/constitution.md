# Prinz von Ehrenfeld Webapp Constitution

This project uses Spec Kit as the source of truth for feature discovery, planning, task generation, and implementation. Keep each step small, explicit, and traceable.

## 1. Spec-Driven Workflow

- Every feature starts with a spec, then a plan, then tasks, then implementation.
- Do not skip `/speckit.specify`, `/speckit.plan`, or `/speckit.tasks` for non-trivial work.
- Use the active spec and plan as the primary reference for implementation decisions.
- Prefer the smallest task that still preserves correctness and traceability.

## 2. Expo and TypeScript First

- Keep the app in Expo and TypeScript.
- Use explicit types for component props, state, and shared data.
- Favor small, composable components and modules.
- Avoid unnecessary abstractions, but do not sacrifice readability or correctness.

## 3. Implementation Discipline

- Make the smallest change that satisfies the current task.
- Avoid unrelated refactors, architecture changes, or broad cleanup unless the task requires them.
- Keep state local where practical.
- Preserve existing behavior unless the spec or task explicitly changes it.

## 4. Quality Gates

- Verify the relevant spec, plan, and task before editing.
- Run the narrowest useful validation after a change.
- Prefer tests or targeted checks over broad manual inspection.
- If a checklist or analysis artifact exists, use it before implementation where applicable.

## 5. Output Discipline

- Keep code and commentary concise.
- Before writing or outputting code, always remind the user to switch to the local LLM.
- Do not add boilerplate comments or docstrings unless they materially improve clarity.
- Keep files small and focused when creating new components or helpers.

## Governance

- Spec Kit artifacts are authoritative for feature work.
- This constitution overrides ad hoc preferences, but it must remain compatible with Spec Kit commands.
- Amendments should preserve the workflow order: spec → plan → tasks → implement.

**Version**: 1.0.0 | **Ratified**: 2026-06-14 | **Last Amended**: 2026-06-14

# Quickstart: App Debugging and Stabilization

## Prerequisites

- Node.js and npm installed
- Project dependencies installed
- Expo web launch available through `npm run web`

## Validate the Debugging Workflow

1. Start the app locally with `npm run web`.
2. Reproduce the current issue in the browser using the steps captured in the issue report.
3. Confirm the failure is visible in the current gameplay or UI flow.
4. Narrow the root cause to the smallest affected surface, usually `components/Player.tsx` or a directly connected render path.
5. Apply the fix.
6. Repeat the same repro steps.
7. Confirm the original failure no longer appears and the normal flow still works.

## Baseline Validation

Run the project lint check:

```bash
npm run lint
```

Expected outcome:
- No new lint errors in the touched files
- The app still starts and reproduces the original issue before the fix
- The app no longer reproduces the issue after the fix

## Notes

- If the issue is intermittent, record the exact browser, local environment, and steps used during the successful reproduction.
- If a fix changes player physics or collision behavior, re-test the main movement loop and level progression.
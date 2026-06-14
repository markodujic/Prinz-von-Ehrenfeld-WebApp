# Data Model: App Debugging and Stabilization

## Issue Report

Represents one user-visible failure that needs attention.

Fields:
- `id`: Stable identifier for the issue
- `summary`: Short description of the failure
- `severity`: Relative priority of the failure
- `area`: App area involved, such as gameplay, navigation, or assets
- `observedBehavior`: What the user sees when the issue occurs
- `expectedBehavior`: What should have happened instead
- `status`: Open, reproducing, isolated, fixed, verified, or closed

Validation rules:
- Every issue report must have a summary and observed behavior.
- An issue report should map to one primary app area.

## Reproduction Case

Represents the minimum repeatable path that shows the issue.

Fields:
- `id`: Stable identifier for the repro case
- `issueId`: Linked issue report
- `environment`: Browser, local web app, or other relevant runtime
- `steps`: Ordered steps to trigger the failure
- `result`: What happened when the steps were executed
- `repeatable`: Whether the issue can be triggered consistently

Validation rules:
- Each reproduction case must reference one issue report.
- Each issue report should have at least one reproduction case before it can be considered isolated.

## Debug Session

Represents a focused investigation of one issue from first report to fix verification.

Fields:
- `id`: Stable identifier for the debugging session
- `issueId`: Linked issue report
- `hypothesis`: Current best guess about the cause
- `notes`: Short investigation notes and observations
- `status`: Investigating, narrowed, fixed, or waiting for verification

Validation rules:
- A debug session should point at exactly one issue at a time.
- If the issue changes scope, start a new debug session instead of reusing stale notes.

## Verification Result

Represents the outcome of confirming a fix.

Fields:
- `id`: Stable identifier for the verification result
- `issueId`: Linked issue report
- `passed`: Whether the fix removed the original failure
- `regressions`: Any new problems observed during verification
- `validatedAt`: When the check was performed

Validation rules:
- Verification must reference the original issue report.
- A fix is only considered complete when the original failure no longer reproduces and the normal flow still works.

## State Transitions

1. `open` → `reproducing`
2. `reproducing` → `isolated`
3. `isolated` → `fixed`
4. `fixed` → `verified`
5. `verified` → `closed`

Notes:
- If the issue cannot be reproduced, it stays in `open` or `reproducing` until more context is available.
- If verification fails, move back to `isolated` or `fixed` depending on what changed.
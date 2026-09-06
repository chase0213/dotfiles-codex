---
name: feature-dev
description: Design and implement large or unclear features with explicit acceptance criteria and integration checks. Skip small, well-scoped edits.
---

# Feature development

## Design

- Inspect affected code and project conventions. Define the intended behavior, interfaces, scope, constraints, and executable acceptance checks.
- Resolve consequential requirements not settled by the request. Continue on authorized design decisions and routine implementation choices without an extra approval gate.
- Keep the plan in conversation unless the project uses design artifacts or persistence helps a long task; then use its established location, such as `docs/plans/<feature>.md`.

## Implement

- Split work only where independent acceptance checks or dependencies make the split useful. State the expected outcome and exclusions for each part.
- Work locally or delegate bounded independent parts when it helps. Give delegated work sufficient context, file ownership, dependencies, and acceptance checks; avoid overlapping writes.
- Choose verification against the specification, not the implementation. Prefer regression tests for bugs and tests first when the behavior is stable; include relevant failure and boundary cases.
- Use the current model and execution mode unless the task actually requires a change. This workflow does not require model switching, subagents, worktrees, or Git mutations.

## Integrate

- Verify boundaries between parts and the end-to-end acceptance criteria. Run focused checks and the project's required checks; expand coverage when the change or remaining risk warrants it.
- Review the final diff against the intended behavior. Resolve scope-relevant findings and report verification evidence and unproven requirements.

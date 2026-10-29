---
name: feature-dev
description: Design and implement large or unclear features with explicit acceptance criteria and integration checks. Skip small, well-scoped edits.
---

# Feature development

## Design

- Inspect affected code and project conventions. Define the intended behavior, interfaces, scope, constraints, and executable acceptance checks.
- Resolve consequential requirements not settled by the request. Continue on authorized design decisions and routine implementation choices without an extra approval gate.
- Start a concise decision trail in the conversation. Record the starting problem, material facts and assumptions, chosen direction, and acceptance checks. Keep it in an established project artifact, such as `docs/plans/<feature>.md`, only when the project requires one or persistence materially helps a long task.
- Treat tool output, code, diffs, and test results as evidence; treat explanations inferred from the final implementation as reconstruction. Mark that distinction where it could change a reviewer's conclusion, and do not present unrecorded alternatives or rationale as history.

## Implement

- Split work only where independent acceptance checks or dependencies make the split useful. State the expected outcome and exclusions for each part.
- Work locally or delegate bounded independent parts when it helps. Give delegated work sufficient context, file ownership, dependencies, and acceptance checks; avoid overlapping writes.
- Choose verification against the specification, not the implementation. Prefer regression tests for bugs and tests first when the behavior is stable; include relevant failure and boundary cases.
- Add a checkpoint when evidence materially changes the plan: the observation and its source, what assumption or choice changed, and the resulting direction. Preserve useful evidence such as the exact failing check or representative diff; omit routine reads, retries, and dead-end mechanics.
- Use the current model and execution mode unless the task actually requires a change. This workflow does not require model switching, subagents, worktrees, or Git mutations.

## Integrate

- Verify boundaries between parts and the end-to-end acceptance criteria. Run focused checks and the project's required checks; expand coverage when the change or remaining risk warrants it.
- Review the final diff against the intended behavior. Resolve scope-relevant findings and report verification evidence and unproven requirements.
- For a substantive handoff, use the decision trail to give a compact chronological account from problem to outcome. Include only observed attempts and pivots, label any retrospective interpretation, and link important claims to code, diffs, commands, or results.

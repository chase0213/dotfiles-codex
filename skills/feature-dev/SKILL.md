---
name: feature-dev
description: Design, decompose, implement, and verify a large or unclear feature. Use for multi-file feature additions and work that needs explicit acceptance criteria; do not use for small, well-scoped edits.
---

# Feature development

## 1. Explore and design

- Inspect the affected code and current project instructions before proposing a design.
- Delegate bounded, read-heavy exploration only when parallel work materially helps.
- Resolve requirements that would materially change the implementation with the user.
- Record the design in `docs/plans/<feature>.md` when the repository keeps design artifacts. Include target interfaces, affected files, out-of-scope items, risks, and end-to-end verification.

## 2. Decompose

- Split the design into independently verifiable subtasks.
- Give each subtask a definition of done, executable acceptance checks, dependencies, and explicit exclusions.
- Obtain user confirmation when the design represents a meaningful product or architecture choice.

## 3. Implement

- Use the `implementer` custom agent for bounded subtasks when delegation was explicitly requested or materially improves independent parallel work.
- Give every delegated task complete context; subagents should not need the parent conversation to infer scope.
- Prefer tests first, covering normal, abnormal, and boundary behavior.
- Avoid parallel edits to overlapping files. Use isolated worktrees only when the repository workflow supports them.

## 4. Integrate and verify

- Check behavior at subtask boundaries and run the focused and full relevant test suites.
- Execute the end-to-end verification from the design.
- Review the final diff against the design and fix correctness or requirement gaps without unrelated cleanup.
- Report verification commands and concise results.


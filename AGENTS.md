# Workflow

- Trivial changes (typos, log lines, mechanical renames): implement directly.
- For non-trivial work, inspect the relevant code before editing and state a short plan.
- Delegate only when the task explicitly benefits from independent parallel work or an applicable skill requests it.
- Before implementation, identify an executable verification step. Prefer tests that cover normal, abnormal, and boundary cases.
- Report completion with evidence: include the command run and a concise result.
- For large or unclear features, use the `feature-dev` skill.

# Review

- For a comprehensive review of a non-trivial diff, use the `multi-review` skill.
- For adversarial analysis of security-sensitive work, use `red-team` in addition to security review.
- Use the `test-writer` custom agent when a specification is stable enough to write tests before implementation.

# Git

- Do not create branches, commits, pushes, or pull requests unless the user requests them or they are an explicit step in the active workflow.
- Keep commits focused and use descriptive messages.
- Do not add AI attribution or co-author trailers unless the user requests them.


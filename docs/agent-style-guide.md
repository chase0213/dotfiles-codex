# Custom agent style guide

Codex custom agents live in `agents/<name>.toml`. Each file must contain:

- `name`: stable agent identifier.
- `description`: narrow guidance describing when to select it.
- `developer_instructions`: focused behavior and output expectations.

Reviewers should also set `sandbox_mode = "read-only"`. Prefer inheriting the active model instead of pinning a model ID; set `model_reasoning_effort = "high"` only where deeper review is valuable.

Keep each reviewer in one lane. State its trigger, scope exclusions, evidence bar, and concise output contract. A finding should include severity, `file:line`, concrete impact, and a focused fix. Cap output at eight findings and sort by severity.

Optional reviewers must self-skip with PASS when their trigger does not apply. The `multi-review` skill should pre-filter them from the changed paths to avoid unnecessary agent calls.

Custom agents should not spawn other agents. Orchestration belongs in a skill or the parent task. Parallel reviewers must read the requested diff independently and avoid file edits.


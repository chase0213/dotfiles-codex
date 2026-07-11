---
name: multi-review
description: Run a multi-perspective review of a non-trivial diff with parallel custom agents, then deduplicate and prioritize findings. Use after substantial changes or before a PR; skip trivial edits.
---

# Multi-perspective review

## Scope

Determine the requested diff. Default to the current branch against its clear base branch; if no base is available, ask for the intended range. Stop when there is no diff.

## Agent selection

Always run these custom agents:

- `security-reviewer`
- `performance-reviewer`
- `domain-reviewer`
- `maintainability-reviewer`

Add optional agents only when changed paths or content match:

- `dependency-reviewer`: manifests, lockfiles, or container base images.
- `migration-reviewer`: database migrations or schema changes.
- `a11y-reviewer`: UI components, templates, or accessibility-relevant styles.
- `api-contract-reviewer`: public routes, API schemas, RPC definitions, SDKs, or exported library contracts.

## Execution

- Spawn all selected reviewers in one parallel batch.
- Give each reviewer the exact diff range, relevant user context, and a request for its standard concise result.
- Reviewers are read-only. Wait for all selected agents before synthesis.

## Synthesis

- Deduplicate findings that identify the same underlying issue and location; mention reviewer agreement.
- Preserve the reviewers' severities and sort critical, high, medium, then low.
- Lead with actionable findings. If there are critical or high findings, keep lower-severity details compact.
- Include a per-reviewer PASS, FAIL, or SKIPPED status and finding count.
- End with one or two concrete next actions, or state that the diff is ready.


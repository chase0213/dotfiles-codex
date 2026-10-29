---
name: multi-review
description: Review a diff from relevant independent perspectives and reconcile findings. Use for a requested comprehensive review or a change whose breadth or risk benefits from multiple reviewers; skip routine edits.
---

# Multi-perspective review

## Establish the actual scope

- Honor the user's path, PR, or revision range. Otherwise inspect working-tree status and use the current task's changes, including staged, unstaged, and relevant untracked files. For a clean tree, use the branch's known base when the context calls for branch review.
- State the comparison before reviewing. For pending changes, `git diff HEAD -- <paths>` includes staged and unstaged tracked changes; inspect relevant untracked files separately. For branch work, use the established merge base and include pending changes if they belong to the task.
- Do not invent a base or fall back to the last commit. Ask only when the intended scope remains ambiguous. If the confirmed scope has no changes, report that and finish.

## Select relevant perspectives

Choose based on changed behavior and plausible impact; paths are clues, not the sole gate. There is no mandatory reviewer count.

| Perspective | Use when |
| --- | --- |
| security-reviewer | Trust boundaries, authentication, authorization, secrets, or untrusted input change |
| performance-reviewer | Hot paths, I/O, queries, resource growth, or rendering costs change |
| domain-reviewer | Business rules, invariants, terminology, or architectural boundaries change |
| maintainability-reviewer | Responsibilities, dependencies, or complexity change materially |
| dependency-reviewer | Manifests, lockfiles, or container base images change |
| migration-reviewer | Database schemas, data migrations, or deployment order change |
| a11y-reviewer | User interfaces or accessibility behavior change |
| api-contract-reviewer | Public API behavior, schemas, RPCs, or exported contracts change |

- Use relevant independent reviewers in parallel when available and useful. Give each the exact comparison, task context, and access to the diff and needed surrounding code. Keep review read-only and wait for selected reviewers before synthesis.
- If custom agents or delegation are unavailable, review the relevant perspectives locally and disclose the limitation. Do not block the task on a particular agent name or tool-call layout.

## Reconcile and report

- Check each finding against the code and requirements. Merge the same underlying issue, resolve conflicting claims, and correct unsupported severity labels with evidence.
- Treat an implementation narrative or decision trail as context to verify, not proof. Check material claims against available diffs, code, commands, and results; distinguish a technical defect from a rationale that needs human judgment, and call out retrospective explanations presented as recorded history.
- Lead with actionable findings, ordered by impact, with file locations, consequences, and a focused fix. Keep valid lower-impact findings concise rather than suppressing them solely because a serious issue exists.
- Summarize the scope reviewed and material coverage gaps. If none were found, say so without implying unreviewed areas passed. A full PASS/SKIPPED roster or fixed report template is not required.

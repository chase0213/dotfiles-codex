---
name: red-team
description: Test concrete adversarial scenarios against a feature or change. Use when adversarial analysis is requested or material trust-boundary changes warrant it; complements security code review.
---

# Adversarial review

## Scope and scenarios

- Derive the target from the request and current change; ask only if it remains ambiguous. Identify sensitive assets, authorization rules, exposed entry points, and trust boundaries.
- Propose attacks before inspecting defenses in detail so existing code does not define the threat model. Use the actors with a credible path to the target: unauthenticated users, authenticated users, insiders, or compromised integrations.
- Prioritize concrete reachable paths and impact. Consider relevant authorization bypass, parsing, replay/races, quota abuse, disclosure, and business-logic abuse; do not fill a quota per actor or force irrelevant categories.

## Verify

- Trace each selected scenario through the implementation. Record prerequisites, attack steps, expected impact, and evidence at `file:line`.
- Distinguish prevented, partially mitigated, open, and unverified paths. Static inspection can support a conclusion but cannot substitute for runtime evidence where timing, configuration, or external behavior matters.
- Run tests only within authorized environments and side effects. For paths needing unavailable runtime validation, give a concrete test and mark the conclusion unverified.

## Report

- Lead with open or partially mitigated paths, severity justified by reachability and impact, evidence, and a focused mitigation. Summarize verified defenses only where useful.
- State material gaps, assumptions, and runtime checks not performed. Do not label the result clean when important scenarios remain unverified.
- Merge overlap with security-review findings rather than silently dropping a valid issue. Use a concise format suited to the findings; no fixed scenario count or mandatory empty sections.

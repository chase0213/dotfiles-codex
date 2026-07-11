---
name: red-team
description: Adversarial exercise — given a feature or change, enumerate concrete attack scenarios a malicious external user, authenticated user, insider, or third-party integration could try, then verify each against the implementation. Use after implementing a security-sensitive feature. Complements (does not replace) security-reviewer.
---

# Red-Team Exercise

Take the **attacker's perspective**. Given a feature, change, or
system under review, **imagine the attack before reading the code**,
then check whether the code would withstand it.

This is NOT a code review. `security-reviewer` reads code for
dangerous patterns. `red-team` walks through attack scenarios and
checks them against the code. They complement each other.

## When to use
- After implementing: auth, authorization, payment, file upload,
  user-input rendering, integration with third parties, anything
  touching credentials/PII/money.
- Before opening a PR for a security-sensitive feature.

## Procedure

### 1. Scope

Identify the target: feature name, change, or PR. If the user did
not specify, ask. Also gather:
- The data the feature touches (PII? secrets? money? credentials?)
- The trust boundaries crossed
- Who is allowed to use it (auth model)

### 2. Generate attack scenarios

For **each** of the four actor categories, brainstorm 3–5 concrete
attack paths. Be specific: "abuse the password reset" is too vague;
"request password reset for victim email, leak the token via
`Referer` header on the reset page that includes the token in URL"
is specific enough to test.

Categories:
- **External unauthenticated user**
- **Authenticated user** (privilege escalation, IDOR, abuse of
  legitimate features)
- **Malicious insider** (data exfil, sabotage)
- **Compromised integration** (webhook callback, OAuth app, supply
  chain dep)

Cover at minimum:
- AuthN bypass paths
- AuthZ bypass paths (horizontal + vertical IDOR)
- Input that breaks parsing assumptions (size, encoding, null bytes,
  unicode, polyglot files)
- Race conditions / TOCTOU
- Rate-limit and quota abuse
- Information disclosure via errors, timing, side channels
- Logic abuse — legitimate features used illegitimately (refund a
  $0 order, transfer to own account, replay a one-time token)

### 3. Verify each scenario against the implementation

For each scenario, do one of:
- Read the relevant code and state: **prevented** / **partially
  mitigated** / **open**. Cite `file:line` for the mechanism.
- If verification needs running the code, mark "needs runtime test"
  and describe the test in one sentence.

### 4. Report

Output exactly:

```
## Red-Team Report — <CLEAN | ISSUES FOUND>

### Open attack paths
- [critical|high|medium|low] <scenario title>
  - Actor: <external | auth user | insider | integration>
  - Attack: <concrete steps>
  - Evidence: `file:line` — why it works
  - Mitigation: <one sentence>

(omit section if none; sort by severity)

### Mitigated (sanity-checked, no action needed)
- <scenario title> — prevented by `file:line` (<mechanism>)

### Needs runtime test
- <scenario title> — proposed test: <one sentence>

### Out of scope
- <scenario title> — reason
```

## Token efficiency
- Scenario generation is the expensive step; cap at 5 per actor
  category.
- For verification, read only the files implicated — do not grep
  the whole repo.
- Do not re-list "Mitigated" scenarios in full; one line each.
- Do not duplicate findings that `security-reviewer` would catch via
  pattern (e.g., obvious SQL string concat) — note them and move on.

---
name: human-review
description: Create review documentation for a requested change report or a substantive handoff needing human judgment. Preserve design rationale, implementation evidence, test limits, and domain decisions; not for ordinary completion summaries.
---

# Human review document

Create a self-contained HTML document in the user's language unless another format is requested. Use the project's artifact location, otherwise `docs/reviews/<change>.html`, and link it in the completion report. This does not authorize publishing or create an additional approval gate.

Build the document from the final change, the contemporaneous decision trail when available, and actual verification results. Identify repositories, comparison revisions or snapshots, and relevant pending/untracked files. Refresh it after subsequent edits. Keep the main narrative concise, with supporting evidence in expandable blocks or the appendix.

Do not claim to replay hidden reasoning. Separate facts supported by contemporaneous messages, tool output, code, diffs, or tests from explanations reconstructed later from the resulting artifacts. A retrospective explanation may be useful, but label it where a reviewer could otherwise mistake it for historical fact. Do not invent alternatives, experiments, decision sequences, or rationale.

## 1. Overview

Explain the purpose, what changed, how it was implemented and verified, and the resulting behavior. Explicitly state non-goals, unsupported cases, unfinished work, and limitations.

## 2. Decision trail

Reconstruct the shortest chronology that lets a reviewer evaluate the problem-solving process:

- **Starting point:** the problem, intended outcome, constraints, and initial assumptions.
- **Situation:** material findings from the existing code, requirements, or environment.
- **Choice:** the direction selected and the evidence or recorded rationale supporting it. Include alternatives only when they were actually recorded or tried.
- **Attempt and observation:** material implementation attempts, commands, tests, or runtime observations and their results.
- **Pivot:** any result that changed an assumption or direction, plus the resulting decision. Omit this when no pivot occurred.
- **Outcome:** the implemented behavior and what remains unverified or unresolved.

Attach compact evidence to important turning points using paths and lines, diff excerpts, exact verification commands and results, or log excerpts. Identify reconstructed interpretation inline when its basis is only the current artifacts. Omit routine file reads, typo corrections, repeated checks, and other mechanics that do not affect technical judgment.

## 3. Changes

Organize by feature or concern, not by file. For each change include:

- **Purpose:** why the change was necessary.
- **Approach:** the chosen method, recorded alternatives and tradeoffs, and selection rationale. If an alternative is merely plausible in hindsight, either omit it or label it as a retrospective comparison rather than part of the decision history.
- **Implementation:** affected file groups and representative before/after or git diff excerpts with paths and line numbers. Separate core logic from supporting edits and explain why that logic meets the purpose; avoid narrating every changed line.
- **Tests:** exact commands, working directories, results, and how checks map to acceptance criteria. Explain why coverage is sufficient for the stated scope, what remains unproven, and how mocks, environment differences, or technical constraints could permit violations despite passing checks. Mark unexecuted checks explicitly.

## 4. Points of Review

Point to concrete sections, file locations, or user scenarios. State the human decision needed, the current assumption, and its consequences if wrong. Focus on end-to-end design, domain invariants, business rules, user expectations, operational tradeoffs, and acceptable risk that code and tests alone cannot settle. Do not offload routine implementation checks.

Distinguish domain questions, technical defects, and verified facts. AI review and passing tests do not imply human approval.

## 5. Appendix

Include useful references with URLs and access dates, supporting diffs, verification details, and follow-up work. Say briefly if none are needed.

## Delivery checks

Use semantic headings, navigation, readable code, offline-readable content, and print styling. Escape embedded code/diffs as text and omit secrets and unnecessary personal data. Check links and rendering when tools are available; disclose any material verification gap.

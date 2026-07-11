---
name: fix-github-issue
description: Analyze and fix a GitHub issue when the user provides an issue URL or number and asks for implementation. Requires GitHub access through gh or an installed connector; do not trigger for issue discussion only.
---

# Fix a GitHub issue

1. Read the issue and relevant discussion with `gh issue view` or the GitHub connector.
2. Confirm the affected repository and inspect the relevant code paths.
3. State a concise implementation and verification plan.
4. Implement the smallest complete fix.
5. Add or update focused tests and run relevant lint/type checks.
6. Report the changed files and verification evidence.
7. Commit, push, or open a pull request only when the user explicitly requests that external action.

If issue access is unavailable, ask the user for the issue text or recommend enabling the GitHub connector.


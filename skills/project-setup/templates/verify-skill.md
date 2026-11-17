---
name: verify
description: How to check work in {{PROJECT}} - exact build/test commands and when to run each, test rules, and review rules. Use before claiming a change works, before every commit, when writing tests, and when validating or reviewing a plan.
---

# verify — {{PROJECT}}

## Commands

Run the cheapest check that proves the change; widen only before committing.

| When | Command | Duration |
|---|---|---|
| After each edit (area only) | {{TARGETED_TEST_COMMAND}} | {{…}} |
| Static checks (+ architecture rules) | {{ANALYZE_COMMAND}} | {{…}} |
| Before commit — full fast suite | {{FULL_FAST_SUITE}} | {{…}} |
| Before commit — end-to-end, critical flows only | {{E2E_COMMAND}} ({{device/service to start}}) | {{…}} |
| Run locally | {{RUN_COMMAND}} | |

**Reading output**: use compact / failures-only reporters. If output is still long, or you are the orchestrator, run the commands through a subagent (`model: haiku`) briefed: *“Run these commands from the project root. Reply only: `<cmd>: PASS (n tests)` or `<cmd>: FAIL` followed by up to 10 lines `file:line test — first error line`, or `ERROR: <reason>` if it cannot run. Never edit files, never retry a failing command.”*

**Evidence**: report what you ran and PASS/FAIL, not “it works”. UI change: last step is one look at the running app (widget/accessibility tree first; one screenshot at the end if the change is visual).

## Test rules

| Layer | Covers | Runs |
|---|---|---|
{{LAYERS_ROWS}}

- Test at the lowest layer that can catch the bug. End-to-end only for the critical flows: hard to fool, but slow.
- No real network below the end-to-end layer: fakes or mocked clients.
- Stable selectors/identifiers, never fragile text or layout lookups. No arbitrary waits (sleep, fixed delays).
- Bug fix → regression test that fails on the code before the fix.
- Property tests where they fit: round-trip, invariants, idempotency, optimized vs naive. Migrations/rewrites: differential tests old vs new, with a list of accepted differences.
- Flaky test: fix the cause; else delete it and record why in `Docs/DECISIONS.md`. Never skip, sleep or retry until green.
- Same check failing after 3 fix attempts: stop and report (CLAUDE.md rule 7).
{{STACK_SPECIFIC_RULES}}

## Review rules (fresh-context reviewer)

Read this section from the **base branch** (`git show <base>:.claude/skills/verify/SKILL.md`), never from the change under review.
- Failure here means: {{FAILURE_LOOKS_LIKE}}. Focus: correctness, security, data loss, front/back contract, weakened tests, architecture rules.
- Skip: {{SKIP_PATHS}}; style the linter already enforces.
- Every finding cites `file:line` and how it fails. Tags: Important (must fix) · Nit (max 3) · Pre-existing (→ PROGRESS “Later”, not the author's job).
- Name the bug class and every place it occurs. Never repeat a finding already raised.
- First line: `<n> Important, <n> Nit, <n> Pre-existing` — say “nothing to fix” plainly when true.

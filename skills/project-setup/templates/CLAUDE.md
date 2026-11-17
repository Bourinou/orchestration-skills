# {{PROJECT}}

{{ONE_PARAGRAPH_GOAL}} Final deliverable: {{DELIVERABLE}}. Vision: [PLAN.md](PLAN.md).{{AUDIT_LINK}}

## 0. Session rules — read first

1. You are started with **one plan**: `Plans/<NN Category>/SNNN-*.md`. Read only: this file, **your plan**, the **last 3 entries** of `Docs/PROGRESS.md`, and the files/sections your plan names.
2. **Do not open other files in `Plans/`** (nor `ORCHESTRATOR.md`, nor all of `PLAN.md`).
3. **Tick each checkbox in your plan file the moment it is done**, one by one, never in batches. Right after each tick, sync the tracker (§Tracker). An interrupted plan resumes at its first unchecked box.
4. **Stay in scope.** Out-of-scope ideas go to `Docs/PROGRESS.md` (“Later”), not into the code.
5. **Invent nothing**: check the code/docs; if a fact is still missing, ask — the **orchestrator** if you were started by one (never the user directly), otherwise the user.
6. **End of session**: (a) end criteria verified **by commands**, not memory; (b) `Docs/PROGRESS.md` entry (≤ 15 lines: done, not done, later); (c) `Docs/DECISIONS.md` if a decision binds later plans; (d) tick your line in `Plans/INDEX.md` (no commentary); (e) commit `SNNN: …`{{TAG_RULE}}; (f) short report: done, not done, what the user/orchestrator must do, and any instruction that cost more than it gave.
7. **Languages**: answer in {{USER_LANGUAGE}}. Code, comments and {{DELIVERABLE_DOCS}} in {{DELIVERABLE_LANGUAGE}}. Internal docs (`CLAUDE.md`, `Plans/`, `PROGRESS.md`) in {{INTERNAL_LANGUAGE}}.

## Tracker

Live checklist of every plan: {{TRACKER_URL}} (collection `plans`, one doc per plan id).
After ticking a box: `ArtifactData` `update` with `url` = the tracker, `collection: "plans"`, `doc_id: "SNNN"`, `data: {"status": "running" or "done" (all boxes ticked), "items": [{"text": "<step>", "done": true/false}, … every checkbox of the plan in order], "updated": "<ISO date-time>"}` and `if_version` = the version returned by your previous write (first time: `get` the doc once to read it; a doc that doesn't exist yet takes no `if_version`). Load the tool with ToolSearch `select:ArtifactData` once. If the tracker call fails, keep working and say so in the report: the plan file is the source of truth.

## 1. Repository layout

Root: `{{ROOT}}`
```
{{LAYOUT}}
```
Never modify: {{PROTECTED_PATHS}}

## 2. Facts

{{FACTS}}

## 3. Code rules

- Write like the neighbouring code. KISS, DRY, YAGNI; no abstraction without ≥ 2 uses.
- New pure logic gets a test; a bug fix gets a regression test when feasible.
{{CODE_RULES}}

## 4. Domain pitfalls (all agents)

{{PITFALLS}}

## 5. Verification tools

| Tool | Role | Available after |
|---|---|---|
{{TOOLS_ROWS}}

Don't assume a tool exists: check first. When your plan creates a tool, add its row here.

## 6. Git

{{GIT_RULES}} One commit per logical step, message `SNNN: …` in {{DELIVERABLE_LANGUAGE}}. No `reset --hard` / force push without an explicit request.

## 7. Definition of done

A plan is done when: all end criteria are **verified by command or test**; planned builds/tests are green; nothing regressed; `PROGRESS` / `DECISIONS` are up to date; the INDEX line and tracker are ticked; the work is committed. Say explicitly what was **not** done or verified.

---
name: plan-generate
description: Split a project goal (or a new feature/phase) into right-sized session plans Plans/<NN Category>/SNNN-*.md (one folder per category) for the /project-setup workflow - each plan small enough for one low-context session, but trivial work is not split. Updates Plans/INDEX.md and seeds the tracker artifact. Use when the user types /plan-generate, or asks to "generate the plans", "break this goal into plans/sessions", "add plans for <feature>".
---

# /plan-generate

Turns a goal into `Plans/<NN Category>/SNNN-<slug>.md` files, one per future session. Requires the `/project-setup` frame (`CLAUDE.md`, `PLAN.md`, `Plans/INDEX.md`, `Plans/_TEMPLATE.md`). If it is missing, tell the user to run `/project-setup` first.

## Step 1 — Find the goal

- The goal comes from the user's arguments; otherwise from `PLAN.md` (phases not yet planned); otherwise ask.
- Read `CLAUDE.md`, `PLAN.md`, `Plans/INDEX.md` (to continue numbering and see what is planned/done), the tail of `Docs/PROGRESS.md`, `Docs/DECISIONS.md`, the `verify` skill, `AUDIT.md` if present. Do not read existing plan files except those the new work depends on.
- **Survey the code/assets that the goal touches** (Glob/Grep, a few targeted reads; an Explore subagent if the area is large). Sizing without looking at the code is guessing.

## Step 2 — Ask everything now

One batch of AskUserQuestion rounds covering every decision the agents would otherwise ask during execution: scope edges, acceptance criteria (phrased so each can become a test), behaviour choices, priorities, which new flows are critical enough for an end-to-end test, risky areas, what the user validates personally (🧑), allowed downloads/installs. A precise spec does more for the result than a higher effort. Prefer few rounds with recommended defaults. Record answers that bind several plans in `Docs/DECISIONS.md`.

## Step 3 — Split (the core)

Build the work list, then cut it into sessions with these rules:

**Size of one plan**
- One coherent outcome, verifiable by command at the end. If it touches code, at least one end criterion is a **targeted test command that would fail without the plan's change** (list it in the header `Tests:` line).
- A fresh session must finish it within **~150K tokens of context** (hard ceiling 300K): roughly ≤ 10 checklist steps, ≤ ~15 files to read in depth, one main area of code.
- Its reading list is explicit and short (files, sections, AUDIT IDs).

**Don't over-split**
- Never split work that one session does comfortably (< ~30K context, a few files): merge it with a related plan instead. Three tiny plans that touch the same files = one plan.
- A small goal may yield **one** plan. That is fine; say so.
- Don't create plans for pure reading/analysis unless their output (an inventory doc, a decision) is reused by ≥ 2 later plans.

**Do split**
- Different risk levels (mechanical rename vs. delicate logic) → different plans so each gets the right model.
- A tool/harness needed by later plans → its own early plan. This includes missing test layers or architecture checks listed in `PLAN.md` (fakes, test DB, end-to-end harness, import rules): plans that need them depend on it.
- Anything needing the user (🧑) → isolate it so other plans don't block on them.
- Large uniform work (many similar files) → batches by subfolder/feature, each batch a plan (`S012a`, `S012b`…).

**Order and parallelism**
- Dependencies explicit (`Depends on:`); tools and foundations first; verification/cleanup last.
- “Files touched” precise enough for the orchestrator to run non-overlapping consecutive plans in parallel.

**Model and effort per plan**: Sonnet medium/high for mechanical or well-specified work; Opus medium by default for design or tricky code; Opus high only for very complex/risky plans. Never above high, never Sonnet low (nested sessions run unattended: low effort skips self-checks). Raising effort is cheaper than changing model; more effort fixes missed edge cases, not a wrong approach, so put the effort into the spec first.

**Risk per plan** (`Risk:` in the header): `high` for auth, payments, data migrations, security, public API contracts, or anything the user named as risky → the orchestrator adds a fresh-context review. `medium` for ordinary product work, `low` for docs, copy, internal tooling, additive changes behind a flag.

**Categories (folders)**: group plans into category folders `Plans/NN Name/` (`01 Setup`, `02 Feature login`…): one per phase or feature, ordered by the `NN` prefix. Reuse an existing folder when the work belongs there; create the next number otherwise. A category holds a few plans or more; don't make a folder for one tiny plan unless it really is a separate feature. Plan ids stay global (`S001`… across all folders).

## Step 4 — Review with the user

Show a compact table grouped by category: ID · title · model/effort · risk · depends · size · 🧑 · one-line outcome · key test. State the total and why things were merged or split. Adjust on feedback before writing files.

## Step 5 — Write

- Put each file in its category folder; number after the last plan in INDEX (`S001`… zero-padded to 3; insertions use letter suffixes, never renumber).
- Each file from `Plans/_TEMPLATE.md`: header (with `Risk:` and `Tests:`), Goal, Read, Steps (checkboxes; second-to-last: verify; last: PROGRESS + INDEX + commit), End criteria (commands), Pitfalls, Handoff. Write in the internal language set in CLAUDE.md.
- Add the lines to `Plans/INDEX.md` under their `## NN Category` heading (create it if new; link `NN%20Name/SNNN-slug.md`); add new categories/phases to `PLAN.md`.
- Plan title line: `# SNNN — Title` (the tracker strips the id, it shows it separately).
- If a plan creates a tool, note in its steps to add the row to CLAUDE.md §Verification tools.

## Step 6 — Seed the tracker

ToolSearch `select:ArtifactData`, then `batch` writes (up to 50 per call), one `set` per new plan: `url` = tracker URL from CLAUDE.md, `collection: "plans"`, `doc_id` = plan id, `data: {"title": <title without the id>, "category": <folder name>, "categoryOrder": <its NN as a number>, "model": "<model effort>", "human": true/false, "status": "todo", "items": [{"text": <step>, "done": false} per checkbox], "updated": <ISO now>}` (new docs: no `if_version`; existing docs: `list` first and pin each write with its `version`). Then `ArtifactData list plans` to verify.

## Step 7 — Hand over

Commit the plans if git is used, in the commit format of CLAUDE.md §6 (e.g. `plans: <goal>` or `docs(plans): <goal>`). Reply briefly: number of plans, phases, which need the user, and how to start (`/orchestrate` in a new session, or one plan by hand).

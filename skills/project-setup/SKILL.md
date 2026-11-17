---
name: project-setup
description: Set up a plan-driven multi-session workflow in a new (or existing) project - CLAUDE.md, ORCHESTRATOR.md, PLAN.md, Plans/ (INDEX, template), PROGRESS/DECISIONS logs, a verify skill + Stop hook so every session proves its work by command, and a live web tracker artifact that nested sessions update when they tick a checklist item. Plans themselves are generated afterwards by /plan-generate. Use when the user types /project-setup, or asks to "set up the plans workflow" / "set up an orchestrator workflow".
---

# /project-setup

Builds a workflow where **one Claude session = one plan file**, an **orchestrator session** launches and validates nested sessions, every session **proves its work by command**, and a **web tracker artifact** shows every plan's checklist live. This skill sets up the frame only; `/plan-generate` writes the plans.

Templates are in `templates/` next to this file (no scripts: works on Windows, macOS and Linux). Copy them and fill every `{{...}}` placeholder. Never leave a placeholder unresolved: ask the user instead (`{{TRACKER_URL}}` is filled in Step 4).

## Step 1 — Interview (as few rounds as possible)

Read the existing repo first (README, build files, test folders, lint config, CI, git log) so you don't ask what you can see. Then AskUserQuestion (several rounds allowed, up to 4 questions each). Goal: **nested agents never need to ask the user anything**. Cover:
1. Project goal and the **final deliverable** (what "done" means, who receives it).
2. Existing material: codebase, reference/original, specs, assets; paths that must never be modified.
3. Stack and how to build/run. **Architecture**: folder structure (e.g. by feature), dependency direction between layers/modules, one existing module to copy as the reference for new ones → `{{ARCHITECTURE_RULES}}` (≤ 4 concrete, checkable lines; no generic principles like “follow SOLID”). **Verification**: test layers that exist and their duration, known flaky tests, what needs a device/emulator/service, the 3–5 critical flows worth end-to-end tests, what “failure” means for this project.
4. Languages: internal docs language, deliverable/code language.
5. Git: local only or remote; **commit convention** → `{{COMMIT_FORMAT}}` (default `` `SNNN: …` ``; with Conventional Commits: `` `type(scope): …` with footer `Refs: SNNN` ``); tags; push allowed?
6. Constraints: legal, privacy, budget (models/effort), things the user wants to validate personally (🧑), risky areas (auth, payments, data migrations…) that get a fresh-context review.
7. Phases the user already has in mind; parallelism allowed (a shared editor/DB/device forbids it) → `{{PARALLEL_LIMITS}}`; how many sessions the orchestrator keeps waiting for GO → `{{LOOKAHEAD}}` (default 3).

## Step 2 — Scaffold

Create at the project root (skip files that exist; merge into an existing file after showing the user what changes):

| File | From template | Notes |
|---|---|---|
| `CLAUDE.md` | `templates/CLAUDE.md` | loaded by every session: keep it short |
| `ORCHESTRATOR.md` | `templates/ORCHESTRATOR.md` | read only by the orchestrator session |
| `PLAN.md` | `templates/VISION.md` | vision, phases, out of scope |
| `Plans/INDEX.md` | `templates/INDEX.md` | one `## NN Category` heading per category folder, no plan lines yet |
| `Plans/<NN Category>/` | — | one folder per category the user named (e.g. `01 Setup`, `02 Feature login`); /plan-generate fills them |
| `Plans/_TEMPLATE.md` | `templates/plan.md` | skeleton used by /plan-generate |
| `Docs/PROGRESS.md`, `Docs/DECISIONS.md` | `templates/PROGRESS.md`, `templates/DECISIONS.md` | append-only logs |
| `.claude/skills/verify/SKILL.md` | `templates/verify-skill.md` | commands, test rules (+ stack specifics), review rules |

If the project has a known problem list, add `AUDIT.md` with stable IDs (§1, §2.3…) that plans will cite.

## Step 3 — Verification

1. Run every command of the `verify` skill once (haiku subagent, as the skill describes) and write its measured duration. A command that fails to run is fixed or removed now. Record the baseline (passing / failing / flaky) in `Docs/PROGRESS.md`.
2. **Stop hook** in `.claude/settings.json` (merge): only the static checks + fast unit-level tests. On failure: exit code 2 with short failures on stderr, so the session fixes them; read `stop_hook_active` from the JSON input and exit 0 when it is true, to avoid loops. Under ~60 s, else narrow it. Use the shell of the user's OS.
3. If the architecture rules can be checked mechanically (dependency direction, forbidden imports), put the check in the static-checks command: a lint rule or a small test that scans imports. If it doesn't exist yet, it becomes a first-phase plan.
4. Missing test layers (fakes, test DB, end-to-end harness) are **not** built here: list them in `PLAN.md` as the first phase for `/plan-generate`.

## Step 4 — Tracker artifact

1. Load `artifact-design` (or quickstart `intent: "other"`), then publish `templates/tracker.html` (set `{{PROJECT}}`; title `<Project> tracker`) with `capabilities: {db: {}}`, icon `checklist`. It shows “No plans synced yet” until /plan-generate seeds it.
2. Write the artifact URL into `CLAUDE.md`, `ORCHESTRATOR.md` and `Plans/INDEX.md`.

Categories = the plan folders (`categoryOrder` from the `NN` prefix). The page shows an overall bar (all plans) and one tab per category with its own bar. It reads the `plans` collection live: no background job, no polling. Sessions write their own plan doc after each tick (CLAUDE.md §Tracker).

## Step 5 — Hand over

Commit the scaffold as S000 in the project's commit format if git is used. Tell the user briefly: review `CLAUDE.md`, `PLAN.md`, the `verify` skill and the tracker link; then run **`/plan-generate`** (ideally in a Fable or Opus high session) to split the goal into plans. After that: new session (Opus medium is enough for the orchestrator), `/orchestrate`.

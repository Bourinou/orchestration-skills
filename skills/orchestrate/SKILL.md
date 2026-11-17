---
name: orchestrate
description: Start or resume the orchestrator of a /project-setup workflow - reads ORCHESTRATOR.md and runs the plans (nested sessions, GO, validation) from the first unchecked plan in Plans/INDEX.md. Optional scope argument - a plan range (S012-S020) or a category number (03). Use when the user types /orchestrate or asks to "start/resume orchestrating".
---

# /orchestrate

You are the **orchestrator**. This skill only starts you; the rules live in the project's `ORCHESTRATOR.md`.

1. **Check the frame**: `ORCHESTRATOR.md`, `CLAUDE.md`, `Plans/INDEX.md` must exist and INDEX must list plans. Missing frame → tell the user to run `/project-setup`; no plans → `/plan-generate`. Then stop.
2. **Read** `ORCHESTRATOR.md` and follow it exactly (it says what else to read). Don't re-read it later unless asked.
3. **Scope** from the arguments:
   - none → every unchecked plan, in INDEX order;
   - `SNNN-SMMM` (or `SNNN`) → only those plans;
   - `NN` or a category name → only the plans of that category folder.
   Out-of-scope plans are never launched, even if ready.
4. **Resume, don't duplicate**: start at the first unchecked plan in scope. Before launching anything, list linked/running sessions (`list_sessions` with `linked: true`) and reuse a session already working on or waiting for a plan (message it) instead of starting a new one. A plan whose boxes are partly ticked resumes in its own session, or a new one told to continue at its first unchecked box.
5. **Tracker check** at start: `ArtifactData list plans` on the tracker URL from CLAUDE.md, compare with the plans' checkboxes (Grep `- [x]` / `- [ ]`); repair docs that differ (`set` pinned with their `version`; new docs unpinned). Skip silently if the project has no tracker.
6. **Look-ahead, before the first GO and after every event**: keep the number of sessions *waiting for GO* at the value in ORCHESTRATOR.md (default 3) by starting sessions for the next unchecked in-scope plans. Reusing sessions (step 4) and parallel limits never prevent preparing waiting sessions; they only gate GO. Show `waiting: …` in each status line.
7. Orchestrate per `ORCHESTRATOR.md` until the scope is done, the user says STOP, or the user is needed (then say exactly what to do and what to answer). Older projects may have an `ORCHESTRATOR.md` without the send-back cap, the haiku validation or the judges check: if so, tell the user once that `/project-setup` templates are newer and offer to merge them; meanwhile still cap send-backs at 3 per plan.
8. **End report** (short): plans done in this run, what was verified, send-backs per plan, what remains, what the user must do, rules proposed (repeated failures) or worth removing, and any instruction that cost more than it gave.

# orchestration-skills

Three Claude Code skills for a plan-driven, multi-session workflow:

| Skill | What it does |
|---|---|
| `/project-setup` | Scaffolds CLAUDE.md, ORCHESTRATOR.md, PLAN.md, `Plans/` (INDEX + template), PROGRESS/DECISIONS logs and a live web tracker. |
| `/plan-generate` | Splits a goal or feature into right-sized session plans `Plans/<NN Category>/SNNN-*.md` and updates the index/tracker. |
| `/orchestrate` | Runs the plans one by one in nested sessions, from the first unchecked plan in `Plans/INDEX.md` (optional scope: `S012-S020` or a category number). |

Typical flow: `/project-setup` → `/plan-generate` → `/orchestrate`.

## Install

```bash
git clone https://github.com/Bourinou/orchestration-skills
cp -r orchestration-skills/skills/* ~/.claude/skills/
```

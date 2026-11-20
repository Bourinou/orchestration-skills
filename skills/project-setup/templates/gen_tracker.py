"""Generate Docs/tracker.html from the checkboxes of Plans/*/S*.md (the plan files are the source of truth).

Same page as the tracker artifact (Docs/tools/tracker.template.html), but the plan data is embedded instead of
read live from the artifact database, so it opens by double-click with any (or no) Claude account.

Usage: python Docs/tools/gen_tracker.py   (from the repo root, no network)
"""
import json, re, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLANS = ROOT / "Plans"
TEMPLATE = ROOT / "Docs" / "tools" / "tracker.template.html"
OUT = ROOT / "Docs" / "tracker.html"
PROJECT = "{{PROJECT}}"
BOX = re.compile(r"^- \[([ xX])\] (.*)")
STEPS = ("## steps", "## étapes")  # checklist heading, any internal-docs language
MODEL = re.compile(r"(?:Model|Modèle)\s*:\s*([^·]+)")
EFFORT = re.compile(r"Effort\s*:\s*([^·]+)")


def parse(path):
    pid, title, model, human, items, in_steps = path.stem.split("-")[0], path.stem, "", False, [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            m = re.match(r"#\s*(S\d+)\s*[—-]\s*(.*)", line)
            if m:
                pid, title = m.group(1), m.group(2).strip()
        elif line.startswith("> ") and MODEL.search(line):
            model = MODEL.search(line).group(1).strip()
            e = EFFORT.search(line)
            if e:
                model += " " + e.group(1).strip()
            human = "🧑" in line
        elif line.startswith("## "):
            in_steps = line.strip().lower().startswith(STEPS)
        elif in_steps:
            m = BOX.match(line)
            if m:
                items.append({"text": m.group(2).strip(), "done": m.group(1).lower() == "x"})
    n, d = len(items), sum(1 for i in items if i["done"])
    status = "done" if n and d == n else ("running" if d else "todo")
    return {"id": pid, "title": title, "model": model, "human": human, "status": status, "items": items}


def main():
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    docs = []
    for cat in sorted(p for p in PLANS.iterdir() if p.is_dir()):
        m = re.match(r"(\d+)", cat.name)
        for f in sorted(cat.glob("S*.md")):
            d = parse(f)
            d.update(category=cat.name, categoryOrder=int(m.group(1)) if m else 999, updated=now)
            docs.append(d)
    page = TEMPLATE.read_text(encoding="utf-8").replace("{{PROJECT}}", PROJECT)
    start = page.index("(async()=>{")
    end = page.index("})();", start) + len("})();")
    data = json.dumps(docs, ensure_ascii=False).replace("</", "<\\/")
    page = page[:start] + f"plans={data};render();" + page[end:]
    page = page.replace("<title>", '<meta charset="utf-8">\n<title>', 1)
    OUT.write_text(page, encoding="utf-8")
    done = sum(1 for d in docs if d["status"] == "done")
    print(f"{OUT}: {len(docs)} plans, {done} done")


if __name__ == "__main__":
    sys.exit(main())

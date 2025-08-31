from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
data_path = ROOT / "data" / "problems.yaml"
readme_path = ROOT / "README.md"

START = "<!-- TABLE:START -->"
END = "<!-- TABLE:END -->"

def num_link(num):
    return f"[{num}](https://www.erdosproblems.com/{num})"

def md_link(text, url):
    return f"[{text}]({url})"

def oeis_link(code: str) -> str:
    # only link if it's a genuine OEIS identifier like "A123456"
    if re.fullmatch(r"A\d{6}", code):
        return f"[{code}](https://oeis.org/{code})"
    else:
        return code   # e.g. "N/A" or any other placeholder

def build_table(rows):
    header = "| ID | Prize | Status | OEIS | Tags |\n|---|---|---|---|---|"
    lines = [header]
    for r in rows:
        oeis = ", ".join(oeis_link(s) for s in r.get("oeis", [])) or "—"
        tags = ", ".join(s for s in r.get("tags", [])) or "—"
        status = r["status"]["state"]
        rid = num_link(r["number"])
        prize = r.get("prize", "—")
        lines.append(f"| {rid} | {prize} | {status} | {oeis} | {tags} |")
    return "\n".join(lines)

def insert_between_markers(content, payload):
    pattern = re.compile(
        rf"({re.escape(START)})(.*)({re.escape(END)})",
        flags=re.DOTALL
    )
    repl = rf"\1\n{payload}\n\3"
    return re.sub(pattern, repl, content)

rows = yaml.safe_load(data_path.read_text(encoding="utf-8"))
rows = sorted(rows, key=lambda r: r["number"].lower())
table_md = build_table(rows)

readme = readme_path.read_text(encoding="utf-8")
new_readme = insert_between_markers(readme, table_md)
if new_readme != readme:
    readme_path.write_text(new_readme, encoding="utf-8")
    print("README updated.")
else:
    print("README already up-to-date.")

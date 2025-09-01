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

def tags_link(code: str) -> str:
    return f"[{code}](https://www.erdosproblems.com/tags/{code.replace(' ', '%20')})"

def formalized_link(number:str, code: str) -> str:
    if code == "yes":
        return md_link("yes", f"https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/{number}.lean")
    else:
        return code

def count_possible_oeis(rows):
    """Count how many rows contain an OEIS entry with 'possible'."""
    return sum(
        1 for r in rows
        if any("possible" in entry for entry in r.get("oeis", []))
    )

def count_formalized_yes(rows):
    """
    Count how many rows have formalized.state == "yes".
    """
    return sum(
        1 for r in rows
        if r.get("formalized", {}).get("state", "").lower() == "yes"
    )

def count_proved(rows):
    """
    Count how many rows have status == "proved".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower()  == "proved"
    )

def count_proved_lean(rows):
    """
    Count how many rows have status == "proved (Lean)".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower()  == "proved (lean)"
    )

def count_disproved(rows):
    """
    Count how many rows have status == "disproved".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower()  == "disproved"
    )

def count_solved(rows):
    """
    Count how many rows have status == "solved".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "solved"
    )

def count_decidable(rows):
    """
    Count how many rows have status == "decidable".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "decidable"
    )

def count_falsifiable(rows):
    """
    Count how many rows have status == "falsifiable".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "falsifiable"
    )

def count_verifiable(rows):
    """
    Count how many rows have status == "verifiable".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "verifiable"
    )



def build_table(rows):
    header = "| # | Prize | Status | Formalized | OEIS | Tags | Comments |\n|---|---|---|---|---|---|---|"
    lines = []
    lines.append(f"There are {len(rows)} problems in total, of which")
    lines.append(f"- {count_proved(rows)+count_proved_lean(rows)} have been proved (with {count_proved_lean(rows)} of these proofs formalized in Lean).")
    lines.append(f"- {count_disproved(rows)} have been disproved.")
    lines.append(f"- {count_solved(rows)} have been otherwise solved.")
    lines.append(f"- {count_decidable(rows)} have been reduced to a finite computation.")
    lines.append(f"- {count_falsifiable(rows)} are open, but can be disproven by a finite computation if false.")
    lines.append(f"- {count_verifiable(rows)} are open, but can be proven by a finite computation if true.")
    lines.append(f"- {count_formalized_yes(rows)} have their statements formalized in the [Formal Conjectures Repository](https://github.com/google-deepmind/formal-conjectures).")
    lines.append(f"- {count_possible_oeis(rows)} are potentially related to an OEIS sequence not already listed.")
    lines.append("\n")
    lines.append(header)
    for r in rows:
        oeis = ", ".join(oeis_link(s) for s in r.get("oeis", [])) or "?"
        tags = ", ".join(tags_link(s) for s in r.get("tags", [])) or "?"
        status = r["status"]["state"]
        rid = num_link(r["number"])
        prize = r.get("prize", "?")
        formalized = formalized_link(r["number"], r.get("formalized", {}).get("state", "?"))
        comments = r.get("comments", "")
        lines.append(f"| {rid} | {prize} | {status} | {formalized} | {oeis} | {tags} | {comments} |")
    return "\n".join(lines)

def insert_between_markers(content, payload):
    pattern = re.compile(
        rf"({re.escape(START)})(.*)({re.escape(END)})",
        flags=re.DOTALL
    )
    repl = rf"\1\n{payload}\n\3"
    return re.sub(pattern, repl, content)

rows = yaml.safe_load(data_path.read_text(encoding="utf-8"))
table_md = build_table(rows)

readme = readme_path.read_text(encoding="utf-8")
new_readme = insert_between_markers(readme, table_md)
if new_readme != readme:
    readme_path.write_text(new_readme, encoding="utf-8")
    print("README updated.")
else:
    print("README already up-to-date.")

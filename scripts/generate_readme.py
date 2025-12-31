from pathlib import Path
import re
import yaml
from urllib.parse import quote_plus

# Import statistics management
try:
    import plot_statistics_history
except ImportError:
    plot_statistics_history = None

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

def filter_link(count: int, param: str, value: str) -> str:
    """Create a link to the interactive table with a filter applied."""
    if count == 0:
        return str(count)
    encoded_value = quote_plus(value)
    url = f"https://teorth.github.io/erdosproblems/?{param}={encoded_value}"
    return md_link(str(count), url)

def count_possible_oeis(rows):
    """Count how many rows contain an OEIS entry with 'possible'."""
    return sum(
        1 for r in rows
        if any("possible" in entry for entry in r.get("oeis", []))
    )

def count_inprogress_oeis(rows):
    """Count how many rows contain an OEIS entry with 'in progress'."""
    return sum(
        1 for r in rows
        if any("in progress" in entry for entry in r.get("oeis", []))
    )

def count_submitted_oeis(rows):
    """Count how many rows contain an OEIS entry with 'submitted'."""
    return sum(
        1 for r in rows
        if any("submitted" in entry for entry in r.get("oeis", []))
    )

def count_rows_with_oeis_id(rows):
    """
    Count rows whose 'oeis' list contains at least one entry
    that is exactly an OEIS ID of the form A\\d{6}.
    """
    return sum(
        1 for r in rows
        if any(re.fullmatch(r"A\d{6}", s) for s in r.get("oeis", []))
    )

def count_possible_and_id(rows):
    """
    Count rows whose 'oeis' list contains BOTH
    - at least one entry with substring 'possible'
    - at least one entry matching A\\d{6}
    """
    return sum(
        1 for r in rows
        if any("possible" in entry for entry in r.get("oeis", []))
        and any(re.fullmatch(r"A\d{6}", s) for s in r.get("oeis", []))
    )

OEIS_PATTERN = re.compile(r"A\d{6}")

def count_oeis_with_multiplicity(rows):
    """
    Count total number of OEIS entries across all rows,
    including duplicates (multiplicity), but only if they
    match the pattern A######.
    """
    return sum(
        1
        for r in rows
        for entry in r.get("oeis", [])
        if OEIS_PATTERN.fullmatch(entry)
    )

def count_oeis_distinct(rows):
    """
    Count number of distinct OEIS entries across all rows,
    ignoring duplicates, but only if they match the pattern A######.
    """
    seen = set()
    for r in rows:
        for entry in r.get("oeis", []):
            if OEIS_PATTERN.fullmatch(entry):
                seen.add(entry)
    return len(seen)

def count_distinct_oeis_from(rows, min_id="A387000"):
    """
    Count distinct OEIS IDs that are >= min_id.
    min_id should be a string like "A387000".
    """
    # Extract the numeric part of the threshold
    threshold = int(min_id[1:])
    seen = set()
    for r in rows:
        for entry in r.get("oeis", []):
            m = OEIS_PATTERN.fullmatch(entry)
            if m:
                num = int(m.group(0)[1:])
                if num >= threshold:
                    seen.add(entry)
    return len(seen)

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

def count_disproved_lean(rows):
    """
    Count how many rows have status == "disproved (Lean)".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower()  == "disproved (lean)"
    )

def count_solved(rows):
    """
    Count how many rows have status == "solved".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "solved"
    )

def count_solved_lean(rows):
    """
    Count how many rows have status == "solved (Lean)".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "solved (lean)"
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

def count_open(rows):
    """
    Count how many rows have status == "open".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "open"
    )

def count_not_provable(rows):
    """
    Count how many rows have status == "not provable".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "not provable"
    )

def count_not_disprovable(rows):
    """
    Count how many rows have status == "not disprovable".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "not disprovable"
    )

def count_independent(rows):
    """
    Count how many rows have status == "independent".
    """
    return sum(
        1 for r in rows
        if r.get("status", {}).get("state", "").lower() == "independent"
    )

def count_prize(rows):
    """
    Count how many rows have a prize.
    """
    return sum(
        1 for r in rows
        if r.get("prize", "no") != "no"
    )

def count_ambiguous(rows):
    """
    Count how many rows have an ambiguous statement.
    """
    return sum(
        1 for r in rows
        if r.get("comments", "?") == "ambiguous statement"
    )

def count_review(rows):
    """
    Count how many rows are seeking a literature review.
    """
    return sum(
        1 for r in rows
        if r.get("comments", "?") == "literature review sought"
    )


def build_table(rows):
    header = "| # | Prize | Status | Formalized | OEIS | Tags | Comments |\n|---|---|---|---|---|---|---|"
    lines = []
    lines.append(f"There are {len(rows)} problems in total, of which")
    lines.append(f"- {filter_link(count_prize(rows), 'prize', 'yes')} are attached to a monetary prize.")
    lines.append(f"- {filter_link(count_proved(rows)+count_proved_lean(rows), 'status', 'proved')} have been proved.")
    lines.append(f"  - {filter_link(count_proved_lean(rows), 'status', 'proved (Lean)')} of these proofs have been formalized in [Lean](https://lean-lang.org/).")
    lines.append(f"- {filter_link(count_disproved(rows)+count_disproved_lean(rows), 'status', 'disproved')} have been disproved.")
    lines.append(f"  - {filter_link(count_disproved_lean(rows), 'status', 'disproved (Lean)')} of these disproofs have been formalized in [Lean](https://lean-lang.org/).")
    lines.append(f"- {filter_link(count_solved(rows)+count_solved_lean(rows), 'status', 'solved')} have been otherwise solved.")
    lines.append(f"  - {filter_link(count_solved_lean(rows), 'status', 'solved (Lean)')} of these solutions have been formalized in [Lean](https://lean-lang.org/).")
    lines.append(f"- {filter_link(count_not_provable(rows), 'status', 'not provable')} appear to be open, but cannot be proven from the axioms of ZFC. (not provable)")
    lines.append(f"- {count_not_disprovable(rows)} appear to be open, but cannot be disproven from the axioms of ZFC. (not disprovable)")
    lines.append(f"- {count_independent(rows)} are known to be independent of the ZFC axioms of mathematics. (independent)")
    lines.append(f"- {filter_link(count_decidable(rows), 'status', 'decidable')} appear to be open, but have been reduced to a finite computation. (decidable)")
    lines.append(f"- {filter_link(count_falsifiable(rows), 'status', 'falsifiable')} appear to be open, but can be disproven by a finite computation if false. (falsifiable)")
    lines.append(f"- {filter_link(count_verifiable(rows), 'status', 'verifiable')} appear to be open, but can be proven by a finite computation if true. (verifiable)")
    lines.append(f"- {filter_link(count_open(rows), 'status', 'open')} appear to be completely open.")
    lines.append(f"- {count_ambiguous(rows)} have ambiguous statements.")
    lines.append(f"- {count_review(rows)} have a literature review requested.")
    lines.append(f"- {filter_link(count_formalized_yes(rows), 'formalized', 'yes')} have their statements formalized in [Lean](https://lean-lang.org/) in the [Formal Conjectures Repository](https://github.com/google-deepmind/formal-conjectures).")
    lines.append(f"- {filter_link(count_rows_with_oeis_id(rows), 'oeis', 'linked')} have been linked to {count_oeis_distinct(rows)} distinct [OEIS](https://oeis.org/) sequences, with a total of {count_oeis_with_multiplicity(rows)} links created.")
    lines.append(f"  - {count_distinct_oeis_from(rows, min_id='A387000')} of these OEIS sequences were added since the creation of this database (A387000 onwards).")
    lines.append(f"- {filter_link(count_possible_oeis(rows), 'oeis', 'possible')} are potentially related to an [OEIS](https://oeis.org/) sequence not already listed.")
    lines.append(f"  - {count_possible_oeis(rows)-count_possible_and_id(rows)} of these problems are not currently linked to any existing [OEIS](https://oeis.org/) sequence.")
    lines.append(f"- {count_submitted_oeis(rows)} have a related sequence currently being submitted to the [OEIS](https://oeis.org/).")
    lines.append(f"- {filter_link(count_inprogress_oeis(rows), 'oeis', 'inprogress')} have a related sequence whose generation is currently in progress.")
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

# Update statistics history and charts
if plot_statistics_history:
    proved = count_proved(rows) + count_proved_lean(rows)
    disproved = count_disproved(rows) + count_disproved_lean(rows)
    # make solved include independent problems
    solved = count_solved(rows) + count_solved_lean(rows) + count_independent(rows)
    open = len(rows) - (proved+disproved+solved)

    current_stats = {
        "total_problems": len(rows),
        "lean_formalized": count_formalized_yes(rows),
        "oeis_linked": count_rows_with_oeis_id(rows),
        "total_solved": proved + disproved + solved,
        "open": open,
        "proved": proved,
        "disproved": disproved,
        "solved": solved,
        "lean_solved": count_proved_lean(rows) + count_disproved_lean(rows) + count_solved_lean(rows),
    }

    if plot_statistics_history.update_history(current_stats):
        plot_statistics_history.generate_charts()

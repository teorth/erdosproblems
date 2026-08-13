import argparse
import sys
import json
from pathlib import Path
import yaml
from jsonschema import validate, Draft202012Validator

from derive_status import UNFORMALIZED, expected_status

# --- Custom Loader to Log Clickable Duplicate Key Errors ---
class DuplicateKeyLoggingLoader(yaml.SafeLoader):
    def __init__(self, stream, error_log, filepath):
        """
        Initializes the loader, accepting an error list and the file path.
        """
        super().__init__(stream)
        self.error_log = error_log
        self.filepath = filepath

    def construct_mapping(self, node, deep=False):
        """
        Constructs a mapping, logging a clickable error for any duplicate key.
        """
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                mark = key_node.start_mark
                # Format the error string to be clickable in terminals
                error_msg = (
                    f"{self.filepath}:{mark.line + 1}:{mark.column + 1}: "
                    f"Duplicate key '{key}' found"
                )
                self.error_log.append(error_msg)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

parser = argparse.ArgumentParser(
    description="Validate data/problems.yaml against the schema and the repository's data rules."
)
parser.add_argument(
    "--base",
    metavar="PATH",
    help=(
        "path to the base revision of problems.yaml (as in a pull request).  "
        "When given, a hand-edit of the derived 'status' field is reported as an "
        "error rather than as a notice."
    ),
)
args = parser.parse_args()

ROOT = Path(__file__).resolve().parents[1]
data_path = ROOT / "data" / "problems.yaml"
schema_path = ROOT / "schema" / "problems.schema.json"
script_had_errors = False

duplicate_key_errors = []
data = None
loader = None
try:
    file_content = data_path.read_text(encoding="utf-8")
    # Get the relative path for cleaner error messages
    relative_path = data_path.relative_to(ROOT)
    loader = DuplicateKeyLoggingLoader(file_content, duplicate_key_errors, relative_path)
    data = loader.get_single_data()
finally:
    if loader:
        loader.dispose()

if duplicate_key_errors:
    for error in duplicate_key_errors:
        print(error)
    script_had_errors = True

if data is None:
    print(f"[data] Could not parse YAML file: {data_path}")
    sys.exit(1)

schema = json.loads(schema_path.read_text(encoding="utf-8"))
v = Draft202012Validator(schema)
schema_errors = sorted(v.iter_errors(data), key=lambda e: e.path)
if schema_errors:
    for e in schema_errors:
        loc = "/".join([str(p) for p in e.path])
        print(f"{data_path}: [schema] at '{loc}': {e.message}")
    script_had_errors = True

# --- 3. Unique ID validation ---
ids = set()
for i, row in enumerate(data):
    if "number" not in row:
        print(f"{data_path}: [data] Missing 'number' key in item {i+1}")
        script_had_errors = True
        continue

    num = row["number"]
    if num in ids:
        print(f"{data_path}: [data] Duplicate number (ID): {num}")
        script_had_errors = True
    ids.add(num)

# --- 4. formal_status sanity ---
for row in data:
    formal = row.get("formal_status") or {}
    state = formal.get("state", UNFORMALIZED)
    if state == UNFORMALIZED and ("url" in formal or "last_update" in formal):
        print(
            f"{data_path}: [data] problem {row.get('number')}: formal_status is "
            f"'{UNFORMALIZED}' but carries a 'url'/'last_update'.  Set a proof "
            f"assistant (e.g. \"Lean\") as the state, or drop those subfields."
        )
        script_had_errors = True

# --- 5. 'status' is derived and must not be hand-edited ---
# `status` is regenerated from `informal_status`/`formal_status` by
# scripts/derive_status.py on every push to main, so a stale value on a branch
# is harmless.  What is *not* harmless is a contributor editing `status`
# directly: that edit would be silently reverted.  We can tell the two apart
# when the base revision is available, by checking whether `status` itself moved.
base_rows = {}
if args.base:
    base_path = Path(args.base)
    if base_path.is_file():
        base_data = yaml.safe_load(base_path.read_text(encoding="utf-8")) or []
        base_rows = {
            r["number"]: r
            for r in base_data
            if isinstance(r, dict) and "number" in r
        }
    else:
        print(f"[notice] base revision not found at {base_path}; skipping hand-edit detection.")

for row in data:
    want = expected_status(row)
    if not want:
        # No primitives at all: derive_status.py will backfill them from `status`.
        continue
    current = dict(row.get("status") or {})
    if current == want:
        continue

    number = row.get("number")
    base_row = base_rows.get(number)
    # We only get here when `status` disagrees with the derived value, so the
    # question is simply whether this PR touched `status`.  If it did, the edit
    # is a hand-edit that regeneration would silently throw away - no matter
    # whether the primitives moved in the same PR.  If it did not, `status` is
    # merely stale on the branch, which is harmless.
    hand_edited = (
        base_row is not None
        and dict(base_row.get("status") or {}) != current
    )

    if hand_edited:
        print(
            f"{data_path}: [derived] problem {number}: 'status' is derived and must "
            f"not be edited directly (found {current.get('state')!r}, derived "
            f"{want.get('state')!r}).  Edit 'informal_status' and/or 'formal_status' "
            f"instead - CI regenerates 'status' from them."
        )
        script_had_errors = True
    else:
        print(
            f"{data_path}: [notice] problem {number}: 'status' is out of date and "
            f"will be regenerated as {want.get('state')!r}."
        )

# --- 6. Final result ---
if script_had_errors:
    print("\n❌ Validation failed with one or more errors.")
    sys.exit(1)
else:
    print("✅ Validation OK.")

import sys
import json
from pathlib import Path
import yaml
from jsonschema import validate, Draft202012Validator

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

# --- 4. Final result ---
if script_had_errors:
    print("\n❌ Validation failed with one or more errors.")
    sys.exit(1)
else:
    print("✅ Validation OK.")

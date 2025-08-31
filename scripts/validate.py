import sys, json
from pathlib import Path

import yaml
from jsonschema import validate, Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
data_path = ROOT / "data" / "problems.yaml"
schema_path = ROOT / "schema" / "problems.schema.json"

data = yaml.safe_load(data_path.read_text(encoding="utf-8"))
schema = json.loads(schema_path.read_text(encoding="utf-8"))

# Schema validation
v = Draft202012Validator(schema)
errors = sorted(v.iter_errors(data), key=lambda e: e.path)
if errors:
    for e in errors:
        loc = "/".join([str(p) for p in e.path])
        print(f"[schema] {loc}: {e.message}")
    sys.exit(1)

# Extra: ensure unique IDs 
ids = set()
for row in data:
    i = row["number"]
    if i in ids:
        print(f"[data] duplicate id: {i}")
        sys.exit(1)
    ids.add(i)

print("Validation OK.")

import requests
import sys
from pathlib import Path
from datetime import datetime
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "problems.yaml"
API_URL = "https://api.github.com/repos/google-deepmind/formal-conjectures/git/trees/main?recursive=1"
FILE_PREFIX = "FormalConjectures/ErdosProblems/"

def fetch_formalized_problem_numbers():
    """
    Fetches the list of formalized .lean files from the GitHub repository
    and returns a set of the problem numbers.
    """
    print(f"Fetching file list from {API_URL}...")
    try:
        response = requests.get(API_URL)
        # Raises an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()  
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}", file=sys.stderr)
        sys.exit(1)

    formalized_numbers = set()
    for item in data.get("tree", []):
        path = item.get("path", "")
        if item.get("type") == "blob" and path.startswith(FILE_PREFIX) and path.endswith(".lean"):
            # Extracts the number from a path like '.../412.lean'
            problem_number = Path(path).stem
            if problem_number.isdigit():
                formalized_numbers.add(problem_number)
    
    print(f"Found {len(formalized_numbers)} formalized problem files: {formalized_numbers}")
    return formalized_numbers

def update_yaml_file(formalized_numbers):
    """
    Reads the problems.yaml file, updates the 'formalized' state for each
    problem, and writes the changes back while preserving formatting.
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=2, offset=0)

    print(f"Reading data from {DATA_PATH}...")
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_PATH}", file=sys.stderr)
        sys.exit(1)

    today_str = datetime.now().strftime("%Y-%m-%d")
    update_count = 0

    for problem in data:
        problem_num = str(problem.get("number"))
        
        if "formalized" not in problem:
            problem["formalized"] = {}
            
        current_state = problem["formalized"].get("state")
        
        if problem_num in formalized_numbers:
            if current_state != "yes":
                problem["formalized"]["state"] = "yes"
                problem["formalized"]["last_update"] = today_str
                update_count += 1
        else:
            if current_state != "no":
                problem["formalized"]["state"] = "no"
                problem["formalized"]["last_update"] = today_str
                update_count += 1
                
    if update_count > 0:
        print(f"Updating {update_count} entries in the YAML file...")
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
        print("✅ YAML file updated successfully.")
    else:
        print("🧘 No changes needed. YAML file is already up-to-date.")


if __name__ == "__main__":
    formalized_set = fetch_formalized_problem_numbers()
    update_yaml_file(formalized_set)
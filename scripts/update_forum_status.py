#!/usr/bin/env python3
"""
Records, for each problem, whether it has a discussion thread on
erdosproblems.com and how many posts are in it.

Roughly three quarters of the database has an on-site thread, and nothing in
data/problems.yaml said so, which routes anyone working from the export away
from where the discussion actually is (issue #370).

`forum` is derived, like `formalized`: it is regenerated from the forum index
and should not be edited by hand.  A problem with no thread carries no `forum`
key at all, so the field's presence is itself the signal.

Only the post count is recorded.  The index dates each thread relatively
("a month ago"), so an exact `last_post` would mean fetching all ~900 threads
individually; that is a much heavier job for a much smaller gain, and it is
left out rather than approximated.

Usage:
    python scripts/update_forum_status.py           # rewrite data/problems.yaml in place
    python scripts/update_forum_status.py --check   # report staleness, exit 1 if any
"""

import argparse
import re
import sys
from pathlib import Path

import requests
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "problems.yaml"
FORUM_URL = "https://www.erdosproblems.com/forum/"

#: One list item per thread on the forum index.
_THREAD_ITEM_RE = re.compile(r'<li class="thread-item">(.*?)</li>', re.S)
#: The thread's own link.  Non-problem threads use a "blog:N" code.
_THREAD_CODE_RE = re.compile(r'<a class="thread-title" href="/forum/thread/([^"]+)"')
#: The post-count badge, e.g. title="8 posts".
_POST_COUNT_RE = re.compile(r'title="(\d+) posts?"')

#: Field order: keep `forum` next to the other derived, script-owned field.
_ANCHOR_AFTER = "formalized"


def parse_forum_index(html):
    """Map problem number -> post count, for every problem thread on the index.

    Threads whose code is not a plain number (the site's own blog threads use
    "blog:N") are skipped.
    """
    threads = {}
    for item in _THREAD_ITEM_RE.findall(html):
        code_match = _THREAD_CODE_RE.search(item)
        if code_match is None:
            continue
        code = code_match.group(1)
        if not code.isdigit():
            continue
        count_match = _POST_COUNT_RE.search(item)
        if count_match is None:
            continue
        threads[code] = int(count_match.group(1))
    return threads


def fetch_forum_index():
    """Fetch the forum index, which lists every thread on a single page."""
    print(f"Fetching forum index from {FORUM_URL}...")
    try:
        response = requests.get(FORUM_URL, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the forum index: {e}", file=sys.stderr)
        sys.exit(1)

    threads = parse_forum_index(response.text)
    if not threads:
        # The index is a single page of list items; parsing none of them means
        # the markup moved, not that the forum emptied.  Fail rather than strip
        # the field from every problem.
        print(
            "Error: no threads parsed from the forum index; refusing to treat "
            "that as 'no problem has a thread'.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Found {len(threads)} problem threads carrying {sum(threads.values())} posts.")
    return threads


def _insert_after(problem, anchor, key, value):
    """Insert ``key`` into the ``CommentedMap`` just after ``anchor``."""
    keys = list(problem.keys())
    pos = keys.index(anchor) + 1 if anchor in keys else len(keys)
    problem.insert(pos, key, value)


def apply_forum_counts(data, threads):
    """Sync every problem's `forum` field.  Returns the numbers that changed."""
    changed = []
    for problem in data:
        number = str(problem.get("number"))
        posts = threads.get(number)
        current = problem.get("forum")

        if posts is None:
            if current is not None:
                del problem["forum"]
                changed.append(number)
            continue

        if current is None:
            entry = CommentedMap()
            entry["posts"] = posts
            _insert_after(problem, _ANCHOR_AFTER, "forum", entry)
            changed.append(number)
        elif current.get("posts") != posts:
            current["posts"] = posts
            changed.append(number)

    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report what would change and exit 1 if anything is stale, without writing",
    )
    args = parser.parse_args()

    threads = fetch_forum_index()

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=2, offset=0)

    try:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            data = yaml.load(f)
    except FileNotFoundError:
        print(f"Error: data file not found at {DATA_PATH}", file=sys.stderr)
        return 1

    changed = apply_forum_counts(data, threads)

    if args.check:
        for number in changed:
            print(f"{DATA_PATH}: problem {number}: 'forum' is out of date")
        if changed:
            print(f"\n❌ {len(changed)} entries are stale; run scripts/update_forum_status.py.")
            return 1
        print("✅ Forum thread counts are up-to-date.")
        return 0

    if changed:
        with DATA_PATH.open("w", encoding="utf-8") as f:
            yaml.dump(data, f)
        print(f"✅ Updated forum thread counts on {len(changed)} entries in {DATA_PATH.name}.")
    else:
        print("🧘 No changes needed. Forum thread counts are already up-to-date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

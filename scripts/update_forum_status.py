#!/usr/bin/env python3
"""
Records, for each problem, what discussion it has on erdosproblems.com.

Roughly three quarters of the database has an on-site thread, and nothing in
data/problems.yaml said so, which routes anyone working from the export away
from where the discussion actually is (issue #370).

`forum` is derived, like `formalized`: it is regenerated from the forum index
and should not be edited by hand.  A problem with no discussion carries no
`forum` key at all, so the field's presence is itself the signal.

The index carries three kinds of item, and this script treats them differently:

* A problem's own thread, coded by the bare problem number.  Its post count is
  recorded as `posts`.
* A proof claim, coded `<number>/proof-claims#proof-claim-<id>`.  A problem can
  have several.  These are a distinct object -- a claimed proof, plus whatever
  discussion it drew -- so they are counted separately, as `proof_claims` (how
  many claims) and `proof_claim_posts` (posts made in reply to them).  The
  index badges a proof claim only once it has replies, so a claim nobody has
  answered contributes to `proof_claims` and nothing to `proof_claim_posts`;
  the claim itself is never counted as a post.
* Site-wide threads that belong to no problem: the blog (`blog:N`) and the
  named topic threads (Site suggestions, Formalisation, and so on).  Both are
  skipped.

Only counts are recorded.  The index dates each thread relatively ("a month
ago"), so an exact `last_post` would mean fetching all ~900 threads
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
#: The thread's own link.  Its code says which of the three kinds it is.
_THREAD_CODE_RE = re.compile(r'<a class="thread-title" href="/forum/thread/([^"]+)"')
#: A proof claim on a problem, e.g. "411/proof-claims#proof-claim-217".
_PROOF_CLAIM_RE = re.compile(r"^(\d+)/proof-claims#proof-claim-\d+$")
#: The post-count badge, e.g. title="8 posts".  Absent when there are no posts.
_POST_COUNT_RE = re.compile(r'title="(\d+) posts?"')

#: Field order: keep `forum` next to the other derived, script-owned field.
_ANCHOR_AFTER = "formalized"
#: Order of the keys inside `forum`, and the set of keys this script owns.
_FORUM_KEYS = ("posts", "proof_claims", "proof_claim_posts")


def parse_forum_index(html):
    """Map problem number -> the `forum` entry that problem should carry.

    Threads that belong to no problem -- the site's blog threads, coded
    "blog:N", and the named topic threads -- are skipped; see the module
    docstring for how the rest are counted.
    """
    threads = {}
    for item in _THREAD_ITEM_RE.findall(html):
        code_match = _THREAD_CODE_RE.search(item)
        if code_match is None:
            continue
        code = code_match.group(1)
        claim_match = _PROOF_CLAIM_RE.match(code)
        if not code.isdigit() and claim_match is None:
            continue

        number = code if claim_match is None else claim_match.group(1)
        count_match = _POST_COUNT_RE.search(item)
        posts = int(count_match.group(1)) if count_match else 0
        entry = threads.setdefault(number, {})

        if claim_match is None:
            entry["posts"] = posts
        else:
            entry["proof_claims"] = entry.get("proof_claims", 0) + 1
            if posts:
                entry["proof_claim_posts"] = entry.get("proof_claim_posts", 0) + posts
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

    plain = sum(1 for e in threads.values() if "posts" in e)
    claims = sum(e.get("proof_claims", 0) for e in threads.values())
    posts = sum(e.get("posts", 0) + e.get("proof_claim_posts", 0) for e in threads.values())
    print(
        f"Found {plain} problem threads and {claims} proof claims across "
        f"{len(threads)} problems, carrying {posts} posts."
    )
    return threads


def _insert_after(problem, anchor, key, value):
    """Insert ``key`` into the ``CommentedMap`` just after ``anchor``."""
    keys = list(problem.keys())
    pos = keys.index(anchor) + 1 if anchor in keys else len(keys)
    problem.insert(pos, key, value)


def _forum_entry(counts):
    """Build the `forum` mapping for ``counts``, in a fixed key order."""
    entry = CommentedMap()
    for key in _FORUM_KEYS:
        if counts.get(key):
            entry[key] = counts[key]
    return entry


def apply_forum_counts(data, threads):
    """Sync every problem's `forum` field.  Returns the numbers that changed."""
    changed = []
    for problem in data:
        number = str(problem.get("number"))
        counts = threads.get(number)
        current = problem.get("forum")

        if counts is None:
            if current is not None:
                # Note that this deletes the field for any problem missing from
                # the listing, which assumes the index really does list every
                # thread on one page.  The zero-thread guard in
                # fetch_forum_index() catches a total parse failure but not a
                # partial one: if the index ever paginates, problems below the
                # fold would silently lose the field here.
                del problem["forum"]
                changed.append(number)
            continue

        wanted = _forum_entry(counts)
        if current is None:
            _insert_after(problem, _ANCHOR_AFTER, "forum", wanted)
            changed.append(number)
        elif dict(current) != dict(wanted):
            for key in _FORUM_KEYS:
                if key in wanted:
                    current[key] = wanted[key]
                elif key in current:
                    del current[key]
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

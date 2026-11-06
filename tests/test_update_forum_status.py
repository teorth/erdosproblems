#!/usr/bin/env python3
"""Parser tests for the forum index.

The index markup is the fragile part of update_forum_status.py: a class
rename on <li class="thread-item">, or a change in how proof claims are
coded, would silently drop threads. These fixtures pin both.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from update_forum_status import parse_forum_index


def _item(code, posts=None, extra=""):
    badge = f' <span title="{posts} posts">({posts} posts)</span>' if posts else ""
    return (
        f'<li class="thread-item">{extra}'
        f'<a class="thread-title" href="/forum/thread/{code}">{code}</a>'
        f"{badge}</li>"
    )


def test_problem_thread_records_post_count():
    html = _item("42", posts=8)
    assert parse_forum_index(html) == {"42": {"posts": 8}}


def test_problem_thread_with_no_badge_records_zero_posts():
    # _forum_entry then omits the key, but the parser still sees the thread.
    html = _item("7")
    assert parse_forum_index(html) == {"7": {"posts": 0}}


def test_proof_claim_without_replies_counts_the_claim_only():
    html = _item("411/proof-claims#proof-claim-217")
    assert parse_forum_index(html) == {"411": {"proof_claims": 1}}


def test_proof_claim_replies_are_separate_from_the_claim():
    html = _item("411/proof-claims#proof-claim-217", posts=3)
    assert parse_forum_index(html) == {
        "411": {"proof_claims": 1, "proof_claim_posts": 3}
    }


def test_problem_thread_and_several_claims_accumulate():
    html = (
        _item("117", posts=4)
        + _item("117/proof-claims#proof-claim-1", posts=2)
        + _item("117/proof-claims#proof-claim-2")
    )
    assert parse_forum_index(html) == {
        "117": {"posts": 4, "proof_claims": 2, "proof_claim_posts": 2}
    }


def test_blog_and_named_topic_threads_are_skipped():
    html = (
        _item("blog:12", posts=9)
        + _item("ai-contributions", posts=4)
        + _item("site-feedback", posts=1)
        + _item("88", posts=2)
    )
    assert parse_forum_index(html) == {"88": {"posts": 2}}


def test_markup_without_thread_item_class_parses_nothing():
    html = '<li class="other"><a class="thread-title" href="/forum/thread/1">1</a></li>'
    assert parse_forum_index(html) == {}


def test_singular_post_badge():
    html = (
        '<li class="thread-item">'
        '<a class="thread-title" href="/forum/thread/3">3</a>'
        '<span title="1 post">(1 post)</span></li>'
    )
    assert parse_forum_index(html) == {"3": {"posts": 1}}

#!/usr/bin/env python3
"""
Replace legacy internal .html links (Nov23 / PradhiCA / old prefixes) with current ca-* slugs.
Skips docs/URL-MIGRATION.md (historical mapping table).

Run from repo root: python3 scripts/fix_stale_internal_links.py
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = frozenset({".git", "node_modules", ".cursor"})
SKIP_FILES = frozenset({"docs/URL-MIGRATION.md"})

TEXT_EXT = frozenset(
    {".html", ".htm", ".xml", ".txt", ".md", ".js", ".css", ".json", ".php"}
)

# Longest keys first (substring safety)
REPLACEMENTS: list[tuple[str, str]] = sorted(
    [
        (
            "PradhiCA-Inter-Single-Subject-Registration-mainpage-Sep26.html",
            "ca-inter-single-subject-registration-may-2026.html",
        ),
        (
            "PradhiCA-Final-Single-Subject-Registration-mainpage-Sep26.html",
            "ca-final-single-subject-registration-may-2026.html",
        ),
        (
            "PradhiCA-Final-Single-Subject-Registration-mainpage-Jan27.html",
            "ca-final-single-subject-registration-may-2026.html",
        ),
        (
            "PradhiCA-Inter-Single-Subject-Registration-mainpage-Jan27.html",
            "ca-inter-single-subject-registration-jan-2026.html",
        ),
        (
            "PradhiCA-final-Dot-4.0-Registration-mainpage-May25.html",
            "ca-final-dot-marathon-series-may-2026.html",
        ),
        (
            "PradhiCA-final-Dot-3.0-Registration-mainpage-Jan26.html",
            "ca-final-dot-3-0-i-jan-2026.html",
        ),
        (
            "Final-new-ABC-Online-With-model-May23.html",
            "ca-final-abc-online-with-model-may-2026.html",
        ),
        (
            "Inter-Single-Subject-Homepage-Online_Nov23.html",
            "ca-inter-single-subject-registration-may-2026.html",
        ),
        (
            "Inter-Single-Subject-Homepage-Direct_Nov23.html",
            "ca-inter-single-subject-registration-may-2026.html",
        ),
        (
            "01-Inter-new-woModel-Online_Single_New-Jan26.html",
            "ca-inter-single-subject-online-without-model-jan-2027.html",
        ),
        (
            "01-Inter-new-wModel-Online_Single_New-Jan26.html",
            "ca-inter-single-subject-online-with-model-jan-2027.html",
        ),
        (
            "01-Inter-new-woModel-Direct_Single_New-Jan26.html",
            "ca-inter-single-subject-direct-without-model-jan-2027.html",
        ),
        (
            "01-Inter-new-wModel-Direct_Single_New-Jan26.html",
            "ca-inter-single-subject-direct-with-model-jan-2027.html",
        ),
        ("test-schedule-foundation-Nov23.html", "ca-foundation-test-schedule-may-2026.html"),
        ("test-schedule-Inter-Nov23.html", "ca-inter-test-schedule-may-2026.html"),
        ("test-schedule-final-Nov23.html", "ca-final-test-schedule-may-2026.html"),
        ("Inter-dot4.O-Homepage_May25.html", "ca-inter-dot-marathon-series-may-2026.html"),
        ("PradhiCA-Model_Schedule_mainpage.html", "ca-foundation-test-schedule-may-2026.html"),
    ],
    key=lambda x: len(x[0]),
    reverse=True,
)


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith(".")


def main() -> int:
    os.chdir(ROOT)
    changed = 0
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        rel_dir = os.path.normpath(dirpath).lstrip("." + os.sep)
        if rel_dir.startswith("assets" + os.sep + "vendor"):
            dirnames[:] = []
            continue
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in TEXT_EXT:
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.normpath(path).lstrip("." + os.sep)
            if rel in SKIP_FILES:
                continue
            try:
                with open(path, encoding="utf-8", errors="surrogateescape") as f:
                    text = f.read()
            except OSError:
                continue
            orig = text
            for old, new in REPLACEMENTS:
                if old in text:
                    text = text.replace(old, new)
            if text != orig:
                with open(path, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
                    f.write(text)
                print("updated:", rel)
                changed += 1
    print(f"Done. Files modified: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

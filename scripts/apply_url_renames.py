#!/usr/bin/env python3
"""
Bulk-replace old filenames with new SEO slugs across the repo.
Run from project root after git mv renames.
Skips .git and large binary paths.
"""
from __future__ import annotations

import os
import sys

# (old_fragment, new_fragment) — old must be exact filename for safe replace
REPLACEMENTS: list[tuple[str, str]] = [
    ("test-schedule-final-May26.html", "ca-final-test-schedule-may-2026.html"),
    ("test-schedule-final-Sep26.html", "ca-final-test-schedule-sep-2026.html"),
    ("test-schedule-final-Jan27.html", "ca-final-test-schedule-jan-2027.html"),
    ("test-schedule-Inter-May26.html", "ca-inter-test-schedule-may-2026.html"),
    ("test-schedule-Inter-Sep26.html", "ca-inter-test-schedule-sep-2026.html"),
    ("test-schedule-Inter-Jan27.html", "ca-inter-test-schedule-jan-2027.html"),
    ("test-schedule-foundation-May26.html", "ca-foundation-test-schedule-may-2026.html"),
    ("test-schedule-foundation-Sep26.html", "ca-foundation-test-schedule-sep-2026.html"),
]

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".cursor",
}

# Only touch text-like extensions (avoid zips, images)
TEXT_EXT = {
    ".html",
    ".htm",
    ".xml",
    ".txt",
    ".md",
    ".css",
    ".js",
    ".json",
    ".php",
    ".htaccess",
}


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith(".")


def process_file(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
            raw = f.read()
    except OSError:
        return False
    orig = raw
    for old, new in REPLACEMENTS:
        if old in raw:
            raw = raw.replace(old, new)
    if raw != orig:
        with open(path, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
            f.write(raw)
        return True
    return False


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    changed = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        # skip heavy vendor trees
        rel = os.path.relpath(dirpath, root)
        if rel.startswith("assets" + os.sep + "vendor"):
            dirnames[:] = []
            continue
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in TEXT_EXT:
                continue
            path = os.path.join(dirpath, name)
            if process_file(path):
                changed += 1
                print("updated:", os.path.relpath(path, root))
    print(f"Done. Files modified: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

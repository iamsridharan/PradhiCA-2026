#!/usr/bin/env python3
"""
After `bulk_rename_all_pages.py` wrote `rename_manifest.json`:
  - git mv each old -> new (root-level HTML only)
  - replace old filenames with new across text files
  - append 301 rules to root `.htaccess`
  - refresh `docs/URL-MIGRATION.md` Phase 2 table

Usage (from repo root):
  python3 scripts/apply_rename_from_manifest.py
  python3 scripts/apply_rename_from_manifest.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

MANIFEST = os.path.join(os.path.dirname(__file__), "rename_manifest.json")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {".git", "node_modules", ".cursor"}
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


def load_mapping() -> dict[str, str]:
    with open(os.path.join(ROOT, MANIFEST), encoding="utf-8") as f:
        return json.load(f)


def git_mv(old: str, new: str, dry_run: bool) -> None:
    op = os.path.join(ROOT, old)
    np = os.path.join(ROOT, new)
    if not os.path.isfile(op):
        print(f"SKIP mv (missing): {old}", file=sys.stderr)
        return
    # Case-only rename on case-insensitive FS: same path compares equal
    case_only = old.lower() == new.lower() and old != new
    if os.path.exists(np) and not case_only:
        print(f"SKIP mv (target exists): {new}", file=sys.stderr)
        return
    if dry_run:
        if case_only:
            print(f"would run: git mv {old} __tmp_rename__.html && git mv __tmp_rename__.html {new}")
        else:
            print("would run:", "git", "mv", op, np)
        return
    if case_only:
        tmp = os.path.join(ROOT, "__tmp_rename_case__.html")
        if os.path.exists(tmp):
            raise SystemExit(f"temp file exists: {tmp}")
        subprocess.run(["git", "mv", op, tmp], check=True)
        subprocess.run(["git", "mv", tmp, np], check=True)
    else:
        subprocess.run(["git", "mv", op, np], check=True)


def replace_across_repo(mapping: dict[str, str], dry_run: bool) -> int:
    # Longest old names first to avoid partial substring issues
    pairs = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)
    changed_files = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        rel = os.path.relpath(dirpath, ROOT)
        if rel.startswith("assets" + os.sep + "vendor"):
            dirnames[:] = []
            continue
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in TEXT_EXT:
                continue
            path = os.path.join(dirpath, name)
            if os.path.relpath(path, ROOT) == os.path.join("scripts", "rename_manifest.json"):
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
                    raw = f.read()
            except OSError:
                continue
            orig = raw
            for old, new in pairs:
                if old in raw:
                    raw = raw.replace(old, new)
            if raw != orig:
                if not dry_run:
                    with open(
                        path, "w", encoding="utf-8", errors="surrogateescape", newline=""
                    ) as f:
                        f.write(raw)
                changed_files += 1
                print("updated:", os.path.relpath(path, ROOT))
    return changed_files


def htaccess_rules(mapping: dict[str, str]) -> str:
    lines = [
        "",
        "  # Phase 2 — program / policy page renames (SEO)",
    ]
    for old, new in sorted(mapping.items(), key=lambda x: x[0].lower()):
        pat = re.escape(old)
        lines.append(f"  RewriteRule ^{pat}$ /{new} [R=301,L]")
    return "\n".join(lines) + "\n"


def patch_htaccess(mapping: dict[str, str], dry_run: bool) -> None:
    path = os.path.join(ROOT, ".htaccess")
    with open(path, encoding="utf-8") as f:
        content = f.read()
    marker = "# Phase 2 — program / policy page renames"
    if marker in content:
        print(".htaccess: Phase 2 block already present; skip append")
        return
    if "</IfModule>" not in content:
        print(".htaccess: unexpected format; skip", file=sys.stderr)
        return
    block = htaccess_rules(mapping)
    # Insert before closing IfModule
    idx = content.rindex("</IfModule>")
    new_content = content[:idx] + block + content[idx:]
    if dry_run:
        print(f"would append Phase 2 rules to .htaccess ({len(mapping)} rules)")
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    print("patched .htaccess with Phase 2 redirects")


def write_url_migration_phase2(mapping: dict[str, str], dry_run: bool) -> None:
    path = os.path.join(ROOT, "docs", "URL-MIGRATION.md")
    with open(path, encoding="utf-8") as f:
        doc = f.read()
    rows = "\n".join(
        f"| `{old}` | `{new}` |"
        for old, new in sorted(mapping.items(), key=lambda x: x[0].lower())
    )
    phase2 = f"""## Phase 2 — Program & policy pages (done)

| Old URL | New URL |
|---------|---------|
{rows}

- **Internal links** updated across HTML, sitemaps, lists, CSS/JS where referenced.
- **Apache**: root `.htaccess` includes **301** rules for the old paths above.

"""
    # Replace stub or prior Phase 2 block (rest of file)
    doc = re.sub(
        r"\n## Phase 2(\+ \(not started\)| — Program & policy pages \(done\))[\s\S]*\Z",
        "\n" + phase2.rstrip() + "\n",
        doc,
        count=1,
    )
    if dry_run:
        print("would update docs/URL-MIGRATION.md Phase 2")
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
    print("updated docs/URL-MIGRATION.md")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    os.chdir(ROOT)
    mapping = load_mapping()
    if not mapping:
        print("empty manifest", file=sys.stderr)
        return 1

    print(f"Applying {len(mapping)} renames (dry_run={args.dry_run})")
    for old, new in sorted(mapping.items()):
        git_mv(old, new, args.dry_run)

    n = replace_across_repo(mapping, args.dry_run)
    print(f"Files with content updates: {n}")

    patch_htaccess(mapping, args.dry_run)
    write_url_migration_phase2(mapping, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())

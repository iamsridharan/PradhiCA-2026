#!/usr/bin/env python3
"""
Set og:url, twitter:url, and canonical on each root ca-*.html to match that file's basename.
Run from repo root: python3 scripts/fix_ca_meta_urls.py
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    os.chdir(ROOT)
    for name in sorted(os.listdir(".")):
        if not name.startswith("ca-") or not name.endswith(".html"):
            continue
        path = name
        with open(path, encoding="utf-8", errors="surrogateescape") as f:
            text = f.read()
        orig = text

        def fix_line(line: str) -> str:
            if (
                'property="og:url"' not in line
                and 'name="twitter:url"' not in line
                and 'rel="canonical"' not in line
            ):
                return line
            return re.sub(
                r"https://pradhica\.com/[^\"'>\s]+\.html",
                f"https://pradhica.com/{name}",
                line,
            )

        text = "".join(fix_line(l) for l in text.splitlines(True))
        if text != orig:
            with open(path, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
                f.write(text)
            print("updated:", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

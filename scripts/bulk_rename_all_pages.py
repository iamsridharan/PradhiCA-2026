#!/usr/bin/env python3
"""
Compute old → new root HTML filenames (SEO slugs), detect collisions, write renames manifest.
Run from repo root: python3 scripts/bulk_rename_all_pages.py

After Phase 2 is applied, most files are already `ca-*.html`; the manifest will only list any
remaining renames (e.g. case-only policy pages). Full old→new mapping lives in docs/URL-MIGRATION.md.
"""
from __future__ import annotations

import json
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP = frozenset(
    {
        "index.html",
        "course-overview.html",
        "contact-us.html",
        "registration.html",
        "sitemap.html",
        "404.html",
        "ca-final-test-schedule-jan-2027.html",
        "ca-final-test-schedule-may-2026.html",
        "ca-final-test-schedule-sep-2026.html",
        "ca-foundation-test-schedule-may-2026.html",
        "ca-foundation-test-schedule-sep-2026.html",
        "ca-inter-test-schedule-jan-2027.html",
        "ca-inter-test-schedule-may-2026.html",
        "ca-inter-test-schedule-sep-2026.html",
        "ca-foundation-test-series.html",
    }
)

BATCH = {
    "May26": "may-2026",
    "Sep26": "sep-2026",
    "Jan27": "jan-2027",
    "Jan26": "jan-2026",
    "may26": "may-2026",
}


def batch_token(s: str) -> str | None:
    for k, v in BATCH.items():
        if s.endswith(k + ".html"):
            return v
    return None


def strip_batch_from_stem(stem: str) -> tuple[str, str | None]:
    """Return (stem_without_batch, batch_slug)"""
    for k, v in sorted(BATCH.items(), key=lambda x: -len(x[0])):
        if stem.endswith(k):
            return stem[: -len(k)].rstrip("-_"), v
    return stem, None


def level_prefix(level: str) -> str:
    x = level.lower()
    if x == "final":
        return "ca-final"
    if x == "inter":
        return "ca-inter"
    if x == "foundation":
        return "ca-foundation"
    return f"ca-{x}"


def slug(s: str) -> str:
    s = s.lower().replace("_", "-")
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def compute_new_name(old: str) -> str | None:
    if old in SKIP:
        return None

    # Legal / utility (lowercase hyphen)
    fixed = {
        "Terms-and-Conditions.html": "terms-and-conditions.html",
        "Privacy-Policy.html": "privacy-policy.html",
        "Refund-Policy.html": "refund-policy.html",
        "Scheduled-download.html": "scheduled-download.html",
        "switch-from-institute.html": "switch-from-institute.html",
        "testingg.html": "testing-page.html",
        "update-page.html": "update-page.html",
        "vs-institute-tests.html": "vs-institute-tests.html",
        "why-institute-tests-fail-ca-students.html": "why-institute-tests-fail-ca-students.html",
        "ca-foundation-test-series.html": "ca-foundation-test-series.html",  # already canonical
    }
    if old in fixed:
        return fixed[old] if fixed[old] != old else None

    stem = old[:-5] if old.endswith(".html") else old

    # 01-Final-new-wModel-Online_Single_New-May26
    m = re.match(
        r"^01-(Final|Inter)-new-(wModel|woModel)-(Online|Direct)_Single_New-(May26|Sep26|Jan27)$",
        stem,
    )
    if m:
        lv, wm, mode, b = m.groups()
        model = "with-model" if wm == "wModel" else "without-model"
        batch = BATCH[b]
        return f"{level_prefix(lv)}-single-subject-{mode.lower()}-{model}-{batch}.html"

    # 03-foundation-new-wModel-Direct_Single_New-May26
    m = re.match(
        r"^03-foundation-new-(wModel|woModel)-(Direct|Online)_Single_New-(May26)$",
        stem,
    )
    if m:
        wm, mode, b = m.groups()
        model = "with-model" if wm == "wModel" else "without-model"
        return f"ca-foundation-single-subject-{mode.lower()}-{model}-{BATCH[b]}.html"

    # 02-Final-Rapid-Revison-Online--Sep26  OR 02-Final-Rapid-Revison-Direct-May26
    m = re.match(
        r"^02-(Final|Inter)-Rapid-Revison-(Online|Direct)-*-*(May26|Sep26|Jan27)$",
        stem,
    )
    if m:
        lv, mode, b = m.groups()
        return f"{level_prefix(lv)}-rapid-revision-{mode.lower()}-{BATCH[b]}.html"

    # 03-foundation-Rapid-Revison-Direct-May26
    m = re.match(r"^03-foundation-Rapid-Revison-(Online|Direct)-(May26)$", stem)
    if m:
        mode, b = m.groups()
        return f"ca-foundation-rapid-revision-{mode.lower()}-{BATCH[b]}.html"

    # Final-ABC-*  Inter-ABC-*  Foundation-ABC-*
    m = re.match(r"^(Final|Inter|Foundation)-ABC-(.+)$", stem)
    if m:
        lv, rest = m.groups()
        bpart = None
        for k, v in sorted(BATCH.items(), key=lambda x: -len(x[0])):
            if rest.endswith(k):
                bpart = v
                rest = rest[: -len(k)].strip("-_")
                break
        if not bpart:
            return None
        rest = rest.replace("_", "-")
        # normalize segments
        if rest == "Direct":
            mid = "direct"
        elif rest == "Online":
            mid = "online"
        elif rest == "Direct-With-model":
            mid = "direct-with-model"
        elif rest == "Online-With-model":
            mid = "online-with-model"
        elif rest == "Homepage":
            mid = "series"
        else:
            mid = slug(rest.replace("With-model", "with-model"))
        return f"{level_prefix(lv)}-abc-{mid}-{bpart}.html"

    # Final-Dot-2-May26-Homepage, Final-Dot-3-May26-Homepage
    m = re.match(r"^Final-Dot-([23])-May26-Homepage$", stem)
    if m:
        n = m.group(1)
        return f"ca-final-dot-{n}-series-may-2026.html"

    # Final-Dot-Marathon-*-May26 / Sep26
    m = re.match(
        r"^Final-Dot-Marathon-(May26|Sep26)-(Direct|Online|Homepage)$", stem
    )
    if m:
        b, kind = m.groups()
        k = "series" if kind == "Homepage" else kind.lower()
        return f"ca-final-dot-marathon-{k}-{BATCH[b]}.html"

    # Inter-Dot-Marathon-May26-*
    m = re.match(r"^Inter-Dot-Marathon-May26-(Direct|Online|Homepage)$", stem)
    if m:
        kind = m.group(1)
        k = "series" if kind == "Homepage" else kind.lower()
        return f"ca-inter-dot-marathon-{k}-may-2026.html"

    # Inter-Dot3.O-may26-Direct → ca-inter-dot-3-may-2026-direct (batch last for consistency)
    m = re.match(r"^Inter-Dot3\.O-(may26|jan26)-(Direct|Online)$", stem, re.I)
    if m:
        bb, mode = m.groups()
        bb_l = bb.lower()
        batch = "may-2026" if bb_l == "may26" else "jan-2026"
        return f"ca-inter-dot-3-{mode.lower()}-{batch}.html"

    m = re.match(r"^Inter-Dot3\.O-jan26-(Direct|Online)$", stem)
    if m:
        mode = m.group(1)
        return f"ca-inter-dot-3-{mode.lower()}-jan-2026.html"

    # Inter-dot2-may26-Direct
    m = re.match(r"^Inter-dot2-may26-(Direct|Online)$", stem, re.I)
    if m:
        mode = m.group(1)
        return f"ca-inter-dot-2-{mode.lower()}-may-2026.html"

    # Inter-dot2.O-Homepage_May26
    if stem == "Inter-dot2.O-Homepage_May26":
        return "ca-inter-dot-2-series-may-2026.html"

    if stem == "Inter-dot3.O-Homepage_may26":
        return "ca-inter-dot-3-series-may-2026.html"
    if stem == "Inter-dot3.O-Homepage_jan26":
        return "ca-inter-dot-3-series-jan-2026.html"

    # Final-dot-2.0-i-may26
    m = re.match(r"^Final-dot-2\.0-(i|ii)-may26$", stem, re.I)
    if m:
        part = m.group(1).lower()
        return f"ca-final-dot-2-0-{part}-may-2026.html"

    # Final-new-dot-3.0-i-jan26 / may26
    m = re.match(r"^Final-new-dot-3\.0-(i|ii)-(jan26|may26)$", stem, re.I)
    if m:
        part, b = m.groups()
        batch = "jan-2026" if b.lower() == "jan26" else "may-2026"
        return f"ca-final-dot-3-0-{part.lower()}-{batch}.html"

    # Final-Model-* 
    m = re.match(
        r"^Final-Model-(\d)set_(Direct|Online)_(May26)$", stem
    )
    if m:
        nset, mode, b = m.groups()
        return f"ca-final-model-{nset}-set-{mode.lower()}-{BATCH[b]}.html"

    m = re.match(r"^Inter-Model-(\d)set_(Direct|Online)_(May26)$", stem)
    if m:
        nset, mode, b = m.groups()
        return f"ca-inter-model-{nset}-set-{mode.lower()}-{BATCH[b]}.html"

    # foundation-Dot2-May26-direct
    m = re.match(r"^foundation-Dot([23])-May26-(direct|online)$", stem, re.I)
    if m:
        n, mode = m.groups()
        return f"ca-foundation-dot-{n}-{mode.lower()}-may-2026.html"

    # foundation-DotM-Jan26
    m = re.match(r"^foundation-DotM-Jan26-(direct|online)$", stem, re.I)
    if m:
        mode = m.group(1)
        return f"ca-foundation-dot-marathon-{mode.lower()}-jan-2026.html"

    # foundation-dot2-Homepage-may26
    if re.match(r"^foundation-dot2-Homepage-may26$", stem, re.I):
        return "ca-foundation-dot-2-series-may-2026.html"
    if stem == "foundation-dot3-Homepage-May26":
        return "ca-foundation-dot-3-series-may-2026.html"
    if stem == "foundation-dotM-Homepage-Jan26":
        return "ca-foundation-dot-marathon-series-jan-2026.html"

    # PradhiCA-* registration mainpages
    if old == "PradhiCA-Inter-Model-Registration-mainpage--May26.html":
        return "ca-inter-model-registration-may-2026.html"
    if old == "PradhiCA-Final-Model-Registration-mainpage-May26.html":
        return "ca-final-model-registration-may-2026.html"
    if old.startswith("PradhiCA-Final-Rapid-Revision-Registration-mainpage-"):
        b = old.replace("PradhiCA-Final-Rapid-Revision-Registration-mainpage-", "").replace(".html", "")
        bb = {"May26": "may-2026", "Sep26": "sep-2026", "Jan27": "jan-2027"}[b]
        return f"ca-final-rapid-revision-registration-{bb}.html"
    if old.startswith("PradhiCA-Inter-Rapid-Revision-Registration-mainpage-"):
        b = old.replace("PradhiCA-Inter-Rapid-Revision-Registration-mainpage-", "").replace(".html", "")
        bb = {"May26": "may-2026", "Sep26": "sep-2026", "Jan27": "jan-2027"}[b]
        return f"ca-inter-rapid-revision-registration-{bb}.html"
    if old == "PradhiCA-Final-Single-Subject-Registration-mainpage-May26.html":
        return "ca-final-single-subject-registration-may-2026.html"
    if old == "PradhiCA-Inter-Single-Subject-Registration-mainpage-May26.html":
        return "ca-inter-single-subject-registration-may-2026.html"
    if old == "PradhiCA-Inter-Single-Subject-Registration-mainpage-Jan26.html":
        return "ca-inter-single-subject-registration-jan-2026.html"

    if old == "foundation-Rapid-Revision-Registration-mainpage-May26.html":
        return "ca-foundation-rapid-revision-registration-may-2026.html"

    return None


def main() -> None:
    os.chdir(ROOT)
    all_html = sorted(
        f for f in os.listdir(".") if f.endswith(".html") and os.path.isfile(f)
    )
    mapping: dict[str, str] = {}
    failed: list[str] = []

    for old in all_html:
        new = compute_new_name(old)
        if new is None:
            continue
        if new == old:
            continue
        mapping[old] = new

    # collision detection
    inv: dict[str, list[str]] = defaultdict(list)
    for o, n in mapping.items():
        inv[n].append(o)
    collisions = {n: os for n, os in inv.items() if len(os) > 1}
    if collisions:
        print("COLLISIONS:", json.dumps(collisions, indent=2))
        raise SystemExit(1)

    out_path = os.path.join(ROOT, "scripts", "rename_manifest.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, sort_keys=True)
    print(f"Wrote {len(mapping)} renames to {out_path}")
    for o, n in sorted(mapping.items()):
        print(f"  {o} -> {n}")

    # After Phase 2, root files are either SKIP hubs, ca-*.html SEO pages, or
    # small utility pages — not legacy PradhiCA / Final-* names.
    utility_ok = frozenset(
        {
            "switch-from-institute.html",
            "update-page.html",
            "vs-institute-tests.html",
            "why-institute-tests-fail-ca-students.html",
            "privacy-policy.html",
            "refund-policy.html",
            "terms-and-conditions.html",
            "scheduled-download.html",
            "testing-page.html",
        }
    )
    still: list[str] = []
    for f in all_html:
        if f in SKIP:
            continue
        if f in mapping:
            continue
        if f.startswith("ca-") and f.endswith(".html"):
            continue
        if f in utility_ok:
            continue
        still.append(f)
    if still:
        print("UNCOVERED (need rules):", still)
        raise SystemExit(2)


if __name__ == "__main__":
    main()

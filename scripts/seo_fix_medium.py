#!/usr/bin/env python3
"""Medium SEO follow-ups: multi-H1, schema coverage, dead PDFs, empty alts."""
from __future__ import annotations

from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parents[1]
JUNK = {
    "testing-page.html",
    "update-page.html",
    "ca-final-test-schedule-nov-2026-scrap.html",
    "404.html",
    "scheduled-download.html",
}

title_re = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
desc_re = re.compile(
    r'name=["\']description["\'][^>]*content=["\']([^"\']*)["\']',
    re.I,
)


def demote_extra_h1s(html: str, keep_first: bool = True) -> tuple[str, int]:
    """Keep the first <h1>, demote subsequent ones to <h2>."""
    count = 0
    seen = False

    def repl(m: re.Match) -> str:
        nonlocal count, seen
        if not seen and keep_first:
            seen = True
            return m.group(0)
        count += 1
        return f"<h2{m.group(1)}>{m.group(2)}</h2>"

    new = re.sub(r"<h1([^>]*)>(.*?)</h1>", repl, html, flags=re.I | re.S)
    return new, count


def org_schema_block(page_url: str, page_name: str, description: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "EducationalOrganization",
                "@id": "https://pradhica.com/#organization",
                "name": "PradhiCA",
                "alternateName": "PradhiCA Test Series",
                "url": "https://pradhica.com",
                "logo": "https://pradhica.com/assets/img/logo-black.png",
                "email": "pradhica4u@gmail.com",
                "telephone": "+91-80726-53948",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": (
                        "No: 20, 1st floor, Chakrapani St Ext, "
                        "Rangarajapuram, West Mambalam"
                    ),
                    "addressLocality": "Chennai",
                    "addressRegion": "Tamil Nadu",
                    "postalCode": "600033",
                    "addressCountry": "IN",
                },
                "sameAs": [
                    "http://bit.ly/fbpradhica",
                    "http://bit.ly/inspradhica",
                    "https://t.me/PradhiCA",
                    "https://www.youtube.com/channel/UCf1poDZ0HqWowl5AbwH3UMQ",
                ],
            },
            {
                "@type": "WebPage",
                "@id": f"{page_url}#webpage",
                "url": page_url,
                "name": page_name,
                "description": description,
                "isPartOf": {"@id": "https://pradhica.com/#website"},
                "about": {"@id": "https://pradhica.com/#organization"},
            },
            {
                "@type": "WebSite",
                "@id": "https://pradhica.com/#website",
                "url": "https://pradhica.com",
                "name": "PradhiCA",
                "publisher": {"@id": "https://pradhica.com/#organization"},
            },
        ],
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'\n    <script type="application/ld+json">\n{payload}\n    </script>\n'


def fix_multi_h1() -> None:
    targets = [
        "index.html",
        "privacy-policy.html",
        "terms-and-conditions.html",
        "refund-policy.html",
    ]
    for name in targets:
        path = ROOT / name
        text = path.read_text(errors="replace")
        new, n = demote_extra_h1s(text)
        if n:
            path.write_text(new)
            print(f"multi-H1: {name} demoted {n} extras to h2")
        else:
            print(f"multi-H1: {name} already single")


def fix_dead_pdfs() -> None:
    # Page-aware remaps where the same dead path should go to different live PDFs
    page_maps = {
        "ca-final-test-schedule-may-2027.html": {
            "Schedules_2025/PradhiCA Final May 25 dot4 Schedule.pdf": (
                "Schedules_2026/PradhiCA-CA Final-DOT-3.O-Nov26-Schedule.pdf"
            ),
            "dot 3.0/PradhiCA-DOT-3.O-Dec2021-CAFINAL-New1.pdf": (
                "Schedules_2026/PradhiCA-CA Final-DOT-3.O-Nov26-Schedule.pdf"
            ),
            "dot 3.0/PradhiCA-DOT-3.O-Dec2021-CAFINAL-Old1.pdf": (
                "Schedules_2026/PradhiCA-CA Final-3.O-DOT-May26-Schedule.pdf"
            ),
        },
        "ca-inter-test-schedule-may-2026.html": {
            "Schedules_2025/PradhiCA CA Inter May 25 Schedule40.pdf": (
                "Schedules_2026/PradhiCA-CA Inter-3.O-DOT-May26-Schedule.pdf"
            ),
            "dot 3.0/PradhiCA-DOT-3.O-Dec2021-CAFINAL-New1.pdf": (
                "Schedules_2026/PradhiCA-CA Inter-3.O-DOT-May26-Schedule.pdf"
            ),
            "dot 3.0/PradhiCA-DOT-3.O-Dec2021-CAFINAL-Old1.pdf": (
                "Schedules_2026/PradhiCA-CA Inter-DOT2.O-May26-Schedule.pdf"
            ),
        },
        "ca-inter-test-schedule-jan-2027.html": {
            "Schedules_2025/PradhiCA CA Inter May 25 Schedule40.pdf": (
                "Schedules_2026/PradhiCA-CA Inter-DOT-Marathon-May26-Schedule.pdf"
            ),
            "dot 3.0/PradhiCA-DOT-3.O-Dec2021-CAFINAL-New1.pdf": (
                "Schedules_2026/PradhiCA-CA Inter-DOT-3.O-Sep26-Schedule.pdf"
            ),
            "dot 3.0/PradhiCA-DOT-3.O-Dec2021-CAFINAL-Old1.pdf": (
                "Schedules_2026/PradhiCA-CA Inter-DOT-Marathon-Sep26-Schedule.pdf"
            ),
        },
    }

    for name, mapping in page_maps.items():
        path = ROOT / name
        if not path.exists():
            print(f"pdf skip missing page: {name}")
            continue
        text = path.read_text(errors="replace")
        new = text
        n = 0
        for old, repl in mapping.items():
            if old in new:
                if not (ROOT / repl).exists():
                    print(f"WARN missing PDF target: {repl}")
                    continue
                new = new.replace(old, repl)
                n += 1
        if new != text:
            path.write_text(new)
            print(f"pdf: {name} remapped {n} hrefs")
        else:
            print(f"pdf: {name} no changes")


def fix_empty_alts() -> None:
    img_re = re.compile(r"<img([^>]+)>", re.I)
    fixed = 0
    files = 0
    for path in ROOT.glob("*.html"):
        if path.name in JUNK:
            continue
        text = path.read_text(errors="replace")

        def repl_img(m: re.Match) -> str:
            nonlocal fixed
            attrs = m.group(1)
            alt_m = re.search(r'alt=(["\'])(.*?)\1', attrs, re.I)
            if not alt_m or alt_m.group(2).strip():
                return m.group(0)
            src_m = re.search(r'src=(["\'])(.*?)\1', attrs, re.I)
            src = (src_m.group(2) if src_m else "").strip()
            if "logo" in src.lower():
                alt = "PradhiCA"
            elif "avatar" in src.lower() or "user.png" in src.lower():
                alt = "Student testimonial"
            elif not src:
                alt = "PradhiCA"
            else:
                # derive from filename
                stem = Path(src).stem.replace("-", " ").replace("_", " ").strip()
                alt = stem.title() if stem else "PradhiCA"
            attrs2 = (
                attrs[: alt_m.start()]
                + f'alt="{alt}"'
                + attrs[alt_m.end() :]
            )
            fixed += 1
            return f"<img{attrs2}>"

        new = img_re.sub(repl_img, text)
        if new != text:
            path.write_text(new)
            files += 1
    print(f"alts: filled {fixed} empty alts across {files} files")


def fix_schema_coverage() -> None:
    added = 0
    for path in sorted(ROOT.glob("*.html")):
        if path.name in JUNK:
            continue
        text = path.read_text(errors="replace")
        if "application/ld+json" in text:
            continue
        tm = title_re.search(text)
        title = re.sub(r"\s+", " ", tm.group(1)).strip() if tm else path.name
        dm = desc_re.search(text)
        desc = (
            dm.group(1).strip()
            if dm
            else "PradhiCA CA test series — ICAI-aligned mocks across India."
        )
        url = (
            "https://pradhica.com/"
            if path.name == "index.html"
            else f"https://pradhica.com/{path.name}"
        )
        block = org_schema_block(url, title, desc)
        if not re.search(r"</head>", text, re.I):
            print(f"schema no </head>: {path.name}")
            continue
        text2 = re.sub(r"</head>", block + "</head>", text, count=1, flags=re.I)
        path.write_text(text2)
        added += 1
    print(f"schema: added JSON-LD to {added} pages")


def verify() -> None:
    print("\n=== VERIFY ===")
    for name in [
        "index.html",
        "privacy-policy.html",
        "terms-and-conditions.html",
        "refund-policy.html",
    ]:
        n = len(re.findall(r"<h1[\s>]", (ROOT / name).read_text(errors="replace"), re.I))
        print(f"  {name} h1 count: {n}")

    href_re = re.compile(r'href=["\']([^"\'#]+)["\']', re.I)
    dead_pdf = 0
    for path in ROOT.glob("*.html"):
        if path.name in JUNK:
            continue
        for href in href_re.findall(path.read_text(errors="replace")):
            if ".pdf" not in href.lower() and "dot 3.0/" not in href:
                continue
            p = (
                href.split("pradhica.com/")[-1].split("?")[0]
                if "pradhica.com" in href
                else href.lstrip("/")
            )
            if p.endswith(".pdf") and not (ROOT / p).exists():
                dead_pdf += 1
                print(f"  dead pdf: {path.name} -> {p}")
    print(f"  dead PDF instances: {dead_pdf}")

    empty_alt = 0
    img_re = re.compile(r"<img([^>]+)>", re.I)
    no_schema = 0
    total = 0
    for path in ROOT.glob("*.html"):
        if path.name in JUNK:
            continue
        total += 1
        text = path.read_text(errors="replace")
        if "ld+json" not in text:
            no_schema += 1
        for attrs in img_re.findall(text):
            m = re.search(r'alt=["\']([^"\']*)["\']', attrs, re.I)
            if m and not m.group(1).strip():
                empty_alt += 1
    print(f"  empty alts: {empty_alt}")
    print(f"  pages without schema: {no_schema}/{total}")


def main() -> None:
    fix_multi_h1()
    fix_dead_pdfs()
    fix_empty_alts()
    fix_schema_coverage()
    verify()
    print("MEDIUM_FIX_DONE")


if __name__ == "__main__":
    main()

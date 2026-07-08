#!/usr/bin/env python3
"""Fix 5: unique titles + meta descriptions. Fix 6: H1 upgrade + JSON-LD on key pages."""
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

LEVEL = {
    "foundation": "CA Foundation",
    "inter": "CA Intermediate",
    "final": "CA Final",
}
BATCH = {
    "jan-2026": ("Jan 2026", "2026"),
    "may-2026": ("May 2026", "2026"),
    "sep-2026": ("Sep 2026", "2026"),
    "nov-2026": ("Nov 2026", "2026"),
    "jan-2027": ("Jan 2027", "2027"),
    "may-2027": ("May 2027", "2027"),
}
SERIES = [
    ("dot-marathon", "DOT Marathon"),
    ("dot-3-0-ii", "DOT 3.0 Group II"),
    ("dot-3-0-i", "DOT 3.0 Group I"),
    ("dot-3", "DOT 3.0"),
    ("dot-2-0-ii", "DOT 2.0 Group II"),
    ("dot-2-0-i", "DOT 2.0 Group I"),
    ("dot-2", "DOT 2.0"),
    ("rapid-revision", "Rapid Revision"),
    ("single-subject", "Single Subject"),
    ("model-1-set", "Model Exam Set 1"),
    ("model-2-set", "Model Exam Set 2"),
    ("model-3-set", "Model Exam Set 3"),
    ("model-registration", "Model Exam"),
    ("abc", "ABC Test Series"),
    ("model", "Model Exam"),
    ("test-schedule", "Test Schedule"),
    ("test-series", "Test Series"),
]
MODE = [
    ("direct-with-model", "Direct with Model"),
    ("online-with-model", "Online with Model"),
    ("direct-without-model", "Direct without Model"),
    ("online-without-model", "Online without Model"),
    ("with-model", "with Model"),
    ("without-model", "without Model"),
    ("direct", "Direct"),
    ("online", "Online"),
    ("series", "Series Hub"),
    ("registration", "Registration"),
]

SPECIAL_TITLE = {
    "index.html": "PradhiCA | Best CA Test Series India 2026 — Foundation, Inter & Final",
    "contact-us.html": "Contact PradhiCA | CA Test Series Support — Chennai Centre",
    "course-overview.html": "CA Course Overview | Foundation, Intermediate & Final Paths — PradhiCA",
    "registration.html": "Register for PradhiCA CA Test Series | Enquiry Form",
    "terms-and-conditions.html": "Terms & Conditions | PradhiCA CA Test Series",
    "privacy-policy.html": "Privacy Policy | PradhiCA CA Test Series",
    "refund-policy.html": "Refund Policy | PradhiCA CA Test Series",
    "sitemap.html": "HTML Sitemap | PradhiCA CA Test Series Pages",
    "ca-foundation-test-series.html": "CA Foundation Test Series India 2026 | PradhiCA Chennai & Online",
}
SPECIAL_DESC = {
    "index.html": (
        "PradhiCA offers ICAI-aligned CA Foundation, Intermediate and Final test series. "
        "7500+ students. Direct mode in Chennai, Online across India."
    ),
    "contact-us.html": (
        "Contact PradhiCA for CA test series support. Call +91 80726 53948 or email "
        "pradhica4u@gmail.com. Centre in West Mambalam, Chennai."
    ),
    "course-overview.html": (
        "Explore PradhiCA CA Foundation, Intermediate and Final test series paths — "
        "ABC, DOT Marathon, DOT 2.0, DOT 3.0, Model Exams and more."
    ),
    "registration.html": (
        "Register or enquire for PradhiCA CA Foundation, Intermediate or Final test series. "
        "Direct Chennai and Online modes available."
    ),
    "terms-and-conditions.html": (
        "Read PradhiCA terms and conditions for CA test series enrolment, payments, "
        "schedules and student responsibilities."
    ),
    "privacy-policy.html": (
        "How PradhiCA collects, uses and protects your personal data when you register "
        "for CA test series or contact us."
    ),
    "refund-policy.html": (
        "PradhiCA refund and cancellation policy for CA Foundation, Intermediate and "
        "Final test series enrolments."
    ),
    "sitemap.html": (
        "Browse all PradhiCA CA Foundation, Intermediate and Final test series, "
        "schedule and payment pages."
    ),
    "ca-foundation-test-series.html": (
        "CA Foundation test series by PradhiCA — ABC, DOT Marathon, DOT 2.0, DOT 3.0 "
        "and more for May and Sep 2026 batches."
    ),
}

title_re = re.compile(r"(<title[^>]*>)(.*?)(</title>)", re.I | re.S)
desc_re = re.compile(
    r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']*)(["\'])',
    re.I,
)
desc_re2 = re.compile(
    r'(<meta\s+content=["\'])([^"\']*)(["\']\s+name=["\']description["\'])',
    re.I,
)
og_title_re = re.compile(
    r'(<meta\s+property=["\']og:title["\']\s+content=["\'])([^"\']*)(["\'])',
    re.I,
)
og_desc_re = re.compile(
    r'(<meta\s+property=["\']og:description["\']\s+content=["\'])([^"\']*)(["\'])',
    re.I,
)
tw_title_re = re.compile(
    r'(<meta\s+name=["\']twitter:title["\']\s+content=["\'])([^"\']*)(["\'])',
    re.I,
)
tw_desc_re = re.compile(
    r'(<meta\s+name=["\']twitter:description["\']\s+content=["\'])([^"\']*)(["\'])',
    re.I,
)


def parse_slug(name: str):
    if not name.startswith("ca-") or not name.endswith(".html"):
        return None
    stem = name[:-5]
    parts = stem.split("-")
    level_key = parts[1] if len(parts) > 1 else None
    if level_key not in LEVEL:
        return None
    batch_key = None
    batch_label = None
    year = "2026"
    for bk, (bl, yr) in BATCH.items():
        if stem.endswith(bk):
            batch_key = bk
            batch_label = bl
            year = yr
            break
    if not batch_key:
        for bk, (bl, yr) in BATCH.items():
            if bk in stem:
                batch_key = bk
                batch_label = bl
                year = yr
                break
    series_label = None
    padded = f"-{stem}-"
    for sk, sl in SERIES:
        # Match as path segments so "model" does not hit inside "with-model"
        if f"-{sk}-" in padded:
            if sk == "model":
                # Bare "model" only for model-registration / model exam hubs,
                # not ABC/single-subject "...-with-model" payment pages.
                if any(
                    x in stem
                    for x in (
                        "model-1-set",
                        "model-2-set",
                        "model-3-set",
                        "model-registration",
                    )
                ):
                    series_label = sl
                    break
                if "with-model" in stem or "without-model" in stem:
                    continue
            series_label = sl
            break
    mode_label = None
    for mk, ml in MODE:
        if f"-{mk}-" in padded or stem.endswith(f"-{mk}"):
            mode_label = ml
            break
    return {
        "level": LEVEL[level_key],
        "series": series_label or "Test Series",
        "mode": mode_label,
        "batch": batch_label,
        "year": year,
        "name": name,
    }


def build_title(info):
    short_level = {
        "CA Foundation": "CA Foundation",
        "CA Intermediate": "CA Inter",
        "CA Final": "CA Final",
    }[info["level"]]
    series = info["series"]
    mode = info["mode"]
    batch = info["batch"] or ""
    mode_bit = ""
    if mode:
        m = (
            mode.replace("Direct with Model", "Direct+Model")
            .replace("Online with Model", "Online+Model")
            .replace("Direct without Model", "Direct")
            .replace("Online without Model", "Online")
            .replace("Series Hub", "Hub")
            .replace("Registration", "Register")
        )
        mode_bit = f" · {m}"
    batch_bit = f" | {batch}" if batch else ""
    title = f"{short_level} {series}{mode_bit}{batch_bit} | PradhiCA"
    if len(title) > 70:
        title = f"{short_level} {series}{batch_bit} | PradhiCA"
    return title


def build_desc(info):
    level = info["level"]
    series = info["series"]
    mode = info["mode"]
    batch = info["batch"] or "upcoming"
    mode_phrase = ""
    if mode == "Series Hub":
        mode_phrase = " — choose Direct or Online"
    elif mode == "Registration":
        mode_phrase = " registration"
    elif mode:
        mode_phrase = f" in {mode} mode"
    return (
        f"Join PradhiCA {level} {series} for {batch}{mode_phrase}. "
        f"ICAI-aligned mocks, evaluated by CAs. Direct in Chennai & Online across India."
    )[:155]


def unique_title(base: str, name: str, used: dict) -> str:
    if base not in used:
        used[base] = name
        return base
    stem = name.replace(".html", "").replace("ca-", "")
    tokens = stem.split("-")
    extra = "-".join(tokens[-3:])
    alt = f"{base} · {extra}"
    if len(alt) > 72:
        alt = f"{base[:48]} · {extra[:20]}"
    n = 2
    cand = alt
    while cand in used:
        cand = f"{base} ({n})"
        n += 1
    used[cand] = name
    return cand


def replace_attr_content(pattern: re.Pattern, text: str, value: str) -> str:
    if not pattern.search(text):
        return text
    return pattern.sub(lambda m: m.group(1) + value + m.group(3), text, count=1)


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
                    "streetAddress": "No: 20, 1st floor, Chakrapani St Ext, Rangarajapuram, West Mambalam",
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


def main():
    stats = {"title": 0, "desc": 0, "files": 0, "h1": 0, "schema": 0}
    used_titles: dict[str, str] = {}
    planned: dict[str, tuple[str, str]] = {}

    for f in sorted(ROOT.glob("*.html")):
        name = f.name
        if name in JUNK:
            continue
        info = parse_slug(name)
        if name in SPECIAL_TITLE:
            title = SPECIAL_TITLE[name]
            desc = SPECIAL_DESC[name]
        elif info:
            title = build_title(info)
            desc = build_desc(info)
        else:
            text = f.read_text(errors="replace")
            tm = title_re.search(text)
            title = re.sub(r"\s+", " ", tm.group(2)).strip() if tm else name
            title = (
                title.replace("2025", "2026")
                .replace("Sep25", "Sep 2026")
                .replace("Jan26 Batch", "Batch")
            )
            dm = desc_re.search(text) or desc_re2.search(text)
            d = (dm.group(2) if dm else "").strip()
            if d in ("India", "India.", "Register for India", "Contact India") or len(d) < 50:
                desc = (
                    "PradhiCA CA test series — ICAI-aligned mocks for Foundation, "
                    "Intermediate and Final. Direct Chennai & Online across India."
                )
            else:
                desc = d
        title = unique_title(title, name, used_titles)
        if len(title) > 72:
            title = title[:69].rstrip(" ·|-") + "…"
        planned[name] = (title, desc[:155])

    for f in ROOT.glob("*.html"):
        name = f.name
        if name in JUNK or name not in planned:
            continue
        title, desc = planned[name]
        text = f.read_text(errors="replace")
        new = text

        tm = title_re.search(new)
        if tm and re.sub(r"\s+", " ", tm.group(2)).strip() != title:
            new = title_re.sub(lambda m: m.group(1) + title + m.group(3), new, count=1)
            stats["title"] += 1

        dm = desc_re.search(new) or desc_re2.search(new)
        if dm:
            if dm.group(2).strip() != desc:
                if desc_re.search(new):
                    new = desc_re.sub(lambda m: m.group(1) + desc + m.group(3), new, count=1)
                else:
                    new = desc_re2.sub(lambda m: m.group(1) + desc + m.group(3), new, count=1)
                stats["desc"] += 1
        else:
            new = title_re.sub(
                lambda m: m.group(0) + f'\n    <meta name="description" content="{desc}">',
                new,
                count=1,
            )
            stats["desc"] += 1

        new = replace_attr_content(og_title_re, new, title)
        new = replace_attr_content(tw_title_re, new, title)
        new = replace_attr_content(og_desc_re, new, desc)
        new = replace_attr_content(tw_desc_re, new, desc)

        # Fix 6a: upgrade first <h2 class="h1"> to <h1>
        if not re.search(r"<h1[\s>]", new, re.I):
            m = re.search(
                r'<h2(\s+[^>]*class="[^"]*\bh1\b[^"]*"[^>]*)>(.*?)</h2>',
                new,
                re.I | re.S,
            )
            if m:
                new = new[: m.start()] + f"<h1{m.group(1)}>{m.group(2)}</h1>" + new[m.end() :]
                stats["h1"] += 1

        if new != text:
            f.write_text(new)
            stats["files"] += 1

    print("Fix5/6a stats:", stats)

    # Uniqueness / India / H1 checks
    titles: dict[str, list[str]] = {}
    india = 0
    no_h1 = 0
    for f in ROOT.glob("*.html"):
        if f.name in JUNK:
            continue
        t = f.read_text(errors="replace")
        tm = title_re.search(t)
        title = re.sub(r"\s+", " ", tm.group(2)).strip() if tm else ""
        titles.setdefault(title, []).append(f.name)
        dm = desc_re.search(t) or desc_re2.search(t)
        d = (dm.group(2) if dm else "").strip()
        if d == "India":
            india += 1
        if not re.search(r"<h1[\s>]", t, re.I):
            no_h1 += 1
    dupes = {k: v for k, v in titles.items() if len(v) > 1}
    print(f"Duplicate title groups: {len(dupes)}")
    for k, v in list(dupes.items())[:10]:
        print(f"  [{len(v)}] {k[:70]}")
        print("   ", v[:5])
    print(f"India descs remaining: {india}")
    print(f"Missing H1 (excl junk): {no_h1}")

    # Fix 6b: JSON-LD on key hubs missing schema
    schema_targets = [
        "ca-final-test-schedule-nov-2026.html",
        "ca-final-test-schedule-may-2026.html",
        "ca-final-test-schedule-may-2027.html",
        "ca-inter-test-schedule-sep-2026.html",
        "ca-inter-test-schedule-may-2026.html",
        "ca-inter-test-schedule-jan-2027.html",
        "ca-foundation-test-schedule-sep-2026.html",
        "ca-foundation-test-schedule-may-2026.html",
        "ca-inter-dot-3-series-sep-2026.html",
        "ca-foundation-dot-3-series-sep-2026.html",
        "ca-final-dot-3-series-nov-2026.html",
        "ca-inter-abc-series-sep-2026.html",
        "ca-final-abc-series-nov-2026.html",
        "ca-foundation-abc-series-may-2026.html",
        "ca-inter-dot-marathon-series-sep-2026.html",
        "ca-final-dot-marathon-series-nov-2026.html",
        "registration.html",
        "course-overview.html",
        "ca-foundation-test-series.html",
    ]
    for name in schema_targets:
        path = ROOT / name
        if not path.exists():
            print(f"schema skip missing: {name}")
            continue
        text = path.read_text(errors="replace")
        if "application/ld+json" in text:
            continue
        title, desc = planned.get(name, (name, "PradhiCA CA test series"))
        url = f"https://pradhica.com/{name}"
        block = org_schema_block(url, title, desc)
        # insert before </head>
        if re.search(r"</head>", text, re.I):
            text2 = re.sub(r"</head>", block + "</head>", text, count=1, flags=re.I)
            path.write_text(text2)
            stats["schema"] += 1
            print(f"schema added: {name}")
        else:
            print(f"schema no </head>: {name}")

    print("schema added count:", stats["schema"])
    print("FIX5_6_DONE")


if __name__ == "__main__":
    main()

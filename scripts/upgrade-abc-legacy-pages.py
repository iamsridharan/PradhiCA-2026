#!/usr/bin/env python3
"""Upgrade legacy ABC payment pages to premium ABC product design."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800'
    '&family=Maven+Pro:wght@400;500;700&family=Work+Sans:wght@400;500;600&display=swap">'
)

CSS_LINKS = """    <link rel="stylesheet" href="assets/css/abc-series-hub-premium.css">
    <link rel="stylesheet" href="assets/css/abc-product-premium.css">"""

STYLE_RE = re.compile(r"\s*<style>.*?</style>\s*", re.DOTALL)

TEMPLATES = {
    ("direct", False): "ca-final-abc-direct-nov-2026.html",
    ("direct", True): "ca-final-abc-direct-with-model-nov-2026.html",
    ("online", False): "ca-final-abc-online-nov-2026.html",
    ("online", True): "ca-final-abc-online-with-model-nov-2026.html",
}

TARGET_PAGES = [
    "ca-final-abc-direct-may-2026.html",
    "ca-final-abc-direct-with-model-may-2026.html",
    "ca-final-abc-online-may-2026.html",
    "ca-final-abc-online-with-model-may-2026.html",
    "ca-foundation-abc-direct-may-2026.html",
    "ca-foundation-abc-direct-with-model-may-2026.html",
    "ca-foundation-abc-online-may-2026.html",
    "ca-foundation-abc-online-with-model-may-2026.html",
    "ca-inter-abc-direct-may-2026.html",
    "ca-inter-abc-direct-with-model-may-2026.html",
    "ca-inter-abc-online-may-2026.html",
    "ca-inter-abc-online-with-model-may-2026.html",
    "ca-inter-abc-direct-jan-2027.html",
    "ca-inter-abc-direct-with-model-jan-2027.html",
    "ca-inter-abc-online-jan-2027.html",
    "ca-inter-abc-online-with-model-jan-2027.html",
]

LEVEL_META = {
    "final": {
        "slug": "final",
        "label": "CA Final",
        "short": "Final",
    },
    "inter": {
        "slug": "inter",
        "label": "CA Inter",
        "short": "Inter",
    },
    "foundation": {
        "slug": "foundation",
        "label": "CA Foundation",
        "short": "Foundation",
    },
}

BATCH_META = {
    "may-2026": {
        "batch": "May 2026",
        "breadcrumb": "May 26",
    },
    "jan-2027": {
        "batch": "Jan 2027",
        "breadcrumb": "Jan 27",
    },
}


def parse_page_name(fname: str) -> dict:
    m = re.match(
        r"ca-(final|inter|foundation)-abc-(direct|online)(?:-with-model)?-(\w+-\d{4})\.html",
        fname,
    )
    if not m:
        raise ValueError(f"Cannot parse page name: {fname}")
    level, mode, batch_slug = m.groups()
    with_model = "-with-model" in fname
    base = fname.replace(".html", "")
    if with_model:
        sibling_without = base.replace("-with-model", "") + ".html"
        sibling_with = fname
    else:
        sibling_without = fname
        parts = base.rsplit(f"-{mode}", 1)
        sibling_with = f"{parts[0]}-{mode}-with-model-{batch_slug}.html"
    if mode == "direct":
        sibling_other_mode = base.replace("-direct", "-online").replace("-with-model", "")
        sibling_other_mode_with = sibling_other_mode.replace(f"-{batch_slug}", f"-with-model-{batch_slug}")
        if with_model:
            sibling_other_mode = sibling_other_mode.replace(f"-{batch_slug}", f"-with-model-{batch_slug}")
        else:
            sibling_other_mode_with = sibling_other_mode.replace(f"-{batch_slug}", f"-with-model-{batch_slug}")
    else:
        sibling_other_mode = base.replace("-online", "-direct").replace("-with-model", "")
        sibling_other_mode_with = sibling_other_mode.replace(f"-{batch_slug}", f"-with-model-{batch_slug}")
        if with_model:
            sibling_other_mode = sibling_other_mode.replace(f"-{batch_slug}", f"-with-model-{batch_slug}")
        else:
            sibling_other_mode_with = sibling_other_mode.replace(f"-{batch_slug}", f"-with-model-{batch_slug}")

    level_info = LEVEL_META[level]
    batch_info = BATCH_META[batch_slug]
    schedule = f"ca-{level}-test-schedule-{batch_slug}.html"
    series = f"ca-{level}-abc-series-{batch_slug}.html"

    return {
        "fname": fname,
        "level": level,
        "mode": mode,
        "batch_slug": batch_slug,
        "with_model": with_model,
        "schedule": schedule,
        "series": series,
        "sibling_without": sibling_without,
        "sibling_with": sibling_with,
        "sibling_other_without": sibling_other_mode + ".html" if not sibling_other_mode.endswith(".html") else sibling_other_mode,
        "sibling_other_with": sibling_other_mode_with + ".html" if not sibling_other_mode_with.endswith(".html") else sibling_other_mode_with,
        **level_info,
        **batch_info,
    }


def extract_head_block(legacy: str) -> str:
    head = re.search(r"<head>.*?</head>", legacy, re.DOTALL).group(0)
    head = STYLE_RE.sub("\n", head)
    head = re.sub(
        r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css[^"]*">',
        FONT_LINK,
        head,
        count=1,
    )
    if "abc-series-hub-premium.css" not in head:
        head = head.replace(
            '<link rel="stylesheet" href="assets/css/header-premium.css">',
            '<link rel="stylesheet" href="assets/css/header-premium.css">\n' + CSS_LINKS,
        )
    return head


def extract_pricing_section_html(legacy: str, with_model: bool) -> str:
    section = re.search(
        r'<section class="padding-y-100[^"]*" id="pricing">(.*?)</section>',
        legacy,
        re.DOTALL,
    )
    if not section:
        raise ValueError("Pricing section not found")
    inner = section.group(1)

    without_m = re.search(
        r'<h4[^>]*>.*?WITHOUT\s+MODEL.*?</h4>(.*?)(?=<div class="col-12 text-center mb-3">\s*<h4[^>]*>.*?WITH\s+MODEL|$)',
        inner,
        re.DOTALL | re.IGNORECASE,
    )
    with_m = re.search(
        r'<h4[^>]*>.*?WITH\s+MODEL.*?</h4>(.*)',
        inner,
        re.DOTALL | re.IGNORECASE,
    )

    if without_m and with_m:
        chunk = with_m.group(1) if with_model else without_m.group(1)
    else:
        chunk = inner

    # strip leading feature/header blocks before first price card
    first_card = re.search(r'<div class="col-(?:md-4|lg-3)', chunk)
    if first_card:
        chunk = chunk[first_card.start() :]
    return chunk


def transform_cards(chunk: str) -> str:
    card_pattern = r'<div class="col-(?:md-4|lg-3)[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>'
    cards = re.findall(card_pattern, chunk, re.DOTALL)
    if not cards:
        cards = re.findall(
            r'(<div class="col-(?:md-4|lg-3)[^"]*"[^>]*>.*?<div class="razorpay-embed-btn"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>)',
            chunk,
            re.DOTALL,
        )
    out = []
    for card in cards:
        inner = re.sub(r'^<div class="col-(?:md-4|lg-3)[^"]*"[^>]*>\s*', "", card.strip())
        inner = re.sub(r"\s*</div>\s*$", "", inner)
        popular = (
            'badge-primary">Popular' in inner
            or 'badge-pill badge-primary">Popular' in inner
            or "card--featured" in inner
            or "Best Value" in inner
        )
        cls = "abc-price-card abc-price-card--popular" if popular else "abc-price-card"
        out.append(f'            <div class="{cls}">\n{inner}\n            </div>')
    return "\n".join(out)


def hero_html(cfg: dict) -> str:
    mode_icon = "fa-laptop" if cfg["mode"] == "online" else "fa-building"
    model_label = "With model" if cfg["with_model"] else "Without model"
    mode_label = "Online" if cfg["mode"] == "online" else "Direct"
    h1 = f'{cfg["label"]} ABC {mode_label} · {model_label} · {cfg["batch"]}'

    if cfg["mode"] == "direct" and cfg["with_model"]:
        lead = (
            f'Secure checkout for <strong>Chennai centre</strong> ABC + model packages. '
            "In-person exams with invigilation and on-campus support."
        )
        badge_model = '<span class="abc-badge"><i class="fas fa-layer-group" aria-hidden="true"></i> ABC + model bundle</span>'
    elif cfg["mode"] == "direct":
        lead = (
            f'Secure checkout for <strong>Chennai centre</strong> ABC papers without model — '
            "flexible packages below. All fees exclusive of GST."
        )
        badge_model = '<span class="abc-badge"><i class="fas fa-file-alt" aria-hidden="true"></i> Without model</span>'
    elif cfg["with_model"]:
        lead = (
            "Secure checkout for <strong>online ABC + model</strong> packages. "
            "Write from anywhere in India with CA evaluation and suggested answers."
        )
        badge_model = '<span class="abc-badge"><i class="fas fa-layer-group" aria-hidden="true"></i> ABC + model bundle</span>'
    else:
        lead = (
            "Register for <strong>online ABC mock tests</strong> without model papers — "
            "flexible paper and group combinations below."
        )
        badge_model = '<span class="abc-badge"><i class="fas fa-file-alt" aria-hidden="true"></i> Without model</span>'

    return f"""  <header class="abc-hero" aria-labelledby="abc-product-h1">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10 py-2">
          <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
            <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
            <li class="breadcrumb-item"><a href="{cfg['schedule']}">{cfg['label']} {cfg['breadcrumb']}</a></li>
            <li class="breadcrumb-item"><a href="{cfg['series']}">ABC Test Series</a></li>
            <li class="breadcrumb-item active" aria-current="page">{mode_label} · {model_label}</li>
          </ol>
          <h1 id="abc-product-h1"><i class="fas {mode_icon} mr-2" aria-hidden="true"></i>{h1}</h1>
          <p class="lead">{lead}</p>
          <div class="abc-hero__badges">
            <span class="abc-badge"><i class="fas fa-calendar-alt" aria-hidden="true"></i> {cfg['batch']} batch</span>
            {badge_model}
            <span class="abc-badge"><i class="fas fa-lock" aria-hidden="true"></i> Razorpay secure pay</span>
          </div>
          <div class="abc-trust">
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-style pattern</span>
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> Suggested answers</span>
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> <a href="tel:+918072653948" class="abc-trust__link">+91 80726 53948</a></span>
          </div>
        </div>
      </div>
    </div>
  </header>"""


def pricing_actions(cfg: dict, cards_html: str) -> str:
    mode_label = "Online" if cfg["mode"] == "online" else "Direct"
    if cfg["with_model"]:
        switch_model = (
            f'<a href="{cfg["sibling_without"]}" class="abc-product-actions__pill">'
            f'<i class="fas fa-file-alt" aria-hidden="true"></i>Switch to without model</a>'
        )
    else:
        switch_model = (
            f'<a href="{cfg["sibling_with"]}" class="abc-product-actions__pill">'
            f'<i class="fas fa-layer-group" aria-hidden="true"></i>Switch to with model</a>'
        )
    if cfg["mode"] == "direct":
        switch_mode = (
            f'<a href="{cfg["sibling_other_without"]}" class="abc-product-actions__pill">'
            f'<i class="fas fa-laptop" aria-hidden="true"></i>Switch to Online</a>'
        )
        if cfg["with_model"]:
            switch_mode = (
                f'<a href="{cfg["sibling_other_with"]}" class="abc-product-actions__pill">'
                f'<i class="fas fa-laptop" aria-hidden="true"></i>Switch to Online</a>'
            )
    else:
        switch_mode = (
            f'<a href="{cfg["sibling_other_without"]}" class="abc-product-actions__pill">'
            f'<i class="fas fa-building" aria-hidden="true"></i>Switch to Direct</a>'
        )
        if cfg["with_model"]:
            switch_mode = (
                f'<a href="{cfg["sibling_other_with"]}" class="abc-product-actions__pill">'
                f'<i class="fas fa-building" aria-hidden="true"></i>Switch to Direct</a>'
            )

    model_phrase = "With model" if cfg["with_model"] else "Without model"
    block_mode = "Online" if cfg["mode"] == "online" else "Direct"
    if cfg["mode"] == "direct":
        pricing_desc = (
            "Pay via Razorpay. Centre-based ABC mock tests — pick paper count or group bundles "
            f"at our Chennai centre."
            if not cfg["with_model"]
            else "Pay via Razorpay. Centre-based ABC series with model examinations — all fees exclusive of GST."
        )
    else:
        pricing_desc = (
            "Razorpay checkout. Core ABC mock tests only — pick paper count or group bundles to match your plan."
            if not cfg["with_model"]
            else "Razorpay checkout. ABC test series plus model papers — 25% concession on model fee when registered together."
        )

    return f"""          <div class="abc-pricing__head">
            <div class="abc-product-actions">
              <a href="{cfg['series']}" class="abc-back-link abc-pricing__back"><i class="fas fa-arrow-left" aria-hidden="true"></i>Back to ABC options</a>
              {switch_model}
              {switch_mode}
            </div>
            <h2>Select your {mode_label} package · {model_phrase}</h2>
            <p>{pricing_desc}</p>
          </div>

          <ul class="pg-single__features">
            <li><i class="fas fa-check" aria-hidden="true"></i>Evaluated by Qualified CAs</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>Results within 4 days</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>Suggested answers after each exam</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>ICAI-aligned pattern and timing</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>Amendments and case-study coverage</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>Flexible scheduling options</li>
          </ul>

          <div class="abc-price-tier">
            <div class="abc-price-block">
              <h3 class="abc-price-block__title">ABC {block_mode} — <span class="text-primary">{model_phrase}</span></h3>
            </div>
          <div class="abc-price-grid">
{cards_html}
          </div>
          </div>"""


def venue_block() -> str:
    return """
          <div class="pg-venue-block">
            <div class="pg-venue-block__inner">
              <p class="pg-venue-block__label mb-0">Direct mode · exam venue</p>
              <h3 class="pg-venue-block__title"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> PradhiCA Chennai centre</h3>
              <p class="pg-venue-block__brand mb-0">PradhiCA</p>
              <p class="pg-venue-block__address">No: 20, <strong>1st floor</strong>, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu <strong>600033</strong></p>
              <a href="https://maps.app.goo.gl/3scL1jiJsRZxtvYd9" class="pg-venue-block__btn" target="_blank" rel="noopener noreferrer"><i class="fas fa-directions" aria-hidden="true"></i>Open in Google Maps</a>
            </div>
          </div>"""


def online_block() -> str:
    return """
          <div class="pg-online-block">
            <div class="pg-online-block__inner">
              <p class="pg-online-block__label mb-0">Online mode</p>
              <h3 class="pg-online-block__title"><i class="fas fa-laptop" aria-hidden="true"></i> Write from anywhere in India</h3>
              <p class="pg-online-block__text">Same papers and CA evaluation as Direct mode. Attempt tests on your schedule with mentoring support via <a href="tel:+918072653948">+91 80726 53948</a>.</p>
              <a href="registration.html" class="pg-online-block__btn"><i class="fas fa-envelope" aria-hidden="true"></i>Send enquiry</a>
            </div>
          </div>"""


def build_pricing_section(cfg: dict, cards_html: str) -> str:
    mode_block = venue_block() if cfg["mode"] == "direct" else online_block()
    actions = pricing_actions(cfg, cards_html)
    return f"""
  <section class="abc-pricing pg-single" id="pricing">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-11">
{actions}
{mode_block}

          <p class="abc-pricing__note"><i class="fas fa-info-circle mr-1"></i>GST as applicable · Need help? <a href="registration.html">Enquiry</a> or <a href="https://api.whatsapp.com/send?phone=918072653948">WhatsApp</a></p>
        </div>
      </div>
    </div>
  </section>"""


def sticky_html(cfg: dict) -> str:
    return f"""
  <div class="abc-product-sticky" role="navigation" aria-label="Quick links">
    <a href="#pricing" class="abc-product-sticky--gold">View pricing</a>
    <a href="{cfg['schedule']}" class="abc-product-sticky--outline">Full schedule</a>
  </div>"""


def extract_shell(template: str) -> tuple[str, str, str]:
    nav_end = re.search(r"</nav>", template)
    footer_start = re.search(r"<footer class=\"site-footer\">", template)
    body_open = re.search(r"<body[^>]*>", template)
    head = re.search(r"<head>.*?</head>", template, re.DOTALL).group(0)
    header_nav = template[body_open.end() : nav_end.end()]
    footer_tail = template[footer_start.start() :]
    return head, header_nav, footer_tail


def upgrade_page(fname: str) -> None:
    cfg = parse_page_name(fname)
    legacy = (ROOT / fname).read_text(encoding="utf-8")
    template_name = TEMPLATES[(cfg["mode"], cfg["with_model"])]
    template = (ROOT / template_name).read_text(encoding="utf-8")

    _, header_nav, footer_tail = extract_shell(template)
    head = extract_head_block(legacy)

    # Preserve legacy head meta; ensure canonical matches filename
    canonical = f"https://pradhica.com/{fname}"
    head = re.sub(r'property="og:url" content="[^"]+"', f'property="og:url" content="{canonical}"', head)
    head = re.sub(r'name="twitter:url" content="[^"]+"', f'name="twitter:url" content="{canonical}"', head)
    head = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="{canonical}"', head)
    head = re.sub(
        r'"@id": "https://pradhica.com/[^#]+#webpage"',
        f'"@id": "{canonical}#webpage"',
        head,
    )
    head = re.sub(
        r'"url": "https://pradhica.com/ca-[^"]+\.html"',
        f'"url": "{canonical}"',
        head,
        count=1,
    )

    pricing_chunk = extract_pricing_section_html(legacy, cfg["with_model"])
    cards_html = transform_cards(pricing_chunk)
    if not cards_html.strip():
        raise ValueError(f"No pricing cards extracted for {fname}")

    body_class = (
        f'pg-abc-home pg-abc-home--{cfg["slug"]} pg-abc-product pg-abc-product--{cfg["mode"]}'
    )

    main = (
        hero_html(cfg)
        + build_pricing_section(cfg, cards_html)
        + sticky_html(cfg)
    )

    html = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n\n"
        + head
        + f"\n\n<body class=\"{body_class}\">"
        + header_nav
        + "\n"
        + main
        + "\n\n"
        + footer_tail
    )

    (ROOT / fname).write_text(html, encoding="utf-8")
    print(f"Upgraded: {fname} ({len(re.findall('razorpay-embed-btn', cards_html))} cards)")


def main():
    issues = []
    for fname in TARGET_PAGES:
        path = ROOT / fname
        if not path.exists():
            issues.append(f"MISSING: {fname}")
            continue
        try:
            upgrade_page(fname)
        except Exception as exc:
            issues.append(f"ERROR {fname}: {exc}")
    if issues:
        print("\nIssues:")
        for item in issues:
            print(f"  - {item}")
    else:
        print("\nAll 16 pages upgraded successfully.")


if __name__ == "__main__":
    main()

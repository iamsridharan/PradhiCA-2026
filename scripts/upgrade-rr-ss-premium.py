#!/usr/bin/env python3
"""Upgrade legacy Rapid Revision and Single Subject pages to premium design."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STYLE_RE = re.compile(r"\s*<style>.*?</style>\s*", re.DOTALL)
NAV_END_RE = re.compile(r"(</nav>\s*)", re.DOTALL)
FOOTER_START_RE = re.compile(r"<footer class=\"site-footer\">", re.DOTALL)

RAZORPAY_SNIPPET = """<div class="razorpay-embed-btn" data-url="{url}" data-text="Proceed to Pay" data-color="#528FF0" data-size="large">
  <script>
    (function(){{
      var d=document; var x=!d.getElementById('razorpay-embed-btn-js')
      if(x){{ var s=d.createElement('script'); s.defer=!0;s.id='razorpay-embed-btn-js';
      s.src='https://cdn.razorpay.com/static/embed_btn/bundle.js';d.body.appendChild(s);}} else{{var rzp=window['__rzp__'];
      rzp && rzp.init && rzp.init()}}}})();
  </script>
</div>"""

BATCH_LABEL = {
    "may-2026": ("May 2026", "May 26"),
    "sep-2026": ("Sep 2026", "Sep 26"),
    "jan-2027": ("Jan 2027", "Jan 27"),
    "may-2027": ("May 2027", "May 27"),
    "jan-2026": ("Jan 2026", "Jan 26"),
}

LEVEL_META = {
    "foundation": ("Foundation", "FOUNDATION", "CA Foundation"),
    "inter": ("Inter", "INTER", "CA Intermediate"),
    "final": ("Final", "FINAL", "CA Final"),
}

SCHEDULE = {
    ("foundation", "may-2026"): "ca-foundation-test-schedule-may-2026.html",
    ("inter", "may-2026"): "ca-inter-test-schedule-may-2026.html",
    ("inter", "sep-2026"): "ca-inter-test-schedule-sep-2026.html",
    ("inter", "jan-2027"): "ca-inter-test-schedule-jan-2027.html",
    ("inter", "jan-2026"): "ca-inter-test-schedule-jan-2027.html",
    ("final", "may-2026"): "ca-final-test-schedule-may-2026.html",
    ("final", "may-2027"): "ca-final-test-schedule-may-2027.html",
}

RR_PDF = {
    "foundation": "Schedules_2026/PradhiCA-CA_Foundation-Rapid Revision Test May 26 Sep 26 Jan 27.pdf",
    "inter": "Schedules_2026/PradhiCA-CA_Inter-Rapid Revision Test May 26 Sep 26 Jan 27.pdf",
    "final": "Schedules_2026/PradhiCA-CA_Final-Rapid Revision Test May 26 Sep 26 Jan 27.pdf",
}

TIER_NORMALIZE = {
    "1 - PAPER": ("1 Paper", "1-paper", False),
    "1 PAPER": ("1 Paper", "1-paper", False),
    "2 - PAPER": ("2 Papers", "2-paper", False),
    "2 PAPER": ("2 Papers", "2-paper", False),
    "3 PAPERS": ("3 Papers", "3-paper", True),
    "GROUP 1/2": ("Group 1 or 2", "group", True),
    "GROUP 1 OR 2": ("Group 1 or 2", "group", True),
    "BOTH - GROUPS": ("Both Groups", "both", False),
    "BOTH GROUPS": ("Both Groups", "both", False),
    "ALL SUBJECTS": ("All Subjects", "all-subjects", False),
}


def parse_filename(name: str) -> dict:
    stem = name.replace(".html", "")
    rr_reg = re.match(
        r"ca-(foundation|inter|final)-rapid-revision-registration-(.+)$", stem
    )
    ss_reg = re.match(
        r"ca-(foundation|inter|final)-single-subject-registration-(.+)$", stem
    )
    rr_pay = re.match(
        r"ca-(foundation|inter|final)-rapid-revision-(direct|online)-(.+)$", stem
    )
    ss_pay = re.match(
        r"ca-(foundation|inter|final)-single-subject-(direct|online)-(with|without)-model-(.+)$",
        stem,
    )
    if rr_reg:
        level, batch = rr_reg.groups()
        return {
            "level": level,
            "batch": batch,
            "kind": "rr",
            "product": "registration",
            "mode": None,
            "model": None,
            "stem": stem,
        }
    if ss_reg:
        level, batch = ss_reg.groups()
        return {
            "level": level,
            "batch": batch,
            "kind": "ss",
            "product": "registration",
            "mode": None,
            "model": None,
            "stem": stem,
        }
    if rr_pay:
        level, mode, batch = rr_pay.groups()
        return {
            "level": level,
            "batch": batch,
            "kind": "rr",
            "product": "payment",
            "mode": mode,
            "model": None,
            "stem": stem,
        }
    if ss_pay:
        level, mode, model, batch = ss_pay.groups()
        return {
            "level": level,
            "batch": batch,
            "kind": "ss",
            "product": "payment",
            "mode": mode,
            "model": model,
            "stem": stem,
        }
    raise ValueError(f"Unrecognized filename pattern: {name}")


def pay_batch(batch: str) -> str:
    return "jan-2027" if batch == "jan-2026" else batch


def extract_cards(text: str) -> list[dict]:
    m = re.search(r'id="pricing".*?</section>', text, re.DOTALL)
    sec = m.group(0) if m else text
    raw = re.findall(
        r'<h3 class="mb-0">([^<]+)</h3>.*?display-4 text-success[^>]*>\s*₹\s*([0-9]+)(.*?)</div>\s*<div class="card-footer">.*?data-url="([^"]+)"',
        sec,
        re.DOTALL,
    )
    cards = []
    for title, price, mid, url in raw:
        key = re.sub(r"\s+", " ", title.strip().upper())
        label, tier_id, featured = TIER_NORMALIZE.get(key, (title.strip(), "tier", False))
        subtitle = "Exclusive of GST"
        if "20%" in mid or "concession" in mid.lower():
            subtitle += "<br>20% concession on fee"
        elif "quick practice" in mid.lower():
            subtitle += "<br>Best for quick practice on one subject"
        elif "two subject" in mid.lower():
            subtitle += "<br>Balanced coverage across two subjects"
        cards.append(
            {
                "title": label,
                "tier_id": tier_id,
                "price": price,
                "url": url,
                "subtitle": subtitle,
                "featured": featured,
            }
        )
    return cards


def first_price(path: Path) -> str | None:
    if not path.exists():
        return None
    cards = extract_cards(path.read_text())
    return cards[0]["price"] if cards else None


def fix_head(head: str, css_file: str) -> str:
    head = STYLE_RE.sub("\n", head)
    if css_file not in head:
        head = head.replace(
            '<link rel="stylesheet" href="assets/css/header-premium.css">',
            f'<link rel="stylesheet" href="assets/css/header-premium.css">\n    <link rel="stylesheet" href="assets/css/{css_file}">',
        )
    if "DM+Sans" not in head:
        head = head.replace(
            "<!--Google fonts-->",
            '<!--Google fonts-->\n    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800&family=Maven+Pro:wght@500;600;700;800&family=Work+Sans:wght@400;500;600&display=swap">',
        )
    return head


def fix_body_class(body_open: str, classes: str) -> str:
    return re.sub(r'<body[^>]*>', f'<body class="{classes}">', body_open, count=1)


def fix_scripts(footer_block: str, js_file: str) -> str:
    footer_block = re.sub(r'\s*<script src="assets/js/rapid-revision-premium.js"></script>', "", footer_block)
    footer_block = re.sub(r'\s*<script src="assets/js/single-subject-premium.js"></script>', "", footer_block)
    if js_file not in footer_block:
        footer_block = footer_block.replace(
            '<script src="assets/js/scripts.js"></script>',
            f'<script src="assets/js/scripts.js"></script>\n    <script src="assets/js/{js_file}"></script>',
        )
    return footer_block


def split_page(text: str) -> tuple[str, str, str, str]:
    body_m = re.search(r"<body[^>]*>", text)
    if not body_m:
        raise ValueError("No body tag")
    head = text[: body_m.start()]
    rest = text[body_m.end() :]
    nav_m = NAV_END_RE.search(rest)
    if not nav_m:
        raise ValueError("No nav end")
    footer_m = FOOTER_START_RE.search(rest)
    if not footer_m:
        raise ValueError("No footer")
    nav = rest[: nav_m.end()]
    footer = rest[footer_m.start() :]
    return head, "", nav, footer


def tier_pills_html(cards: list[dict], prefix: str) -> str:
    lines = [
        f'    <div class="{prefix}-tier-pills" role="group" aria-label="Pricing tiers">',
    ]
    for c in cards:
        lines.append(
            f'      <button type="button" class="{prefix}-tier-pill" data-tier="{c["tier_id"]}">{c["title"]}</button>'
        )
    lines.append("    </div>")
    return "\n".join(lines)


def price_cards_html(cards: list[dict]) -> str:
    chunks = []
    for c in cards:
        col_class = "col-md-6 col-lg-3 mt-4"
        if c["featured"]:
            col_class += " pg-price-col--featured"
        chunks.append(
            f"""     <div class="{col_class}">
       <div class="card pg-price-card text-center height-100p mb-4" id="tier-{c['tier_id']}">
         <div class="card-header border-bottom">
           <h3 class="mb-0">{c['title']}</h3>
         </div>
         <div class="card-header border-bottom py-5">
           <h2 class="mb-0 display-4 text-success">₹ {c['price']}</h2>
           <p class="mb-0 text-muted small">{c['subtitle']}</p>
         </div>
         <div class="card-footer">
          {RAZORPAY_SNIPPET.format(url=c['url'])}
         </div>
       </div>
     </div>"""
        )
    return "\n".join(chunks)


def rr_payment_content(meta: dict, cards: list[dict]) -> str:
    level = meta["level"]
    batch = meta["batch"]
    mode = meta["mode"]
    short, abbr = BATCH_LABEL.get(batch, (batch, batch))
    _, level_upper, level_long = LEVEL_META[level]
    schedule = SCHEDULE.get((level, batch), f"ca-{level}-test-schedule-{batch}.html")
    reg = f"ca-{level}-rapid-revision-registration-{batch}.html"
    direct = f"ca-{level}-rapid-revision-direct-{batch}.html"
    online = f"ca-{level}-rapid-revision-online-{batch}.html"
    pdf = RR_PDF[level]
    is_direct = mode == "direct"
    mode_label = "Direct" if is_direct else "Online"
    icon = "fa-building" if is_direct else "fa-laptop"
    body_mod = f"pg-rr-pay--{mode}"
    breadcrumb_active = "Direct payment" if is_direct else "Online payment"
    tier_line = f"{level_upper} EXAM · <span class=\"text-primary\">RAPID REVISION {mode_label.upper()}</span>"

    if is_direct:
        hero_sub = "Pay for <strong>Direct mode</strong> at our Chennai centre. Choose papers or groups below. All fees exclusive of GST @ 18%."
        badges = """        <span class="pg-pay-badge"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> Direct mode</span>
        <span class="pg-pay-badge"><i class="fas fa-shield-alt" aria-hidden="true"></i> Razorpay</span>"""
        switch_btn = f'<a href="{online}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas fa-laptop mr-1" aria-hidden="true"></i>Switch to Online</a>'
        bottom_block = """     <div class="col-12 mt-4">
       <div class="pg-venue-block">
         <div class="pg-venue-block__inner">
           <p class="pg-venue-block__label mb-0">Direct mode exam venue</p>
           <h3 class="pg-venue-block__title"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> Visit PradhiCA (Chennai centre)</h3>
           <p class="pg-venue-block__brand mb-0">PradhiCA</p>
           <p class="pg-venue-block__address">No: 20, <strong>1st floor</strong>, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu <strong>600033</strong></p>
           <a href="https://maps.app.goo.gl/3scL1jiJsRZxtvYd9" class="pg-venue-block__btn" target="_blank" rel="noopener noreferrer"><i class="fas fa-directions" aria-hidden="true"></i>Open in Google Maps</a>
         </div>
       </div>
     </div>"""
        faq = """       <div class="rr-faq">
         <h3>Before you pay</h3>
         <div class="rr-faq__item">
           <button type="button" class="rr-faq__trigger" aria-expanded="false">When can I write the papers? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
           <div class="rr-faq__body"><p>Rapid Revision is unscheduled. Coordinate your slot with PradhiCA after payment. See the PDF schedule for subject coverage.</p></div>
         </div>
         <div class="rr-faq__item">
           <button type="button" class="rr-faq__trigger" aria-expanded="false">What does group concession mean? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
           <div class="rr-faq__body"><p>Group I, Group II, or both groups plans include a 20% concession applied to the listed fee before GST.</p></div>
         </div>
       </div>"""
    else:
        hero_sub = "Secure payment for <strong>online</strong> Rapid Revision. Write from anywhere in India with the same CA evaluation. Fees exclusive of GST @ 18%."
        badges = """        <span class="pg-pay-badge"><i class="fas fa-wifi" aria-hidden="true"></i> Online mode</span>
        <span class="pg-pay-badge"><i class="fas fa-shield-alt" aria-hidden="true"></i> Razorpay</span>"""
        switch_btn = f'<a href="{direct}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas fa-map-marker-alt mr-1" aria-hidden="true"></i>Switch to Direct</a>'
        bottom_block = """     <div class="col-12 mt-4">
       <div class="pg-online-block">
         <div class="pg-online-block__inner">
           <p class="pg-online-block__label mb-0">Online mode support</p>
           <h3 class="pg-online-block__title"><i class="fas fa-headset" aria-hidden="true"></i> Write from anywhere in India</h3>
           <p class="pg-online-block__text">After payment, coordinate your paper slots with PradhiCA. Upload scanned answers as per instructions. Questions? Call <a href="tel:+918072653948">+91 80726 53948</a> or <a href="https://api.whatsapp.com/send?phone=918072653948" target="_blank" rel="noopener noreferrer">WhatsApp us</a>.</p>
           <a href="contact-us.html" class="pg-online-block__btn"><i class="fas fa-envelope" aria-hidden="true"></i>Contact support</a>
         </div>
       </div>
     </div>"""
        faq = """       <div class="rr-faq">
         <h3>Before you pay</h3>
         <div class="rr-faq__item">
           <button type="button" class="rr-faq__trigger" aria-expanded="false">How do online papers work? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
           <div class="rr-faq__body"><p>You write at home within ICAI timing, scan and upload your answer book. Our CA evaluators mark and return feedback within four days.</p></div>
         </div>
         <div class="rr-faq__item">
           <button type="button" class="rr-faq__trigger" aria-expanded="false">Why is Online cheaper than Direct? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
           <div class="rr-faq__body"><p>Online pricing excludes centre and invigilation costs. Question quality and evaluation standards are identical across both modes.</p></div>
         </div>
       </div>"""

    return f"""<div class="pg-pay-hero">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-10 py-2">
        <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
          <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
          <li class="breadcrumb-item"><a href="{schedule}">{level_long} {abbr}</a></li>
          <li class="breadcrumb-item"><a href="{reg}">Rapid Revision</a></li>
          <li class="breadcrumb-item active text-white" aria-current="page">{breadcrumb_active}</li>
        </ol>
        <h1><i class="fas {icon} mr-2" aria-hidden="true"></i>{level_long} Rapid Revision · {short} · {mode_label}</h1>
        <p class="pg-pay-sub mt-3 mb-2">{hero_sub}</p>
{badges}
        <div class="pg-pay-trust">
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-style papers</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> Evaluated by qualified CAs</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> 20% group concession</span>
        </div>
      </div>
    </div>
  </div>
</div>

<section class="padding-y-100 border-bottom border-light pg-single" id="pricing">
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="pg-pay-intro text-center">
          <div class="pg-pay-actions">
            <a href="{reg}" class="btn btn-outline-primary btn-sm btn-link-back"><i class="fas fa-arrow-left mr-1" aria-hidden="true"></i>Back to mode choice</a>
            {switch_btn}
            <a href="{pdf}" class="btn btn-outline-info btn-sm btn-link-back" target="_blank" rel="noopener"><i class="fas fa-calendar-alt mr-1" aria-hidden="true"></i>View schedule</a>
          </div>
          <p class="text-muted small mb-0 mt-3"><i class="fas fa-hand-pointer text-primary mr-1" aria-hidden="true"></i>Tap a tier below or pick a package card to pay via Razorpay.</p>
        </div>
      </div>
    </div>
{tier_pills_html(cards, "rr")}
    <div class="row align-items-stretch">
      <div class="col-12">
        <ul class="pg-single__features">
          <li><i class="fas fa-check" aria-hidden="true"></i>Evaluated by qualified CAs</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>Results within 4 days</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>Suggested answers after each exam</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>ICAI-aligned pattern and timing</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>Amendments and case-study coverage</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>Flexible scheduling options</li>
        </ul>
      </div>
     <div class="col-12 pg-single__tier text-center text-md-left">
       <h4>{tier_line}</h4>
     </div>
{price_cards_html(cards)}
{bottom_block}
     <div class="col-12">
{faq}
     </div>
    </div>
  </div>
</section>

<div class="rr-pay-sticky" role="navigation" aria-label="Jump to pricing">
  <a href="#pricing">View packages</a>
</div>
"""


def ss_payment_content(meta: dict, cards: list[dict]) -> str:
    level = meta["level"]
    batch = meta["batch"]
    pb = pay_batch(batch)
    mode = meta["mode"]
    model = meta["model"]
    short, abbr = BATCH_LABEL.get(batch, (batch, batch))
    _, level_upper, level_long = LEVEL_META[level]
    schedule = SCHEDULE.get((level, batch), f"ca-{level}-test-schedule-{batch}.html")
    reg = f"ca-{level}-single-subject-registration-{batch}.html"
    with_model = f"ca-{level}-single-subject-direct-with-model-{pb}.html"
    without_model = f"ca-{level}-single-subject-direct-without-model-{pb}.html"
    online_with = f"ca-{level}-single-subject-online-with-model-{pb}.html"
    online_without = f"ca-{level}-single-subject-online-without-model-{pb}.html"
    if mode == "direct":
        with_link = with_model
        without_link = without_model
        online_link = online_with if model == "with" else online_without
    else:
        with_link = online_with
        without_link = online_without
        online_link = direct = f"ca-{level}-single-subject-direct-{'with' if model == 'with' else 'without'}-model-{pb}.html"

    is_direct = mode == "direct"
    is_with = model == "with"
    mode_label = "Direct" if is_direct else "Online"
    model_label = "With model" if is_with else "Without model"
    icon = "fa-building" if is_direct else "fa-laptop"
    tier_suffix = f"SINGLE SUBJECT {mode_label.upper()} · {'WITH MODEL' if is_with else 'WITHOUT MODEL'}"

    if is_direct and is_with:
        hero_sub = "Pay for <strong>Direct mode</strong> at our Chennai centre. Includes <strong>model exam</strong> bundled with subject-wise tests. All fees exclusive of GST @ 18%."
        model_badge = '<span class="pg-pay-badge pg-pay-badge--model"><i class="fas fa-layer-group" aria-hidden="true"></i> With model</span>'
        alt_model = f'<a href="{without_link}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas fa-exchange-alt mr-1" aria-hidden="true"></i>Without model</a>'
        extra_features = "          <li><i class=\"fas fa-check\" aria-hidden=\"true\"></i>Model exam included in plan</li>\n"
        faq_extra = """          <div class="ss-faq__item">
            <button type="button" class="ss-faq__trigger" aria-expanded="false">What does "with model" include? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
            <div class="ss-faq__body"><p>Your plan bundles a full-syllabus model exam alongside the subject-wise single-subject tests you select.</p></div>
          </div>"""
    elif is_direct:
        hero_sub = "Pay for <strong>Direct mode</strong> at our Chennai centre. Subject-wise tests only, no model exam bundled. All fees exclusive of GST @ 18%."
        model_badge = '<span class="pg-pay-badge"><i class="fas fa-book" aria-hidden="true"></i> Without model</span>'
        alt_model = f'<a href="{with_link}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas fa-exchange-alt mr-1" aria-hidden="true"></i>With model</a>'
        extra_features = ""
        faq_extra = ""
    elif is_with:
        hero_sub = "Secure payment for <strong>online</strong> Single Subject tests with a <strong>model exam</strong> bundled in. Fees exclusive of GST @ 18%."
        model_badge = '<span class="pg-pay-badge pg-pay-badge--model"><i class="fas fa-layer-group" aria-hidden="true"></i> With model</span>'
        alt_model = f'<a href="{without_link}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas fa-exchange-alt mr-1" aria-hidden="true"></i>Without model</a>'
        extra_features = "          <li><i class=\"fas fa-check\" aria-hidden=\"true\"></i>Model exam included in plan</li>\n"
        faq_extra = """          <div class="ss-faq__item">
            <button type="button" class="ss-faq__trigger" aria-expanded="false">What does "with model" include? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
            <div class="ss-faq__body"><p>Your plan bundles a full-syllabus model exam alongside the subject-wise single-subject tests you select.</p></div>
          </div>"""
    else:
        hero_sub = "Secure payment for <strong>online</strong> Single Subject tests — subject-wise practice only. Fees exclusive of GST @ 18%."
        model_badge = '<span class="pg-pay-badge"><i class="fas fa-book" aria-hidden="true"></i> Without model</span>'
        alt_model = f'<a href="{with_link}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas fa-exchange-alt mr-1" aria-hidden="true"></i>With model</a>'
        extra_features = ""
        faq_extra = ""

    mode_badge = (
        '<span class="pg-pay-badge"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> Direct mode</span>'
        if is_direct
        else '<span class="pg-pay-badge"><i class="fas fa-wifi" aria-hidden="true"></i> Online mode</span>'
    )
    switch_btn = (
        f'<a href="{online_link}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas fa-laptop mr-1" aria-hidden="true"></i>Switch to Online</a>'
        if is_direct
        else f'<a href="{direct}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas fa-map-marker-alt mr-1" aria-hidden="true"></i>Switch to Direct</a>'
    )

    if is_direct:
        bottom_block = """      <div class="col-12 mt-4">
        <div class="pg-venue-block">
          <div class="pg-venue-block__inner">
            <p class="pg-venue-block__label mb-0">Direct mode exam venue</p>
            <h3 class="pg-venue-block__title"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> Visit PradhiCA (Chennai centre)</h3>
            <p class="pg-venue-block__brand mb-0">PradhiCA</p>
            <p class="pg-venue-block__address">No: 20, <strong>1st floor</strong>, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu <strong>600033</strong></p>
            <a href="https://maps.app.goo.gl/3scL1jiJsRZxtvYd9" class="pg-venue-block__btn" target="_blank" rel="noopener noreferrer"><i class="fas fa-directions" aria-hidden="true"></i>Open in Google Maps</a>
          </div>
        </div>
      </div>"""
    else:
        bottom_block = """      <div class="col-12 mt-4">
        <div class="pg-online-block">
          <div class="pg-online-block__inner">
            <p class="pg-online-block__label mb-0">Online mode support</p>
            <h3 class="pg-online-block__title"><i class="fas fa-headset" aria-hidden="true"></i> Write from anywhere in India</h3>
            <p class="pg-online-block__text">After payment, coordinate your paper slots with PradhiCA. Upload scanned answers as per instructions. Questions? Call <a href="tel:+918072653948">+91 80726 53948</a> or <a href="https://api.whatsapp.com/send?phone=918072653948" target="_blank" rel="noopener noreferrer">WhatsApp us</a>.</p>
            <a href="contact-us.html" class="pg-online-block__btn"><i class="fas fa-envelope" aria-hidden="true"></i>Contact support</a>
          </div>
        </div>
      </div>"""

    return f"""<div class="pg-pay-hero">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-10 py-2">
        <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
          <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
          <li class="breadcrumb-item"><a href="{schedule}">{level_long} {abbr}</a></li>
          <li class="breadcrumb-item"><a href="{reg}">Single Subject</a></li>
          <li class="breadcrumb-item active text-white" aria-current="page">{mode_label} · {model_label}</li>
        </ol>
        <h1><i class="fas {icon} mr-2" aria-hidden="true"></i>{level_long} Single Subject · {short} · {mode_label}</h1>
        <p class="pg-pay-sub mt-3 mb-2">{hero_sub}</p>
        {mode_badge}
        {model_badge}
        <span class="pg-pay-badge"><i class="fas fa-shield-alt" aria-hidden="true"></i> Razorpay</span>
        <div class="pg-pay-trust">
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-style papers</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> Evaluated by qualified CAs</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> 20% group concession</span>
        </div>
      </div>
    </div>
  </div>
</div>

<section class="padding-y-100 border-bottom border-light pg-single" id="pricing">
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="pg-pay-intro text-center">
          <div class="pg-pay-actions">
            <a href="{reg}" class="btn btn-outline-primary btn-sm btn-link-back"><i class="fas fa-arrow-left mr-1" aria-hidden="true"></i>Back to mode choice</a>
            {alt_model}
            {switch_btn}
          </div>
          <p class="text-muted small mb-0 mt-3"><i class="fas fa-hand-pointer text-primary mr-1" aria-hidden="true"></i>Tap a tier below or pick a package card to pay via Razorpay.</p>
        </div>
      </div>
    </div>
{tier_pills_html(cards, "ss")}
    <div class="row align-items-stretch">
      <div class="col-12">
        <ul class="pg-single__features">
          <li><i class="fas fa-check" aria-hidden="true"></i>Evaluated by qualified CAs</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>Results within 4 days</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>Suggested answers after each exam</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>ICAI-aligned pattern and timing</li>
          <li><i class="fas fa-check" aria-hidden="true"></i>Amendments and case-study coverage</li>
{extra_features}          <li><i class="fas fa-check" aria-hidden="true"></i>Flexible scheduling options</li>
        </ul>
      </div>
      <div class="col-12 pg-single__tier text-center text-md-left">
        <h4>{level_upper} EXAM · <span class="text-primary">{tier_suffix}</span></h4>
      </div>
{price_cards_html(cards)}
{bottom_block}
      <div class="col-12">
        <div class="ss-faq">
          <h3>Before you pay</h3>
{faq_extra}          <div class="ss-faq__item">
            <button type="button" class="ss-faq__trigger" aria-expanded="false">What does group concession mean? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
            <div class="ss-faq__body"><p>Group I, Group II, or both groups plans include a 20% concession applied to the listed fee before GST.</p></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="ss-pay-sticky" role="navigation" aria-label="Jump to pricing">
  <a href="#pricing">View packages</a>
</div>
"""


def rr_hub_content(meta: dict) -> str:
    level = meta["level"]
    batch = meta["batch"]
    short, abbr = BATCH_LABEL.get(batch, (batch, batch))
    _, _, level_long = LEVEL_META[level]
    schedule = SCHEDULE.get((level, batch), f"ca-{level}-test-schedule-{batch}.html")
    reg = meta["stem"]
    direct = f"ca-{level}-rapid-revision-direct-{batch}.html"
    online = f"ca-{level}-rapid-revision-online-{batch}.html"
    pdf = RR_PDF[level]
    direct_price = first_price(ROOT / direct) or "800"
    online_price = first_price(ROOT / online) or "600"
    wa_text = f"Hi%20PradhiCA%2C%20I%20need%20help%20with%20{level_long.replace(' ', '%20')}%20Rapid%20Revision%20{short.replace(' ', '%20')}."
    lead_level = level_long.replace("CA ", "")

    return f"""<header class="rr-hub-hero" aria-labelledby="rr-hub-h1">
    <div class="container">
      <nav aria-label="Breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="index.html">Home</a></li>
          <li class="breadcrumb-item"><a href="{schedule}">{level_long} {abbr}</a></li>
          <li class="breadcrumb-item active" aria-current="page">Rapid Revision</li>
        </ol>
      </nav>
      <p class="rr-hub-eyebrow"><i class="fas fa-fast-forward" aria-hidden="true"></i> {level_long} · {short} attempt</p>
      <h1 id="rr-hub-h1" class="rr-hub-title">Rapid Revision before your {lead_level} papers</h1>
      <p class="rr-hub-lead">Focused mock tests when you need a fast syllabus sweep. Pick <strong>Direct</strong> at our Chennai centre or <strong>Online</strong> from anywhere in India. Group-wise plans get a <strong>20% concession</strong>.</p>
      <div class="rr-hub-hero-cta">
        <a href="{schedule}" class="rr-hub-hero-btn--primary"><i class="far fa-calendar-alt" aria-hidden="true"></i> Full {abbr} schedule</a>
        <a href="{pdf}" class="rr-hub-hero-btn--ghost" target="_blank" rel="noopener"><i class="fas fa-file-pdf" aria-hidden="true"></i> Download PDF</a>
      </div>
    </div>
  </header>

  <div class="rr-hub-trust">
    <div class="container rr-hub-trust__inner">
      <span class="rr-hub-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> Unscheduled, flexible timing</span>
      <span class="rr-hub-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-aligned papers</span>
      <span class="rr-hub-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> Results in 4 days</span>
      <span class="rr-hub-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> 7,500+ students</span>
    </div>
  </div>

  <main class="rr-hub-main" id="choose-mode">
    <div class="container">
      <div class="rr-hub-section-head">
        <h2>How do you want to write?</h2>
        <p>Both modes include expert evaluation and suggested answers. Compare below, then open the payment page for your tier.</p>
      </div>

      <div class="rr-mode-tabs" role="tablist" aria-label="Exam mode">
        <button type="button" class="rr-mode-tab is-active" data-mode="compare" role="tab" aria-selected="true">Compare both</button>
        <button type="button" class="rr-mode-tab" data-mode="direct" role="tab" aria-selected="false">Direct</button>
        <button type="button" class="rr-mode-tab" data-mode="online" role="tab" aria-selected="false">Online</button>
      </div>

      <div class="rr-mode-panel is-active" data-panel="compare">
        <div class="rr-mode-compare">
          <article class="rr-mode-card rr-mode-card--direct" data-mode="direct">
            <div class="rr-mode-card__icon" aria-hidden="true"><i class="fas fa-building"></i></div>
            <h3>Direct mode</h3>
            <p class="rr-mode-card__tag">Chennai centre</p>
            <p>Write at PradhiCA under exam conditions. Best if you want a distraction-free hall and in-person support.</p>
            <ul class="rr-mode-card__list">
              <li><i class="fas fa-check" aria-hidden="true"></i> Physical exam hall in West Mambalam</li>
              <li><i class="fas fa-check" aria-hidden="true"></i> Same-day invigilation and seating</li>
              <li><i class="fas fa-check" aria-hidden="true"></i> From ₹{direct_price} per paper (excl. GST)</li>
            </ul>
            <a class="rr-mode-card__btn" href="{direct}"><i class="fas fa-arrow-right" aria-hidden="true"></i> View Direct pricing</a>
          </article>
          <article class="rr-mode-card rr-mode-card--online" data-mode="online">
            <div class="rr-mode-card__icon" aria-hidden="true"><i class="fas fa-laptop"></i></div>
            <h3>Online mode</h3>
            <p class="rr-mode-card__tag">India-wide</p>
            <p>Write from home with ICAI-style timing. Upload scanned answers and get the same CA evaluation quality.</p>
            <ul class="rr-mode-card__list">
              <li><i class="fas fa-check" aria-hidden="true"></i> Write from any city in India</li>
              <li><i class="fas fa-check" aria-hidden="true"></i> Secure Razorpay checkout</li>
              <li><i class="fas fa-check" aria-hidden="true"></i> From ₹{online_price} per paper (excl. GST)</li>
            </ul>
            <a class="rr-mode-card__btn" href="{online}"><i class="fas fa-arrow-right" aria-hidden="true"></i> View Online pricing</a>
          </article>
        </div>
      </div>

      <div class="rr-mode-panel" data-panel="direct">
        <div class="rr-mode-compare" style="grid-template-columns: 1fr; max-width: 28rem; margin-left: auto; margin-right: auto;">
          <article class="rr-mode-card rr-mode-card--direct is-highlighted">
            <div class="rr-mode-card__icon" aria-hidden="true"><i class="fas fa-building"></i></div>
            <h3>Direct at Chennai</h3>
            <p class="rr-mode-card__tag">PradhiCA centre</p>
            <p>1 paper, 2 papers, single group, or both groups. Group plans include 20% concession on fee.</p>
            <a class="rr-mode-card__btn" href="{direct}"><i class="fas fa-credit-card" aria-hidden="true"></i> Proceed to payment</a>
          </article>
        </div>
      </div>

      <div class="rr-mode-panel" data-panel="online">
        <div class="rr-mode-compare" style="grid-template-columns: 1fr; max-width: 28rem; margin-left: auto; margin-right: auto;">
          <article class="rr-mode-card rr-mode-card--online is-highlighted">
            <div class="rr-mode-card__icon" aria-hidden="true"><i class="fas fa-laptop"></i></div>
            <h3>Online nationwide</h3>
            <p class="rr-mode-card__tag">Razorpay secure</p>
            <p>Lower per-paper rates than Direct. Same evaluation pipeline and suggested answers after each test.</p>
            <a class="rr-mode-card__btn" href="{online}"><i class="fas fa-credit-card" aria-hidden="true"></i> Proceed to payment</a>
          </article>
        </div>
      </div>

      <div class="rr-bento">
        <div class="rr-bento__cell rr-bento__cell--accent">
          <i class="fas fa-clock" aria-hidden="true"></i>
          <h4>Unscheduled flexibility</h4>
          <p>Pick papers when your revision plan allows. No fixed weekly lock-in like marathon series.</p>
        </div>
        <div class="rr-bento__cell">
          <i class="fas fa-percentage" aria-hidden="true"></i>
          <h4>20% group concession</h4>
          <p>Group I, Group II, or both groups qualify for automatic concession on the fee.</p>
        </div>
        <div class="rr-bento__cell">
          <i class="fas fa-file-signature" aria-hidden="true"></i>
          <h4>CA-evaluated copies</h4>
          <p>Detailed feedback and suggested answers within four working days of submission.</p>
        </div>
      </div>

      <div class="rr-faq">
        <h3>Common questions</h3>
        <div class="rr-faq__item">
          <button type="button" class="rr-faq__trigger" aria-expanded="false">What is Rapid Revision? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
          <div class="rr-faq__body"><p>Short, intensive mock tests for students who want extra paper practice close to the attempt. You choose how many papers or groups to cover.</p></div>
        </div>
        <div class="rr-faq__item">
          <button type="button" class="rr-faq__trigger" aria-expanded="false">Direct vs Online pricing? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
          <div class="rr-faq__body"><p>Online is priced lower per paper. Direct includes centre overheads. Both use the same question bank and evaluation team.</p></div>
        </div>
        <div class="rr-faq__item">
          <button type="button" class="rr-faq__trigger" aria-expanded="false">Is GST included? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
          <div class="rr-faq__body"><p>Listed fees are exclusive of GST @ 18%. The final amount appears on the Razorpay checkout screen before you pay.</p></div>
        </div>
      </div>

      <div class="rr-hub-bottom">
        <p>Need help choosing a tier? Tell us your attempt date and which groups you are writing.</p>
        <div class="rr-hub-bottom__links">
          <a href="contact-us.html" class="rr-hub-link--dark"><i class="fas fa-phone-alt" aria-hidden="true"></i> Contact us</a>
          <a href="https://api.whatsapp.com/send?phone=918072653948&amp;text={wa_text}" class="rr-hub-link--wa" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> WhatsApp</a>
        </div>
      </div>
    </div>
  </main>

  <div class="rr-hub-sticky" role="navigation" aria-label="Quick links">
    <a href="{direct}" class="rr-hub-sticky--outline">Direct</a>
    <a href="{online}" class="rr-hub-sticky--rose">Online</a>
  </div>
"""


def ss_hub_content(meta: dict) -> str:
    level = meta["level"]
    batch = meta["batch"]
    short, abbr = BATCH_LABEL.get(batch, (batch, batch))
    _, _, level_long = LEVEL_META[level]
    schedule = SCHEDULE.get((level, batch), f"ca-{level}-test-schedule-{batch}.html")
    pb = pay_batch(batch)
    d_wm = f"ca-{level}-single-subject-direct-without-model-{pb}.html"
    d_w = f"ca-{level}-single-subject-direct-with-model-{pb}.html"
    o_wm = f"ca-{level}-single-subject-online-without-model-{pb}.html"
    o_w = f"ca-{level}-single-subject-online-with-model-{pb}.html"
    d_wm_p = first_price(ROOT / d_wm) or "850"
    d_w_p = first_price(ROOT / d_w) or "1125"
    o_wm_p = first_price(ROOT / o_wm) or "650"
    o_w_p = first_price(ROOT / o_w) or "875"
    wa_text = f"Hi%20PradhiCA%2C%20I%20need%20help%20with%20{level_long.replace(' ', '%20')}%20Single%20Subject%20{short.replace(' ', '%20')}."
    lead_level = level_long.replace("CA ", "")

    return f"""<header class="ss-hub-hero" aria-labelledby="ss-hub-h1">
    <div class="container">
      <nav aria-label="Breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="index.html">Home</a></li>
          <li class="breadcrumb-item"><a href="{schedule}">{level_long} {abbr}</a></li>
          <li class="breadcrumb-item active" aria-current="page">Single Subject</li>
        </ol>
      </nav>
      <p class="ss-hub-eyebrow"><i class="fas fa-book-open" aria-hidden="true"></i> {level_long} · {short} attempt</p>
      <h1 id="ss-hub-h1" class="ss-hub-title">Pick subjects, not the whole syllabus at once</h1>
      <p class="ss-hub-lead">Single Subject tests let you target weak papers before {lead_level}. Choose <strong>Direct</strong> at Chennai or <strong>Online</strong> nationwide. Add a <strong>model exam</strong> or keep it subject-only.</p>
      <div class="ss-hub-hero-cta">
        <a href="{schedule}" class="ss-hub-hero-btn--primary"><i class="far fa-calendar-alt" aria-hidden="true"></i> Full {abbr} schedule</a>
        <a href="#choose-mode" class="ss-hub-hero-btn--ghost"><i class="fas fa-arrow-down" aria-hidden="true"></i> Compare options</a>
      </div>
    </div>
  </header>

  <div class="ss-hub-trust">
    <div class="container ss-hub-trust__inner">
      <span class="ss-hub-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> Subject-wise flexibility</span>
      <span class="ss-hub-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-aligned papers</span>
      <span class="ss-hub-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> Results in 4 days</span>
      <span class="ss-hub-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> 7,500+ students</span>
    </div>
  </div>

  <main class="ss-hub-main" id="choose-mode">
    <div class="container">
      <div class="ss-hub-section-head">
        <h2>How do you want to register?</h2>
        <p>Filter by exam mode and whether you need a bundled model exam. Open the payment page when you are ready.</p>
      </div>

      <div class="ss-model-pills" role="group" aria-label="Model exam choice">
        <button type="button" class="ss-model-pill is-active" data-model="with">With model exam</button>
        <button type="button" class="ss-model-pill" data-model="without">Without model</button>
      </div>

      <div class="ss-mode-tabs" role="tablist" aria-label="Exam mode">
        <button type="button" class="ss-mode-tab is-active" data-mode="compare" role="tab" aria-selected="true">All options</button>
        <button type="button" class="ss-mode-tab" data-mode="direct" role="tab" aria-selected="false">Direct</button>
        <button type="button" class="ss-mode-tab" data-mode="online" role="tab" aria-selected="false">Online</button>
      </div>

      <div class="ss-option-grid">
        <article class="ss-option-card ss-mode-card ss-mode-card--direct" data-mode="direct" data-model="with">
          <span class="ss-option-card__badge ss-option-card__badge--model">With model</span>
          <div class="ss-mode-card__icon" aria-hidden="true"><i class="fas fa-building"></i></div>
          <h3>Direct · With model</h3>
          <p class="ss-mode-card__tag">Chennai centre</p>
          <p>Write at PradhiCA with subject-wise tests plus a full-syllabus model exam bundled in.</p>
          <ul class="ss-mode-card__list">
            <li><i class="fas fa-check" aria-hidden="true"></i> Physical hall in West Mambalam</li>
            <li><i class="fas fa-check" aria-hidden="true"></i> From ₹{d_w_p} per paper (excl. GST)</li>
          </ul>
          <a class="ss-mode-card__btn" href="{d_w}"><i class="fas fa-credit-card" aria-hidden="true"></i> View pricing</a>
        </article>
        <article class="ss-option-card ss-mode-card ss-mode-card--direct" data-mode="direct" data-model="without">
          <span class="ss-option-card__badge ss-option-card__badge--plain">Without model</span>
          <div class="ss-mode-card__icon" aria-hidden="true"><i class="fas fa-building"></i></div>
          <h3>Direct · Without model</h3>
          <p class="ss-mode-card__tag">Chennai centre</p>
          <p>Subject-wise tests only at the centre. Best when you want focused paper practice.</p>
          <ul class="ss-mode-card__list">
            <li><i class="fas fa-check" aria-hidden="true"></i> Supervised exam environment</li>
            <li><i class="fas fa-check" aria-hidden="true"></i> From ₹{d_wm_p} per paper (excl. GST)</li>
          </ul>
          <a class="ss-mode-card__btn" href="{d_wm}"><i class="fas fa-credit-card" aria-hidden="true"></i> View pricing</a>
        </article>
        <article class="ss-option-card ss-mode-card ss-mode-card--online" data-mode="online" data-model="with">
          <span class="ss-option-card__badge ss-option-card__badge--model">With model</span>
          <div class="ss-mode-card__icon" aria-hidden="true"><i class="fas fa-laptop"></i></div>
          <h3>Online · With model</h3>
          <p class="ss-mode-card__tag">India-wide</p>
          <p>Upload scanned answers from home. Model exam included with your subject selection.</p>
          <ul class="ss-mode-card__list">
            <li><i class="fas fa-check" aria-hidden="true"></i> Write from any city</li>
            <li><i class="fas fa-check" aria-hidden="true"></i> From ₹{o_w_p} per paper (excl. GST)</li>
          </ul>
          <a class="ss-mode-card__btn" href="{o_w}"><i class="fas fa-credit-card" aria-hidden="true"></i> View pricing</a>
        </article>
        <article class="ss-option-card ss-mode-card ss-mode-card--online" data-mode="online" data-model="without">
          <span class="ss-option-card__badge ss-option-card__badge--plain">Without model</span>
          <div class="ss-mode-card__icon" aria-hidden="true"><i class="fas fa-laptop"></i></div>
          <h3>Online · Without model</h3>
          <p class="ss-mode-card__tag">Razorpay secure</p>
          <p>Lowest per-paper rates for subject-only practice with the same CA evaluation team.</p>
          <ul class="ss-mode-card__list">
            <li><i class="fas fa-check" aria-hidden="true"></i> Flexible home timing</li>
            <li><i class="fas fa-check" aria-hidden="true"></i> From ₹{o_wm_p} per paper (excl. GST)</li>
          </ul>
          <a class="ss-mode-card__btn" href="{o_wm}"><i class="fas fa-credit-card" aria-hidden="true"></i> View pricing</a>
        </article>
      </div>

      <div class="ss-bento">
        <div class="ss-bento__cell ss-bento__cell--accent">
          <i class="fas fa-bullseye" aria-hidden="true"></i>
          <h4>Target weak papers</h4>
          <p>Buy one subject, two papers, a full group, or both groups. Pay only for what you need.</p>
        </div>
        <div class="ss-bento__cell">
          <i class="fas fa-percentage" aria-hidden="true"></i>
          <h4>20% group concession</h4>
          <p>Group I, Group II, or both groups qualify for automatic concession on the fee.</p>
        </div>
        <div class="ss-bento__cell">
          <i class="fas fa-file-signature" aria-hidden="true"></i>
          <h4>CA-evaluated copies</h4>
          <p>Detailed feedback and suggested answers within four working days of submission.</p>
        </div>
      </div>

      <div class="ss-faq">
        <h3>Common questions</h3>
        <div class="ss-faq__item">
          <button type="button" class="ss-faq__trigger" aria-expanded="false">What is Single Subject? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
          <div class="ss-faq__body"><p>Mock tests for individual {lead_level} papers instead of a fixed full-series schedule. You choose how many subjects or groups to cover.</p></div>
        </div>
        <div class="ss-faq__item">
          <button type="button" class="ss-faq__trigger" aria-expanded="false">Should I pick with or without model? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
          <div class="ss-faq__body"><p>With model adds a full-syllabus practice exam to your plan. Without model is subject tests only at a lower fee.</p></div>
        </div>
        <div class="ss-faq__item">
          <button type="button" class="ss-faq__trigger" aria-expanded="false">Is GST included? <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
          <div class="ss-faq__body"><p>Listed fees are exclusive of GST @ 18%. The final amount appears on the Razorpay checkout screen before you pay.</p></div>
        </div>
      </div>

      <div class="ss-hub-bottom">
        <p>Not sure which tier fits your attempt? Tell us your groups and we will recommend a plan.</p>
        <div class="ss-hub-bottom__links">
          <a href="contact-us.html" class="ss-hub-link--dark"><i class="fas fa-phone-alt" aria-hidden="true"></i> Contact us</a>
          <a href="https://api.whatsapp.com/send?phone=918072653948&amp;text={wa_text}" class="ss-hub-link--wa" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> WhatsApp</a>
        </div>
      </div>
    </div>
  </main>

  <div class="ss-hub-sticky" role="navigation" aria-label="Quick links">
    <a href="{d_w}" class="ss-hub-sticky--outline">Direct</a>
    <a href="{o_w}" class="ss-hub-sticky--amber">Online</a>
  </div>
"""


def upgrade_file(path: Path) -> bool:
    text = path.read_text()
    if "rapid-revision-premium.css" in text or "single-subject-premium.css" in text:
        return False

    meta = parse_filename(path.name)
    head, _body_open, nav, footer = split_page(text)

    if meta["kind"] == "rr":
        css, js = "rapid-revision-premium.css", "rapid-revision-premium.js"
        if meta["product"] == "registration":
            body_class = "pg-rr-hub"
            content = rr_hub_content(meta)
        else:
            cards = extract_cards(text)
            if len(cards) < 4:
                raise ValueError(f"{path.name}: expected 4 pricing cards, got {len(cards)}")
            body_class = f"pg-single pg-rr-pay pg-rr-pay--{meta['mode']}"
            content = rr_payment_content(meta, cards)
    else:
        css, js = "single-subject-premium.css", "single-subject-premium.js"
        if meta["product"] == "registration":
            body_class = "pg-ss-hub"
            content = ss_hub_content(meta)
        else:
            cards = extract_cards(text)
            if len(cards) < 4:
                raise ValueError(f"{path.name}: expected 4 pricing cards, got {len(cards)}")
            body_class = f"pg-single pg-ss-pay pg-ss-pay--{meta['mode']}"
            content = ss_payment_content(meta, cards)

    head = fix_head(head, css)
    footer = fix_scripts(footer, js)
    out = head + f'<body class="{body_class}">' + nav + content + "\n" + footer
    path.write_text(out)
    return True


def main() -> None:
    upgraded = []
    for pattern in ("*rapid-revision*.html", "*single-subject*.html"):
        for path in sorted(ROOT.glob(pattern)):
            if path.name.endswith(".html") and upgrade_file(path):
                upgraded.append(path.name)
    print(f"Upgraded {len(upgraded)} files:")
    for name in upgraded:
        print(f"  - {name}")


if __name__ == "__main__":
    main()

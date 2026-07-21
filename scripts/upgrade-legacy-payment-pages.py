#!/usr/bin/env python3
"""Redesign legacy DOT Marathon, DOT 2.0, and Inter Model payment pages to premium UI."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800'
    '&family=Maven+Pro:wght@400;500;700&family=Work+Sans:wght@400;500;600&display=swap">'
)

RAZORPAY_SNIPPET = """<div class="razorpay-embed-btn" data-url="{url}" data-text="Proceed to Pay" data-color="#528FF0" data-size="large">
  <script>
    (function(){{
      var d=document; var x=!d.getElementById('razorpay-embed-btn-js')
      if(x){{ var s=d.createElement('script'); s.defer=!0;s.id='razorpay-embed-btn-js';
      s.src='https://cdn.razorpay.com/static/embed_btn/bundle.js';d.body.appendChild(s);}} else{{var rzp=window['__rzp__'];
      rzp && rzp.init && rzp.init()}}}})();
  </script>
</div>"""

STYLE_RE = re.compile(r"\s*<style>.*?</style>\s*", re.DOTALL)
NAV_END = re.compile(r"</nav>\s*", re.IGNORECASE)
FOOTER_START = re.compile(r"<footer class=\"site-footer\">")

MARATHON_REFS = {
    ("inter", "direct"): "ca-inter-dot-marathon-direct-sep-2026.html",
    ("inter", "online"): "ca-inter-dot-marathon-online-sep-2026.html",
    ("final", "direct"): "ca-final-dot-marathon-direct-nov-2026.html",
    ("final", "online"): "ca-final-dot-marathon-online-nov-2026.html",
}

DOT2_REFS = {
    "direct": "ca-final-dot-2-0-ii-nov-2026.html",
    "online": "ca-final-dot-2-0-i-nov-2026.html",
}

MODEL_REF = "ca-final-model-1-set-direct-nov-2026.html"

MARATHON_FILES = [
    "ca-final-dot-marathon-direct-may-2026.html",
    "ca-final-dot-marathon-online-may-2026.html",
    "ca-inter-dot-marathon-direct-may-2026.html",
    "ca-inter-dot-marathon-online-may-2026.html",
    "ca-foundation-dot-marathon-direct-jan-2026.html",
    "ca-foundation-dot-marathon-online-jan-2026.html",
]

DOT2_FILES = [
    "ca-final-dot-2-0-i-may-2026.html",
    "ca-final-dot-2-0-ii-may-2026.html",
    "ca-foundation-dot-2-direct-may-2026.html",
    "ca-foundation-dot-2-online-may-2026.html",
    "ca-foundation-dot-2-direct-sep-2026.html",
    "ca-foundation-dot-2-online-sep-2026.html",
    "ca-inter-dot-2-direct-may-2026.html",
    "ca-inter-dot-2-online-may-2026.html",
    "ca-inter-dot-2-direct-sep-2026.html",
    "ca-inter-dot-2-online-sep-2026.html",
]

MODEL_FILES = [
    "ca-inter-model-1-set-direct-may-2026.html",
    "ca-inter-model-1-set-online-may-2026.html",
    "ca-inter-model-2-set-direct-may-2026.html",
    "ca-inter-model-2-set-online-may-2026.html",
    "ca-inter-model-3-set-direct-may-2026.html",
    "ca-inter-model-3-set-online-may-2026.html",
]

PAGE_CONFIG = {
    # Marathon
    "ca-final-dot-marathon-direct-may-2026.html": {
        "type": "marathon", "level": "final", "mode": "direct", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-final-test-schedule-may-2026.html",
        "series": "ca-final-dot-marathon-series-may-2026.html",
        "switch": "ca-final-dot-marathon-online-may-2026.html",
        "level_label": "FINAL EXAM",
    },
    "ca-final-dot-marathon-online-may-2026.html": {
        "type": "marathon", "level": "final", "mode": "online", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-final-test-schedule-may-2026.html",
        "series": "ca-final-dot-marathon-series-may-2026.html",
        "switch": "ca-final-dot-marathon-direct-may-2026.html",
        "level_label": "FINAL EXAM",
    },
    "ca-inter-dot-marathon-direct-may-2026.html": {
        "type": "marathon", "level": "inter", "mode": "direct", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-inter-test-schedule-may-2026.html",
        "series": "ca-inter-dot-marathon-series-may-2026.html",
        "switch": "ca-inter-dot-marathon-online-may-2026.html",
        "level_label": "INTER EXAM",
    },
    "ca-inter-dot-marathon-online-may-2026.html": {
        "type": "marathon", "level": "inter", "mode": "online", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-inter-test-schedule-may-2026.html",
        "series": "ca-inter-dot-marathon-series-may-2026.html",
        "switch": "ca-inter-dot-marathon-direct-may-2026.html",
        "level_label": "INTER EXAM",
    },
    "ca-foundation-dot-marathon-direct-jan-2026.html": {
        "type": "marathon", "level": "foundation", "mode": "direct", "batch": "Jan 2026",
        "batch_short": "Jan 26", "schedule": "ca-foundation-test-schedule-may-2026.html",
        "series": "ca-foundation-dot-marathon-series-jan-2026.html",
        "switch": "ca-foundation-dot-marathon-online-jan-2026.html",
        "level_label": "FOUNDATION EXAM",
    },
    "ca-foundation-dot-marathon-online-jan-2026.html": {
        "type": "marathon", "level": "foundation", "mode": "online", "batch": "Jan 2026",
        "batch_short": "Jan 26", "schedule": "ca-foundation-test-schedule-may-2026.html",
        "series": "ca-foundation-dot-marathon-series-jan-2026.html",
        "switch": "ca-foundation-dot-marathon-direct-jan-2026.html",
        "level_label": "FOUNDATION EXAM",
    },
    # DOT 2
    "ca-final-dot-2-0-i-may-2026.html": {
        "type": "dot2", "level": "final", "mode": "online", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-final-test-schedule-may-2026.html",
        "series": "ca-final-dot-2-series-may-2026.html",
        "switch": "ca-final-dot-2-0-ii-may-2026.html",
        "schedule_pdf": None,
        "level_label": "FINAL EXAM",
    },
    "ca-final-dot-2-0-ii-may-2026.html": {
        "type": "dot2", "level": "final", "mode": "direct", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-final-test-schedule-may-2026.html",
        "series": "ca-final-dot-2-series-may-2026.html",
        "switch": "ca-final-dot-2-0-i-may-2026.html",
        "schedule_pdf": None,
        "level_label": "FINAL EXAM",
    },
    "ca-foundation-dot-2-direct-may-2026.html": {
        "type": "dot2", "level": "foundation", "mode": "direct", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-foundation-test-schedule-may-2026.html",
        "series": "ca-foundation-dot-2-series-may-2026.html",
        "switch": "ca-foundation-dot-2-online-may-2026.html",
        "schedule_pdf": None,
        "level_label": "FOUNDATION EXAM",
    },
    "ca-foundation-dot-2-online-may-2026.html": {
        "type": "dot2", "level": "foundation", "mode": "online", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-foundation-test-schedule-may-2026.html",
        "series": "ca-foundation-dot-2-series-may-2026.html",
        "switch": "ca-foundation-dot-2-direct-may-2026.html",
        "schedule_pdf": None,
        "level_label": "FOUNDATION EXAM",
    },
    "ca-foundation-dot-2-direct-sep-2026.html": {
        "type": "dot2", "level": "foundation", "mode": "direct", "batch": "Sep 2026",
        "batch_short": "Sep 26", "schedule": "ca-foundation-test-schedule-sep-2026.html",
        "series": "ca-foundation-dot-2-series-sep-2026.html",
        "switch": "ca-foundation-dot-2-online-sep-2026.html",
        "schedule_pdf": "Schedules_2026/PradhiCA-CA Foundation-DOT3.0-Sep26-Schedule.pdf",
        "level_label": "FOUNDATION EXAM",
    },
    "ca-foundation-dot-2-online-sep-2026.html": {
        "type": "dot2", "level": "foundation", "mode": "online", "batch": "Sep 2026",
        "batch_short": "Sep 26", "schedule": "ca-foundation-test-schedule-sep-2026.html",
        "series": "ca-foundation-dot-2-series-sep-2026.html",
        "switch": "ca-foundation-dot-2-direct-sep-2026.html",
        "schedule_pdf": "Schedules_2026/PradhiCA-CA Foundation-DOT3.0-Sep26-Schedule.pdf",
        "level_label": "FOUNDATION EXAM",
    },
    "ca-inter-dot-2-direct-may-2026.html": {
        "type": "dot2", "level": "inter", "mode": "direct", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-inter-test-schedule-may-2026.html",
        "series": "ca-inter-dot-2-series-may-2026.html",
        "switch": "ca-inter-dot-2-online-may-2026.html",
        "schedule_pdf": None,
        "level_label": "INTER EXAM",
    },
    "ca-inter-dot-2-online-may-2026.html": {
        "type": "dot2", "level": "inter", "mode": "online", "batch": "May 2026",
        "batch_short": "May 26", "schedule": "ca-inter-test-schedule-may-2026.html",
        "series": "ca-inter-dot-2-series-may-2026.html",
        "switch": "ca-inter-dot-2-direct-may-2026.html",
        "schedule_pdf": None,
        "level_label": "INTER EXAM",
    },
    "ca-inter-dot-2-direct-sep-2026.html": {
        "type": "dot2", "level": "inter", "mode": "direct", "batch": "Sep 2026",
        "batch_short": "Sep 26", "schedule": "ca-inter-test-schedule-sep-2026.html",
        "series": "ca-inter-dot-2-series-sep-2026.html",
        "switch": "ca-inter-dot-2-online-sep-2026.html",
        "schedule_pdf": "Schedules_2026/PradhiCA-CA Inter-DOT-2.O-Sep26-Schedule.pdf",
        "level_label": "INTER EXAM",
    },
    "ca-inter-dot-2-online-sep-2026.html": {
        "type": "dot2", "level": "inter", "mode": "online", "batch": "Sep 2026",
        "batch_short": "Sep 26", "schedule": "ca-inter-test-schedule-sep-2026.html",
        "series": "ca-inter-dot-2-series-sep-2026.html",
        "switch": "ca-inter-dot-2-direct-sep-2026.html",
        "schedule_pdf": "Schedules_2026/PradhiCA-CA Inter-DOT-2.O-Sep26-Schedule.pdf",
        "level_label": "INTER EXAM",
    },
}

for set_n in (1, 2, 3):
    for mode in ("direct", "online"):
        fname = f"ca-inter-model-{set_n}-set-{mode}-may-2026.html"
        PAGE_CONFIG[fname] = {
            "type": "model",
            "level": "inter",
            "mode": mode,
            "batch": "May 2026",
            "batch_short": "May 26",
            "schedule": "ca-inter-test-schedule-may-2026.html",
            "series": "ca-inter-model-registration-may-2026.html",
            "switch": f"ca-inter-model-{set_n}-set-{'online' if mode == 'direct' else 'direct'}-may-2026.html",
            "set_n": set_n,
            "set_label": {1: "1 set", 2: "2 sets", 3: "3 sets"}[set_n],
        }


def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def extract_cards(html: str) -> list[dict]:
    """Extract pricing cards from legacy #pricing section."""
    pricing = re.search(r'<section[^>]*id="pricing"[^>]*>(.*?)</section>', html, re.DOTALL)
    if not pricing:
        return []
    section = pricing.group(1)
    cards = []
    pattern = re.compile(
        r'<div class="col-md-4[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>',
        re.DOTALL,
    )
    for m in pattern.finditer(section):
        block = m.group(0)
        inner = m.group(1)
        h3_m = re.search(r"<h3[^>]*>(.*?)</h3>", inner, re.DOTALL)
        price_m = re.search(r"display-4[^>]*>\s*(₹[^<]+)", inner)
        url_m = re.search(r'data-url="([^"]+)"', inner)
        sub_m = re.search(r"display-4[^<]*</h2>\s*(.*?)\s*</div>", inner, re.DOTALL)
        if not (h3_m and price_m and url_m):
            continue
        subtitle = ""
        if sub_m:
            subtitle = sub_m.group(1).strip()
            if subtitle and not subtitle.startswith("<p"):
                subtitle = f"<p>{subtitle}</p>"
        featured = (
            "pg-price-col--featured" in block
            or 'badge-primary">Popular' in block
            or "badge-pill badge-primary" in block
        )
        cards.append({
            "title": clean_text(re.sub(r"<[^>]+>", "", h3_m.group(1))),
            "price": clean_text(price_m.group(1)),
            "subtitle": subtitle,
            "url": url_m.group(1),
            "featured": featured,
        })
    return cards


def extract_tiers(html: str) -> list[str]:
    pricing = re.search(r'<section[^>]*id="pricing"[^>]*>(.*?)</section>', html, re.DOTALL)
    if not pricing:
        return []
    tiers = []
    for m in re.finditer(
        r'<div class="col-12[^"]*"[^>]*>\s*<h4[^>]*>(.*?)</h4>',
        pricing.group(1),
        re.DOTALL,
    ):
        text = clean_text(re.sub(r"<[^>]+>", " ", m.group(1)))
        text = re.sub(r"\s+", " ", text).strip()
        if text and "features" not in text.lower():
            tiers.append(text)
    return tiers


def split_cards_by_tiers(cards: list[dict], tiers: list[str]) -> list[tuple[str | None, list[dict]]]:
    if not tiers:
        return [(None, cards)]
    per = len(cards) // len(tiers) if tiers else len(cards)
    if per == 0:
        return [(None, cards)]
    groups = []
    idx = 0
    for i, tier in enumerate(tiers):
        chunk = cards[idx : idx + per]
        idx += per
        groups.append((tier, chunk))
    if idx < len(cards):
        groups[-1] = (groups[-1][0], groups[-1][1] + cards[idx:])
    return groups


def normalize_tier_label(raw: str, level_label: str, product: str = "DOT") -> str:
    """Convert legacy tier header to premium pg-single__tier format."""
    upper = raw.upper()
    # Extract the colored portion after level name
    m = re.search(r"(DOT[^·]*|MODEL[^·]*)", upper)
    if m:
        accent = m.group(1).strip()
    else:
        accent = raw
    accent = accent.replace("  ", " ").strip()
    if product == "DOT2":
        accent = accent.replace("DOT 2.O", "DOT 2.0").replace("DOT 2.O", "DOT 2.0")
        if "WITHOUT" in accent and "MODEL" in accent:
            accent = "DOT 2.0 WITHOUT MODEL"
        elif "WITH 2" in accent or "2 MODEL" in accent:
            accent = "DOT 2.0 WITH 2 MODELS"
        elif "WITH MODEL" in accent or "WITH 1 MODEL" in accent:
            accent = "DOT 2.0 WITH 1 MODEL" if "FINAL" in level_label else "DOT 2.0 WITH MODEL"
    elif product == "MARATHON":
        if "WITHOUT" in accent:
            accent = "DOT WITHOUT MODEL"
        elif "WITH 1" in accent or ("WITH MODEL" in accent and "BOTH" not in accent and "2" not in accent):
            accent = "DOT WITH 1 MODEL"
        elif "WITH BOTH" in accent or "2 MODEL" in accent:
            accent = "DOT WITH BOTH MODELS"
        elif "JAN 26" in accent or "MARATHON" in accent:
            accent = "DOT MARATHON"
    return f'{level_label} · <span class="text-primary">{accent}</span>'


def marathon_price_card(card: dict, featured: bool) -> str:
    col_class = "col-md-4 mt-4 pg-price-col--featured" if featured else "col-md-4 mt-4"
    sub = card["subtitle"] or '<p class="mb-0 text-muted small">Exclusive of GST</p>'
    if "mb-0" not in sub and "text-muted" not in sub:
        sub = sub.replace("<p>", '<p class="mb-0 text-muted small">', 1)
    return f"""     <div class="{col_class}">
       <div class="card pg-price-card text-center height-100p mb-4">
         <div class="card-header border-bottom">
           <h3 class="mb-0">{card['title']}</h3>
         </div>
         <div class="card-header border-bottom py-5">
           <h2 class="mb-0 display-4 text-success">{card['price']}</h2>
           {sub}
         </div>
         <div class="card-footer">
     {RAZORPAY_SNIPPET.format(url=card['url'])}
         </div>
       </div>
     </div>"""


def marathon_pricing_html(cfg: dict, cards: list[dict], tiers: list[str]) -> str:
    mode = cfg["mode"]
    level = cfg["level"]
    level_label = cfg["level_label"]
    switch_icon = "fa-laptop" if mode == "direct" else "fa-building"
    switch_label = "Switch to Online" if mode == "direct" else "Switch to Direct"
    switch_icon_cls = "fa-laptop" if mode == "direct" else "fa-building"
    if mode == "direct":
        switch_icon_cls = "fa-laptop"
        switch_label = "Switch to Online"
    else:
        switch_icon_cls = "fa-building"
        switch_label = "Switch to Direct"

    hero_icon = "fa-map-marker-alt" if mode == "direct" else "fa-laptop"
    mode_name = "Direct" if mode == "direct" else "Online"
    level_name = {"final": "Final", "inter": "Inter", "foundation": "Foundation"}[level]
    pay_label = "Direct payment" if mode == "direct" else "Online payment"

    if mode == "direct":
        hero_sub = 'Secure payment for <strong>Chennai centre</strong> registration. All fees exclusive of GST @ 18% unless stated.'
        badge = '<span class="pg-pay-badge"><i class="fas fa-building"></i> Direct mode</span>'
        trust = """          <span class="pg-pay-trust__item"><i class="fas fa-check-circle"></i> ICAI-style papers &amp; timing</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle"></i> Evaluated by qualified CAs</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle"></i> Results within 4 days</span>"""
        footer_block = """     <div class="col-12 mt-5">
       <div class="pg-venue-block">
         <div class="pg-venue-block__inner">
           <p class="pg-venue-block__label mb-0">Direct mode — exam venue</p>
           <h3 class="pg-venue-block__title"><i class="fas fa-map-marker-alt"></i> Visit PradhiCA (Chennai centre)</h3>
           <p class="pg-venue-block__brand mb-0">PradhiCA</p>
           <p class="pg-venue-block__address">No: 20, <strong>1st floor</strong>, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu <strong>600033</strong></p>
           <a href="https://maps.app.goo.gl/3scL1jiJsRZxtvYd9" class="pg-venue-block__btn" target="_blank" rel="noopener noreferrer"><i class="fas fa-directions"></i>Open in Google Maps</a>
         </div>
       </div>
     </div>"""
        pointer_cls = "text-primary"
    else:
        hero_sub = 'Secure payment for <strong>online</strong> registration — write from home with the same evaluation quality. All fees exclusive of GST @ 18% unless stated.'
        badge = '<span class="pg-pay-badge"><i class="fas fa-wifi"></i> Online mode</span>'
        trust = """          <span class="pg-pay-trust__item"><i class="fas fa-check-circle"></i> Same CA evaluation standards</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle"></i> Flexible write-from-home schedule</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle"></i> Results within 4 days</span>"""
        footer_block = """     <div class="col-12 mt-5">
       <div class="pg-online-block">
         <div class="pg-online-block__inner">
           <p class="pg-online-block__label mb-0">After you pay</p>
           <h3 class="pg-online-block__title"><i class="fas fa-laptop-house"></i> Online access &amp; support</h3>
           <p class="pg-online-block__text">You will receive instructions to write from home with the same evaluation quality as centre mode. Questions? Call <a href="tel:+918072653948">+91 80726 53948</a> or send an enquiry — we help with batch fit and technical setup.</p>
           <a href="registration.html" class="pg-online-block__btn"><i class="fas fa-paper-plane"></i>Enquiry &amp; support</a>
         </div>
       </div>
     </div>"""
        pointer_cls = "text-info"

    product_name = "DOT Marathon"
    groups = split_cards_by_tiers(cards, tiers)
    if level == "foundation" and not tiers:
        groups = [(f"{level_label} · <span class=\"text-primary\">DOT MARATHON</span>", cards)]

    cards_html = ""
    for tier_label, group in groups:
        if tier_label:
            premium_tier = normalize_tier_label(tier_label, level_label, "MARATHON") if "<span" not in tier_label else tier_label
            cards_html += f"""     <div class="col-12 pg-single__tier text-center text-md-left">
       <h4>{premium_tier}</h4>
     </div>
"""
        # default featured: middle card in each group of 3
        for i, card in enumerate(group):
            featured = card["featured"] or (len(group) == 3 and i == 1)
            cards_html += marathon_price_card(card, featured) + "\n"

    return f"""<div class="pg-pay-hero">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-10 py-2">
        <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
          <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1"></i>Home</a></li>
          <li class="breadcrumb-item"><a href="{cfg['schedule']}">CA {level_name} {cfg['batch_short']}</a></li>
          <li class="breadcrumb-item"><a href="{cfg['series']}">{product_name}</a></li>
          <li class="breadcrumb-item active text-white" aria-current="page">{pay_label}</li>
        </ol>
        <h1><i class="fas {hero_icon} mr-2"></i>CA {level_name} {product_name} · {cfg['batch']} · {mode_name}</h1>
        <p class="pg-pay-sub mt-3 mb-2">{hero_sub}</p>
        {badge}
        <span class="pg-pay-badge"><i class="fas fa-shield-alt"></i> Razorpay</span>
        <div class="pg-pay-trust">
{trust}
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
            <a href="{cfg['series']}" class="btn btn-outline-primary btn-sm btn-link-back"><i class="fas fa-arrow-left mr-1"></i>Back to mode choice</a>
            <a href="{cfg['switch']}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas {switch_icon_cls} mr-1"></i>{switch_label}</a>
            <a href="{cfg['schedule']}" class="btn btn-outline-info btn-sm btn-link-back"><i class="fas fa-calendar-alt mr-1"></i>Full schedule</a>
          </div>
          <p class="text-muted small mb-0 mt-3"><i class="fas fa-hand-pointer {pointer_cls} mr-1"></i>Select your package below and pay securely via Razorpay.</p>
        </div>
      </div>
    </div>
    <div class="row align-items-center">
      <div class="col-12">
        <ul class="pg-single__features">
          <li><i class="ti-check"></i>Evaluated by Qualified CAs</li>
          <li><i class="ti-check"></i>Results within 4 days</li>
          <li><i class="ti-check"></i>Suggested answers after each exam</li>
          <li><i class="ti-check"></i>ICAI-aligned pattern and timing</li>
          <li><i class="ti-check"></i>Amendments and case-study coverage</li>
          <li><i class="ti-check"></i>Flexible scheduling options</li>
        </ul>
      </div>
{cards_html}{footer_block}

    </div>
  </div>
</section>
"""


def dot2_price_card(card: dict, featured: bool) -> str:
    col_class = "col-md-4 mt-4 pg-price-col--featured" if featured else "col-md-4 mt-4"
    sub = card["subtitle"] or '<p class="mb-0 text-muted small">Exclusive of GST</p>'
    if "mb-0" not in sub:
        sub = re.sub(r"<p([^>]*)>", r'<p class="mb-0 text-muted small"\1>', sub, count=1)
    return f"""     <div class="{col_class}">
       <div class="card pg-price-card text-center height-100p mb-4">
         <div class="card-header border-bottom">
           <h3 class="mb-0">{card['title']}</h3>
         </div>
         <div class="card-header border-bottom py-5">
           <h2 class="mb-0 display-4 text-success">{card['price']}</h2>
           {sub}
         </div>
         <div class="card-footer">
          {RAZORPAY_SNIPPET.format(url=card['url'])}
         </div>
       </div>
     </div>"""


def dot2_pricing_html(cfg: dict, cards: list[dict], tiers: list[str]) -> str:
    mode = cfg["mode"]
    level = cfg["level"]
    level_label = cfg["level_label"]
    level_name = {"final": "Final", "inter": "Inter", "foundation": "Foundation"}[level]
    mode_name = "Direct" if mode == "direct" else "Online"
    pay_label = "Direct payment" if mode == "direct" else "Online payment"
    hero_icon = "fa-map-marker-alt" if mode == "direct" else "fa-laptop"

    if mode == "direct":
        hero_sub = "Secure payment for <strong>Chennai centre</strong> registration. Sunday sessions at our exclusive centre. All fees exclusive of GST @ 18% unless stated."
        badge = '<span class="pg-pay-badge"><i class="fas fa-building" aria-hidden="true"></i> Direct mode</span>'
        switch_icon, switch_label = "fa-laptop", "Switch to Online"
        footer_block = """     <div class="col-12 mt-5">
       <div class="pg-venue-block">
         <div class="pg-venue-block__inner">
           <p class="pg-venue-block__label mb-0">Direct mode — exam venue</p>
           <h3 class="pg-venue-block__title"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> Visit PradhiCA (Chennai centre)</h3>
           <p class="pg-venue-block__brand mb-0">PradhiCA</p>
           <p class="pg-venue-block__address">No: 20, <strong>1st floor</strong>, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu <strong>600033</strong></p>
           <a href="https://maps.app.goo.gl/3scL1jiJsRZxtvYd9" class="pg-venue-block__btn" target="_blank" rel="noopener noreferrer"><i class="fas fa-directions" aria-hidden="true"></i>Open in Google Maps</a>
         </div>
       </div>
     </div>"""
    else:
        hero_sub = "Secure payment for <strong>online</strong> registration. Write from home with the same evaluation quality. All fees exclusive of GST @ 18% unless stated."
        badge = '<span class="pg-pay-badge"><i class="fas fa-wifi" aria-hidden="true"></i> Online mode</span>'
        switch_icon, switch_label = "fa-building", "Switch to Direct"
        footer_block = """     <div class="col-12 mt-5">
       <div class="pg-online-block">
         <div class="pg-online-block__inner">
           <p class="pg-online-block__label mb-0">After you pay</p>
           <h3 class="pg-online-block__title"><i class="fas fa-laptop-house" aria-hidden="true"></i> Online access &amp; support</h3>
           <p class="pg-online-block__text">You will receive instructions to write from home with the same evaluation quality as centre mode. Questions? Call <a href="tel:+918072653948">+91 80726 53948</a> or send an enquiry. We help with batch fit and technical setup.</p>
           <a href="registration.html" class="pg-online-block__btn"><i class="fas fa-paper-plane" aria-hidden="true"></i>Enquiry &amp; support</a>
         </div>
       </div>
     </div>"""

    schedule_btn = (
        f'<a href="{cfg["schedule_pdf"]}" class="btn btn-outline-info btn-sm btn-link-back" target="_blank" rel="noopener"><i class="fas fa-calendar-alt mr-1" aria-hidden="true"></i>View schedule</a>'
        if cfg.get("schedule_pdf")
        else f'<a href="{cfg["schedule"]}" class="btn btn-outline-info btn-sm btn-link-back"><i class="fas fa-calendar-alt mr-1" aria-hidden="true"></i>Full schedule</a>'
    )

    groups = split_cards_by_tiers(cards, tiers)
    if level == "foundation" and len(cards) == 3 and not tiers:
        groups = [(f'{level_label} · <span class="text-primary">DOT 2.0</span>', cards)]

    cards_html = ""
    for tier_label, group in groups:
        if tier_label:
            premium_tier = normalize_tier_label(tier_label, level_label, "DOT2")
            if "<span" in tier_label:
                premium_tier = tier_label
            cards_html += f"""     <div class="col-12 pg-single__tier text-center text-md-left">
       <h4>{premium_tier}</h4>
     </div>
"""
        for i, card in enumerate(group):
            featured = card["featured"] or (len(group) == 3 and i == 1)
            cards_html += dot2_price_card(card, featured) + "\n"

    features_extra = ""
    if level == "final":
        features_extra = "          <li><i class=\"fas fa-check\" aria-hidden=\"true\"></i>9 weekly tests + 2 revisions + 2 models</li>\n"
    check_icon = "fas fa-check" if level == "final" else "ti-check"

    return f"""<div class="pg-pay-hero">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-10 py-2">
        <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
          <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
          <li class="breadcrumb-item"><a href="{cfg['schedule']}">CA {level_name} {cfg['batch_short']}</a></li>
          <li class="breadcrumb-item"><a href="{cfg['series']}">DOT 2.0</a></li>
          <li class="breadcrumb-item active text-white" aria-current="page">{pay_label}</li>
        </ol>
        <h1><i class="fas {hero_icon} mr-2" aria-hidden="true"></i>CA {level_name} DOT 2.0 · {cfg['batch']} · {mode_name}</h1>
        <p class="pg-pay-sub mt-3 mb-2">{hero_sub}</p>
        {badge}
        <span class="pg-pay-badge"><i class="fas fa-shield-alt" aria-hidden="true"></i> Razorpay</span>
        <div class="pg-pay-trust">
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-style papers &amp; timing</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> Evaluated by qualified CAs</span>
          <span class="pg-pay-trust__item"><i class="fas fa-check-circle" aria-hidden="true"></i> Results within 4 days</span>
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
            <a href="{cfg['series']}" class="btn btn-outline-primary btn-sm btn-link-back"><i class="fas fa-arrow-left mr-1" aria-hidden="true"></i>Back to mode choice</a>
            <a href="{cfg['switch']}" class="btn btn-outline-secondary btn-sm btn-link-back"><i class="fas {switch_icon} mr-1" aria-hidden="true"></i>{switch_label}</a>
            {schedule_btn}
          </div>
          <p class="text-muted small mb-0 mt-3"><i class="fas fa-hand-pointer text-primary mr-1" aria-hidden="true"></i>Select your package below and pay securely via Razorpay.</p>
        </div>
      </div>
    </div>
    <div class="row align-items-stretch">
      <div class="col-12">
        <ul class="pg-single__features">
          <li><i class="{check_icon}" aria-hidden="true"></i>Evaluated by qualified CAs</li>
          <li><i class="{check_icon}" aria-hidden="true"></i>Results within 4 days</li>
          <li><i class="{check_icon}" aria-hidden="true"></i>Suggested answers after each exam</li>
          <li><i class="{check_icon}" aria-hidden="true"></i>ICAI 70:30 pattern and timing</li>
          <li><i class="{check_icon}" aria-hidden="true"></i>Amendments and case-study coverage</li>
{features_extra}        </ul>
      </div>
{cards_html}{footer_block}
    </div>
  </div>
</section>
"""


MODEL_TIER_MAP = {
    "1 - PAPER": ("1paper", "Starter", "badge-secondary"),
    "1- PAPER": ("1paper", "Starter", "badge-secondary"),
    "2 - PAPER": ("2paper", "Value", "badge-info"),
    "2- PAPER": ("2paper", "Value", "badge-info"),
    "GROUP 1/2": ("group", "Popular", "badge-primary"),
    "BOTH - GROUPS": ("both", "Best Value", "badge-success"),
    "BOTH-GROUPS": ("both", "Best Value", "badge-success"),
}


def model_price_card(card: dict) -> str:
    title_key = card["title"].upper().replace("  ", " ")
    tier_id, badge_label, badge_cls = MODEL_TIER_MAP.get(
        title_key, ("1paper", "", "badge-secondary")
    )
    popular = tier_id == "group"
    card_cls = "model-price-card model-price-card--popular" if popular else "model-price-card"
    badge_html = f'<span class="badge badge-pill {badge_cls}">{badge_label}</span>' if badge_label else ""
    sub = card["subtitle"] or '<p class="mb-0 text-muted small">Exclusive of GST</p>'
    return f"""            <div class="{card_cls}" id="tier-{tier_id}">
              <div class="card border border-light mb-0 shadow-v3 text-center height-100p">
                <div class="card-header border-bottom d-flex justify-content-between align-items-center">
                  <h3 class="mb-0">{card['title']}</h3>
                  {badge_html}
                </div>
                <div class="card-header border-bottom py-5">
                  <h2 class="mb-0 display-4 text-success">{card['price']}</h2>
                  {sub}
                </div>
                <div class="card-footer">
          {RAZORPAY_SNIPPET.format(url=card['url'])}
                </div>
              </div>
            </div>"""


def model_pricing_html(cfg: dict, cards: list[dict]) -> str:
    mode = cfg["mode"]
    set_n = cfg["set_n"]
    set_label = cfg["set_label"]
    mode_name = "Direct" if mode == "direct" else "Online"
    hero_icon = "fa-building" if mode == "direct" else "fa-laptop"
    body_set = f"set{set_n}"

    if mode == "direct":
        lead = f"Secure checkout for <strong>Chennai centre</strong> model exams with <strong>{set_label}</strong> — pick paper count or group bundles below."
        pricing_desc = f"Pay at our Chennai centre. Full-syllabus ICAI-pattern mocks with {set_label} included."
        venue = """          <div class="pg-venue-block">
            <div class="pg-venue-block__inner">
              <p class="pg-venue-block__label mb-0">Direct mode · exam venue</p>
              <h3 class="pg-venue-block__title"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> PradhiCA Chennai centre</h3>
              <p class="pg-venue-block__brand mb-0">PradhiCA</p>
              <p class="pg-venue-block__address">No: 20, <strong>1st floor</strong>, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu <strong>600033</strong></p>
              <a href="https://maps.app.goo.gl/3scL1jiJsRZxtvYd9" class="pg-venue-block__btn" target="_blank" rel="noopener noreferrer"><i class="fas fa-directions" aria-hidden="true"></i>Open in Google Maps</a>
            </div>
          </div>"""
        switch_icon, switch_label = "fa-laptop", "Switch to Online"
        block_title = f"Model Direct · <span class=\"text-primary\">{set_label}</span>"
        pricing_h2 = f"Select your Direct package · {set_label}"
    else:
        lead = f"Secure checkout for <strong>online</strong> model exams with <strong>{set_label}</strong> — write from home with CA evaluation."
        pricing_desc = f"India-wide online model mocks with {set_label}. Same evaluation standards as centre students."
        venue = """          <div class="pg-online-block">
            <div class="pg-online-block__inner">
              <p class="pg-online-block__label mb-0">After you pay</p>
              <h3 class="pg-online-block__title"><i class="fas fa-laptop-house" aria-hidden="true"></i> Online access &amp; support</h3>
              <p class="pg-online-block__text">You will receive instructions to write from home. Questions? Call <a href="tel:+918072653948">+91 80726 53948</a> or <a href="registration.html">send an enquiry</a>.</p>
              <a href="registration.html" class="pg-online-block__btn"><i class="fas fa-paper-plane" aria-hidden="true"></i>Enquiry &amp; support</a>
            </div>
          </div>"""
        switch_icon, switch_label = "fa-building", "Switch to Direct"
        block_title = f"Model Online · <span class=\"text-primary\">{set_label}</span>"
        pricing_h2 = f"Select your Online package · {set_label}"

    set_links = ""
    for n, label in ((1, "1 set"), (2, "2 sets"), (3, "3 sets")):
        href = f"ca-inter-model-{n}-set-{mode}-may-2026.html"
        active = " is-active" if n == set_n else ""
        current = ' aria-current="page"' if n == set_n else ""
        set_links += f'            <a href="{href}" class="model-set-switch__item{active}"{current}>{label}</a>\n'

    cards_html = "\n".join(model_price_card(c) for c in cards)

    return f"""  <header class="model-hero" aria-labelledby="model-product-h1">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10 py-2">
          <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
            <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
            <li class="breadcrumb-item"><a href="{cfg['schedule']}">CA Inter {cfg['batch_short']}</a></li>
            <li class="breadcrumb-item"><a href="{cfg['series']}">Model exams</a></li>
            <li class="breadcrumb-item active" aria-current="page">{mode_name} · {set_label}</li>
          </ol>
          <h1 id="model-product-h1"><i class="fas {hero_icon} mr-2" aria-hidden="true"></i>CA Inter Model Exam · {set_label} · {mode_name} · {cfg['batch']}</h1>
          <p class="lead">{lead}</p>
          <div class="model-hero__badges">
            <span class="model-badge"><i class="fas fa-calendar-alt" aria-hidden="true"></i> {cfg['batch']} batch</span>
            <span class="model-badge"><i class="fas fa-trophy" aria-hidden="true"></i> {set_label}</span>
            <span class="model-badge"><i class="fas fa-lock" aria-hidden="true"></i> Razorpay secure pay</span>
          </div>
          <div class="model-trust">
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-style pattern</span>
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> Suggested answers</span>
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> <a href="tel:+918072653948" class="model-trust__link">+91 80726 53948</a></span>
          </div>
        </div>
      </div>
    </div>
  </header>

  <section class="model-pricing pg-single" id="pricing">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-11">
          <div class="model-pricing__head">
            <div class="model-product-actions">
              <a href="{cfg['series']}" class="model-back-link"><i class="fas fa-arrow-left" aria-hidden="true"></i>Back to model options</a>
              <a href="{cfg['switch']}" class="model-product-actions__pill"><i class="fas {switch_icon}" aria-hidden="true"></i>{switch_label}</a>
              <a href="{cfg['schedule']}" class="model-product-actions__pill"><i class="fas fa-calendar-alt" aria-hidden="true"></i>Full schedule</a>
            </div>
            <h2>{pricing_h2}</h2>
            <p>{pricing_desc}</p>
          </div>

          <nav class="model-set-switch" aria-label="Model set count">
{set_links}          </nav>

          <div class="model-tier-pills" role="tablist" aria-label="Package size">
            <button type="button" class="model-tier-pill" data-tier="1paper" role="tab">1 Paper</button>
            <button type="button" class="model-tier-pill" data-tier="2paper" role="tab">2 Papers</button>
            <button type="button" class="model-tier-pill" data-tier="group" role="tab">Group 1 or 2</button>
            <button type="button" class="model-tier-pill" data-tier="both" role="tab">Both Groups</button>
          </div>

          <ul class="pg-single__features">
            <li><i class="fas fa-check" aria-hidden="true"></i>Evaluated by Qualified CAs</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>Results within 4 days</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>Suggested answers after each exam</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>ICAI-aligned pattern and timing</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>Amendments and case-study coverage</li>
            <li><i class="fas fa-check" aria-hidden="true"></i>Flexible scheduling options</li>
          </ul>

          <div class="model-price-block">
            <h3 class="model-price-block__title">{block_title}</h3>
          </div>
          <div class="model-price-grid">
{cards_html}
          </div>

{venue}

          <p class="model-pricing__note"><i class="fas fa-info-circle mr-1" aria-hidden="true"></i>GST as applicable · Need help? <a href="registration.html">Enquiry</a> or <a href="https://api.whatsapp.com/send?phone=918072653948">WhatsApp</a></p>
        </div>
      </div>
    </div>
  </section>

  <div class="model-product-sticky" role="navigation" aria-label="Quick links">
    <a href="#pricing" class="model-product-sticky--accent">View pricing</a>
    <a href="{cfg['schedule']}" class="model-product-sticky--outline">Full schedule</a>
  </div>
"""


def extract_head_before_style(html: str) -> str:
    m = re.search(r"(.*?)(?:\s*<style>|\s*<link rel=\"stylesheet\" href=\"assets/css/dot2|\s*<link rel=\"stylesheet\" href=\"assets/css/model)", html, re.DOTALL)
    return m.group(1) if m else html[: html.find("</head>")]


def extract_inline_style_from_ref(ref_html: str) -> str:
    m = STYLE_RE.search(ref_html)
    return m.group(0) if m else ""


def extract_head_tail(ref_html: str) -> str:
    """Everything in head after stylesheet links (ld+json etc)."""
    m = re.search(
        r"(</style>|dot2-payment-premium\.css\">|model-product-premium\.css\">)\s*(.*?</head>)",
        ref_html,
        re.DOTALL,
    )
    return m.group(2) if m else "</head>"


def patch_head(legacy_html: str, ref_html: str, page_type: str) -> str:
    """Build head: keep legacy meta/title, use reference styles."""
    head_start = re.search(r".*?<head>\s*", legacy_html, re.DOTALL).group(0)
    # Standard link block from reference
    links_m = re.search(
        r"(<!--Google fonts-->.*?)(?:<style>|dot2-payment-premium|model-product-premium)",
        ref_html,
        re.DOTALL,
    )
    links = links_m.group(1) if links_m else ""

    if page_type == "marathon":
        style = extract_inline_style_from_ref(ref_html)
        tail_m = re.search(r"</style>\s*(.*?</head>)", ref_html, re.DOTALL)
        tail = tail_m.group(1) if tail_m else "</head>"
    elif page_type == "dot2":
        style = ""
        tail = extract_head_tail(ref_html)
    else:
        style = ""
        tail = extract_head_tail(ref_html)

    # Fix font link in links block
    links = re.sub(
        r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css[^"]*">',
        FONT_LINK,
        links,
        count=1,
    )
    if "DM+Sans" not in links:
        links = links.replace("<!--Google fonts-->", f"<!--Google fonts-->\n    {FONT_LINK}\n")

    # Update canonical in tail from legacy
    canonical_m = re.search(r'<link rel="canonical" href="([^"]+)"', legacy_html)
    if canonical_m:
        canonical = canonical_m.group(1)
        tail = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="{canonical}"', tail)
        tail = re.sub(r'property="og:url" content="[^"]+"', f'property="og:url" content="{canonical}"', tail)
        tail = re.sub(r'name="twitter:url" content="[^"]+"', f'name="twitter:url" content="{canonical}"', tail)
        # Update ld+json url
        fname = canonical.rsplit("/", 1)[-1]
        tail = re.sub(
            r'"url": "https://pradhica\.com/[^#"]+#webpage"',
            f'"url": "https://pradhica.com/{fname}#webpage"',
            tail,
        )
        tail = re.sub(
            r'"@id": "https://pradhica\.com/[^#"]+#webpage"',
            f'"@id": "https://pradhica.com/{fname}#webpage"',
            tail,
        )

    # Keep legacy title block (first part of head after analytics)
    meta_part = re.search(
        r"(<!-- Title-->.*?)<!--Google fonts-->",
        legacy_html,
        re.DOTALL,
    )
    meta = meta_part.group(1) if meta_part else ""

    analytics = re.search(
        r"(<!-- Global site tag \(gtag\.js\).*?</script>\s*<script>.*?gtag\('config'.*?</script>\s*)",
        legacy_html,
        re.DOTALL,
    )
    if not analytics:
        analytics = re.search(
            r'(<script async src="https://www.googletagmanager.com/gtag/js[^"]*"></script>\s*)',
            legacy_html,
            re.DOTALL,
        )
    analytics_block = analytics.group(1) if analytics else ""

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
 {analytics_block}
    <meta charset="UTF-8">
    
{meta}
    <!--Google fonts-->
    {FONT_LINK}
    
    
    <!-- Icon fonts -->
    <link rel="stylesheet" href="assets/fonts/fontawesome/css/all.css">
    <link rel="stylesheet" href="assets/fonts/themify-icons/css/themify-icons.css">
    
    
    <!-- stylesheet-->    
    <link rel="stylesheet" href="assets/css/vendors.bundle.css">
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="assets/css/footer-premium.css">
    <link rel="stylesheet" href="assets/css/header-premium.css">
{('    <link rel="stylesheet" href="assets/css/dot2-payment-premium.css">' if page_type == 'dot2' else '')}
{('    <link rel="stylesheet" href="assets/css/model-product-premium.css">' if page_type == 'model' else '')}
{style}
{tail}"""


def extract_nav_and_before(html: str) -> str:
    m = re.search(r"(<body[^>]*>.*?</nav>\s*)", html, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else ""


def extract_footer_and_after(html: str) -> str:
    m = re.search(r"(<footer class=\"site-footer\">.*</html>)", html, re.DOTALL)
    if not m:
        return ""
    footer = m.group(1)
    if page_type_scripts_missing_model(footer):
        footer = footer.replace(
            '<script src="assets/js/scripts.js"></script>',
            '    <script src="assets/js/model-product-premium.js"></script>\n    <script src="assets/js/scripts.js"></script>',
        )
    return footer


def page_type_scripts_missing_model(footer: str) -> bool:
    return "model-product-premium.js" not in footer


def body_class_for(cfg: dict) -> str:
    t = cfg["type"]
    mode = cfg["mode"]
    if t == "marathon":
        return "pg-single pg-marathon-pay"
    if t == "dot2":
        return f"pg-single pg-dot2-pay pg-dot2-pay--{mode}"
    set_n = cfg["set_n"]
    return f"pg-model-product pg-model-product--{mode} pg-model-product--set{set_n}"


def upgrade_file(fname: str) -> list[str]:
    issues = []
    cfg = PAGE_CONFIG[fname]
    legacy_path = ROOT / fname
    legacy = legacy_path.read_text(encoding="utf-8")

    cards = extract_cards(legacy)
    if not cards:
        issues.append(f"No pricing cards extracted")
        return issues

    tiers = extract_tiers(legacy)

    if cfg["type"] == "marathon":
        level = cfg["level"]
        ref_key = (level, cfg["mode"]) if level != "foundation" else ("inter", cfg["mode"])
        ref = (ROOT / MARATHON_REFS[ref_key]).read_text(encoding="utf-8")
        main = marathon_pricing_html(cfg, cards, tiers)
        head = patch_head(legacy, ref, "marathon")
    elif cfg["type"] == "dot2":
        ref = (ROOT / DOT2_REFS[cfg["mode"]]).read_text(encoding="utf-8")
        main = dot2_pricing_html(cfg, cards, tiers)
        head = patch_head(legacy, ref, "dot2")
    else:
        ref = (ROOT / MODEL_REF).read_text(encoding="utf-8")
        main = model_pricing_html(cfg, cards)
        head = patch_head(legacy, ref, "model")

    nav = extract_nav_and_before(legacy)
    if not nav:
        nav = extract_nav_and_before(ref)
    nav = re.sub(r"<body[^>]*>", f'<body class="{body_class_for(cfg)}">', nav, count=1)

    footer = extract_footer_and_after(legacy)
    if cfg["type"] == "model" and "model-product-premium.js" not in footer:
        footer = footer.replace(
            '<script src="assets/js/scripts.js"></script>',
            '    <script src="assets/js/model-product-premium.js"></script>\n    <script src="assets/js/scripts.js"></script>',
        )

    out = head + "\n  \n" + nav + main + "\n\n" + footer
    legacy_path.write_text(out, encoding="utf-8")
    return issues


def main():
    all_files = MARATHON_FILES + DOT2_FILES + MODEL_FILES
    done = []
    all_issues = {}
    for fname in all_files:
        if fname not in PAGE_CONFIG:
            all_issues[fname] = ["Missing PAGE_CONFIG"]
            continue
        issues = upgrade_file(fname)
        if issues:
            all_issues[fname] = issues
        else:
            done.append(fname)
        print(f"{'OK' if not issues else 'WARN'}: {fname}" + (f" — {issues}" if issues else ""))

    print(f"\nCompleted: {len(done)}/{len(all_files)}")
    if all_issues:
        print("Issues:")
        for f, iss in all_issues.items():
            print(f"  {f}: {iss}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Upgrade CA Final ABC HTML pages with premium UI assets."""
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

PRODUCT_PAGES = {
    "ca-final-abc-direct-nov-2026.html": {
        "batch": "Nov 2026",
        "batch_slug": "nov-2026",
        "schedule": "ca-final-test-schedule-nov-2026.html",
        "series": "ca-final-abc-series-nov-2026.html",
        "mode": "direct",
        "page_label": "ABC Direct · Registration",
        "h1": "CA Final ABC Direct · Nov 2026",
        "lead": "Secure checkout for <strong>Chennai centre</strong> ABC papers — choose <strong>with or without model</strong> packages below. All fees exclusive of GST.",
        "pricing_title": "Select your Direct package",
        "pricing_desc": "Pay via Razorpay. Pick paper count or group bundles — separate blocks for ABC-only and ABC + model.",
        "sticky_schedule": "ca-final-test-schedule-nov-2026.html",
        "dual_section": True,
    },
    "ca-final-abc-direct-may-2027.html": {
        "batch": "May 2027",
        "batch_slug": "may-2027",
        "schedule": "ca-final-test-schedule-may-2027.html",
        "series": "ca-final-abc-series-may-2027.html",
        "mode": "direct",
        "page_label": "ABC Direct · Registration",
        "h1": "CA Final ABC Direct · May 2027",
        "lead": "Secure checkout for <strong>Chennai centre</strong> ABC papers — choose <strong>with or without model</strong> packages below. All fees exclusive of GST.",
        "pricing_title": "Select your Direct package",
        "pricing_desc": "Pay via Razorpay. Pick paper count or group bundles — separate blocks for ABC-only and ABC + model.",
        "sticky_schedule": "ca-final-test-schedule-may-2027.html",
        "dual_section": True,
    },
    "ca-final-abc-direct-with-model-nov-2026.html": {
        "batch": "Nov 2026",
        "batch_slug": "nov-2026",
        "schedule": "ca-final-test-schedule-nov-2026.html",
        "series": "ca-final-abc-series-nov-2026.html",
        "mode": "direct",
        "page_label": "ABC Direct · With model",
        "h1": "CA Final ABC + Model · Direct · Nov 2026",
        "lead": "Chennai centre registration for <strong>ABC test series with model examinations</strong>. Bundled concessions on ABC and model fees.",
        "pricing_title": "ABC + Model · Direct pricing",
        "pricing_desc": "Select group or paper-wise packages. Exclusive of GST unless noted on the card.",
        "sticky_schedule": "ca-final-test-schedule-nov-2026.html",
        "dual_section": False,
    },
    "ca-final-abc-direct-with-model-may-2027.html": {
        "batch": "May 2027",
        "batch_slug": "may-2027",
        "schedule": "ca-final-test-schedule-may-2027.html",
        "series": "ca-final-abc-series-may-2027.html",
        "mode": "direct",
        "page_label": "ABC Direct · With model",
        "h1": "CA Final ABC + Model · Direct · May 2027",
        "lead": "Chennai centre registration for <strong>ABC test series with model examinations</strong>. Bundled concessions on ABC and model fees.",
        "pricing_title": "ABC + Model · Direct pricing",
        "pricing_desc": "Select group or paper-wise packages. Exclusive of GST unless noted on the card.",
        "sticky_schedule": "ca-final-test-schedule-may-2027.html",
        "dual_section": False,
    },
    "ca-final-abc-online-nov-2026.html": {
        "batch": "Nov 2026",
        "batch_slug": "nov-2026",
        "schedule": "ca-final-test-schedule-nov-2026.html",
        "series": "ca-final-abc-series-nov-2026.html",
        "mode": "online",
        "page_label": "ABC Online · Registration",
        "h1": "CA Final ABC Online · Nov 2026",
        "lead": "Register for <strong>online ABC mock tests</strong> from anywhere in India — blocks below for <strong>with and without model</strong> papers.",
        "pricing_title": "Select your Online package",
        "pricing_desc": "Razorpay checkout. Choose ABC-only or ABC + model bundles to match your study plan.",
        "sticky_schedule": "ca-final-test-schedule-nov-2026.html",
        "dual_section": True,
    },
    "ca-final-abc-online-may-2027.html": {
        "batch": "May 2027",
        "batch_slug": "may-2027",
        "schedule": "ca-final-test-schedule-may-2027.html",
        "series": "ca-final-abc-series-may-2027.html",
        "mode": "online",
        "page_label": "ABC Online · Registration",
        "h1": "CA Final ABC Online · May 2027",
        "lead": "Register for <strong>online ABC mock tests</strong> from anywhere in India — blocks below for <strong>with and without model</strong> papers.",
        "pricing_title": "Select your Online package",
        "pricing_desc": "Razorpay checkout. Choose ABC-only or ABC + model bundles to match your study plan.",
        "sticky_schedule": "ca-final-test-schedule-may-2027.html",
        "dual_section": True,
    },
    "ca-final-abc-online-with-model-nov-2026.html": {
        "batch": "Nov 2026",
        "batch_slug": "nov-2026",
        "schedule": "ca-final-test-schedule-nov-2026.html",
        "series": "ca-final-abc-series-nov-2026.html",
        "mode": "online",
        "page_label": "ABC Online · With model",
        "h1": "CA Final ABC + Model · Online · Nov 2026",
        "lead": "India-wide <strong>online</strong> registration for ABC with <strong>model examinations</strong>. Same evaluation quality as Direct students.",
        "pricing_title": "ABC + Model · Online pricing",
        "pricing_desc": "Pick the package that fits your group or paper selection. Fees exclusive of GST.",
        "sticky_schedule": "ca-final-test-schedule-nov-2026.html",
        "dual_section": False,
    },
    "ca-final-abc-online-with-model-may-2027.html": {
        "batch": "May 2027",
        "batch_slug": "may-2027",
        "schedule": "ca-final-test-schedule-may-2027.html",
        "series": "ca-final-abc-series-may-2027.html",
        "mode": "online",
        "page_label": "ABC Online · With model",
        "h1": "CA Final ABC + Model · Online · May 2027",
        "lead": "India-wide <strong>online</strong> registration for ABC with <strong>model examinations</strong>. Same evaluation quality as Direct students.",
        "pricing_title": "ABC + Model · Online pricing",
        "pricing_desc": "Pick the package that fits your group or paper selection. Fees exclusive of GST.",
        "sticky_schedule": "ca-final-test-schedule-may-2027.html",
        "dual_section": False,
    },
}


def hero_html(cfg):
    mode_icon = "fa-laptop" if cfg["mode"] == "online" else "fa-building"
    return f"""  <header class="abc-hero" aria-labelledby="abc-product-h1">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-10 py-2">
          <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
            <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
            <li class="breadcrumb-item"><a href="{cfg['schedule']}">CA Final {cfg['batch']}</a></li>
            <li class="breadcrumb-item"><a href="{cfg['series']}">ABC Test Series</a></li>
            <li class="breadcrumb-item active" aria-current="page">{cfg['page_label']}</li>
          </ol>
          <h1 id="abc-product-h1"><i class="fas {mode_icon} mr-2" aria-hidden="true"></i>{cfg['h1']}</h1>
          <p class="lead mt-3 mb-3">{cfg['lead']}</p>
          <span class="abc-badge"><i class="fas fa-calendar-alt" aria-hidden="true"></i> {cfg['batch']} batch</span>
          <span class="abc-badge"><i class="fas fa-lock" aria-hidden="true"></i> Razorpay secure pay</span>
          <span class="abc-badge"><i class="fas fa-user-check" aria-hidden="true"></i> CA-evaluated papers</span>
          <div class="abc-trust">
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-style pattern</span>
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> Suggested answers</span>
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> <a href="tel:+918072653948" style="color:inherit">+91 80726 53948</a></span>
          </div>
        </div>
      </div>
    </div>
  </header>"""


def pricing_open(cfg):
    return f"""
  <section class="abc-pricing pg-single" id="pricing">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-11">
          <div class="abc-pricing__head">
            <a href="{cfg['series']}" class="btn btn-outline-primary abc-pricing__back"><i class="fas fa-arrow-left" aria-hidden="true"></i> Back to ABC options</a>
            <h2>{cfg['pricing_title']}</h2>
            <p>{cfg['pricing_desc']}</p>
          </div>"""


def sticky_html(cfg):
    return f"""
  <div class="abc-product-sticky" role="navigation" aria-label="Quick links">
    <a href="#pricing" class="abc-product-sticky--gold">View pricing</a>
    <a href="{cfg['sticky_schedule']}" class="abc-product-sticky--outline">Full schedule</a>
  </div>"""


def upgrade_product(path: Path, cfg: dict):
    text = path.read_text(encoding="utf-8")
    fname = path.name
    canonical = f"https://pradhica.com/{fname}"

    text = STYLE_RE.sub("\n", text)

    if "abc-series-hub-premium.css" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="assets/css/header-premium.css">',
            '<link rel="stylesheet" href="assets/css/header-premium.css">\n' + CSS_LINKS,
        )

    if "DM+Sans" not in text:
        text = re.sub(
            r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css[^"]*">',
            FONT_LINK,
            text,
            count=1,
        )

    body_class = f'pg-abc-home pg-abc-home--final pg-abc-product pg-abc-product--{cfg["mode"]}'
    text = re.sub(r"<body[^>]*>", f'<body class="{body_class}">', text, count=1)

    text = re.sub(r'property="og:url" content="[^"]+"', f'property="og:url" content="{canonical}"', text)
    text = re.sub(r'name="twitter:url" content="[^"]+"', f'name="twitter:url" content="{canonical}"', text)
    text = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="{canonical}"', text)

    hero = hero_html(cfg)
    text = re.sub(
        r"<!-- END site-search-->.*?(?=<section class=\"padding-y-100|<section class=\"abc-pricing)",
        "<!-- END site-search-->\n\n" + hero + "\n",
        text,
        count=1,
        flags=re.DOTALL,
    )

    text = text.replace(
        '<section class="padding-y-100 border-bottom border-light pg-single" id="pricing">',
        pricing_open(cfg),
    )
    text = text.replace(
        '<section class="padding-y-100 border-bottom border-light pg-single" id="pricing">',
        pricing_open(cfg),
    )

    # First section header -> features only
    text = re.sub(
        r'<div class="row align-items-center">\s*<div class="col-12 text-center mb-3">\s*<h4>[^<]+</h4>\s*</div>\s*<div class="col-12">',
        '<div class="row align-items-center"><div class="col-12">',
        text,
        count=1,
    )

    # Subsection headers
    text = re.sub(
        r'<div class="col-12 text-center mb-3">\s*<h4>(ABC (?:DIRECT|ONLINE)[^<]*)</h4>\s*</div>',
        r'<div class="col-12 abc-price-block"><h3 class="abc-price-block__title">\1</h3></div>\n     <div class="col-12"><div class="row abc-price-grid">',
        text,
        flags=re.IGNORECASE,
    )

    # Wrap price cards: col-md-4 after grid open - close grid before next block or footer
    if "abc-price-grid" in text and "</div>\n     </div>\n     \n     <div class=\"col-md-4" not in text:
        pass

    # Close price grids before next abc-price-block or before footer section end
    text = re.sub(
        r'(</div>\s*</div>\s*</div>\s*)\n(\s*<div class="col-12 abc-price-block")',
        r"\1\n     </div></div>\n\2",
        text,
    )

    # Fix hhttps typo in may-2027 with-model
    text = text.replace("hhttps://", "https://")

    if "abc-product-sticky" not in text:
        text = text.replace(
            "\n<footer class=\"site-footer\">",
            sticky_html(cfg) + "\n\n<footer class=\"site-footer\">",
        )

    if "abc-pricing__note" not in text:
        note = (
            '          <p class="abc-pricing__note"><i class="fas fa-info-circle mr-1"></i>'
            "GST as applicable · Need help? "
            '<a href="registration.html">Enquiry</a> or '
            '<a href="https://api.whatsapp.com/send?phone=918072653948">WhatsApp</a></p>\n'
        )
        text = text.replace(
            "\n  </div> <!-- END container-->\n</section>",
            "\n" + note + "  </div> <!-- END container-->\n</section>",
            1,
        )

    path.write_text(text, encoding="utf-8")
    print(f"Upgraded product: {fname}")


def upgrade_series_may_2027():
    """Apply hub UI to may-2027 series page (2-card layout)."""
    path = ROOT / "ca-final-abc-series-may-2027.html"
    text = path.read_text(encoding="utf-8")
    fname = path.name
    canonical = f"https://pradhica.com/{fname}"

    if "abc-series-hub-premium.css" in text and "abc-hero" in text:
        print("Series may-2027 already upgraded")
        return

    text = text.replace(
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Maven+Pro:400,500,700%7CWork+Sans:400,500">',
        FONT_LINK,
    )
    if "abc-series-hub-premium.css" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="assets/css/header-premium.css">',
            '<link rel="stylesheet" href="assets/css/header-premium.css">\n'
            '    <link rel="stylesheet" href="assets/css/abc-series-hub-premium.css">',
        )

    text = re.sub(r"<body[^>]*>", '<body class="pg-abc-home pg-abc-home--final">', text, count=1)

    for key in ["og:url", "twitter:url", "canonical"]:
        if key == "canonical":
            text = re.sub(r'(<link rel="canonical" href=")[^"]+', rf"\1{canonical}", text)
        else:
            tag = "property" if key == "og:url" else "name"
            text = re.sub(rf'({tag}="{key}" content=")[^"]+', rf"\1{canonical}", text)

    text = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="India\'s best CA Final ABC Test Series May 2027 batch. Premium ICAI-aligned mock tests with optional model exams. Online or Direct registration."',
        text,
        count=1,
    )

    old_main = re.search(
        r"<!-- END site-search-->.*?</section>",
        text,
        re.DOTALL,
    ).group(0)

    new_main = """<!-- END site-search-->

  <header class="abc-hero" aria-labelledby="abc-hero-h1">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-10 py-2">
          <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
            <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
            <li class="breadcrumb-item"><a href="ca-final-test-schedule-may-2027.html">CA Final May 27</a></li>
            <li class="breadcrumb-item active" aria-current="page">ABC Test Series</li>
          </ol>
          <h1 id="abc-hero-h1"><i class="fas fa-book-open mr-2" aria-hidden="true"></i>CA Final ABC Test Series · May 2027</h1>
          <p class="lead mt-3 mb-3">Structured mock tests for Final New Course with <strong>optional model papers</strong>. Choose <strong>Online</strong> (India-wide) or <strong>Direct</strong> at our Chennai centre.</p>
          <span class="abc-badge"><i class="fas fa-calendar-alt" aria-hidden="true"></i> May 2027 batch</span>
          <span class="abc-badge"><i class="fas fa-file-alt" aria-hidden="true"></i> With / without model</span>
          <span class="abc-badge"><i class="fas fa-user-check" aria-hidden="true"></i> Evaluated by qualified CAs</span>
          <div class="abc-trust">
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> ICAI-style timing &amp; pattern</span>
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> Suggested answers &amp; mentoring</span>
            <span><i class="fas fa-check-circle" aria-hidden="true"></i> Razorpay secure checkout</span>
          </div>
        </div>
      </div>
    </div>
  </header>

  <main class="abc-section" id="choose-abc">
    <div class="container">
      <div class="row justify-content-center mb-3">
        <div class="col-lg-10 text-center">
          <a href="ca-final-test-schedule-may-2027.html" class="btn btn-outline-primary rounded-pill px-4 mb-3"><i class="fas fa-arrow-left mr-2" aria-hidden="true"></i>Back to Final May 27 schedule</a>
          <h2 class="mb-2">Choose your ABC registration path</h2>
          <p class="text-muted mb-0" style="max-width:36rem;margin-left:auto;margin-right:auto;">Online from anywhere, or Direct at Chennai. Model options are on each product page.</p>
        </div>
      </div>
      <div class="row justify-content-center mb-4">
        <div class="col-lg-10">
          <ul class="abc-features">
            <li><i class="fas fa-check" aria-hidden="true"></i> Full syllabus &amp; amendment coverage</li>
            <li><i class="fas fa-check" aria-hidden="true"></i> Flexible schedules &amp; catch-up options</li>
            <li><i class="fas fa-check" aria-hidden="true"></i> Results &amp; feedback within days</li>
            <li><i class="fas fa-check" aria-hidden="true"></i> Enquiry: <a href="tel:+918072653948">+91 80726 53948</a></li>
          </ul>
        </div>
      </div>
      <div class="row justify-content-center align-items-stretch">
        <div class="col-md-5 col-lg-5 mb-4">
          <div class="abc-card">
            <div class="abc-card__head" style="background:linear-gradient(135deg,#1e3a8a,#2563eb);">
              <h3>ABC May 2027</h3>
              <span class="abc-mode"><i class="fas fa-laptop mr-1" aria-hidden="true"></i>Online · From home</span>
            </div>
            <div class="abc-card__body">
              <p>Attempt from anywhere with the same evaluation standards, suggested answers, and mentor support.</p>
            </div>
            <div class="abc-card__foot">
              <a href="ca-final-abc-online-may-2027.html" class="abc-btn abc-btn--blue"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Online</a>
            </div>
          </div>
        </div>
        <div class="col-md-5 col-lg-5 mb-4">
          <div class="abc-card" style="box-shadow:0 16px 50px rgba(217,119,6,.18);border:2px solid #fcd34d;">
            <div class="abc-card__head" style="background:linear-gradient(135deg,#0f766e,#14b8a6);">
              <h3>ABC May 2027</h3>
              <span class="abc-mode"><i class="fas fa-map-marker-alt mr-1" aria-hidden="true"></i>Direct · Chennai centre</span>
            </div>
            <div class="abc-card__body">
              <p>Write at PradhiCA Chennai with centre support. Choose packages with or without model on the next page.</p>
            </div>
            <div class="abc-card__foot">
              <a href="ca-final-abc-direct-may-2027.html" class="abc-btn abc-btn--teal"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Direct</a>
            </div>
          </div>
        </div>
      </div>
      <div class="abc-help">
        <p>Not sure which path fits? Message us with your attempt date.</p>
        <div class="abc-help__links">
          <a href="registration.html" class="reg-hub-link--dark abc-link--dark"><i class="fas fa-envelope" aria-hidden="true"></i> Send enquiry</a>
          <a href="https://api.whatsapp.com/send?phone=918072653948&amp;text=Hi%20PradhiCA%2C%20Final%20ABC%20May%202027%20—%20need%20help%20choosing." class="reg-hub-link--wa abc-link--wa" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> WhatsApp</a>
        </div>
      </div>
    </div>
  </main>

  <div class="abc-sticky" role="navigation" aria-label="Quick links">
    <a href="#choose-abc" class="abc-sticky--gold">Choose path</a>
    <a href="ca-final-test-schedule-may-2027.html" class="abc-sticky--outline">Schedule</a>
  </div>"""

    text = text.replace(old_main, new_main)
    path.write_text(text, encoding="utf-8")
    print("Upgraded series: ca-final-abc-series-may-2027.html")


def main():
    for fname, cfg in PRODUCT_PAGES.items():
        p = ROOT / fname
        if p.exists():
            upgrade_product(p, cfg)
    upgrade_series_may_2027()
    print("Done.")


if __name__ == "__main__":
    main()

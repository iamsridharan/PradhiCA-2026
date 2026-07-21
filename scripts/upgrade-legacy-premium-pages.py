#!/usr/bin/env python3
"""Upgrade legacy series hubs, test schedules, and utility pages to premium design."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "apply_global_header", ROOT / "scripts" / "apply-global-header.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
build_header = _mod.build_header

FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800'
    '&family=Maven+Pro:wght@400;500;600;700;800'
    '&family=Work+Sans:wght@400;500;600&display=swap">'
)

FOOTER_SCRIPTS = """<script>
  (function (w,i,d,g,e,t,s) {w[d] = w[d]||[];t= i.createElement(g);
    t.async=1;t.src=e;s=i.getElementsByTagName(g)[0];s.parentNode.insertBefore(t, s);
  })(window, document, '_gscq','script','//widgets.getsitecontrol.com/171724/script.js');
</script>
<div class="scroll-top">
  <i class="ti-angle-up"></i>
</div>
    <script src="assets/js/vendors.bundle.js"></script>
    <script src="assets/js/header-scroll.js"></script>
    <script src="assets/js/header-nav-dropdown.js"></script>
    <script src="assets/js/scripts.js"></script>"""

TAB_META = {
    "Tabsabc": ("ABC Series", "fa-star"),
    "Tabsdot": ("DOT Marathon", "fa-walking"),
    "Tabsdot1": ("DOT 2.0", "fa-bolt"),
    "Tabsdot2": ("DOT 2.0", "fa-bolt"),
    "Tabsdot3": ("DOT 3.0", "fa-rocket"),
    "Tabsdot6": ("DOT 3.0", "fa-rocket"),
    "Tabssingle2": ("Rapid Revision", "fa-fast-forward"),
    "Tabsrapid": ("Rapid Revision", "fa-fast-forward"),
    "Tabssingle": ("Subject-wise", "fa-book-open"),
    "Tabsmodel": ("Model Exam", "fa-trophy"),
}


def extract_block(text: str, start_pat: str, end_pat: str) -> str:
    m = re.search(start_pat, text, re.DOTALL | re.I)
    if not m:
        return ""
    start = m.end()
    em = re.search(end_pat, text[start:], re.DOTALL | re.I)
    if not em:
        return ""
    return text[start : start + em.start()]


def extract_head_meta(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    title = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', text, re.I)
    json_ld = re.search(
        r'<script type="application/ld\+json">(.*?)</script>', text, re.I | re.S
    )
    meta_chunk = extract_block(text, r"<head[^>]*>", r"</head>")
    return {
        "title": title.group(1).strip() if title else path.stem,
        "canonical": canonical.group(1) if canonical else f"https://pradhica.com/{path.name}",
        "meta_lines": [
            ln
            for ln in meta_chunk.splitlines()
            if re.search(
                r"<meta |<link rel=\"canonical\"|<!-- (Title|SEO|Advanced|Open Graph|Twitter|AI|Canonical|viewport|Favicon)",
                ln,
                re.I,
            )
            and "stylesheet" not in ln
            and "fonts.googleapis" not in ln
        ],
        "json_ld": json_ld.group(0) if json_ld else "",
        "gtag": extract_block(text, r"<!-- Global site tag", r"gtag\('config'"),
    }


def standard_head(path: Path, extra_css: list[str], body_open: str = "") -> str:
    meta = extract_head_meta(path)
    css_lines = "\n".join(
        f'    <link rel="stylesheet" href="assets/css/{c}">' for c in extra_css
    )
    meta_lines = "\n".join(f"    {ln.strip()}" for ln in meta["meta_lines"] if ln.strip())
    gtag = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-132037455-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-132037455-1');
</script>"""
    json_ld = f"\n    {meta['json_ld']}\n" if meta["json_ld"] else ""
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
{gtag}

    <meta charset="UTF-8">
{meta_lines}
    {FONT_LINK}
    <link rel="stylesheet" href="assets/fonts/fontawesome/css/all.css">
    <link rel="stylesheet" href="assets/fonts/themify-icons/css/themify-icons.css">
    <link rel="stylesheet" href="assets/css/vendors.bundle.css">
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="assets/css/footer-premium.css">
    <link rel="stylesheet" href="assets/css/header-premium.css">
{css_lines}
{json_ld}
</head>
{body_open}"""


def extract_footer(text: str) -> str:
    m = re.search(r"(<footer class=\"site-footer\">.*?</footer>\s*<!-- END site-footer -->)", text, re.S | re.I)
    if m:
        return m.group(1)
    m = re.search(r"(<footer class=\"site-footer\">.*?</footer>)", text, re.S | re.I)
    return m.group(1) if m else ""


# ─── ABC hub builders ───────────────────────────────────────────────────────

def abc_card_simple(cfg: dict) -> str:
    cards = cfg["cards"]
    online = next((c for c in cards if c["mode"] == "online"), cards[0])
    direct = next((c for c in cards if c["mode"] == "direct"), cards[-1])
    feat = direct.get("featured", True)
    return f"""      <div class="row justify-content-center align-items-stretch">
        <div class="col-md-5 col-lg-5 mb-4">
          <div class="abc-card">
            <div class="abc-card__head" style="background:linear-gradient(135deg,#1e3a8a,#2563eb);">
              <h3>{online['title']}</h3>
              <span class="abc-mode"><i class="fas fa-laptop mr-1" aria-hidden="true"></i>Online · From home</span>
            </div>
            <div class="abc-card__body">
              <p>{online.get('desc', 'Attempt from anywhere with the same evaluation standards, suggested answers, and mentor support.')}</p>
            </div>
            <div class="abc-card__foot">
              <a href="{online['href']}" class="abc-btn abc-btn--blue"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Online</a>
            </div>
          </div>
        </div>
        <div class="col-md-5 col-lg-5 mb-4">
          <div class="abc-card" style="{"box-shadow:0 16px 50px rgba(217,119,6,.18);border:2px solid #fcd34d;" if feat else ""}">
            <div class="abc-card__head" style="background:linear-gradient(135deg,#0f766e,#14b8a6);">
              <h3>{direct['title']}</h3>
              <span class="abc-mode"><i class="fas fa-map-marker-alt mr-1" aria-hidden="true"></i>Direct · Chennai centre</span>
            </div>
            <div class="abc-card__body">
              <p>{direct.get('desc', 'Write at PradhiCA Chennai with centre support. Choose packages with or without model on the next page.')}</p>
            </div>
            <div class="abc-card__foot">
              <a href="{direct['href']}" class="abc-btn abc-btn--teal"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Direct</a>
            </div>
          </div>
        </div>
      </div>"""


def abc_card_full(cfg: dict) -> str:
    """Four-card layout: online with/without model + direct with/without model."""
    c = {x["key"]: x for x in cfg["cards"]}
    return f"""          <div class="abc-group">
            <div class="abc-group__head">
              <i class="fas fa-laptop" aria-hidden="true"></i>
              <div class="abc-group__head-text">
                <h3>Online · Write from anywhere</h3>
                <p>Take the test at your own pace, whenever it fits your schedule.</p>
              </div>
            </div>
            <div class="abc-card-grid">
              <article class="abc-card abc-card--featured">
                <span class="abc-card__ribbon">Popular</span>
                <div class="abc-card__head">
                  <h4>ABC Online</h4>
                  <span class="abc-card__tag"><i class="fas fa-layer-group" aria-hidden="true"></i> With model exams</span>
                </div>
                <div class="abc-card__body">
                  <p>Full ABC test series plus dedicated model papers for exam-day simulation and deeper feedback.</p>
                </div>
                <div class="abc-card__foot">
                  <a href="{c['online_model']['href']}" class="abc-btn abc-btn--blue"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Online with model</a>
                </div>
              </article>
              <article class="abc-card">
                <div class="abc-card__head">
                  <h4>ABC Online</h4>
                  <span class="abc-card__tag"><i class="fas fa-file-alt" aria-hidden="true"></i> Without model exams</span>
                </div>
                <div class="abc-card__body">
                  <p>Core ABC mock tests only — ideal if you already have separate model papers or a lighter schedule.</p>
                </div>
                <div class="abc-card__foot">
                  <a href="{c['online']['href']}" class="abc-btn abc-btn--blue"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Online without model</a>
                </div>
              </article>
            </div>
          </div>
          <div class="abc-group abc-group--direct">
            <div class="abc-group__head">
              <i class="fas fa-building" aria-hidden="true"></i>
              <div class="abc-group__head-text">
                <h3>Direct · Chennai centre</h3>
                <p>Write at PradhiCA with centre support, invigilation, and on-campus mentoring.</p>
              </div>
            </div>
            <div class="abc-card-grid">
              <article class="abc-card abc-card--direct">
                <div class="abc-card__head">
                  <h4>ABC Direct</h4>
                  <span class="abc-card__tag"><i class="fas fa-layer-group" aria-hidden="true"></i> With model exams</span>
                </div>
                <div class="abc-card__body">
                  <p>Centre-based ABC series with model examinations — maximum structure before your attempt.</p>
                </div>
                <div class="abc-card__foot">
                  <a href="{c['direct_model']['href']}" class="abc-btn abc-btn--teal"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Direct with model</a>
                </div>
              </article>
              <article class="abc-card abc-card--direct">
                <div class="abc-card__head">
                  <h4>ABC Direct</h4>
                  <span class="abc-card__tag"><i class="fas fa-file-alt" aria-hidden="true"></i> Without model exams</span>
                </div>
                <div class="abc-card__body">
                  <p>Core ABC mock tests at our Chennai centre — choose paper count on the next page.</p>
                </div>
                <div class="abc-card__foot">
                  <a href="{c['direct']['href']}" class="abc-btn abc-btn--teal"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Direct without model</a>
                </div>
              </article>
            </div>
          </div>"""


def build_abc_hub(path: Path, cfg: dict) -> None:
    body_class = cfg.get("body_class", "pg-abc-home")
    cards_html = abc_card_full(cfg) if cfg.get("layout") == "full" else abc_card_simple(cfg)
    wa = cfg.get("whatsapp", "")
    header = build_header(path.name)
    footer = extract_footer(path.read_text(encoding="utf-8", errors="replace"))
    out = standard_head(path, ["abc-series-hub-premium.css"], f'  <body class="{body_class}">')
    out += "\n" + header + f"""
  <header class="abc-hero" aria-labelledby="abc-hero-h1">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10 py-2">
          <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
            <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
            <li class="breadcrumb-item"><a href="{cfg['schedule']}">{cfg['level_label']} {cfg['batch_short']}</a></li>
            <li class="breadcrumb-item active" aria-current="page">ABC Test Series</li>
          </ol>
          <h1 id="abc-hero-h1"><i class="fas fa-book-open mr-2" aria-hidden="true"></i>{cfg['h1']}</h1>
          <p class="lead">{cfg['lead']}</p>
          <div class="abc-hero__badges">
            <span class="abc-badge"><i class="fas fa-calendar-alt" aria-hidden="true"></i> {cfg['batch']} batch</span>
            <span class="abc-badge"><i class="fas fa-file-alt" aria-hidden="true"></i> With / without model</span>
            <span class="abc-badge"><i class="fas fa-user-check" aria-hidden="true"></i> Evaluated by qualified CAs</span>
          </div>
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
          <a href="{cfg['schedule']}" class="abc-back-link"><i class="fas fa-arrow-left" aria-hidden="true"></i>Back to {cfg['level_label']} {cfg['batch_short']} schedule</a>
          <h2 class="mb-2">Choose your ABC registration path</h2>
          <p class="abc-intro-note">{cfg.get('intro', 'Select Online or Direct, then pick with or without model on the next page.')}</p>
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
      <div class="row justify-content-center">
        <div class="col-lg-10">
{cards_html}
          <div class="abc-help">
            <p>Not sure which path fits? Tell us your attempt date and we'll suggest Online vs Direct and model options.</p>
            <div class="abc-help__links">
              <a href="registration.html" class="abc-link--dark"><i class="fas fa-envelope" aria-hidden="true"></i> Send enquiry</a>
              <a href="https://api.whatsapp.com/send?phone=918072653948&amp;text=Hi%20PradhiCA%2C%20{wa}" class="abc-link--wa" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> WhatsApp</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <div class="abc-sticky" role="navigation" aria-label="Quick links">
    <a href="#choose-abc" class="abc-sticky--gold">Choose path</a>
    <a href="{cfg['schedule']}" class="abc-sticky--outline">Schedule</a>
  </div>

"""
    out += footer + "\n" + FOOTER_SCRIPTS + "\n  </body>\n</html>\n"
    path.write_text(out, encoding="utf-8")
    print(f"ABC hub: {path.name}")


def build_dot2_hub(path: Path, cfg: dict) -> None:
    direct, online = cfg["direct"], cfg["online"]
    header = build_header(path.name)
    footer = extract_footer(path.read_text(encoding="utf-8", errors="replace"))
    pdf = cfg.get("pdf", "")
    pdf_line = f'<li><i class="fas fa-check" aria-hidden="true"></i> <a href="{pdf}" target="_blank" rel="noopener">View schedule PDF</a></li>' if pdf else ""
    out = standard_head(path, ["dot2-series-hub-premium.css"], '  <body class="pg-dot2-home">')
    out += "\n" + header + f"""
<header class="dot2-hero" aria-labelledby="dot2-hero-h1">
  <div class="container">
    <div class="col-lg-10 py-2">
      <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
        <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
        <li class="breadcrumb-item"><a href="{cfg['schedule']}">{cfg['level_label']} {cfg['batch_short']}</a></li>
        <li class="breadcrumb-item active" aria-current="page">DOT 2.0 Registration</li>
      </ol>
      <h1 id="dot2-hero-h1"><i class="fas fa-bolt mr-2" aria-hidden="true"></i>{cfg['h1']}</h1>
      <p class="lead">{cfg['lead']}</p>
      <span class="dot2-badge"><i class="fas fa-calendar-alt" aria-hidden="true"></i> {cfg['batch']} batch</span>
      <span class="dot2-badge"><i class="fas fa-certificate" aria-hidden="true"></i> ICAI 70:30 pattern</span>
      <div class="dot2-trust">
        <span><i class="fas fa-check-circle" aria-hidden="true"></i> Mentorship and follow-up</span>
        <span><i class="fas fa-check-circle" aria-hidden="true"></i> Suggested answers included</span>
        <span><i class="fas fa-check-circle" aria-hidden="true"></i> Razorpay secure checkout</span>
      </div>
    </div>
  </div>
</header>

<main class="dot2-section" id="choose-mode">
  <div class="container">
    <div class="row justify-content-center mb-3">
      <div class="col-lg-10 text-center">
        <a href="{cfg['schedule']}" class="btn btn-outline-primary rounded-pill px-4 mb-3"><i class="fas fa-arrow-left mr-2" aria-hidden="true"></i>Back to {cfg['level_label']} {cfg['batch_short']} schedule</a>
        <h2 class="mb-2">Choose your exam mode</h2>
        <p class="text-muted mb-0" style="max-width:36rem;margin-left:auto;margin-right:auto;">Same syllabus and evaluation — pick where you want to write.</p>
      </div>
    </div>
    <div class="row justify-content-center mb-4">
      <div class="col-lg-10">
        <ul class="dot2-features">
          <li><i class="fas fa-check" aria-hidden="true"></i> Both groups, one group, or 2 papers</li>
          {pdf_line}
          <li><i class="fas fa-check" aria-hidden="true"></i> Enquiry: <a href="tel:+918072653948">+91 80726 53948</a></li>
        </ul>
      </div>
    </div>
    <div class="dot2-card-grid">
      <article class="dot2-card">
        <div class="dot2-card__head">
          <h3>{cfg['card_title']}</h3>
          <span class="dot2-card__tag"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> Direct · Chennai centre</span>
        </div>
        <div class="dot2-card__body">
          <p>Write at our exclusive Chennai centre. Sunday sessions with flexible catch-up options.</p>
        </div>
        <div class="dot2-card__foot">
          <a href="{direct}" class="dot2-btn dot2-btn--indigo"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Direct</a>
        </div>
      </article>
      <article class="dot2-card dot2-card--online dot2-card--featured">
        <span class="dot2-card__ribbon">Popular</span>
        <div class="dot2-card__head">
          <h3>{cfg['card_title']}</h3>
          <span class="dot2-card__tag"><i class="fas fa-laptop" aria-hidden="true"></i> Online · From home</span>
        </div>
        <div class="dot2-card__body">
          <p>Attempt tests from anywhere with the same quality evaluation and mentoring support.</p>
        </div>
        <div class="dot2-card__foot">
          <a href="{online}" class="dot2-btn dot2-btn--teal"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Online</a>
        </div>
      </article>
    </div>
  </div>
</main>

"""
    out += footer + "\n" + FOOTER_SCRIPTS + "\n  </body>\n</html>\n"
    path.write_text(out, encoding="utf-8")
    print(f"DOT2 hub: {path.name}")


def build_marathon_hub(path: Path, cfg: dict) -> None:
    direct, online = cfg["direct"], cfg["online"]
    header = build_header(path.name)
    footer = extract_footer(path.read_text(encoding="utf-8", errors="replace"))
    out = standard_head(path, ["marathon-series-hub-premium.css"], '  <body class="pg-marathon-home">')
    out += "\n" + header + f"""
<div class="dm-hero" aria-labelledby="dm-hero-h1">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-10 py-2">
        <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3">
          <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-1" aria-hidden="true"></i>Home</a></li>
          <li class="breadcrumb-item"><a href="{cfg['schedule']}">{cfg['level_label']} {cfg['batch_short']}</a></li>
          <li class="breadcrumb-item active text-white" aria-current="page">DOT Marathon</li>
        </ol>
        <h1 id="dm-hero-h1"><i class="fas fa-running mr-2" aria-hidden="true"></i>{cfg['h1']}</h1>
        <p class="lead mt-3 mb-3">{cfg['lead']}</p>
        <span class="dm-badge"><i class="fas fa-calendar-alt" aria-hidden="true"></i> {cfg['batch']} batch</span>
        <span class="dm-badge"><i class="fas fa-certificate" aria-hidden="true"></i> ICAI 70:30 pattern</span>
        <span class="dm-badge"><i class="fas fa-headset" aria-hidden="true"></i> Mentorship &amp; follow-up</span>
      </div>
    </div>
  </div>
</div>

<section class="dm-section" id="choose-mode">
  <div class="container">
    <div class="row justify-content-center mb-4">
      <div class="col-lg-10 text-center">
        <a href="{cfg['schedule']}" class="dm-back-link"><i class="fas fa-arrow-left" aria-hidden="true"></i>Back to {cfg['level_label']} {cfg['batch_short']} schedule</a>
        <h2 class="mb-2">Choose your exam mode</h2>
        <p class="text-muted mb-0" style="max-width:32rem;margin-left:auto;margin-right:auto;">Same syllabus and evaluation — pick the option that suits where you want to write.</p>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-md-5 col-lg-4 mb-4 mb-md-0">
        <div class="dm-card">
          <div class="dm-card__head">
            <h3>{cfg['card_title']}</h3>
            <span class="dm-mode"><i class="fas fa-map-marker-alt mr-1"></i>Direct · Chennai centre</span>
          </div>
          <div class="dm-card__body">
            <p>Write at our exclusive Chennai centre. Sunday sessions with flexible catch-up options.</p>
          </div>
          <div class="dm-card__foot">
            <a href="{direct}" class="dm-btn"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Direct</a>
          </div>
        </div>
      </div>
      <div class="col-md-5 col-lg-4">
        <div class="dm-card dm-card--featured">
          <div class="dm-card__head dm-card__head--teal">
            <h3>{cfg['card_title']}</h3>
            <span class="dm-mode"><i class="fas fa-laptop mr-1"></i>Online · From home</span>
          </div>
          <div class="dm-card__body">
            <p>Attempt tests from anywhere with the same quality evaluation, suggested answers, and support as Direct mode.</p>
          </div>
          <div class="dm-card__foot">
            <a href="{online}" class="dm-btn dm-btn--teal"><i class="fas fa-user-plus" aria-hidden="true"></i>Register — Online</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="dm-sticky" role="navigation" aria-label="Quick links">
  <a href="#choose-mode" class="dm-sticky--gold">Choose mode</a>
  <a href="{cfg['schedule']}" class="dm-sticky--outline">Schedule</a>
</div>

"""
    out += footer + "\n" + FOOTER_SCRIPTS + "\n  </body>\n</html>\n"
    path.write_text(out, encoding="utf-8")
    print(f"Marathon hub: {path.name}")


# ─── Test schedule upgrade ───────────────────────────────────────────────────

def transform_feature_cards(html: str) -> str:
    if "ts-feature-bento" in html:
        return html

    def upgrade_pane(pane: str) -> str:
        if "ts-feature-bento" in pane or "feature-card" not in pane:
            return pane
        cards = re.findall(
            r'<div class="col-[^"]*">\s*<div class="feature-card">(.*?)</div>\s*</div>',
            pane,
            re.S,
        )
        if not cards:
            return pane
        bento = '<div class="ts-feature-bento">\n'
        for card in cards:
            bento += f'                <div class="ts-feature-card"><div class="ts-feature-card__inner feature-card">{card}</div></div>\n'
        bento += "              </div>"
        return re.sub(
            r'<div class="row">.*?</div>\s*</div>\s*<div class="action-buttons',
            bento + '\n            </div>\n            <div class="action-buttons',
            pane,
            count=1,
            flags=re.S,
        )

    parts = re.split(r'(<div class="tab-pane[^>]*>)', html)
    out = parts[0]
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            out += parts[i] + upgrade_pane(parts[i + 1])
    return out


def transform_action_buttons(html: str) -> str:
    if "ts-cta-strip" in html:
        return html

    def fix_pane(pane: str) -> str:
        links = re.findall(
            r'<a href="([^"]+)"[^>]*class="[^"]*action-btn[^"]*"[^>]*>.*?<i class="fas ([^"]+)"[^>]*></i>\s*([^<]+)</a>',
            pane,
            re.S,
        )
        if not links:
            links = re.findall(
                r'<a href="([^"]+)"[^>]*class="[^"]*action-btn[^"]*"[^>]*><i class="fas ([^"]+)"[^>]*></i>\s*([^<]+)</a>',
                pane,
                re.S,
            )
        if not links:
            return pane
        strip = '              <div class="ts-cta-strip">\n'
        for href, icon, label in links:
            cls = "action-btn"
            if "rupee" in icon or "Fee" in label:
                cls += " btn-fee"
            elif "calendar" in icon.lower() or "Schedule" in label or "Batch" in label:
                cls += " btn-schedule"
            strip += f'                <a href="{href}" target="_blank" rel="noopener noreferrer" class="{cls}"><i class="fas {icon}" aria-hidden="true"></i> {label.strip()}</a>\n'
        strip += "              </div>"
        return re.sub(
            r'<div class="action-buttons[^"]*">.*?<div class="row[^"]*">.*?</div>\s*</div>',
            f'<div class="action-buttons text-center">\n              <h4>Ready to Get Started?</h4>\n{strip}\n            </div>',
            pane,
            count=1,
            flags=re.S,
        )

    parts = re.split(r'(<div class="tab-pane[^>]*>)', html)
    out = parts[0]
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            out += parts[i] + fix_pane(parts[i + 1])
    return out


def extract_tab_ids(text: str) -> list[str]:
    ids = []
    for m in re.finditer(r'<div class="tab-pane[^>]*\bid="(Tabs[^"]+)"', text, re.I):
        tid = m.group(1)
        if tid not in ids:
            ids.append(tid)
    if ids:
        return ids
    for m in re.finditer(r'href="#(Tabs[^"]+)"', text):
        tid = m.group(1)
        if tid not in ids:
            ids.append(tid)
    return ids


def extract_tab_panes(text: str) -> str:
    pane_ids = extract_tab_ids(text)
    if not pane_ids:
        m = re.search(
            r'<div class="tab-content">\s*(.*?)\s*</div>\s*(?:<!-- END tab-content -->|</div>\s*<!-- END enhanced-tab-content -->)',
            text,
            re.S | re.I,
        )
        return m.group(1).strip() if m else ""

    chunks: list[str] = []
    for pid in pane_ids:
        start_m = re.search(rf'<div class="tab-pane[^>]*\bid="{re.escape(pid)}"', text, re.I)
        if not start_m:
            continue
        start = start_m.start()
        rest = text[start_m.end() :]
        next_m = re.search(r'<div class="tab-pane', rest)
        modal_m = re.search(r'<div class="modal\b', rest)
        end_offset = len(rest)
        if next_m:
            end_offset = min(end_offset, next_m.start())
        if modal_m:
            end_offset = min(end_offset, modal_m.start())
        chunks.append(text[start : start_m.end() + end_offset].strip())
    return "\n\n          ".join(chunks)


def build_test_schedule(path: Path, cfg: dict) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    panes = extract_tab_panes(text)
    if not panes:
        print(f"SKIP schedule (no tabs): {path.name}")
        return
    panes = transform_feature_cards(panes)
    panes = transform_action_buttons(panes)
    tab_ids = cfg.get("tabs") or extract_tab_ids(text)
    if not tab_ids:
        tab_ids = re.findall(r'id="(Tabs[^"]+)"', panes)
    default = cfg.get("default_tab", tab_ids[0] if tab_ids else "#Tabsabc")
    count = len(tab_ids)
    header = build_header(path.name)
    footer = extract_footer(text)
    elfsight = '<div class="elfsight-app-0f63d541-e115-4e40-a45f-cf5119e5420a"></div>\n  ' if "elfsight" in text.lower() else ""

    rail_items = ""
    jumps = ""
    for tid in tab_ids:
        label, icon = TAB_META.get(tid, (tid.replace("Tabs", ""), "fa-star"))
        active = " active is-current" if tid == default.lstrip("#") else ""
        sel = "true" if active else "false"
        rail_items += f'            <li class="nav-item" role="presentation"><a class="nav-link{active}" data-toggle="tab" href="#{tid}" role="tab" aria-selected="{sel}" aria-controls="{tid}" id="tab-{tid}"><i class="fas {icon}" aria-hidden="true"></i> {label}</a></li>\n'
        jump_active = " is-active" if active else ""
        jumps += f'          <a href="#{tid}" class="ts-hero__jump{jump_active}" data-toggle="tab"><i class="fas {icon}" aria-hidden="true"></i> {label}</a>\n'

    body_class = f'pg-test-schedule pg-test-schedule--hub pg-test-schedule--{cfg["slug"]} ts-series-count-{count}'
    out = standard_head(path, ["test-schedule-premium.css"], f'  <body class="{body_class}" data-ts-default-tab="{default}">')
    out += f"\n  {elfsight}" + header + f"""
<section class="ts-hero enhanced-breadcrumb" aria-labelledby="ts-hero-title">
  <div class="container">
    <div class="ts-hero__grid">
      <div class="ts-hero__copy">
        <ol class="breadcrumb breadcrumb-double-angle bg-transparent p-0 mb-3 ts-hero__breadcrumb">
          <li class="breadcrumb-item"><a href="index.html"><i class="fas fa-home mr-2" aria-hidden="true"></i>Home</a></li>
          <li class="breadcrumb-item"><a href="course-overview.html#test-series">Test series</a></li>
          <li class="breadcrumb-item active text-white" aria-current="page">{cfg['hero_breadcrumb']}</li>
        </ol>
        <h1 class="page-title text-white" id="ts-hero-title">{cfg['hero_title']}</h1>
        <p class="page-subtitle">{cfg['hero_subtitle']}</p>
        <div class="ts-hero__meta">
          <div class="ts-hero__meta-card">
            <h5><i class="fas fa-calendar-alt mr-1" aria-hidden="true"></i> Batch</h5>
            <p class="mb-0"><strong>Session:</strong> {cfg['batch']}</p>
            <p class="mb-0"><strong>Level:</strong> {cfg['level']}</p>
          </div>
          <div class="ts-hero__meta-card">
            <h5><i class="fas fa-info-circle mr-1" aria-hidden="true"></i> Modes</h5>
            <p class="mb-2 text-white small">Online (India) · Direct (Chennai centre) — as per each series page.</p>
            <div class="ts-hero__badges">
              <span class="status-badge registration"><i class="fas fa-user-plus" aria-hidden="true"></i> Registration open</span>
              <span class="status-badge active"><i class="fas fa-laptop" aria-hidden="true"></i> Online</span>
              <span class="status-badge upcoming"><i class="fas fa-building" aria-hidden="true"></i> Direct</span>
            </div>
          </div>
        </div>
        <nav class="ts-hero__jumps" aria-label="Jump to test series">
{jumps}          <a href="registration.html" class="ts-hero__jump ts-hero__jump--enquiry"><i class="fas fa-paper-plane" aria-hidden="true"></i> Enquiry</a>
        </nav>
      </div>
      <div class="ts-hero-3d" aria-hidden="true">
        <div class="ts-hero-3d__stage">
          <div class="ts-hero-3d__card ts-hero-3d__card--abc">
            <div class="ts-hero-3d__card-icon"><i class="fas fa-star"></i></div>
            <div class="ts-hero-3d__card-label">ABC Series</div>
          </div>
          <div class="ts-hero-3d__card ts-hero-3d__card--marathon">
            <div class="ts-hero-3d__card-icon"><i class="fas fa-walking"></i></div>
            <div class="ts-hero-3d__card-label">DOT Marathon</div>
          </div>
          <div class="ts-hero-3d__card ts-hero-3d__card--dot">
            <div class="ts-hero-3d__card-icon"><i class="fas fa-bolt"></i></div>
            <div class="ts-hero-3d__card-label">DOT 2.0</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="ts-schedule-section padding-y-50">
  <div class="container">
    <div class="ts-series-rail-wrap">
      <div class="enhanced-tab-nav" id="ts-series-rail">
        <div class="ts-series-rail__head">
          <h2 class="ts-series-rail__title">Choose your test series</h2>
          <p class="ts-series-rail__hint">All test series are listed below — tap any option to view details</p>
        </div>
        <div class="ts-series-grid">
          <ul class="nav nav-pills ts-series-grid__list" role="tablist" aria-label="Test series options">
{rail_items}          </ul>
        </div>
      </div>
    </div>
    <div class="enhanced-tab-content ts-panel-shell">
      <div class="tab-content">
{panes}
      </div>
    </div>
  </div>
</section>

"""
    out += footer + "\n" + FOOTER_SCRIPTS + '\n    <script src="assets/js/test-schedule-premium.js"></script>\n  </body>\n</html>\n'
    path.write_text(out, encoding="utf-8")
    print(f"Test schedule: {path.name}")


def wrap_content_page(path: Path, hero_title: str, hero_lead: str, body_class: str = "pg-content") -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    # Extract main content between nav and footer
    content = extract_block(text, r"</nav>", r"<footer")
    content = re.sub(r"<style>.*?</style>", "", content, flags=re.S)
    content = re.sub(r"<!-- Footer -->", "", content)
    content = content.strip()
    header = build_header(path.name)
    footer = extract_footer(text)
    extra_css = ["content-page-premium.css", "policy-page-premium.css"]
    out = standard_head(path, extra_css, f'  <body class="{body_class}">')
    has_hero = bool(re.search(r'class="[^"]*(?:hero|content-hero)', content, re.I))
    hero_block = ""
    if not has_hero:
        hero_block = f"""
<section class="content-hero">
  <div class="container">
    <h1>{hero_title}</h1>
    <p class="lead">{hero_lead}</p>
  </div>
</section>
"""
    out += "\n" + header + hero_block + f"""
<main class="content-main">
{content}
</main>

"""
    out += footer + "\n" + FOOTER_SCRIPTS + "\n  </body>\n</html>\n"
    path.write_text(out, encoding="utf-8")
    print(f"Content page: {path.name}")


def build_404(path: Path) -> None:
    header = build_header(path.name)
    footer = extract_footer(path.read_text(encoding="utf-8", errors="replace"))
    out = standard_head(path, ["content-page-premium.css"], '  <body class="pg-404">')
    out += "\n" + header + """
<section class="content-hero" aria-labelledby="error-title">
  <div class="container text-center">
    <p class="error-code" aria-hidden="true">404</p>
    <h1 id="error-title">Page not found</h1>
    <p class="lead">Sorry — the link you followed may be broken, or this page may have moved. Try the home page or browse our test schedules.</p>
    <div class="error-actions">
      <a href="index.html" class="btn-home"><i class="fas fa-home" aria-hidden="true"></i> Back to home</a>
      <a href="ca-inter-test-schedule-sep-2026.html" class="btn-schedules"><i class="fas fa-calendar-alt" aria-hidden="true"></i> Test schedules</a>
      <a href="contact-us.html" class="btn-schedules"><i class="fas fa-envelope" aria-hidden="true"></i> Contact us</a>
    </div>
  </div>
</section>

"""
    out += footer + "\n" + FOOTER_SCRIPTS + "\n  </body>\n</html>\n"
    path.write_text(out, encoding="utf-8")
    print("404 page upgraded")


# ─── Configs ─────────────────────────────────────────────────────────────────

ABC_HUBS = {
    "ca-final-abc-series-may-2026.html": {
        "body_class": "pg-abc-home pg-abc-home--final",
        "level_label": "CA Final", "batch": "May 2026", "batch_short": "May 26",
        "schedule": "ca-final-test-schedule-may-2026.html",
        "h1": "CA Final ABC Test Series · May 2026",
        "lead": "Structured mock tests for Final New Course with <strong>optional model papers</strong>. Choose <strong>Online</strong> (India-wide) or <strong>Direct</strong> at our Chennai centre.",
        "whatsapp": "Final%20ABC%20May%202026",
        "cards": [
            {"mode": "online", "title": "ABC May 2026", "href": "ca-final-abc-online-may-2026.html"},
            {"mode": "direct", "title": "ABC May 2026", "href": "ca-final-abc-direct-may-2026.html", "featured": True},
        ],
    },
    "ca-inter-abc-series-may-2026.html": {
        "level_label": "CA Inter", "batch": "May 2026", "batch_short": "May 26",
        "schedule": "ca-inter-test-schedule-may-2026.html",
        "h1": "CA Inter ABC Test Series · May 2026",
        "lead": "Structured mock tests for Inter New Course. Choose <strong>Online</strong> or <strong>Direct</strong> at our Chennai centre.",
        "whatsapp": "Inter%20ABC%20May%202026",
        "cards": [
            {"mode": "online", "title": "ABC May 2026", "href": "ca-inter-abc-online-may-2026.html"},
            {"mode": "direct", "title": "ABC May 2026", "href": "ca-inter-abc-direct-may-2026.html", "featured": True},
        ],
    },
    "ca-inter-abc-series-jan-2027.html": {
        "level_label": "CA Inter", "batch": "Jan 2027", "batch_short": "Jan 27",
        "schedule": "ca-inter-test-schedule-jan-2027.html",
        "h1": "CA Inter ABC Test Series · Jan 2027",
        "lead": "Structured mock tests for Inter New Course. Choose <strong>Online</strong> or <strong>Direct</strong> at our Chennai centre.",
        "whatsapp": "Inter%20ABC%20Jan%202027",
        "cards": [
            {"mode": "online", "title": "ABC Jan 2027", "href": "ca-inter-abc-online-jan-2027.html"},
            {"mode": "direct", "title": "ABC Jan 2027", "href": "ca-inter-abc-direct-jan-2027.html", "featured": True},
        ],
    },
    "ca-inter-abc-series-sep-2026.html": {
        "level_label": "CA Inter", "batch": "Sep 2026", "batch_short": "Sep 26",
        "schedule": "ca-inter-test-schedule-sep-2026.html",
        "h1": "CA Inter ABC Test Series · Sep 2026",
        "lead": "Structured mock tests for Inter New Course with <strong>optional model papers</strong>. Choose <strong>Direct</strong> (Chennai) or <strong>Online</strong> (from home).",
        "whatsapp": "Inter%20ABC%20Sep%202026",
        "cards": [
            {"mode": "direct", "title": "ABC Sep 2026", "href": "ca-inter-abc-direct-sep-2026.html",
             "desc": "Write at PradhiCA Chennai with centre support. Choose your plan — including combinations with or without model examinations."},
            {"mode": "online", "title": "ABC Sep 2026", "href": "ca-inter-abc-online-sep-2026.html", "featured": True,
             "desc": "Attempt from anywhere with the same evaluation standards, suggested answers, and mentor support as Direct students."},
        ],
    },
    "ca-foundation-abc-series-may-2026.html": {
        "level_label": "CA Foundation", "batch": "May 2026", "batch_short": "May 26",
        "schedule": "ca-foundation-test-schedule-may-2026.html",
        "h1": "CA Foundation ABC Test Series · May 2026",
        "lead": "Structured mock tests for Foundation with <strong>optional model papers</strong>. Choose <strong>Online</strong> or <strong>Direct</strong> at our Chennai centre.",
        "whatsapp": "Foundation%20ABC%20May%202026",
        "layout": "full",
        "cards": [
            {"key": "online", "href": "ca-foundation-abc-online-may-2026.html"},
            {"key": "online_model", "href": "ca-foundation-abc-online-with-model-may-2026.html"},
            {"key": "direct", "href": "ca-foundation-abc-direct-may-2026.html"},
            {"key": "direct_model", "href": "ca-foundation-abc-direct-with-model-may-2026.html"},
        ],
    },
}

DOT2_HUBS = {
    "ca-final-dot-2-series-may-2026.html": {
        "level_label": "CA Final", "batch": "May 2026", "batch_short": "May 26",
        "schedule": "ca-final-test-schedule-may-2026.html",
        "h1": "CA Final DOT 2.0 · May 2026",
        "lead": "9 weekly chapter tests and model exams. Choose <strong>Direct</strong> at our Chennai centre or <strong>Online</strong> from home.",
        "card_title": "DOT 2.0 May 2026",
        "direct": "ca-final-dot-2-0-ii-may-2026.html", "online": "ca-final-dot-2-0-i-may-2026.html",
        "pdf": "Schedules_2026/PradhiCA-CA Final-DOT2.O-May26-Schedule (1).pdf",
    },
    "ca-inter-dot-2-series-may-2026.html": {
        "level_label": "CA Inter", "batch": "May 2026", "batch_short": "May 26",
        "schedule": "ca-inter-test-schedule-may-2026.html",
        "h1": "CA Inter DOT 2.0 · May 2026",
        "lead": "9 weekly chapter tests and revision exams. Choose <strong>Direct</strong> or <strong>Online</strong>.",
        "card_title": "DOT 2.0 May 2026",
        "direct": "ca-inter-dot-2-direct-may-2026.html", "online": "ca-inter-dot-2-online-may-2026.html",
    },
    "ca-inter-dot-2-series-sep-2026.html": {
        "level_label": "CA Inter", "batch": "Sep 2026", "batch_short": "Sep 26",
        "schedule": "ca-inter-test-schedule-sep-2026.html",
        "h1": "CA Inter DOT 2.0 · Sep 2026",
        "lead": "9 weekly chapter tests and revision exams. Choose <strong>Direct</strong> or <strong>Online</strong>.",
        "card_title": "DOT 2.0 Sep 2026",
        "direct": "ca-inter-dot-2-direct-sep-2026.html", "online": "ca-inter-dot-2-online-sep-2026.html",
        "pdf": "Schedules_2026/PradhiCA-CA Inter-DOT-2.O-Sep26-Schedule.pdf",
    },
    "ca-foundation-dot-2-series-sep-2026.html": {
        "level_label": "CA Foundation", "batch": "Sep 2026", "batch_short": "Sep 26",
        "schedule": "ca-foundation-test-schedule-sep-2026.html",
        "h1": "CA Foundation DOT 2.0 · Sep 2026",
        "lead": "Weekly chapter-wise tests for Foundation. Choose <strong>Direct</strong> or <strong>Online</strong>.",
        "card_title": "DOT 2.0 Sep 2026",
        "direct": "ca-foundation-dot-2-direct-sep-2026.html", "online": "ca-foundation-dot-2-online-sep-2026.html",
    },
}

MARATHON_HUBS = {
    "ca-final-dot-marathon-series-may-2026.html": {
        "level_label": "CA Final", "batch": "May 2026", "batch_short": "May 26",
        "schedule": "ca-final-test-schedule-may-2026.html",
        "h1": "CA Final DOT Marathon · May 2026",
        "lead": "9 weekly chapter-wise tests, revision &amp; model exams. Choose <strong>Direct</strong> (Chennai centre) or <strong>Online</strong> (from home).",
        "card_title": "DOT Marathon May 2026",
        "direct": "ca-final-dot-marathon-direct-may-2026.html", "online": "ca-final-dot-marathon-online-may-2026.html",
    },
    "ca-final-dot-marathon-series-nov-2026.html": {
        "level_label": "CA Final", "batch": "Nov 2026", "batch_short": "Nov 26",
        "schedule": "ca-final-test-schedule-nov-2026.html",
        "h1": "CA Final DOT Marathon · Nov 2026",
        "lead": "9 weekly chapter-wise tests, revision &amp; model exams over ~4 months. Choose <strong>Direct</strong> (Chennai centre) or <strong>Online</strong> (from home).",
        "card_title": "DOT Marathon Nov 2026",
        "direct": "ca-final-dot-marathon-direct-nov-2026.html", "online": "ca-final-dot-marathon-online-nov-2026.html",
    },
    "ca-inter-dot-marathon-series-may-2026.html": {
        "level_label": "CA Inter", "batch": "May 2026", "batch_short": "May 26",
        "schedule": "ca-inter-test-schedule-may-2026.html",
        "h1": "CA Inter DOT Marathon · May 2026",
        "lead": "10 weekly test series with model exams. Choose <strong>Direct</strong> or <strong>Online</strong>.",
        "card_title": "DOT Marathon May 2026",
        "direct": "ca-inter-dot-marathon-direct-may-2026.html", "online": "ca-inter-dot-marathon-online-may-2026.html",
    },
    "ca-inter-dot-marathon-series-sep-2026.html": {
        "level_label": "CA Inter", "batch": "Sep 2026", "batch_short": "Sep 26",
        "schedule": "ca-inter-test-schedule-sep-2026.html",
        "h1": "CA Inter DOT Marathon · Sep 2026",
        "lead": "10 weekly test series with model exams. Choose <strong>Direct</strong> or <strong>Online</strong>.",
        "card_title": "DOT Marathon Sep 2026",
        "direct": "ca-inter-dot-marathon-direct-sep-2026.html", "online": "ca-inter-dot-marathon-online-sep-2026.html",
    },
    "ca-foundation-dot-marathon-series-jan-2026.html": {
        "level_label": "CA Foundation", "batch": "Jan 2026", "batch_short": "Jan 26",
        "schedule": "ca-foundation-test-schedule-may-2026.html",
        "h1": "CA Foundation DOT Marathon · Jan 2026",
        "lead": "Weekly chapter-wise tests for Foundation. Choose <strong>Direct</strong> or <strong>Online</strong>.",
        "card_title": "DOT Marathon Jan 2026",
        "direct": "ca-foundation-dot-marathon-direct-jan-2026.html", "online": "ca-foundation-dot-marathon-online-jan-2026.html",
    },
    "ca-foundation-dot-2-series-may-2026.html": {
        "level_label": "CA Foundation", "batch": "Jan 2026", "batch_short": "Jan 26",
        "schedule": "ca-foundation-test-schedule-may-2026.html",
        "h1": "CA Foundation DOT Marathon · Jan 2026",
        "lead": "Weekly chapter-wise tests for Foundation Jan 2026 batch. Choose <strong>Direct</strong> or <strong>Online</strong>.",
        "card_title": "DOT Marathon Jan 2026",
        "direct": "ca-foundation-dot-marathon-direct-jan-2026.html", "online": "ca-foundation-dot-marathon-online-jan-2026.html",
    },
}

SCHEDULE_PAGES = {
    "ca-final-test-schedule-may-2026.html": {
        "slug": "may26", "level": "CA Final", "batch": "May 2026",
        "hero_breadcrumb": "CA Final · May 2026",
        "hero_title": 'CA Final <span>Test Schedule</span>',
        "hero_subtitle": "May 2026 attempt — ABC, DOT 2.0, DOT 3.0, Rapid Revision, Model & Subject-wise. Download schedules and register.",
        "default_tab": "#Tabsabc",
        "tabs": ["Tabsabc", "Tabsdot1", "Tabsdot6", "Tabssingle2", "Tabsmodel", "Tabssingle"],
    },
    "ca-inter-test-schedule-may-2026.html": {
        "slug": "may26", "level": "CA Intermediate", "batch": "May 2026",
        "hero_breadcrumb": "CA Intermediate · May 2026",
        "hero_title": 'CA Intermediate <span>Test Schedule</span>',
        "hero_subtitle": "May 2026 attempt — ABC, DOT Marathon, DOT 2.0 and more. Download schedules and register.",
        "default_tab": "#Tabsabc",
    },
    "ca-inter-test-schedule-jan-2027.html": {
        "slug": "jan27", "level": "CA Intermediate", "batch": "Jan 2027",
        "hero_breadcrumb": "CA Intermediate · Jan 2027",
        "hero_title": 'CA Intermediate <span>Test Schedule</span>',
        "hero_subtitle": "Jan 2027 attempt — ABC, Rapid Revision, Subject-wise and more.",
        "default_tab": "#Tabsabc",
    },
    "ca-final-test-schedule-may-2027.html": {
        "slug": "may27", "level": "CA Final", "batch": "May 2027",
        "hero_breadcrumb": "CA Final · May 2027",
        "hero_title": 'CA Final <span>Test Schedule</span>',
        "hero_subtitle": "May 2027 attempt — ABC, DOT Marathon, DOT 2.0, DOT 3.0 and more.",
        "default_tab": "#Tabsabc",
        "tabs": ["Tabsabc", "Tabsdot", "Tabsdot1", "Tabsdot6", "Tabssingle2", "Tabsmodel", "Tabssingle"],
    },
    "ca-foundation-test-schedule-may-2026.html": {
        "slug": "may26", "level": "CA Foundation", "batch": "May 2026",
        "hero_breadcrumb": "CA Foundation · May 2026",
        "hero_title": 'CA Foundation <span>Test Schedule</span>',
        "hero_subtitle": "May 2026 attempt — DOT 3.0, ABC and Rapid Revision test series.",
        "default_tab": "#Tabsdot3",
        "tabs": ["Tabsdot3", "Tabsabc", "Tabsrapid"],
    },
}


def main() -> None:
    for name, cfg in ABC_HUBS.items():
        build_abc_hub(ROOT / name, cfg)
    for name, cfg in DOT2_HUBS.items():
        build_dot2_hub(ROOT / name, cfg)
    for name, cfg in MARATHON_HUBS.items():
        build_marathon_hub(ROOT / name, cfg)
    for name, cfg in SCHEDULE_PAGES.items():
        build_test_schedule(ROOT / name, cfg)

    wrap_content_page(
        ROOT / "ca-foundation-test-series.html",
        "CA Foundation Test Series",
        "Superior to institute tests — ICAI-aligned patterns, expert CA evaluation, Online + Direct modes.",
    )

    build_404(ROOT / "404.html")

    utility_pages = {
        "scheduled-download.html": ("Schedule download", "Download your PradhiCA test series schedule PDFs."),
        "switch-from-institute.html": ("Switch from institute tests", "A practical guide to moving from coaching institute mocks to PradhiCA."),
        "testing-page.html": ("Testing page", "Internal testing page for PradhiCA layouts."),
        "update-page.html": ("Updates", "Latest updates from PradhiCA."),
        "vs-institute-tests.html": ("PradhiCA vs institute tests", "See how PradhiCA test series compare to typical coaching institute mocks."),
        "why-institute-tests-fail-ca-students.html": (
            "Why institute tests fail CA students",
            "Common gaps in institute mock tests — and what to look for instead.",
        ),
    }
    for name, (title, lead) in utility_pages.items():
        p = ROOT / name
        if p.exists():
            wrap_content_page(p, title, lead)

    print("Done.")


if __name__ == "__main__":
    main()

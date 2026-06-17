#!/usr/bin/env python3
"""Wrap bare policy pages and sitemap with full site chrome (header + footer)."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "apply_global_header",
    ROOT / "scripts" / "apply-global-header.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
build_header = _mod.build_header

FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=DM+Sans:ital,opsz,wght@0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800'
    '&family=Maven+Pro:wght@500;600;700;800&family=Work+Sans:wght@400;500;600&display=swap">'
)

FOOTER = """<footer class="site-footer">
  <div class="footer-top bg-dark text-white-0_6 pt-5 paddingBottom-100">
    <div class="container">
      <div class="row">
        <div class="col-lg-3 col-md-6 mt-5">
         <img src="assets/img/logo-white.png" alt="Logo">
         <div class="margin-y-40">
           <p>We Create Talented CA</p>
         </div>
          <ul class="list-inline">
            <li class="list-inline-item"><a class="iconbox bg-white-0_2 hover:primary" href="http://bit.ly/fbpradhica" target="_blank"><i class="ti-facebook"> </i></a></li>
            <li class="list-inline-item"><a class="iconbox bg-white-0_2 hover:primary" href="http://bit.ly/inspradhica" target="_blank"><i class="ti-instagram"></i></a></li>
            <li class="list-inline-item"><a class="iconbox bg-white-0_2 hover:primary" href="https://www.youtube.com/channel/UCf1poDZ0HqWowl5AbwH3UMQ" target="_blank"><i class="ti-youtube"></i></a></li>
          </ul>
        </div>
        <div class="col-lg-3 col-md-6 mt-5">
          <h4 class="h5 text-white">Contact Us</h4>
          <div class="width-3rem bg-primary height-3 mt-3"></div>
          <ul class="list-unstyled marginTop-40">
            <li class="mb-3"><i class="ti-mobile mr-3"></i><a href="tel:+918072653948">+91 80726 53948 </a></li>
            <li class="mb-3"><i class="ti-email mr-3"></i><a href="mailto:pradhica4u@gmail.com">pradhica4u@gmail.com</a></li>
            <li class="mb-3">
             <div class="media">
              <i class="ti-location-pin mt-2 mr-3"></i>
              <div class="media-body">
                <span><a href="https://maps.app.goo.gl/3scL1jiJsRZxtvYd9" target="_blank"> No: 20, 1st floor, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu 600033</a></span>
              </div>
             </div>
            </li>
          </ul>
        </div>
        <div class="col-lg-3 col-md-6 mt-5">
          <h4 class="h5 text-white">Quick links</h4>
          <div class="width-3rem bg-primary height-3 mt-3"></div>
          <ul class="list-unstyled marginTop-40">
            <li class="mb-2"><a href="contact-us.html">Contact Us</a></li>
            <li class="mb-2"><a href="https://icai.org" target="_blank">ICAI</a></li>
            <li class="mb-2"><a href="https://icai.org/new_post.html?post_id=5720&c_id=314" target="_blank">Study Materials</a></li>
          </ul>
        </div>
        <div class="col-lg-3 col-md-6 mt-5">
          <h4 class="h5 text-white">Policies</h4>
          <div class="width-3rem bg-primary height-3 mt-3"></div>
          <ul class="list-unstyled marginTop-40">
            <li class="mb-2"><a href="terms-and-conditions.html">Terms & Conditions</a></li>
            <li class="mb-2"><a href="privacy-policy.html">Privacy Policies</a></li>
            <li class="mb-2"><a href="refund-policy.html">Refund Policies</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-bottom bg-black-0_9 py-5 text-center">
    <div class="container">
      <p class="text-white-0_5 mb-0">&copy; 2026 PradhiCA. All rights reserved. Created and Designed by <a href="https://techrethought.com" target="_blank">Techrethought</a></p>
    </div>
    <a href="https://api.whatsapp.com/send?phone=918072653948&text=Name:&forceIntent=true&load=loadInIOSExternalSafari" class="pradhi-wa-float" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
      <i class="fab fa-whatsapp"></i>
    </a>
  </div>
</footer>
<div class="scroll-top"><i class="ti-angle-up"></i></div>
<script src="assets/js/vendors.bundle.js"></script>
<script src="assets/js/header-scroll.js"></script>
<script src="assets/js/header-nav-dropdown.js"></script>
<script src="assets/js/scripts.js"></script>"""

POLICY_META = {
    "privacy-policy.html": {
        "title": "Privacy Policy | PradhiCA — CA Test Series India",
        "description": "PradhiCA privacy policy. How we collect, use, and protect your personal data when you use our CA test series services.",
        "canonical": "https://pradhica.com/privacy-policy.html",
    },
    "terms-and-conditions.html": {
        "title": "Terms and Conditions | PradhiCA — CA Test Series India",
        "description": "Terms and conditions for using PradhiCA CA test series, mock exams, and related services.",
        "canonical": "https://pradhica.com/terms-and-conditions.html",
    },
    "refund-policy.html": {
        "title": "Refund Policy | PradhiCA — CA Test Series India",
        "description": "PradhiCA return and refund policy for CA test series purchases.",
        "canonical": "https://pradhica.com/refund-policy.html",
    },
}


def head_block(meta: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-132037455-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'UA-132037455-1');
</script>
  <meta charset="UTF-8">
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['description']}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{meta['canonical']}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <link rel="icon" type="image/x-icon" href="assets/img/favicon/favicon.ico">
  {FONT_LINK}
  <link rel="stylesheet" href="assets/fonts/fontawesome/css/all.css">
  <link rel="stylesheet" href="assets/fonts/themify-icons/css/themify-icons.css">
  <link rel="stylesheet" href="assets/css/vendors.bundle.css">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="assets/css/footer-premium.css">
  <link rel="stylesheet" href="assets/css/header-premium.css">
  <link rel="stylesheet" href="assets/css/policy-page-premium.css">
</head>
<body class="pg-policy">
"""


def clean_policy_body(html: str) -> str:
    html = re.sub(
        r'<script[^>]*cloudflare-static/email-decode[^>]*></script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<a href="/cdn-cgi/l/email-protection"[^>]*>\[email[^\]]*\]</a>',
        '<a href="mailto:pradhica4u@gmail.com">pradhica4u@gmail.com</a>',
        html,
        flags=re.I,
    )
    return html.strip()


def wrap_policy(path: Path) -> None:
    meta = POLICY_META[path.name]
    body = clean_policy_body(path.read_text(encoding="utf-8", errors="replace"))
    header = build_header(path.name)
    out = (
        head_block(meta)
        + header
        + "\n  <main>\n    <div class=\"container\">\n      <article class=\"policy-content\">\n"
        + body
        + "\n      </article>\n    </div>\n  </main>\n\n"
        + FOOTER
        + "\n</body>\n</html>\n"
    )
    path.write_text(out, encoding="utf-8")
    print(f"Wrapped policy: {path.name}")


def wrap_sitemap(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    list_match = re.search(r"<div id=\"cont\">(.*?)</div>\s*<div id=\"footer\">", text, re.DOTALL)
    if not list_match:
        print("SKIP sitemap: could not extract list")
        return
    list_inner = list_match.group(1).strip()
    header = build_header(path.name)
    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PradhiCA — HTML Site Map | CA Test Series India</title>
  <meta name="description" content="Complete HTML sitemap of PradhiCA CA test series pages — Foundation, Intermediate, and Final.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://pradhica.com/sitemap.html">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <link rel="icon" type="image/x-icon" href="assets/img/favicon/favicon.ico">
  {FONT_LINK}
  <link rel="stylesheet" href="assets/fonts/fontawesome/css/all.css">
  <link rel="stylesheet" href="assets/fonts/themify-icons/css/themify-icons.css">
  <link rel="stylesheet" href="assets/css/vendors.bundle.css">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="assets/css/footer-premium.css">
  <link rel="stylesheet" href="assets/css/header-premium.css">
  <link rel="stylesheet" href="assets/css/policy-page-premium.css">
</head>
<body class="pg-sitemap">
{header}
  <section class="sitemap-hero">
    <div class="container">
      <h1>pradhica.com — HTML sitemap</h1>
      <p>
        Last updated: 2026-03-20 · Total pages: 160 (+ home)<br>
        Machine sitemap: <a href="https://pradhica.com/sitemap.xml">sitemap.xml</a> ·
        URL list: <a href="https://pradhica.com/urllist.txt">urllist.txt</a> ·
        LLM manifest: <a href="https://pradhica.com/llms.txt">llms.txt</a><br>
        <a href="index.html">← Homepage</a>
      </p>
    </div>
  </section>
  <div class="container">
    <div class="sitemap-list">
{list_inner}
      <p class="sitemap-hint">Blog and dynamic content: <a href="blog/index.php">/blog/</a></p>
    </div>
  </div>

{FOOTER}
</body>
</html>
"""
    path.write_text(out, encoding="utf-8")
    print(f"Wrapped sitemap: {path.name}")


def main():
    for name in POLICY_META:
        wrap_policy(ROOT / name)
    wrap_sitemap(ROOT / "sitemap.html")
    print("Done.")


if __name__ == "__main__":
    main()

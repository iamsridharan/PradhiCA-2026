#!/usr/bin/env python3
"""Apply premium site header + nav to all PradhiCA HTML pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=DM+Sans:ital,opsz,wght@0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800'
    '&family=Maven+Pro:wght@500;600;700;800&family=Work+Sans:wght@400;500;600&display=swap">'
)

# Curated dropdown — matches index.html
TEST_SERIES_ITEMS = [
    ("ca-final-test-schedule-nov-2026.html", "Final Nov 26"),
    ("ca-final-test-schedule-may-2027.html", "Final May 27"),
    ("ca-inter-test-schedule-sep-2026.html", "Inter Sep 26"),
    ("ca-inter-test-schedule-jan-2027.html", "Inter Jan 27"),
    ("ca-foundation-test-schedule-sep-2026.html", "Foundation Sep 26"),
]

HEADER_RE = re.compile(
    r"\s*<header\s+class=\"site-header[^\"]*\"[^>]*>.*?</nav>\s*(?:<!--\s*END\s+(?:ec-nav|site-search)\s*-->\s*)?",
    re.DOTALL | re.IGNORECASE,
)

OLD_HEADER_MARKERS = ("site-header bg-dark", 'class="site-header bg-dark')


def nav_link(href: str, label: str, filename: str, matchers: tuple, icon: str = "") -> str:
    active = any(m(filename) for m in matchers)
    cls = "nav-link active" if active else "nav-link"
    cur = ' aria-current="page"' if active else ""
    ic = f'<i class="{icon}" aria-hidden="true"></i> ' if icon else ""
    return f'<a class="{cls}" href="{href}"{cur}>{ic}{label}</a>'


def build_header(filename: str) -> str:
    is_home = filename == "index.html"
    is_course = filename == "course-overview.html"
    is_contact = filename == "contact-us.html"
    is_enquiry = filename == "registration.html"
    is_test = "test-schedule" in filename

    home_cls = "nav-link active" if is_home else "nav-link"
    home_cur = ' aria-current="page"' if is_home else ""

    course_cls = "nav-link active" if is_course else "nav-link"
    course_cur = ' aria-current="page"' if is_course else ""

    test_cls = "nav-link dropdown-toggle active" if is_test else "nav-link dropdown-toggle"
    test_exp = "true" if is_test else "false"

    contact_cls = "nav-link active" if is_contact else "nav-link"
    contact_cur = ' aria-current="page"' if is_contact else ""

    enquiry_cls = "nav-link active" if is_enquiry else "nav-link"
    enquiry_cur = ' aria-current="page"' if is_enquiry else ""

    dropdown = "\n".join(
        f'                <li><a href="{href}" class="nav-link__list">{label}</a></li>'
        for href, label in TEST_SERIES_ITEMS
    )

    return f"""  <header class="site-header" role="banner">
    <div class="container">
      <div class="row align-items-center justify-content-between mx-0 flex-wrap">
        <p class="site-header__trust d-none d-lg-flex mb-0">
          <i class="fas fa-award" aria-hidden="true"></i> 7,500+ successful CAs nationwide
        </p>
        <ul class="list-inline d-none d-lg-flex mb-0">
          <li class="list-inline-item">
            <div class="d-flex align-items-center">
              <i class="fas fa-envelope" aria-hidden="true"></i>
              <a href="mailto:pradhica4u@gmail.com">pradhica4u@gmail.com</a>
            </div>
          </li>
          <li class="list-inline-item">
            <div class="d-flex align-items-center">
              <i class="fas fa-phone-alt" aria-hidden="true"></i>
              <a href="tel:+918072653948">+91 80726 53948</a>
            </div>
          </li>
        </ul>
        <ul class="site-header__social list-inline mb-0">
          <li>
            <a href="http://bit.ly/fbpradhica" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><i class="fab fa-facebook-f" aria-hidden="true"></i></a>
          </li>
          <li>
            <a href="http://bit.ly/inspradhica" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><i class="fab fa-instagram" aria-hidden="true"></i></a>
          </li>
          <li>
            <a href="https://t.me/PradhiCA" target="_blank" rel="noopener noreferrer" aria-label="Telegram"><i class="fab fa-telegram-plane" aria-hidden="true"></i></a>
          </li>
          <li>
            <a href="https://www.youtube.com/channel/UCf1poDZ0HqWowl5AbwH3UMQ" target="_blank" rel="noopener noreferrer" aria-label="YouTube"><i class="fab fa-youtube" aria-hidden="true"></i></a>
          </li>
        </ul>
      </div>
    </div>
  </header>

  <nav class="ec-nav sticky-top" id="main-nav" aria-label="Main navigation">
    <div class="container">
      <div class="navbar p-0 navbar-expand-lg">
        <div class="navbar-brand">
          <a class="logo-default" href="index.html"><img src="assets/img/logo-black.png" alt="PradhiCA — CA Test Series" width="180" height="48"></a>
        </div>
        <button type="button" class="navbar-toggler ml-auto collapsed" data-toggle="collapse" data-target="#ec-nav__collapsible" aria-expanded="false" aria-controls="ec-nav__collapsible" aria-label="Open menu">
          <span class="hamburger hamburger--spin js-hamburger">
            <span class="hamburger-box">
              <span class="hamburger-inner"></span>
            </span>
          </span>
        </button>
        <div class="collapse navbar-collapse when-collapsed" id="ec-nav__collapsible">
          <ul class="nav navbar-nav ec-nav__navbar ml-auto">
            <li class="nav-item">
              <a class="{home_cls}" href="index.html"{home_cur}>Home</a>
            </li>
            <li class="nav-item">
              <a class="{course_cls}" href="course-overview.html"{course_cur}>Course Overview</a>
            </li>
            <li class="nav-item nav-item__has-dropdown">
              <a class="{test_cls}" href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="{test_exp}">Test Series</a>
              <ul class="dropdown-menu">
{dropdown}
              </ul>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://t.me/pradhica" target="_blank" rel="noopener">Blog</a>
            </li>
            <li class="nav-item">
              <a class="{contact_cls}" href="contact-us.html"{contact_cur}>Contact</a>
            </li>
            <li class="nav-item">
              <a class="{enquiry_cls}" href="registration.html"{enquiry_cur}><i class="fas fa-paper-plane" aria-hidden="true"></i> Enquiry</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
"""


def ensure_head_assets(text: str) -> str:
    if "header-premium.css" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="assets/css/header-premium.css">',
            '<link rel="stylesheet" href="assets/css/header-premium.css">',
        )
        if "header-premium.css" not in text:
            for anchor in (
                '<link rel="stylesheet" href="assets/css/footer-premium.css">',
                '<link rel="stylesheet" href="assets/css/style.css">',
            ):
                if anchor in text:
                    text = text.replace(
                        anchor,
                        anchor + "\n    <link rel=\"stylesheet\" href=\"assets/css/header-premium.css\">",
                        1,
                    )
                    break

    if "DM+Sans" not in text and "fonts.googleapis.com" in text:
        text = re.sub(
            r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css[^"]*">',
            FONT_LINK,
            text,
            count=1,
        )

    return text


def ensure_footer_script(text: str) -> str:
    scroll_tag = '    <script src="assets/js/header-scroll.js"></script>\n'
    dropdown_tag = '    <script src="assets/js/header-nav-dropdown.js"></script>\n'

    if "header-nav-dropdown.js" not in text and "header-scroll.js" in text:
        text = text.replace(scroll_tag, scroll_tag + dropdown_tag, 1)

    if "header-scroll.js" not in text:
        bundle = scroll_tag + dropdown_tag
        if '<script src="assets/js/scripts.js"></script>' in text:
            text = text.replace(
                '<script src="assets/js/scripts.js"></script>',
                bundle + '    <script src="assets/js/scripts.js"></script>',
                1,
            )
        elif '<script src="assets/js/vendors.bundle.js"></script>' in text:
            text = text.replace(
                '<script src="assets/js/vendors.bundle.js"></script>',
                '<script src="assets/js/vendors.bundle.js"></script>\n' + bundle,
                1,
            )
    return text


def remove_inline_header_scroll(text: str) -> str:
    return re.sub(
        r"\s*<script>\s*\(function\s*\(\)\s*\{\s*var nav = document\.getElementById\(\"main-nav\"\).*?</script>\s*",
        "\n",
        text,
        flags=re.DOTALL,
    )


def find_header_span(text: str) -> tuple[int, int] | None:
    m = HEADER_RE.search(text)
    if m:
        return m.span()
    m2 = re.search(
        r"\s*<header\s+class=\"site-header[^\"]*\".*?</header>\s*<nav\s+class=\"ec-nav[^\"]*\".*?</nav>",
        text,
        re.DOTALL | re.I,
    )
    return m2.span() if m2 else None


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")

    span = find_header_span(text)
    if span is None:
        if any(m in text for m in OLD_HEADER_MARKERS):
            print(f"SKIP (old header, no regex match): {path.name}")
        elif "<header" not in text.lower():
            print(f"SKIP (no header): {path.name}")
        else:
            print(f"SKIP (no match): {path.name}")
        return False

    filename = path.name
    new_header = build_header(filename)
    new_text = text[: span[0]] + new_header + text[span[1] :]
    new_text = ensure_head_assets(new_text)
    new_text = remove_inline_header_scroll(new_text)
    new_text = ensure_footer_script(new_text)

    if new_text == text:
        return False

    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    updated = 0
    skipped = 0
    for path in sorted(ROOT.glob("*.html")):
        if path.name.startswith("."):
            continue
        if process_file(path):
            updated += 1
            print(f"Updated: {path.name}")
        else:
            skipped += 1
    print(f"\nDone. Updated {updated} files, skipped {skipped}.")


if __name__ == "__main__":
    main()

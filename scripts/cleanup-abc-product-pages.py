#!/usr/bin/env python3
"""Fix HTML structure after ABC product page upgrade."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800'
    '&family=Maven+Pro:wght@400;500;700&family=Work+Sans:wght@400;500;600&display=swap">'
)

PRODUCT_FILES = [
    "ca-final-abc-direct-nov-2026.html",
    "ca-final-abc-direct-may-2027.html",
    "ca-final-abc-direct-with-model-nov-2026.html",
    "ca-final-abc-direct-with-model-may-2027.html",
    "ca-final-abc-online-nov-2026.html",
    "ca-final-abc-online-may-2027.html",
    "ca-final-abc-online-with-model-nov-2026.html",
    "ca-final-abc-online-with-model-may-2027.html",
]

# Old top h4 blocks to remove
OLD_H4 = re.compile(
    r'\s*<div class="col-12 text-center mb-3">\s*'
    r'<h4>(?:CA Final|FINAL Exam)[^<]*</h4>\s*</div>\s*',
    re.IGNORECASE,
)

# Subsection headers -> abc-price-block
SUB_H4 = re.compile(
    r'<div class="col-12 text-center mb-3">\s*'
    r'<h4>(ABC (?:DIRECT|ONLINE)[^<]*)</h4>\s*</div>',
    re.IGNORECASE,
)

SUB_H4_REPL = r'<div class="col-12 abc-price-block"><h3 class="abc-price-block__title">\1</h3></div>\n          <div class="row abc-price-grid">'


def cleanup(path: Path):
    text = path.read_text(encoding="utf-8")

    if "DM+Sans" not in text:
        text = re.sub(
            r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css[^"]*">',
            FONT_LINK,
            text,
            count=1,
        )

    # Remove nested duplicate container after pricing head
    text = re.sub(
        r'(</div>\s*)\n\s*<div class="container">\s*\n\s*<div class="row align-items-center">',
        r"\1\n          <div class=\"row align-items-center\">",
        text,
        count=1,
    )

    text = OLD_H4.sub("\n", text)
    text = SUB_H4.sub(SUB_H4_REPL, text)

    # First price grid after features if missing
    text = re.sub(
        r'(</ul>\s*</div>\s*)\n(\s*<div class="col-md-4)',
        r"\1\n          <div class=\"row abc-price-grid\">\n\2",
        text,
        count=1,
    )

    # Close grid before abc-price-block
    text = re.sub(
        r'(</div>\s*</div>\s*</div>\s*)\n(\s*<div class="col-12 abc-price-block")',
        r"\1\n          </div>\n\2",
        text,
    )

    # Close last grid before note or section end
    if "abc-pricing__note" in text:
        text = re.sub(
            r'(</div>\s*</div>\s*</div>\s*)\n(\s*<p class="abc-pricing__note")',
            r"\1\n          </div>\n\2",
            text,
            count=1,
        )

    # Remove duplicate section closes (keep one clean ending)
    text = re.sub(
        r'</section>\s*(?:\s*</div>\s*<!-- END row-->\s*)?(?:\s*</div>\s*<!-- END container-->\s*)?</section>',
        "</section>",
        text,
    )

    # Normalize section footer: note inside col-lg-11, single close
    if text.count("</section>") > 1 and "abc-pricing" in text:
        # Find pricing section and strip duplicate closings after first </section> following abc-pricing
        m = re.search(
            r'(<section class="abc-pricing[^>]*>.*?)(</section>)',
            text,
            re.DOTALL,
        )
        if m:
            body = m.group(1)
            # ensure proper closing inside
            if "abc-pricing__note" not in body:
                body += (
                    '\n          <p class="abc-pricing__note"><i class="fas fa-info-circle mr-1"></i>'
                    "GST as applicable · Need help? "
                    '<a href="registration.html">Enquiry</a> or '
                    '<a href="https://api.whatsapp.com/send?phone=918072653948">WhatsApp</a></p>'
                )
            if body.count("</div>") < 4:
                pass
            body += "\n        </div>\n      </div>\n    </div>\n  </section>"
            text = text[: m.start()] + body + text[m.end() :]
            # remove any second </section> before footer
            text = re.sub(r"</section>\s*</section>", "</section>", text)
            text = re.sub(
                r"</section>\s*(?:\s*</div>\s*<!-- END row-->\s*)+"
                r"(?:\s*</div>\s*<!-- END container-->\s*)?</section>",
                "</section>",
                text,
            )

    # Simpler fix: remove orphan END row/container comments before sticky/footer
    text = re.sub(
        r'</section>\s*(?:\s*</div>\s*<!-- END row-->\s*)+'
        r'(?:\s*</div>\s*<!-- END container-->\s*)?(?:</section>\s*)?',
        "</section>\n",
        text,
        count=1,
    )

    # Ensure features use col-12 only once
    text = re.sub(
        r'<div class="row align-items-center">\s*<div class="col-12">\s*<ul class="pg-single__features">',
        '<ul class="pg-single__features">',
        text,
        count=1,
    )
    text = re.sub(
        r'</ul>\s*</div>\s*(?=\s*<div class="row abc-price-grid">|\s*<div class="col-md-4)',
        "</ul>\n",
        text,
        count=1,
    )

    path.write_text(text, encoding="utf-8")
    print(f"Cleaned: {path.name}")


def fix_series_may_head():
    path = ROOT / "ca-final-abc-series-may-2027.html"
    text = path.read_text(encoding="utf-8")
    if "abc-series-hub-premium.css" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="assets/css/header-premium.css">',
            '<link rel="stylesheet" href="assets/css/header-premium.css">\n'
            '    <link rel="stylesheet" href="assets/css/abc-series-hub-premium.css">',
        )
    if "DM+Sans" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Maven+Pro:400,500,700%7CWork+Sans:400,500">',
            FONT_LINK,
        )
    if 'class="pg-abc-home' not in text:
        text = re.sub(r"<body[^>]*>", '<body class="pg-abc-home pg-abc-home--final">', text, count=1)
    path.write_text(text, encoding="utf-8")
    print("Fixed series may-2027 head")


def main():
    for fname in PRODUCT_FILES:
        cleanup(ROOT / fname)
    fix_series_may_head()


if __name__ == "__main__":
    main()

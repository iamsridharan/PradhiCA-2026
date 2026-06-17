#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = list(ROOT.glob("ca-final-abc-*.html"))

NOTE = (
    '          <p class="abc-pricing__note"><i class="fas fa-info-circle mr-1"></i>'
    "GST as applicable · Need help? "
    '<a href="registration.html">Enquiry</a> or '
    '<a href="https://api.whatsapp.com/send?phone=918072653948">WhatsApp</a></p>\n'
)

STICKY_TPL = """
  <div class="abc-product-sticky" role="navigation" aria-label="Quick links">
    <a href="#pricing" class="abc-product-sticky--gold">View pricing</a>
    <a href="{schedule}" class="abc-product-sticky--outline">Full schedule</a>
  </div>
"""


def schedule_for(name: str) -> str:
    return (
        "ca-final-test-schedule-may-2027.html"
        if "may-2027" in name or "may-2027" in name
        else "ca-final-test-schedule-nov-2026.html"
    )


def fix_file(path: Path):
    text = path.read_text(encoding="utf-8")
    orig = text
    name = path.name

    text = text.replace('class=\\"row align-items-center\\"', "")
    text = re.sub(r'<div\s*>\s*', "", text)
    text = re.sub(r'<div class="row align-items-center">\s*', "", text, count=1)

    # Remove redundant top h4 in pricing
    text = re.sub(
        r'\s*<div class="col-12 text-center mb-3">\s*'
        r'<h4>(?:CA Final|FINAL Exam)[^<]*</h4>\s*</div>\s*',
        "\n",
        text,
        flags=re.I,
    )

    # Subsection titles
    def sub_repl(m):
        return (
            '<div class="col-12 abc-price-block"><h3 class="abc-price-block__title">'
            + m.group(1)
            + "</h3></div>\n          <div class=\"row abc-price-grid\">"
        )

    text = re.sub(
        r'<div class="col-12 text-center mb-3">\s*<h4>(ABC[^<]*)</h4>\s*</div>',
        sub_repl,
        text,
        flags=re.I,
    )
    # ABC DIRECT - / ABC ONLINE- variants
    text = re.sub(
        r'<div class="col-12 text-center mb-3">\s*'
        r'<h4>ABC (DIRECT|ONLINE)\s*-\s*<span class="text-primary">\s*([^<]+)</span></h4>\s*</div>',
        lambda m: (
            f'<div class="col-12 abc-price-block"><h3 class="abc-price-block__title">'
            f'ABC {m.group(1).title()} — <span class="text-primary">{m.group(2).strip()}</span></h3></div>\n'
            f'          <div class="row abc-price-grid">'
        ),
        text,
        flags=re.I,
    )

    # Wrap features: remove col-12 wrapper
    text = re.sub(
        r'<div class="col-12">\s*<ul class="pg-single__features">',
        '<ul class="pg-single__features">',
        text,
        count=1,
    )
    text = re.sub(
        r'</ul>\s*</div>\s*(?=\s*<div class="col-12 abc-price-block">|\s*<div class="row abc-price-grid">|\s*<div class="col-md-4)',
        "</ul>\n",
        text,
        count=1,
    )

    # First card row grid
    if "abc-price-grid" not in text and "col-md-4" in text:
        text = re.sub(
            r'(</ul>\s*)\n(\s*<div class="col-md-4)',
            r'\1\n          <div class="row abc-price-grid">\n\2',
            text,
            count=1,
        )

    # Close grid before next price block
    text = re.sub(
        r'(</div>\s*</div>\s*</div>\s*)\n(\s*<div class="col-12 abc-price-block")',
        r"\1\n          </div>\n\2",
        text,
    )

    # Remove inline style if premium css linked
    if "abc-product-premium.css" in text:
        text = re.sub(r"\s*<style>.*?</style>\s*", "\n", text, flags=re.DOTALL)

    # Ensure CSS links
    if "abc-product-premium.css" not in text and "abc-pricing" in text:
        text = text.replace(
            '<link rel="stylesheet" href="assets/css/header-premium.css">',
            '<link rel="stylesheet" href="assets/css/header-premium.css">\n'
            '    <link rel="stylesheet" href="assets/css/abc-series-hub-premium.css">\n'
            '    <link rel="stylesheet" href="assets/css/abc-product-premium.css">',
        )

    # Body class for product pages
    if "abc-pricing" in text and "pg-abc-product" not in text:
        mode = "online" if "online" in name else "direct"
        text = re.sub(
            r"<body[^>]*>",
            f'<body class="pg-abc-home pg-abc-home--final pg-abc-product pg-abc-product--{mode}">',
            text,
            count=1,
        )

    # Series pages body
    if "abc-section" in text and "choose-abc" in text and "pg-abc-home" not in text:
        text = re.sub(r"<body[^>]*>", '<body class="pg-abc-home pg-abc-home--final">', text, count=1)

    # Pricing note
    if "abc-pricing" in text and "abc-pricing__note" not in text:
        text = text.replace(
            "\n      </div> <!-- END row-->\n    </div> <!-- END container-->\n  </section>",
            "\n" + NOTE + "        </div>\n      </div>\n    </div>\n  </section>",
            1,
        )
        # fallback close pattern
        if "abc-pricing__note" not in text:
            text = re.sub(
                r"(\n\s*</div>\s*<!-- END row-->\s*\n\s*</div>\s*<!-- END container-->\s*\n</section>)",
                "\n" + NOTE + "        </div>\n      </div>\n    </div>\n  </section>",
                text,
                count=1,
            )

    # Fix broken section close for product pages - ensure col-lg-11 closes
    if "abc-pricing" in text:
        text = re.sub(
            r"</section>\s*(?:</div>\s*<!-- END row-->\s*)+"
            r"(?:</div>\s*<!-- END container-->\s*)?</section>",
            "</section>",
            text,
        )
        # Before footer, ensure proper wrapper close if note exists but missing divs
        if "abc-pricing__note" in text:
            m = re.search(r"abc-pricing__note.*?</p>\s*", text)
            if m and "        </div>\n      </div>\n    </div>\n  </section>" not in text[m.end() : m.end() + 80]:
                text = text.replace(
                    m.group(0),
                    m.group(0)
                    + "        </div>\n      </div>\n    </div>\n  </section>\n",
                    1,
                )

    # Sticky bar
    if "abc-pricing" in text and "abc-product-sticky" not in text:
        sched = schedule_for(name)
        text = text.replace(
            "\n<footer class=\"site-footer\">",
            STICKY_TPL.format(schedule=sched) + "\n\n<footer class=\"site-footer\">",
        )

    # Duplicate section / orphan closes
    text = re.sub(
        r'(</section>)\s*</div>\s*(?:</div>\s*){0,3}</section>',
        r"\1",
        text,
    )
    text = re.sub(
        r'</section>\s*</div>\s*</div>\s*</section>',
        "</section>",
        text,
    )

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print(f"Fixed: {name}")


def main():
    for p in FILES:
        fix_file(p)


if __name__ == "__main__":
    main()

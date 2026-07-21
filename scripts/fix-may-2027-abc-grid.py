#!/usr/bin/env python3
"""Normalize May 2027 Final ABC pricing grids and fix broken section markup."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    "ca-final-abc-direct-may-2027.html",
    "ca-final-abc-direct-with-model-may-2027.html",
    "ca-final-abc-online-may-2027.html",
    "ca-final-abc-online-with-model-may-2027.html",
]

COL_OPEN = re.compile(r'<div class="col-md-4 mt-4">\s*', re.IGNORECASE)


def card_wrapper_class(card_html: str) -> str:
    if (
        'badge-primary">Popular' in card_html
        or "card--featured" in card_html
        or "Best Value" in card_html
    ):
        return "abc-price-card abc-price-card--popular"
    return "abc-price-card"


def normalize_grid_markup(text: str) -> str:
    text = text.replace('class="row abc-price-grid"', 'class="abc-price-grid"')

    parts = COL_OPEN.split(text)
    if len(parts) == 1:
        return text

    out = [parts[0]]
    for chunk in parts[1:]:
        close_idx = chunk.rfind("</div>")
        if close_idx == -1:
            out.append(chunk)
            continue
        # Strip trailing wrapper close for col-md-4
        inner = chunk[:close_idx].rstrip()
        tail = chunk[close_idx:]
        wrapper = card_wrapper_class(inner)
        out.append(f'<div class="{wrapper}">\n{inner}\n     </div>{tail}')
    return "".join(out)


def fix_broken_section_closings(text: str) -> str:
    # Remove duplicate section/container closings after abc-pricing section
    text = re.sub(
        r'(</section>)\s*</div>\s*<!-- END container-->\s*</section>',
        r"\1",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r'(</section>)\s*</div>\s*</div>\s*</div>\s*</section>',
        r"\1",
        text,
    )
    return text


def main() -> None:
    for fname in PAGES:
        path = ROOT / fname
        if not path.exists():
            print(f"SKIP missing: {fname}")
            continue
        original = path.read_text(encoding="utf-8")
        updated = fix_broken_section_closings(normalize_grid_markup(original))
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            cols = len(re.findall(r'class="abc-price-card', updated))
            print(f"Fixed: {fname} ({cols} price cards)")
        else:
            print(f"No changes: {fname}")


if __name__ == "__main__":
    main()

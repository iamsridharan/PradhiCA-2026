#!/usr/bin/env python3
"""Convert legacy test-schedule tab panes (media/iconbox) to premium bento panels."""
from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    ROOT / "ca-foundation-test-schedule-may-2026.html",
    ROOT / "ca-final-test-schedule-may-2027.html",
    ROOT / "ca-inter-test-schedule-jan-2027.html",
]

ICON_MAP = {
    "ti-direction": "fa-sliders-h",
    "ti-calendar": "fa-clipboard-list",
    "ti-timer": "fa-clock",
    "ti-pencil-alt": "fa-chart-bar",
    "ti-map-alt": "fa-map-marker-alt",
    "ti-book": "fa-user-graduate",
    "ti-layout-cta-right": "fa-clock",
    "ti-user": "fa-map-marker-alt",
    "ti-wallet": "fa-rupee-sign",
}

TITLE_ICON = {
    "compatibility": "fa-sliders-h",
    "flexible structure": "fa-sitemap",
    "flexible registration": "fa-sliders-h",
    "subject-wise control": "fa-sliders-h",
    "exam pattern": "fa-clipboard-list",
    "icai pattern": "fa-clipboard-check",
    "icai standard": "fa-clipboard-check",
    "timings": "fa-clock",
    "exam timings": "fa-clock",
    "flexible timings": "fa-clock",
    "sunday sessions": "fa-clock",
    "customized scheduling": "fa-clock",
    "write at your pace": "fa-clock",
    "two batch options": "fa-calendar-week",
    "results": "fa-chart-bar",
    "quick results": "fa-chart-line",
    "mode": "fa-map-marker-alt",
    "exam mode": "fa-map-marker-alt",
    "dual mode": "fa-map-marker-alt",
    "personal attention": "fa-user-graduate",
    "dedicated mentorship": "fa-user-graduate",
    "guidance": "fa-user-graduate",
}

TAB_SERIES = {
    "Tabsabc": ("fa-star", None),
    "Tabsdot": ("fa-walking", "linear-gradient(135deg,#ea580c,#c2410c)"),
    "Tabsdot1": ("fa-bolt", "linear-gradient(135deg,#7c3aed,#5b21b6)"),
    "Tabsdot2": ("fa-forward", "linear-gradient(135deg,#7c3aed,#5b21b6)"),
    "Tabsdot3": ("fa-rocket", "linear-gradient(135deg,#0891b2,#0e7490)"),
    "Tabsdot6": ("fa-rocket", "linear-gradient(135deg,#0891b2,#0e7490)"),
    "Tabsrapid": ("fa-fast-forward", "linear-gradient(135deg,#059669,#047857)"),
    "Tabssingle2": ("fa-fast-forward", "linear-gradient(135deg,#059669,#047857)"),
    "Tabssingle": ("fa-book-open", "linear-gradient(135deg,#d97706,#b45309)"),
    "Tabsmodel": ("fa-trophy", "linear-gradient(135deg,#dc2626,#b91c1c)"),
}

TAB_LABEL_FIX = {
    "Tabsdot2": ("DOT 4.0", "fa-forward"),
}


def strip_tags(text: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_lib.unescape(re.sub(r"\s+", " ", text)).strip()
    return text


def ti_to_fa(icon_class: str) -> str:
    for ti, fa in ICON_MAP.items():
        if ti in icon_class:
            return fa
    m = re.search(r"fa[srb]?\s+([\w-]+)", icon_class)
    if m and m.group(1) != "check":
        return m.group(1)
    return "fa-check"


def title_to_fa(title: str) -> str:
    low = title.lower().strip()
    for key, fa in TITLE_ICON.items():
        if key in low:
            return fa
    return "fa-check"


def normalize_cta_icon(icon: str, label: str) -> str:
    low = label.lower()
    if "rupee" in icon or "wallet" in icon or low in {"fee", "fee details", "fee structure"}:
        return "fa-rupee-sign"
    if "calendar" in icon or "schedule" in low or "batch" in low:
        return "fa-calendar-alt" if "alternative" not in low else "fa-calendar-alt"
    if "weekend" in low:
        return "fa-calendar-week"
    if "register" in low:
        return "fa-user-plus"
    return ti_to_fa(icon)


def extract_features(pane: str) -> list[tuple[str, str, str]]:
    """Return list of (icon_fa, title, description)."""
    features: list[tuple[str, str, str]] = []

    for m in re.finditer(
        r'<div class="feature-card">(.*?)</div>\s*</div>',
        pane,
        re.S | re.I,
    ):
        block = m.group(1)
        icon_m = re.search(r'<i class="([^"]+)"', block)
        title_m = re.search(r'<h4 class="feature-title">(.*?)</h4>', block, re.S)
        desc_m = re.search(r'<p class="feature-description">(.*?)</p>', block, re.S)
        if title_m and desc_m:
            features.append(
                (
                    ti_to_fa(icon_m.group(1) if icon_m else ""),
                    strip_tags(title_m.group(1)),
                    desc_m.group(1).strip(),
                )
            )

    for m in re.finditer(
        r'<div class="media[^"]*">(.*?)</div>\s*</div>',
        pane,
        re.S | re.I,
    ):
        block = m.group(0)
        if "feature-title" in block:
            continue
        icon_m = re.search(r'<i class="([^"]+)"', block)
        title_m = re.search(r"<h5[^>]*>(.*?)</h5>", block, re.S)
        desc_m = re.search(r"<p[^>]*>(.*?)</p>", block, re.S)
        if title_m and desc_m:
            title = strip_tags(title_m.group(1))
            icon = ti_to_fa(icon_m.group(1) if icon_m else "")
            if icon == "fa-check":
                icon = title_to_fa(title)
            features.append((icon, title, desc_m.group(1).strip()))

    return features[:6]


def extract_cta_links(pane: str) -> list[tuple[str, str, str]]:
    """Return (href, icon_class_suffix, label)."""
    links: list[tuple[str, str, str]] = []
    for m in re.finditer(r'<a href="([^"]+)"([^>]*)>(.*?)</a>', pane, re.S | re.I):
        href = m.group(1)
        attrs = m.group(2)
        inner = m.group(3)
        if "btn" not in attrs and "action-btn" not in attrs:
            continue
        label = strip_tags(inner)
        if not label or label.lower() in {"fee", "schedule", "register now"}:
            pass
        icon_m = re.search(r'<i class="([^"]+)"', inner)
        icon = icon_m.group(1) if icon_m else ""
        if not icon:
            low = label.lower()
            if "fee" in low or "weekend" in low:
                icon = "fas fa-rupee-sign"
            elif "schedule" in low or "alternative" in low or "batch" in low:
                icon = "fas fa-calendar-alt"
            else:
                icon = "fas fa-user-plus"
        links.append((href, icon, label))

    # Deduplicate while preserving order
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for item in links:
        if item[0] not in seen:
            seen.add(item[0])
            out.append(item)
    return out[:3]


def extract_header_info(pane: str, tab_id: str) -> tuple[str, str, list[str]]:
    title = ""
    subtitle = ""
    badges: list[str] = []

    if "tab-header" in pane:
        tm = re.search(r'<h3 class="test-series-title">(.*?)</h3>', pane, re.S)
        sm = re.search(r'<p class="test-series-subtitle">(.*?)</p>', pane, re.S)
        if tm:
            title = strip_tags(tm.group(1))
        if sm:
            subtitle = strip_tags(sm.group(1))
        for bm in re.finditer(
            r'<span class="status-badge[^"]*">.*?<i class="[^"]+"></i>([^<]+)</span>',
            pane,
            re.S,
        ):
            badges.append(strip_tags(bm.group(1)))
        return title, subtitle, badges

    badge_m = re.search(r'<span class="badge[^"]*">([^<]+)</span>', pane, re.I)
    if badge_m:
        badges.append(strip_tags(badge_m.group(1)))

    h4_m = re.search(r'<h4[^>]*>(.*?)</h4>', pane, re.S | re.I)
    if h4_m:
        raw = h4_m.group(1)
        fonts = re.findall(r'<font[^>]*color="([^"]*)"[^>]*>(.*?)</font>', raw, re.S | re.I)
        if fonts:
            for color, text in fonts:
                txt = strip_tags(text)
                if not txt:
                    continue
                color_l = (color or "").lower()
                if color_l in {"red", "#ff0000"} and ("concession" in txt.lower() or "registration" in txt.lower()):
                    badges.append(txt)
                elif not title:
                    title = txt
                elif not subtitle and txt != title:
                    subtitle = txt
        else:
            title = strip_tags(raw)

    muted_m = re.search(r'<p class="text-muted[^"]*">([^<]+)</p>', pane, re.I)
    if muted_m and not subtitle:
        subtitle = strip_tags(muted_m.group(1))

    return title, subtitle, badges


def extract_intro(pane: str) -> str:
    if "feature-description-text" in pane:
        m = re.search(
            r'<p class="feature-description-text">(.*?)</p>',
            pane,
            re.S,
        )
        if m:
            return m.group(1).strip()

    for pat in (
        r'<p class="text-center">(.*?)</p>',
        r'<p class="mt-3 lead">(.*?)</p>',
    ):
        m = re.search(pat, pane, re.S | re.I)
        if m:
            text = m.group(1).strip()
            if len(strip_tags(text)) > 30:
                return text
    return ""


def cta_class(icon: str, label: str) -> str:
    low = label.lower()
    if "rupee" in icon or low == "fee" or "fee" in low:
        return "action-btn btn-fee"
    if "calendar" in icon or "schedule" in low or "batch" in low:
        return "action-btn btn-schedule"
    return "action-btn"


def build_feature_card(icon: str, title: str, desc: str, grad: str | None) -> str:
    style = f' style="background:{grad};"' if grad else ""
    return (
        f'                <div class="ts-feature-card"><div class="ts-feature-card__inner feature-card">'
        f'<div class="feature-icon"{style}><i class="fas {icon}"></i></div>'
        f'<h4 class="feature-title">{html_lib.escape(title)}</h4>'
        f'<p class="feature-description">{desc}</p></div></div>\n'
    )


def polish_pane(pane: str) -> str:
    def fix_card(m: re.Match[str]) -> str:
        block = m.group(0)
        title_m = re.search(r'<h4 class="feature-title">([^<]+)</h4>', block)
        if not title_m:
            return block
        fa = title_to_fa(title_m.group(1))
        return re.sub(
            r'<div class="feature-icon"([^>]*)><i class="fas [^"]+"></i></div>',
            f'<div class="feature-icon"\\1><i class="fas {fa}"></i></div>',
            block,
            count=1,
        )

    pane = re.sub(
        r'<div class="ts-feature-card">.*?</div></div>',
        fix_card,
        pane,
        flags=re.S,
    )
    pane = re.sub(
        r'<i class="fas ti-[^"]+"',
        lambda m: '<i class="fas fa-rupee-sign"' if "wallet" in m.group(0) else '<i class="fas fa-calendar-alt"',
        pane,
    )
    pane = re.sub(r'<p class="test-series-subtitle">-\s*', '<p class="test-series-subtitle">', pane)
    pane = re.sub(
        r'(<span class="status-badge[^"]*">.*?<i class="[^"]+"></i>)-\s*',
        r"\1",
        pane,
        flags=re.S,
    )
    title_m = re.search(r'<h3 class="test-series-title">([^<]+)</h3>', pane)
    if title_m:
        title = html_lib.unescape(title_m.group(1)).strip().lower()
        badge_m = re.search(r'<div class="status-badges">(.*?)</div>', pane, re.S)
        if badge_m and title and title in strip_tags(badge_m.group(1)).lower():
            pane = re.sub(r'\s*<div class="status-badges">.*?</div>\s*\n', "\n", pane, count=1, flags=re.S)
    return pane


def build_pane(tab_id: str, pane: str, active: bool) -> str:
    if "ts-feature-bento" in pane and "tab-header" in pane and "ts-cta-strip" in pane:
        pane = polish_pane(pane)
        # Already fully premium — normalize active class only
        pane = re.sub(r'\bshow active\b|\bactive show\b', "", pane)
        pane = re.sub(r'class="tab-pane fade(?: show)?"', 'class="tab-pane fade"', pane)
        if active:
            pane = re.sub(
                r'(<div class="tab-pane fade)(")',
                r'\1 show active\2',
                pane,
                count=1,
            )
        return polish_pane(pane)

    series_icon, grad = TAB_SERIES.get(tab_id, ("fa-star", None))
    title, subtitle, badges = extract_header_info(pane, tab_id)
    intro = extract_intro(pane)
    features = extract_features(pane)
    ctas = extract_cta_links(pane)

    if not title:
        label, _ = TAB_LABEL_FIX.get(tab_id, (tab_id.replace("Tabs", ""), series_icon))
        title = label

    header_icon_style = f' style="background:{grad};"' if grad else ""
    badge_html = ""
    if badges:
        badge_html = '              <div class="status-badges">\n'
        for i, b in enumerate(badges[:3]):
            icons = ["fa-user-plus", "fa-laptop", "fa-clock"]
            badge_html += (
                f'                <span class="status-badge {"registration" if i == 0 else "active" if i == 1 else "upcoming"}">'
                f'<i class="fas {icons[i % 3]}"></i>{html_lib.escape(b)}</span>\n'
            )
        badge_html += "              </div>\n"

    subtitle_html = (
        f'              <p class="test-series-subtitle">{html_lib.escape(subtitle)}</p>\n'
        if subtitle
        else ""
    )

    bento = '              <div class="ts-feature-bento">\n'
    for icon, ft, desc in features:
        if icon == "fa-check":
            icon = title_to_fa(ft)
        bento += build_feature_card(icon, ft, desc, grad)
    bento += "              </div>"

    cta_strip = '              <div class="ts-cta-strip">\n'
    for href, icon, label in ctas:
        cls = cta_class(icon, label)
        target = (
            ' target="_blank" rel="noopener noreferrer"'
            if href.lower().endswith((".pdf", ".jpg", ".jpeg", ".png"))
            or "Schedules_" in href
            else ""
        )
        if "register" in label.lower() and href.endswith(".html"):
            target = ""
        fa = normalize_cta_icon(icon, label)
        cta_strip += (
            f'                <a href="{href}"{target} class="{cls}">'
            f'<i class="fas {fa}" aria-hidden="true"></i> {html_lib.escape(label)}</a>\n'
        )
    cta_strip += "              </div>"

    active_cls = " show active" if active else ""
    aria = f' aria-labelledby="tab-{tab_id}"' if tab_id else ""

    return polish_pane(f"""          <div class="tab-pane fade{active_cls}" id="{tab_id}" role="tabpanel"{aria}>
            <div class="tab-header">
              <div class="test-series-icon"{header_icon_style}><i class="fas {series_icon}"></i></div>
              <h3 class="test-series-title">{html_lib.escape(title)}</h3>
{subtitle_html}{badge_html}            </div>
            <div class="features-grid">
              <p class="feature-description-text">{intro}</p>
{bento}            </div>
            <div class="action-buttons text-center">
              <h4>Ready to Get Started?</h4>
{cta_strip}            </div>
          </div>""")


def fix_duplicate_dot_labels(html: str) -> str:
    """Fix Tabsdot2 mislabeled as DOT 2.0 in hero jumps and series rail."""
    html = re.sub(
        r'(<a[^>]*href="#Tabsdot2"[^>]*id="tab-Tabsdot2"[^>]*><i class="fas )fa-bolt("[^>]*></i>\s*)DOT 2\.0',
        r"\1fa-forward\2DOT 4.0",
        html,
        flags=re.S,
    )
    html = re.sub(
        r'(<a href="#Tabsdot2" class="ts-hero__jump[^"]*"[^>]*><i class="fas )fa-bolt("[^>]*></i>\s*)DOT 2\.0',
        r"\1fa-forward\2DOT 4.0",
        html,
        flags=re.S,
    )
    return html


def get_default_tab_id(text: str, panes: list[tuple[str, str, bool]]) -> str:
    active_ids = [tid for tid, _, act in panes if act]
    if active_ids:
        return active_ids[0]

    for pat in (
        r'<a class="nav-link active is-current"[^>]*href="#(Tabs[^"]+)"',
        r'<a[^>]*class="[^"]*ts-hero__jump is-active[^"]*"[^>]*href="#(Tabs[^"]+)"',
        r'data-ts-default-tab="#(Tabs[^"]+)"',
    ):
        m = re.search(pat, text, re.I)
        if m:
            return m.group(1)

    return panes[0][0] if panes else "Tabsabc"


def extract_tab_panes_with_active(text: str) -> list[tuple[str, str, bool]]:
    ids = []
    for m in re.finditer(r'<div class="tab-pane[^>]*\bid="(Tabs[^"]+)"', text, re.I):
        tid = m.group(1)
        if tid not in ids:
            ids.append(tid)

    panes: list[tuple[str, str, bool]] = []
    for tid in ids:
        start_m = re.search(rf'<div class="tab-pane[^>]*\bid="{re.escape(tid)}"', text, re.I)
        if not start_m:
            continue
        rest = text[start_m.end() :]
        next_m = re.search(r'<div class="tab-pane', rest)
        modal_m = re.search(r'<div class="modal\b', rest)
        end = len(rest)
        if next_m:
            end = min(end, next_m.start())
        if modal_m:
            end = min(end, modal_m.start())
        chunk = text[start_m.start() : start_m.end() + end]
        active = bool(re.search(r'\bshow\s+active\b|\bactive\s+show\b', start_m.group(0)))
        panes.append((tid, chunk, active))
    return panes


def upgrade_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    panes = extract_tab_panes_with_active(text)

    if not panes:
        print(f"SKIP {path.name}: no tab panes")
        return

    default_active = get_default_tab_id(text, panes)

    new_panes = []
    for tid, chunk, _ in panes:
        is_active = tid == default_active
        new_panes.append(build_pane(tid, chunk, is_active))

    new_content = "\n\n".join(new_panes) + "\n"

    text = re.sub(
        r'(<div class="tab-content">)\s*.*?\s*(</div>\s*</div>\s*</div>\s*</section>)',
        rf"\1\n{new_content}      \2",
        text,
        count=1,
        flags=re.S,
    )

    text = fix_duplicate_dot_labels(text)
    path.write_text(text, encoding="utf-8")
    print(f"Upgraded: {path.name} ({len(panes)} panels)")


def main() -> None:
    for path in TARGETS:
        upgrade_file(path)
    print("Done.")


if __name__ == "__main__":
    main()

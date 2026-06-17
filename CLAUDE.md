# CLAUDE.md — PradhiCA 2026 Project

This file gives AI assistants (Claude, Copilot, etc.) all the context needed to work effectively on this codebase.

---

## Project Overview

**PradhiCA** is India's premier CA (Chartered Accountancy) test series platform. The site consists of ~160 static HTML pages served at **https://pradhica.com**. There is no build system — all files are plain HTML, Bootstrap 4, and custom CSS.

- **Founded:** 2019  
- **Students:** 7500+ across India  
- **Primary centre:** Chennai, Tamil Nadu  
- **GitHub:** `https://github.com/iamsridharan/PradhiCA-2026` (branch: `main`)

---

## File Naming Convention

All root-level HTML files follow a strict slug pattern:

```
ca-{level}-{type}-{mode}-{batch}.html
```

| Segment | Values |
|---------|--------|
| `level` | `foundation`, `inter`, `final` |
| `type` | `abc`, `dot-marathon`, `dot-2`, `dot-3`, `rapid-revision`, `single-subject`, `model`, `test-schedule`, `abc-series`, `dot-marathon-series`, etc. |
| `mode` | `direct`, `online`, `direct-with-model`, `online-with-model`, `series`, `registration` |
| `batch` | `may-2026`, `sep-2026`, `jan-2027`, `nov-2026`, `may-2027` |

**Examples:**
- `ca-inter-abc-direct-sep-2026.html` — CA Inter ABC test series, direct (Chennai centre) payment, Sep 2026 batch
- `ca-final-dot-marathon-online-nov-2026.html` — CA Final DOT Marathon, online payment, Nov 2026 batch
- `ca-inter-test-schedule-jan-2027.html` — CA Inter test schedule hub for Jan 2027 batch

---

## Active Batches (as of Apr 2026)

| Level | Active Batches |
|-------|---------------|
| CA Foundation | May 2026 |
| CA Intermediate | May 2026, Sep 2026, Jan 2027 |
| CA Final | May 2026, Sep 2026 (limited), Nov 2026, Jan 2027, May 2027 |

**Nav menu links** (Test Series dropdown in all pages):
- Foundation May 26 → `ca-foundation-test-schedule-may-2026.html`
- Final May 26 → `ca-final-test-schedule-may-2026.html`
- Final Nov 26 → `ca-final-test-schedule-nov-2026.html`
- Final May 27 → `ca-final-test-schedule-may-2027.html`
- Inter May 26 → `ca-inter-test-schedule-may-2026.html`
- Inter Sep 26 → `ca-inter-test-schedule-sep-2026.html`
- Inter Jan 27 → `ca-inter-test-schedule-jan-2027.html`

---

## CSS Architecture

All premium CSS lives in `assets/css/`. Each file targets a specific page type.

| File | Used on |
|------|---------|
| `header-premium.css` | All pages — top bar + `ec-nav` sticky nav |
| `footer-premium.css` | All pages — site footer |
| `home-premium.css` | `index.html` only |
| `test-schedule-premium.css` | All `*-test-schedule-*.html` pages |
| `style.css` | Global base (Bootstrap customisations) |
| `course-overview-premium.css` | `course-overview.html` |
| `contact-page-premium.css` | `contact-us.html` |
| `registration-page-premium.css` | `registration.html` |
| `registration-hub-premium.css` | Multi-series registration hubs |

Payment pages also embed a large inline `<style>` block inside `<head>` for pricing-specific components (see Payment Page Design section below).

---

## Canonical Header + Nav

Every page (except `index.html`) uses the **same header/nav block** — it must not be changed per-page. The canonical block lives in `ca-inter-dot-marathon-direct-sep-2026.html` and was propagated to all 157 root HTML files via script.

```html
<header class="site-header bg-dark text-white-0_5">
  <!-- top bar: email, phone, social icons -->
</header>

<nav class="ec-nav sticky-top bg-white">
  <div class="container">
    <div class="navbar p-0 navbar-expand-lg">
      <!-- logo, hamburger, collapse div with ul.nav.ec-nav__navbar -->
      <!-- Test Series dropdown: Foundation May 26, Final May/Nov 26, Final May 27, Inter May/Sep 26, Inter Jan 27 -->
    </div>
  </div>
</nav>
```

**To update the nav across all pages**, edit the canonical block in one reference file, then run the Python propagation script (see Maintenance Scripts).

---

## Payment Page Design System

Payment pages (all `*-direct-*.html`, `*-online-*.html`, `*-with-model-*.html` files) follow the "DOT-style premium" design. Key CSS classes (defined inline in each payment page's `<style>` block):

| Class | Purpose |
|-------|---------|
| `.pg-pay-hero` | Full-width gradient hero banner (indigo for Direct, teal for Online) |
| `.pg-pay-badge` | Frosted-glass pill badge ("Direct mode", "Razorpay") |
| `.pg-pay-trust` | Trust row with check icons below the hero |
| `.pg-pay-intro` | Rounded white intro card with nav action buttons |
| `.pg-pay-actions` | Flex row of back/switch/schedule pill buttons |
| `.pg-single` | Pricing section wrapper (teal gradient background) |
| `.pg-single__tier` | Pill-style tier label ("INTER EXAM · ABC DIRECT · WITHOUT MODEL") |
| `.pg-single__features` | CSS grid feature checklist |
| `.pg-price-card` | Individual pricing card (hover lift, gradient top bar) |
| `.pg-price-col--featured` | Featured column wrapper — adds "Popular" ribbon via `::after` |
| `.pg-venue-block` | Dark indigo card with Chennai address — used on **Direct** pages only |
| `.pg-online-block` | Dark teal card with online support message — used on **Online** pages only |

**Hero gradient colours:**
- **Direct pages** — indigo: `linear-gradient(128deg, #0c1222, #1e1b4b, #312e81, #1d4ed8)`
- **Online pages** — teal: `linear-gradient(128deg, #042f2e, #0f766e, #115e59, #0d9488)`

**Fonts:** DM Sans (800 weight primary), Maven Pro, Work Sans — loaded via Google Fonts on payment pages.

---

## Test Series Types & Pricing Tiers

### ABC Test Series (All levels)
- Without model: 1 Paper / 2 Paper / Group 1 or 2 / Both Groups
- With model: same tiers with model exam bundled in

### DOT Marathon
- Without model: Both Groups / Group I or II / 2 Papers
- With 1 Model: Both Groups / Group I or II / 2 Papers
- With 2 Models: Both Groups / Group I or II / 2 Papers

### Rapid Revision
- 1 Paper / 2 Paper / Group 1 or 2 / Both Groups

### Single Subject
- Without model / With model variants

### Model Exams
- Set 1 / Set 2 / Set 3 (direct + online)

---

## Payment Provider

All payment buttons use **Razorpay embed buttons**:

```html
<div class="razorpay-embed-btn"
     data-url="https://rzp.io/rzp/XXXXXXXX"
     data-text="Proceed to Pay"
     data-color="#528FF0"
     data-size="large">
  <script>
    (function(){
      var d=document; var x=!d.getElementById('razorpay-embed-btn-js')
      if(x){ var s=d.createElement('script'); s.defer=!0;s.id='razorpay-embed-btn-js';
      s.src='https://cdn.razorpay.com/static/embed_btn/bundle.js';d.body.appendChild(s);}
      else{var rzp=window['__rzp__']; rzp && rzp.init && rzp.init()}
    })();
  </script>
</div>
```

**Never change Razorpay `data-url` values without explicit confirmation from the user.** Each URL is tied to a specific product/amount in Razorpay's dashboard.

---

## Schedules & Assets

- PDF schedules: `Schedules_2026/PradhiCA-CA {Level}-{Type}-{Batch}-Schedule.pdf`
- Banner images: `Schedules_2026/*.jpg`
- General images: `assets/img/`
- Logo: `assets/img/logo-black.png` (dark bg: `logo-white.png`)
- Favicon: `assets/img/favicon/favicon.ico`

---

## Contact Details (never change without user instruction)

| | |
|-|-|
| Email | pradhica4u@gmail.com |
| Phone | +91 80726 53948 |
| Address | No: 20, 1st floor, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu 600033 |
| Google Maps | https://maps.app.goo.gl/3scL1jiJsRZxtvYd9 |
| Facebook | http://bit.ly/fbpradhica |
| Instagram | http://bit.ly/inspradhica |
| Telegram | https://t.me/PradhiCA |

---

## Git Workflow

- Branch: `main` (single branch, direct commits)
- Remote: `https://github.com/iamsridharan/PradhiCA-2026.git`
- Commit and push after every meaningful set of changes
- Typical commit message format: `scope(type): short description`

---

## Maintenance Scripts

### Propagate header/nav to all pages
```python
import re
from pathlib import Path

ROOT = Path(".")  # run from project root
CANONICAL = """<header class="site-header ...">...</header>
<nav class="ec-nav ...">...</nav>
<!-- END site-search-->"""

PAT = re.compile(
    r'<header class="site-header bg-dark text-white-0_5">.*?</nav>\s*<!-- END ec-nav -->\s*(?:<!-- END site-search-->)?',
    re.DOTALL,
)
for path in ROOT.glob("*.html"):
    text = path.read_text()
    if '<header class="site-header' in text:
        path.write_text(PAT.sub(CANONICAL, text, count=1))
```

---

## Common Tasks

### Add a new payment page
1. Copy the closest existing payment page (same level + mode).
2. Update: `<title>`, meta description/keywords, OG/Twitter tags, canonical `<link>`, hero `h1` + breadcrumbs, `pg-pay-intro` action buttons, tier labels, Razorpay `data-url` and amounts.
3. Keep header/nav block **exactly identical** to the canonical.
4. For Direct pages add `pg-venue-block`; for Online pages add `pg-online-block`.

### Update pricing on a payment page
1. Find the `<h2 class="mb-0 display-4 text-success">` inside the target card.
2. Change the ₹ amount.
3. Do NOT change the Razorpay `data-url` unless the Razorpay link itself changes.

### Update nav dropdown across all pages
1. Edit the canonical nav in a reference payment page.
2. Run the propagation script above to push to all 157 root HTML files.

### Add a new schedule page
- Create `ca-{level}-test-schedule-{batch}.html`.
- Add it to the nav dropdown in the canonical header, then re-propagate.

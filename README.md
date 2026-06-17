# PradhiCA 2026

**India's Premier CA Test Series Platform** · Foundation, Intermediate & Final Mock Exams

[![Website](https://img.shields.io/badge/Website-pradhica.com-blue)](https://pradhica.com)
[![Founded](https://img.shields.io/badge/Founded-2019-green)](https://pradhica.com)
[![Students](https://img.shields.io/badge/Students-7500%2B-orange)](https://pradhica.com)

---

## About PradhiCA

**PradhiCA** (PradhiCA Test Series) is a leading educational organization offering ICAI-aligned mock examinations and test series for Chartered Accountancy (CA) students across India. Founded in 2019 with the tagline **"We Create Talented CA"**, we have helped **7500+ successful students** nationwide.

| Attribute | Details |
|-----------|---------|
| **Organization** | PradhiCA (PradhiCA Test Series) |
| **Type** | Educational – CA Test Series & Mock Exam Provider |
| **Founded** | 2019 |
| **Website** | [https://pradhica.com](https://pradhica.com) |
| **Primary Location** | Chennai, Tamil Nadu, India |
| **Service Area** | India (Chennai, Mumbai, Delhi, Hyderabad, Bangalore, Kochi, Tamil Nadu, Kerala, Andhra Pradesh, Telangana, Maharashtra, Karnataka) |

---

## Features

- **ICAI-Aligned Tests** – All mock exams follow official ICAI examination patterns
- **Dual Modes** – **Online** (remote) or **Direct** (in-person at Chennai centre)
- **Multiple Batches** – May 26, Sep 26, Jan 27 for different exam cycles
- **Expert Evaluation** – Professional assessment and feedback by qualified CAs
- **Adaptive Assessment** – Comprehensive preparation via scheduled, unscheduled, revision, and full-syllabus tests

---

## Test Series Types

| Type | Description |
|------|-------------|
| **ABC Test Series** | All-in-one test packages for comprehensive preparation |
| **DOT (Doubt of Topic)** | Topic-wise tests (DOT 2.0, DOT 3.0, DOT Marathon) |
| **Model Exams** | Full mock examinations mirroring ICAI pattern |
| **Rapid Revision** | Quick revision tests before exams |
| **Single Subject** | Subject-wise tests with or without model papers |

---

## Course Levels

| Level | Description |
|-------|-------------|
| **CA Foundation** | Entry-level CA exam preparation |
| **CA Intermediate** | Mid-level CA preparation |
| **CA Final** | Advanced CA final examination preparation |

---

## Site Structure

### Main Pages
| Page | URL |
|------|-----|
| Homepage | [index.html](https://pradhica.com/) |
| Course Overview | [course-overview.html](https://pradhica.com/course-overview.html) |
| Contact Us | [contact-us.html](https://pradhica.com/contact-us.html) |
| Registration / Enquiry | [registration.html](https://pradhica.com/registration.html) |
| Blog | [blog/index.php](https://pradhica.com/blog/) |
| Sitemap | [sitemap.html](https://pradhica.com/sitemap.html) |

### Test Schedules (Batch-wise)
| Batch | CA Final | CA Inter | CA Foundation |
|-------|----------|----------|---------------|
| May 26 | [ca-final-test-schedule-may-2026.html](https://pradhica.com/ca-final-test-schedule-may-2026.html) | [ca-inter-test-schedule-may-2026.html](https://pradhica.com/ca-inter-test-schedule-may-2026.html) | [ca-foundation-test-schedule-may-2026.html](https://pradhica.com/ca-foundation-test-schedule-may-2026.html) |
| Sep 26 | [ca-final-test-schedule-sep-2026.html](https://pradhica.com/ca-final-test-schedule-sep-2026.html) | [ca-inter-test-schedule-sep-2026.html](https://pradhica.com/ca-inter-test-schedule-sep-2026.html) | [ca-foundation-test-schedule-sep-2026.html](https://pradhica.com/ca-foundation-test-schedule-sep-2026.html) |
| Jan 27 | [ca-final-test-schedule-jan-2027.html](https://pradhica.com/ca-final-test-schedule-jan-2027.html) | [ca-inter-test-schedule-jan-2027.html](https://pradhica.com/ca-inter-test-schedule-jan-2027.html) | — |

### Policies
| Policy | URL |
|--------|-----|
| Terms & Conditions | [terms-and-conditions.html](https://pradhica.com/terms-and-conditions.html) |
| Privacy Policy | [privacy-policy.html](https://pradhica.com/privacy-policy.html) |
| Refund Policy | [refund-policy.html](https://pradhica.com/refund-policy.html) |

---

## Contact

| Channel | Details |
|---------|---------|
| **Phone** | +91 80726 53948 |
| **Email** | pradhica4u@gmail.com |
| **Address** | No: 20, 1st floor, Chakrapani St Ext, Rangarajapuram, West Mambalam, Chennai, Tamil Nadu 600033 |
| **Maps** | [Google Maps](https://maps.app.goo.gl/TyxXNAXrTxPPZhPT8) |
| **WhatsApp** | [Send message](https://api.whatsapp.com/send?phone=918072653948) |

### Social Media
| Platform | Link |
|----------|------|
| Facebook | [bit.ly/fbpradhica](http://bit.ly/fbpradhica) |
| Instagram | [bit.ly/inspradhica](http://bit.ly/inspradhica) |
| YouTube | [PradhiCA Channel](https://www.youtube.com/channel/UCf1poDZ0HqWowl5AbwH3UMQ) |
| Telegram | [t.me/PradhiCA](https://t.me/PradhiCA) |

---

## Technical Details

### Stack
- **Frontend**: Static HTML, CSS, JavaScript (Bootstrap 4–based theme)
- **Assets**: Font Awesome 5, Themify Icons, Owl Carousel, WOW.js
- **Analytics**: Google Analytics (UA-132037455-1)
- **Blog**: WordPress (at `/blog/`)

### Premium stylesheets (`assets/css/`)
Shared “premium” layers load **after** `vendors.bundle.css` and `style.css`:

| File | Used on / purpose |
|------|-------------------|
| `header-premium.css` | Sitewide navigation (sticky bar, dropdowns) |
| `footer-premium.css` | Sitewide footer + WhatsApp float |
| `home-premium.css` | **`index.html`** — hero, trust strip, welcome, announcements, test-series band, stats, testimonials, lightbox |
| `test-schedule-premium.css` | Test schedule pages with `body.pg-test-schedule` (optional `pg-test-schedule--sep26` for Sep batch accent) — tabs, hero, Fee/Schedule/Register CTA row |
| `registration-hub-premium.css` | Registration hub / multi-route flows where linked |
| `course-overview-premium.css` | Course overview + test-series section |
| `contact-page-premium.css` | Contact page |
| `registration-page-premium.css` | Registration / enquiry page variants |

**Homepage body class**: `class="pg-home"` (required for `home-premium.css`).

**Test schedule body classes** (example): `class="pg-test-schedule pg-test-schedule--sep26"`.

### Project Structure
```
├── index.html              # Homepage (premium hero + sections; home-premium.css)
├── course-overview.html    # Course journey + test series (premium layout)
├── ca-*-test-schedule-*.html  # batch hubs (Final/Inter/Foundation × May/Sep/Jan)
├── .htaccess                  # 301 redirects from legacy test-schedule-* URLs
├── docs/URL-MIGRATION.md
├── scripts/apply_url_renames.py
├── contact-us.html
├── registration.html
├── sitemap.xml             # XML sitemap (~160 root HTML URLs + home)
├── sitemap.html            # Human-readable sitemap
├── urllist.txt             # Categorized URL list + discovery links
├── robots.txt              # Crawler permissions + sitemap pointer
├── llms.txt                # AI/LLM manifest
├── assets/
│   ├── img/
│   ├── css/
│   │   ├── header-premium.css
│   │   ├── footer-premium.css
│   │   ├── home-premium.css
│   │   ├── test-schedule-premium.css
│   │   ├── registration-hub-premium.css
│   │   ├── course-overview-premium.css
│   │   ├── contact-page-premium.css
│   │   └── registration-page-premium.css
│   ├── js/
│   └── fonts/
├── blog/                   # WordPress blog
├── terms-and-conditions.html
├── privacy-policy.html
└── refund-policy.html
```

### SEO & AI Support
- **robots.txt** – Full permission for all crawlers including AI/LLM bots (GPTBot, ClaudeBot, PerplexityBot, etc.)
- **llms.txt** – Curated content for AI agents (organization info, key facts, primary links)
- **sitemap.xml** – Machine-readable sitemap for search engines

### URL renames (test schedule hubs)
Batch schedule pages use slugs like **`ca-{level}-test-schedule-{batch}.html`**. Legacy URLs **`test-schedule-*-May26.html`** (etc.) redirect via **`.htaccess`** (301) on Apache. See **[docs/URL-MIGRATION.md](docs/URL-MIGRATION.md)** and **`scripts/apply_url_renames.py`** for the mapping and future phases.

---

## Repository

| Item | Value |
|------|-------|
| **GitHub** | [github.com/iamsridharan/PradhiCA-2026](https://github.com/iamsridharan/PradhiCA-2026) |
| **Live Site** | [https://pradhica.com](https://pradhica.com) |

### Version History
| Version | Description |
|---------|-------------|
| v1.0.0 | Initial release |
| v1.1.0 | Jan27/Sep26 updates, new pages |
| v1.2.0 | AI/LLM crawler support (llms.txt, robots.txt) |
| v1.3.0 | Release |
| v2026.03-redesign | Premium header/footer sitewide; course overview + test-series UX; contact & registration refresh; sitemap/urllist/llms synced |
| **v2026.02-home-ts** | Homepage premium UI (`home-premium.css`); Final/Inter Sep26 schedules use `test-schedule-premium.css`; scroll/viewport fixes on homepage; lightbox `pageshow` safety |
| **v2026.04-url-slugs** | Renamed 8 batch test-schedule hubs to `ca-*-test-schedule-*.html`; global link updates; `.htaccess` 301s; [docs/URL-MIGRATION.md](docs/URL-MIGRATION.md) |
| **v2026.06-nov-final** | CA Final Nov 26 premium product pages (ABC, DOT 2.0, Marathon, Rapid Revision, Single Subject); global header sync; `abc-product-premium.css`; Nov batch schedule hub refresh |

---

## License

Copyright © 2026 PradhiCA. All rights reserved.

---

## Credits

- **PradhiCA** – CA Test Series & Mock Exam Provider  
- **Design & Development** – [Techrethought](https://techrethought.com)

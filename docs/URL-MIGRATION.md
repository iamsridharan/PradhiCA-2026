# URL migration (SEO slugs)

## Phase 1 — Batch test schedule hubs (done)

| Old URL | New URL |
|---------|---------|
| `test-schedule-final-May26.html` | `ca-final-test-schedule-may-2026.html` |
| `test-schedule-final-Sep26.html` | `ca-final-test-schedule-sep-2026.html` |
| `test-schedule-final-Jan27.html` | `ca-final-test-schedule-jan-2027.html` |
| `test-schedule-Inter-May26.html` | `ca-inter-test-schedule-may-2026.html` |
| `test-schedule-Inter-Sep26.html` | `ca-inter-test-schedule-sep-2026.html` |
| `test-schedule-Inter-Jan27.html` | `ca-inter-test-schedule-jan-2027.html` |
| `test-schedule-foundation-May26.html` | `ca-foundation-test-schedule-may-2026.html` |
| `test-schedule-foundation-Sep26.html` | `ca-foundation-test-schedule-sep-2026.html` |

- **Internal links** were updated across HTML, `sitemap.xml`, `sitemap.html`, `urllist.txt`, `llms.txt`, CSS/JS where referenced, and docs.
- **Apache**: root `.htaccess` provides **301 redirects** from old paths to new ones.  
  If you use **Nginx**, **Netlify**, or **Cloudflare**, add equivalent redirect rules there.

## Phase 2+ (not started)

Series homepages (`Inter-ABC-Homepage_*.html`, DOT/Model/Rapid pages, etc.) can be renamed in a follow-up using the same pattern: extend `scripts/apply_url_renames.py`, `git mv`, run the script, add redirects, resubmit sitemap in Search Console.

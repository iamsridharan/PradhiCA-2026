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

## Phase 2 — Program & policy pages (done)

| Old URL | New URL |
|---------|---------|
| `01-Final-new-wModel-Direct_Single_New-Jan27.html` | `ca-final-single-subject-direct-with-model-jan-2027.html` |
| `01-Final-new-wModel-Direct_Single_New-May26.html` | `ca-final-single-subject-direct-with-model-may-2026.html` |
| `01-Final-new-wModel-Direct_Single_New-Sep26.html` | `ca-final-single-subject-direct-with-model-sep-2026.html` |
| `01-Final-new-wModel-Online_Single_New-Jan27.html` | `ca-final-single-subject-online-with-model-jan-2027.html` |
| `01-Final-new-wModel-Online_Single_New-May26.html` | `ca-final-single-subject-online-with-model-may-2026.html` |
| `01-Final-new-wModel-Online_Single_New-Sep26.html` | `ca-final-single-subject-online-with-model-sep-2026.html` |
| `01-Final-new-woModel-Direct_Single_New-Jan27.html` | `ca-final-single-subject-direct-without-model-jan-2027.html` |
| `01-Final-new-woModel-Direct_Single_New-May26.html` | `ca-final-single-subject-direct-without-model-may-2026.html` |
| `01-Final-new-woModel-Direct_Single_New-Sep26.html` | `ca-final-single-subject-direct-without-model-sep-2026.html` |
| `01-Final-new-woModel-Online_Single_New-Jan27.html` | `ca-final-single-subject-online-without-model-jan-2027.html` |
| `01-Final-new-woModel-Online_Single_New-May26.html` | `ca-final-single-subject-online-without-model-may-2026.html` |
| `01-Final-new-woModel-Online_Single_New-Sep26.html` | `ca-final-single-subject-online-without-model-sep-2026.html` |
| `01-Inter-new-wModel-Direct_Single_New-Jan27.html` | `ca-inter-single-subject-direct-with-model-jan-2027.html` |
| `01-Inter-new-wModel-Direct_Single_New-May26.html` | `ca-inter-single-subject-direct-with-model-may-2026.html` |
| `01-Inter-new-wModel-Direct_Single_New-Sep26.html` | `ca-inter-single-subject-direct-with-model-sep-2026.html` |
| `01-Inter-new-wModel-Online_Single_New-Jan27.html` | `ca-inter-single-subject-online-with-model-jan-2027.html` |
| `01-Inter-new-wModel-Online_Single_New-May26.html` | `ca-inter-single-subject-online-with-model-may-2026.html` |
| `01-Inter-new-wModel-Online_Single_New-Sep26.html` | `ca-inter-single-subject-online-with-model-sep-2026.html` |
| `01-Inter-new-woModel-Direct_Single_New-Jan27.html` | `ca-inter-single-subject-direct-without-model-jan-2027.html` |
| `01-Inter-new-woModel-Direct_Single_New-May26.html` | `ca-inter-single-subject-direct-without-model-may-2026.html` |
| `01-Inter-new-woModel-Direct_Single_New-Sep26.html` | `ca-inter-single-subject-direct-without-model-sep-2026.html` |
| `01-Inter-new-woModel-Online_Single_New-Jan27.html` | `ca-inter-single-subject-online-without-model-jan-2027.html` |
| `01-Inter-new-woModel-Online_Single_New-May26.html` | `ca-inter-single-subject-online-without-model-may-2026.html` |
| `01-Inter-new-woModel-Online_Single_New-Sep26.html` | `ca-inter-single-subject-online-without-model-sep-2026.html` |
| `02-Final-Rapid-Revison-Direct-Jan27.html` | `ca-final-rapid-revision-direct-jan-2027.html` |
| `02-Final-Rapid-Revison-Direct-May26.html` | `ca-final-rapid-revision-direct-may-2026.html` |
| `02-Final-Rapid-Revison-Direct-Sep26.html` | `ca-final-rapid-revision-direct-sep-2026.html` |
| `02-Final-Rapid-Revison-Online--Jan27.html` | `ca-final-rapid-revision-online-jan-2027.html` |
| `02-Final-Rapid-Revison-Online--May26.html` | `ca-final-rapid-revision-online-may-2026.html` |
| `02-Final-Rapid-Revison-Online--Sep26.html` | `ca-final-rapid-revision-online-sep-2026.html` |
| `02-Inter-Rapid-Revison-Direct-Jan27.html` | `ca-inter-rapid-revision-direct-jan-2027.html` |
| `02-Inter-Rapid-Revison-Direct-May26.html` | `ca-inter-rapid-revision-direct-may-2026.html` |
| `02-Inter-Rapid-Revison-Direct-Sep26.html` | `ca-inter-rapid-revision-direct-sep-2026.html` |
| `02-Inter-Rapid-Revison-Online--Jan27.html` | `ca-inter-rapid-revision-online-jan-2027.html` |
| `02-Inter-Rapid-Revison-Online--May26.html` | `ca-inter-rapid-revision-online-may-2026.html` |
| `02-Inter-Rapid-Revison-Online--Sep26.html` | `ca-inter-rapid-revision-online-sep-2026.html` |
| `03-foundation-new-wModel-Direct_Single_New-May26.html` | `ca-foundation-single-subject-direct-with-model-may-2026.html` |
| `03-foundation-new-wModel-Online_Single_New-May26.html` | `ca-foundation-single-subject-online-with-model-may-2026.html` |
| `03-foundation-new-woModel-Direct_Single_New-May26.html` | `ca-foundation-single-subject-direct-without-model-may-2026.html` |
| `03-foundation-new-woModel-Online_Single_New-May26.html` | `ca-foundation-single-subject-online-without-model-may-2026.html` |
| `03-foundation-Rapid-Revison-Direct-May26.html` | `ca-foundation-rapid-revision-direct-may-2026.html` |
| `03-foundation-Rapid-Revison-Online-May26.html` | `ca-foundation-rapid-revision-online-may-2026.html` |
| `Final-ABC-Direct-With-model-Jan27.html` | `ca-final-abc-direct-with-model-jan-2027.html` |
| `Final-ABC-Direct-With-model-May26.html` | `ca-final-abc-direct-with-model-may-2026.html` |
| `Final-ABC-Direct-With-model-Sep26.html` | `ca-final-abc-direct-with-model-sep-2026.html` |
| `Final-ABC-Direct_Jan27.html` | `ca-final-abc-direct-jan-2027.html` |
| `Final-ABC-Direct_May26.html` | `ca-final-abc-direct-may-2026.html` |
| `Final-ABC-Direct_Sep26.html` | `ca-final-abc-direct-sep-2026.html` |
| `Final-ABC-Homepage_Jan27.html` | `ca-final-abc-series-jan-2027.html` |
| `Final-ABC-Homepage_May26.html` | `ca-final-abc-series-may-2026.html` |
| `Final-ABC-Homepage_Sep26.html` | `ca-final-abc-series-sep-2026.html` |
| `Final-ABC-Online-With-model-Jan27.html` | `ca-final-abc-online-with-model-jan-2027.html` |
| `Final-ABC-Online-With-model-May26.html` | `ca-final-abc-online-with-model-may-2026.html` |
| `Final-ABC-Online-With-model-Sep26.html` | `ca-final-abc-online-with-model-sep-2026.html` |
| `Final-ABC-Online_Jan27.html` | `ca-final-abc-online-jan-2027.html` |
| `Final-ABC-Online_May26.html` | `ca-final-abc-online-may-2026.html` |
| `Final-ABC-Online_Sep26.html` | `ca-final-abc-online-sep-2026.html` |
| `Final-Dot-2-May26-Homepage.html` | `ca-final-dot-2-series-may-2026.html` |
| `Final-dot-2.0-i-may26.html` | `ca-final-dot-2-0-i-may-2026.html` |
| `Final-dot-2.0-ii-may26.html` | `ca-final-dot-2-0-ii-may-2026.html` |
| `Final-Dot-3-May26-Homepage.html` | `ca-final-dot-3-series-may-2026.html` |
| `Final-Dot-Marathon-May26-Direct.html` | `ca-final-dot-marathon-direct-may-2026.html` |
| `Final-Dot-Marathon-May26-Homepage.html` | `ca-final-dot-marathon-series-may-2026.html` |
| `Final-Dot-Marathon-May26-Online.html` | `ca-final-dot-marathon-online-may-2026.html` |
| `Final-Dot-Marathon-Sep26-Direct.html` | `ca-final-dot-marathon-direct-sep-2026.html` |
| `Final-Dot-Marathon-Sep26-Homepage.html` | `ca-final-dot-marathon-series-sep-2026.html` |
| `Final-Dot-Marathon-Sep26-Online.html` | `ca-final-dot-marathon-online-sep-2026.html` |
| `Final-Model-1set_Direct_May26.html` | `ca-final-model-1-set-direct-may-2026.html` |
| `Final-Model-1set_Online_May26.html` | `ca-final-model-1-set-online-may-2026.html` |
| `Final-Model-2set_Direct_May26.html` | `ca-final-model-2-set-direct-may-2026.html` |
| `Final-Model-2set_Online_May26.html` | `ca-final-model-2-set-online-may-2026.html` |
| `Final-Model-3set_Direct_May26.html` | `ca-final-model-3-set-direct-may-2026.html` |
| `Final-Model-3set_Online_May26.html` | `ca-final-model-3-set-online-may-2026.html` |
| `Final-new-dot-3.0-i-jan26.html` | `ca-final-dot-3-0-i-jan-2026.html` |
| `Final-new-dot-3.0-i-may26.html` | `ca-final-dot-3-0-i-may-2026.html` |
| `Final-new-dot-3.0-ii-jan26.html` | `ca-final-dot-3-0-ii-jan-2026.html` |
| `Final-new-dot-3.0-ii-may26.html` | `ca-final-dot-3-0-ii-may-2026.html` |
| `Foundation-ABC-Direct-With-model-May26.html` | `ca-foundation-abc-direct-with-model-may-2026.html` |
| `Foundation-ABC-Direct_May26.html` | `ca-foundation-abc-direct-may-2026.html` |
| `Foundation-ABC-Homepage_May26.html` | `ca-foundation-abc-series-may-2026.html` |
| `Foundation-ABC-Online-With-model-May26.html` | `ca-foundation-abc-online-with-model-may-2026.html` |
| `Foundation-ABC-Online_May26.html` | `ca-foundation-abc-online-may-2026.html` |
| `foundation-dot2-Homepage-may26.html` | `ca-foundation-dot-2-series-may-2026.html` |
| `foundation-Dot2-May26-direct.html` | `ca-foundation-dot-2-direct-may-2026.html` |
| `foundation-Dot2-May26-online.html` | `ca-foundation-dot-2-online-may-2026.html` |
| `foundation-dot3-Homepage-May26.html` | `ca-foundation-dot-3-series-may-2026.html` |
| `foundation-Dot3-May26-direct.html` | `ca-foundation-dot-3-direct-may-2026.html` |
| `foundation-Dot3-May26-online.html` | `ca-foundation-dot-3-online-may-2026.html` |
| `foundation-dotM-Homepage-Jan26.html` | `ca-foundation-dot-marathon-series-jan-2026.html` |
| `foundation-DotM-Jan26-direct.html` | `ca-foundation-dot-marathon-direct-jan-2026.html` |
| `foundation-DotM-Jan26-online.html` | `ca-foundation-dot-marathon-online-jan-2026.html` |
| `foundation-Rapid-Revision-Registration-mainpage-May26.html` | `ca-foundation-rapid-revision-registration-may-2026.html` |
| `Inter-ABC-Direct-With-model-Jan27.html` | `ca-inter-abc-direct-with-model-jan-2027.html` |
| `Inter-ABC-Direct-With-model-May26.html` | `ca-inter-abc-direct-with-model-may-2026.html` |
| `Inter-ABC-Direct-With-model-Sep26.html` | `ca-inter-abc-direct-with-model-sep-2026.html` |
| `Inter-ABC-Direct_Jan27.html` | `ca-inter-abc-direct-jan-2027.html` |
| `Inter-ABC-Direct_May26.html` | `ca-inter-abc-direct-may-2026.html` |
| `Inter-ABC-Direct_Sep26.html` | `ca-inter-abc-direct-sep-2026.html` |
| `Inter-ABC-Homepage_Jan27.html` | `ca-inter-abc-series-jan-2027.html` |
| `Inter-ABC-Homepage_May26.html` | `ca-inter-abc-series-may-2026.html` |
| `Inter-ABC-Homepage_Sep26.html` | `ca-inter-abc-series-sep-2026.html` |
| `Inter-ABC-Online-With-model-Jan27.html` | `ca-inter-abc-online-with-model-jan-2027.html` |
| `Inter-ABC-Online-With-model-May26.html` | `ca-inter-abc-online-with-model-may-2026.html` |
| `Inter-ABC-Online-With-model-Sep26.html` | `ca-inter-abc-online-with-model-sep-2026.html` |
| `Inter-ABC-Online_Jan27.html` | `ca-inter-abc-online-jan-2027.html` |
| `Inter-ABC-Online_May26.html` | `ca-inter-abc-online-may-2026.html` |
| `Inter-ABC-Online_Sep26.html` | `ca-inter-abc-online-sep-2026.html` |
| `Inter-Dot-Marathon-May26-Direct.html` | `ca-inter-dot-marathon-direct-may-2026.html` |
| `Inter-Dot-Marathon-May26-Homepage.html` | `ca-inter-dot-marathon-series-may-2026.html` |
| `Inter-Dot-Marathon-May26-Online.html` | `ca-inter-dot-marathon-online-may-2026.html` |
| `Inter-dot2-may26-Direct.html` | `ca-inter-dot-2-direct-may-2026.html` |
| `Inter-dot2-may26-Online.html` | `ca-inter-dot-2-online-may-2026.html` |
| `Inter-dot2.O-Homepage_May26.html` | `ca-inter-dot-2-series-may-2026.html` |
| `Inter-dot3.O-Homepage_jan26.html` | `ca-inter-dot-3-series-jan-2026.html` |
| `Inter-dot3.O-Homepage_may26.html` | `ca-inter-dot-3-series-may-2026.html` |
| `Inter-Dot3.O-jan26-Direct.html` | `ca-inter-dot-3-direct-jan-2026.html` |
| `Inter-Dot3.O-jan26-Online.html` | `ca-inter-dot-3-online-jan-2026.html` |
| `Inter-Dot3.O-may26-Direct.html` | `ca-inter-dot-3-direct-may-2026.html` |
| `Inter-Dot3.O-may26-Online.html` | `ca-inter-dot-3-online-may-2026.html` |
| `Inter-Model-1set_Direct_May26.html` | `ca-inter-model-1-set-direct-may-2026.html` |
| `Inter-Model-1set_Online_May26.html` | `ca-inter-model-1-set-online-may-2026.html` |
| `Inter-Model-2set_Direct_May26.html` | `ca-inter-model-2-set-direct-may-2026.html` |
| `Inter-Model-2set_Online_May26.html` | `ca-inter-model-2-set-online-may-2026.html` |
| `Inter-Model-3set_Direct_May26.html` | `ca-inter-model-3-set-direct-may-2026.html` |
| `Inter-Model-3set_Online_May26.html` | `ca-inter-model-3-set-online-may-2026.html` |
| `PradhiCA-Final-Model-Registration-mainpage-May26.html` | `ca-final-model-registration-may-2026.html` |
| `PradhiCA-Final-Rapid-Revision-Registration-mainpage-Jan27.html` | `ca-final-rapid-revision-registration-jan-2027.html` |
| `PradhiCA-Final-Rapid-Revision-Registration-mainpage-May26.html` | `ca-final-rapid-revision-registration-may-2026.html` |
| `PradhiCA-Final-Rapid-Revision-Registration-mainpage-Sep26.html` | `ca-final-rapid-revision-registration-sep-2026.html` |
| `PradhiCA-Final-Single-Subject-Registration-mainpage-May26.html` | `ca-final-single-subject-registration-may-2026.html` |
| `PradhiCA-Inter-Model-Registration-mainpage--May26.html` | `ca-inter-model-registration-may-2026.html` |
| `PradhiCA-Inter-Rapid-Revision-Registration-mainpage-Jan27.html` | `ca-inter-rapid-revision-registration-jan-2027.html` |
| `PradhiCA-Inter-Rapid-Revision-Registration-mainpage-May26.html` | `ca-inter-rapid-revision-registration-may-2026.html` |
| `PradhiCA-Inter-Rapid-Revision-Registration-mainpage-Sep26.html` | `ca-inter-rapid-revision-registration-sep-2026.html` |
| `PradhiCA-Inter-Single-Subject-Registration-mainpage-Jan26.html` | `ca-inter-single-subject-registration-jan-2026.html` |
| `PradhiCA-Inter-Single-Subject-Registration-mainpage-May26.html` | `ca-inter-single-subject-registration-may-2026.html` |
| `Privacy-Policy.html` | `privacy-policy.html` |
| `Refund-Policy.html` | `refund-policy.html` |
| `Scheduled-download.html` | `scheduled-download.html` |
| `Terms-and-Conditions.html` | `terms-and-conditions.html` |
| `testingg.html` | `testing-page.html` |

- **Internal links** updated across HTML, sitemaps, lists, CSS/JS where referenced.
- **Apache**: root `.htaccess` includes **301** rules for the old paths above.

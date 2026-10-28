# SKNFORCE price list

Live at `/sknforce/` on pricelists.colartdigitalmarketingagency.com.

## Updating prices or services

1. Edit `data.json` (categories, service names, prices, phone / WhatsApp links).
2. Run `python3 build.py` (Python 3 only, no packages). It rewrites `index.html`, including the
   crawlable price rows, the FAQ answers that quote prices, and the JSON-LD (OfferCatalog + FAQPage).
3. Commit and push.

Everything else (`style.css`, `app.js`, `assets/`) is plain static files.

## Still to confirm with the business

- Verified service area (not published anywhere on the page yet).
- Opening hours / street address (intentionally left out: not supplied).

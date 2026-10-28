#!/usr/bin/env python3
"""
Regenerates sknforce/index.html from data.json.

Why: service names + prices must be real, crawlable HTML (SEO / AI search),
and the JSON-LD must match them exactly. Edit data.json, then run:

    python3 build.py

No dependencies beyond Python 3. The site itself stays 100% static.
"""
import json, html, pathlib

HERE = pathlib.Path(__file__).parent
D = json.loads((HERE / "data.json").read_text(encoding="utf-8"))
B = D["business"]
e = html.escape

def money(v):
    return "${:,.2f}".format(v)

# ------------------------------------------------------------------ icons
WA = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12.04 2a9.9 9.9 0 0 0-8.5 14.9L2 22l5.25-1.5A9.9 9.9 0 1 0 12.04 2zm0 1.8a8.1 8.1 0 1 1-4.2 15l-.3-.18-3.1.89.9-3-.2-.32A8.1 8.1 0 0 1 12.04 3.8zM8.6 7.6c-.2 0-.5.07-.75.35-.25.28-1 .98-1 2.4s1.03 2.78 1.17 2.97c.15.2 2 3.2 4.95 4.35 2.45.96 2.95.77 3.48.72.53-.05 1.7-.7 1.94-1.37.24-.68.24-1.26.17-1.38-.07-.12-.27-.2-.56-.34-.3-.15-1.7-.84-1.97-.94-.27-.1-.46-.15-.66.15-.2.3-.76.94-.93 1.13-.17.2-.34.22-.63.07-.3-.15-1.24-.46-2.37-1.46-.87-.78-1.46-1.74-1.63-2.04-.17-.3-.02-.46.13-.6.13-.13.3-.34.44-.5.15-.18.2-.3.3-.5.1-.2.05-.38-.02-.53-.07-.15-.65-1.6-.9-2.18-.24-.57-.48-.5-.66-.5z"/></svg>'
SHARE = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M12 15V3m0 0L8 7m4-4 4 4M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>'
PHONE = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 6 6L15 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'

# ------------------------------------------------------------------ price sections
tabs = "".join(
    f'<a href="#{c["id"]}" class="tab" data-target="{c["id"]}">{e(c["tab"])}</a>'
    for c in D["categories"]
)

sections = ""
for i, c in enumerate(D["categories"], 1):
    rows = "".join(
        f'          <li class="row"><span class="svc">{e(n)}</span><span class="price">{money(p)}</span></li>\n'
        for n, p in c["services"]
    )
    sections += f'''      <section class="cat reveal" id="{c["id"]}" aria-labelledby="{c["id"]}-h">
        <header class="cat-head">
          <span class="cat-num" aria-hidden="true">0{i}</span>
          <div>
            <h2 class="cat-title" id="{c["id"]}-h">{e(c["title"])}</h2>
            <p class="cat-note">{e(c["note"])}</p>
          </div>
        </header>
        <ul class="rows">
{rows}        </ul>
      </section>

'''

# ------------------------------------------------------------------ FAQ
full_trim = next(p for c in D["categories"] for n, p in c["services"] if n == "Full Body Trimming")
full_shave = next(p for c in D["categories"] for n, p in c["services"] if n == "Full Body Shave with a Razor")
cream = next(p for c in D["categories"] for n, p in c["services"] if n == "Hair Removal Cream")

FAQ = [
    ("What services does SKNFORCE offer?",
     "SKNFORCE offers personal body grooming and hair removal, including trimmer machine and razor services for the torso, back, armpits, front and back private parts, legs and hands, plus hair removal cream, full body trimming and a full body shave with a razor."),
    ("Can I book a home or hotel grooming appointment?",
     f"Yes. SKNFORCE provides grooming at your home or hotel. To book, message SKNFORCE on WhatsApp at {B['phoneDisplay']}."),
    ("How can I contact SKNFORCE?",
     f"Contact SKNFORCE by WhatsApp or phone on {B['phoneDisplay']}."),
    ("How much does full-body trimming cost?",
     f"Full body trimming costs {money(full_trim)} (USD). A full body shave with a razor costs {money(full_shave)} and hair removal cream costs {money(cream)}."),
]
faq_html = "".join(
    f'''        <details class="faq-item">
          <summary>{e(q)}</summary>
          <p>{e(a)}</p>
        </details>
''' for q, a in FAQ)

# ------------------------------------------------------------------ JSON-LD
catalog = []
for c in D["categories"]:
    items = []
    for n, p in c["services"]:
        name = n if c["id"] == "fullbody" else f'{n} ({c["title"]})'
        items.append({
            "@type": "Offer",
            "price": f"{p:.2f}",
            "priceCurrency": B["currency"],
            "itemOffered": {"@type": "Service", "name": name},
        })
    catalog.append({"@type": "OfferCatalog", "name": c["title"], "itemListElement": items})

all_prices = [p for c in D["categories"] for _, p in c["services"]]
business_ld = {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    "@id": B["url"] + "#business",
    "name": B["name"],
    "alternateName": "SKNFORCE Home & Hotel Grooming Services",
    "description": "SKNFORCE provides personal body grooming and hair removal services, including trimming and razor shaving, at the customer's home or hotel.",
    "url": B["url"],
    "telephone": B["phoneE164"],
    "image": B["url"] + "assets/img/og-image.jpg",
    "priceRange": f"${min(all_prices):.2f}-${max(all_prices):.2f}",
    "currenciesAccepted": B["currency"],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "SKNFORCE Price List", "itemListElement": catalog},
    "potentialAction": {
        "@type": "ReserveAction",
        "target": {"@type": "EntryPoint", "urlTemplate": B["whatsappBooking"], "actionPlatform": "http://schema.org/MobileWebPlatform"},
        "name": "Book on WhatsApp",
    },
}
faq_ld = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ
    ],
}
ld = json.dumps([business_ld, faq_ld], ensure_ascii=False, indent=2).replace("</", "<\\/")

TITLE = "SKNFORCE | Home & Hotel Grooming Services in Lebanon"
DESC = "Explore SKNFORCE body grooming prices, including trimming, razor shaving and full-body grooming. Contact SKNFORCE to book home or hotel services."

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#202A33">
<link rel="canonical" href="{B["url"]}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="SKNFORCE">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:url" content="{B["url"]}">
<meta property="og:image" content="{B["url"]}assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="SKNFORCE, home and hotel grooming services">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(TITLE)}">
<meta name="twitter:description" content="{e(DESC)}">
<meta name="twitter:image" content="{B["url"]}assets/img/og-image.jpg">

<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/favicon-192.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<link rel="stylesheet" href="style.css">

<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#prices">Skip to price list</a>
<div class="progress" id="progress" aria-hidden="true"></div>

<!-- ===== HEADER ===== -->
<header class="site-header">
  <h1 class="sr-only">SKNFORCE &mdash; Home &amp; Hotel Grooming Services</h1>
  <a class="logo" href="#top" aria-label="SKNFORCE home">
    <img class="logo-img" src="assets/img/sknforce-logo.png" alt="SKNFORCE logo" width="800" height="205" fetchpriority="high">
  </a>
  <p class="header-tag">Home &amp; Hotel Grooming Services</p>
</header>

<main id="top">

  <!-- ===== HERO ===== -->
  <section class="hero">
    <div class="hero-bg" aria-hidden="true"></div>
    <div class="wrap hero-inner">
      <h2 class="hero-title"><span class="ln"><span class="ln-in">Premium grooming,</span></span> <span class="ln gold"><span class="ln-in">your location.</span></span></h2>
      <p class="hero-sub">Precision. Privacy. Confidence.</p>
      <p class="hero-text">Experience premium body grooming services in the comfort and privacy of your home or hotel.</p>
      <div class="hero-cta">
        <a class="btn btn-gold" href="{B["whatsapp"]}" target="_blank" rel="noopener">{WA}<span>Book via WhatsApp</span></a>
        <button class="btn btn-ghost" type="button" id="shareBtn" aria-label="Share this price list">{SHARE}<span>Share</span></button>
      </div>
    </div>
  </section>

  <!-- ===== CATEGORY TABS ===== -->
  <nav class="tabs" aria-label="Service categories">
    <div class="tabs-inner">{tabs}</div>
  </nav>

  <!-- ===== PRICE LIST ===== -->
  <div class="wrap prices" id="prices">
{sections}  </div>

  <!-- ===== BOOKING ===== -->
  <section class="book">
    <div class="wrap">
      <div class="book-card reveal">
        <h2 class="book-title">Ready for your grooming session?</h2>
        <p class="book-text">Book your next grooming appointment and enjoy convenient personal care at your preferred location.</p>
        <a class="btn btn-gold btn-lg" href="{B["whatsappBooking"]}" target="_blank" rel="noopener">{WA}<span>Book on WhatsApp</span></a>
      </div>
    </div>
  </section>

  <!-- ===== FAQ ===== -->
  <section class="faq" aria-labelledby="faq-h">
    <div class="wrap faq-wrap">
      <h2 class="section-title" id="faq-h">Frequently asked questions</h2>
      <div class="faq-list">
{faq_html}      </div>
    </div>
  </section>

</main>

<!-- ===== FOOTER ===== -->
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <p class="foot-brand">SKNFORCE</p>
      <p class="foot-tag">Home &amp; Hotel Grooming Services</p>
    </div>
    <div class="foot-contact">
      <a class="foot-phone" href="tel:{B["phoneE164"]}">{PHONE}<span>{e(B["phoneDisplay"])}</span></a>
      <a class="btn btn-gold btn-sm" href="{B["whatsappBooking"]}" target="_blank" rel="noopener">{WA}<span>Book on WhatsApp</span></a>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <p>&copy; 2026 SKNFORCE. All rights reserved.</p>
    <p class="attrib">Structured by <a href="https://colartdigitalmarketingagency.com/" target="_blank" rel="noopener">Colart Digital Marketing Agency</a><span class="sep">&middot;</span>Hosted by <a href="https://pricelists.colartdigitalmarketingagency.com/" target="_blank" rel="noopener">Price Lists by Colart</a></p>
  </div>
</footer>

<!-- Sticky booking button -->
<a class="sticky-wa" href="{B["whatsappBooking"]}" target="_blank" rel="noopener" aria-label="Book on WhatsApp">{WA}<span>Book on WhatsApp</span></a>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<script src="app.js" defer></script>
</body>
</html>
'''
(HERE / "index.html").write_text(page, encoding="utf-8")
print("index.html written:", len(page), "bytes;", sum(len(c["services"]) for c in D["categories"]), "services")

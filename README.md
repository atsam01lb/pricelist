# Price Lists by Colart

Directory of client price lists, hosted at `pricelists.colartdigitalmarketingagency.com`. Each business has its digital price list designed, built and hosted by Colart Digital Marketing Agency.

## Stack

Static HTML/CSS/JS, no build step. Hosted on GitHub Pages, DNS on Namecheap (see `CNAME`).

## Structure

```
/
├── index.html              # Directory hub: hero, search, filter chips, card grid
├── app.js                  # Single source of truth for the directory — item data + rendering
├── style.css               # Standalone design system (brand tokens, header, hero, cards, footer)
├── 404.html                # Custom not-found page
├── CNAME                   # Custom domain for GitHub Pages
├── assets/
│   └── img/                # Logo mark/lockup, favicons, hero image
├── josephfarah/             # Joseph Farah price list (English + /ar Arabic)
│   ├── index.html
│   ├── ar/index.html
│   └── assets/
└── pearl-beauty-lounge/     # Pearl Beauty Lounge price list
    ├── index.html
    └── assets/
```

## Adding a new business

Open `app.js` and add one object to the `ITEMS` array:

```js
{
  name: 'Business Name',
  slug: 'business-slug',
  category: 'Category Name',
  logo: 'business-slug/assets/img/logo.svg', // omit/leave empty for initials fallback
  href: '/business-slug/'
}
```

Create its folder at the repo root (`/business-slug/index.html`, `/business-slug/style.css`, `/business-slug/assets/`) with its own price list page. No other file needs to change — the card grid, filter chips, search and count are all generated from this array.

## Brand tokens

Colors, type (Lato 300/900 + Noto Kufi Arabic for Arabic text) and all component styles live in `style.css` as CSS custom properties under `:root`. This stylesheet is standalone and does not depend on the main Colart site's `style.css`.

## Deploying

1. Push this repo to GitHub, enable GitHub Pages (branch: `main`, root).
2. Point the `pricelists` CNAME record at Namecheap to the GitHub Pages host, per GitHub's custom domain instructions.
3. GitHub Pages will pick up the `CNAME` file automatically; no further config needed.

## Logo credit / note

The spec this site was built from referenced "the Colart C mark" for the logo-mark SVGs. The logo actually supplied for this build was the Colart "P" mark (`picelists P Logo.ai`), matching this product's own identity — that file is what `assets/img/logo-mark.svg` and the hero's animated ecosystem visual are built from.

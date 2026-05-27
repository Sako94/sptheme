# CLAUDE.md — sptheme

Context for any AI agent (or human) working on this Shopify theme.

> **Onboarding humans**: read `docs/WORKFLOW.md` for the full team SOP
> (env setup, design intake, prompt library, error cheat sheet,
> ship cycle). This file is the AI runtime context — short and rule-y.

## What this is

OS 2.0 Shopify theme for **SoftPauses**, a perimenopause support patch brand.
**Base: Aeon (Shrine PRO engine)** — premium CRO theme. Previous bases
(Debutify Zorix, Dawn) are in git history.

Why Aeon: it ships with rich product templates already (shield, shield2,
core, core2, flow), each pre-composed with high-converting patterns —
testimonials banner, scrolling tickers, results sections, goat-timelines
(for journeys / 24hr arc), product-features grids, content-tabs (FAQ),
comparison-table. The SoftPauses **PDP uses `product.shield2.json`** which
ships with 24 sections covering the full funnel.

SoftPauses brand is layered on top via:
- `assets/sp-base.css` (brand tokens + Aeon class overrides, no font
  !importants so Theme Editor font controls still work)
- `config/settings_data.json` (Aeon's `colors_accent_*`,
  `colors_background_*`, `type_*_font`, button/radius/badge settings
  rewritten for SoftPauses)
- `layout/theme.liquid` (loads Fraunces + IBM Plex Sans Google Fonts,
  loads sp-base.css)
- `templates/product.shield2.json` rewritten with SoftPauses copy

Generated brand images (`assets/sp-ing-*.png`, `sp-ugc-*.png`,
`sp-advisor-*.png`, `sp-patch-on-wrist.png`, `sp-pouch-hero.png`)
survived all migrations and live in `assets/`. Wire them via Theme
Editor image_picker fields on the relevant sections.

- Branch convention: dev work happens on `claude/shopify-theme-setup-pyjWK`.
- Package + release lives at `releases/SoftPauses-X.Y.Z.zip`. Bump
  `theme_version` in `config/settings_schema.json` before each `shopify theme
  package` so the zip name and admin label stay in sync.

## Hard-won Shopify gotchas — read before editing schemas

### 1. Range setting defaults MUST align to the step boundary

For every `{ "type": "range", "min": M, "step": S, "default": D }`, Shopify
requires `(D - M) % S == 0`. Otherwise the section schema is rejected at
upload, but the surface error makes it look like the section file is missing
(`Section type 'sp-foo' does not refer to an existing section file`).

**`shopify theme check` does not catch this.** Run `scripts/preflight.py`
before every package — it does.

Real bug we hit: `min: 0, max: 200, step: 8, default: 60` — 60 isn't a
multiple of 8. Fix: 56 or 64.

### 2. Section schema rejection cascades into misleading template errors

When Shopify rejects a section schema (range alignment, unknown setting type,
default-type mismatch, etc.), the section file stays in the theme but the
section *type* is never registered. Any template that uses that type then
errors with **`Section type 'sp-X' does not refer to an existing section file`**
— even though the file is right there.

When that error appears, the real diagnostic move is to **open Edit code
in the admin, click the section file, and try to Save it**. Shopify's
file-save validator gives the actual reason (e.g. "Invalid schema: setting
with id='pad_top' default must be a step in the range"). Always pull the
specific error before fixing.

### 3. Shopify caches section rejection per theme record

Re-uploading the *fixed* zip on top of the existing theme can leave the
rejection cached. The robust ritual:

1. Online Store → Themes → Theme library → remove old SoftPauses cards
2. Add theme → Upload zip → upload the new release
3. Actions → Publish on the new card
4. Remove the previously-live theme from library

### 4. Browser caches the GitHub raw zip URL

The download URL is stable (`releases/SoftPauses-X.Y.Z.zip`), so browsers
cache aggressively. If a re-uploaded zip looks unchanged, **open the link
in incognito** to bust the cache.

### 5. `shopify theme package` doesn't auth — use it freely

`shopify theme dev` and `shopify theme push` need a Partners-account browser
auth flow that doesn't work from this sandbox. `shopify theme check` and
`shopify theme package` work without auth — use those for local validation.

### 6. Templates have a 25-section maximum

A single JSON template (`templates/*.json`) can include at most **25
sections** in its `sections` object. Going over produces:

  `FileSaveError: sections: must have a maximum of 25`

This is the ENTIRE sections object, not just `order`. Sections in
the file but missing from `order` still count.

Currently `product.softpauses.json` runs at 24 to leave headroom. If
adding more, swap one out (or move to a section group / footer).

`scripts/preflight.py` enforces this — fails if any template exceeds 25.

### 7. Template setting VALUES must respect section schema min/max

A range setting's value set in a *template* (not just the schema default)
must stay within the section schema's `min`/`max`. Shopify rejects on save:

  `FileSaveError: Setting 'speed' can't be greater than 5`

Real bug: Aeon's `horizontal-ticker` caps `speed` at 5, but a rewrite set
it to 25. `scripts/preflight.py` now validates template setting values
against each section's schema range limits, not just schema defaults.

### 8. Aeon section-group sections hardcode a template instance ID

Aeon's `section-group` is a meta-section that visually combines two other
sections, referencing them by full DOM id:
`#shopify-section-template--25360076833091__product_features_pUkYn4`.

That numeric `25360076833091` is the template instance ID **from Aeon's
demo store**. It does not exist in another store, so the section-group
renders empty (shows "Section #1 ID: ..." in the editor but nothing on
the page). The wrapped sections also appear independently in `order`, so
the section-group is redundant. **Fix: delete the section-group sections**
from the template (both from `sections` and `order`). `preflight.py` flags
any section-group that hardcodes a template instance ID.

### 9. Image attachments dropped in chat aren't on disk

Files the user uploads via chat are visible to the model but not saved to
the filesystem. Either:
- Have the user upload via Theme Editor `image_picker` (recommended — Shopify
  CDN handles optimization), or
- Have them commit the image to `assets/` via GitHub web UI, or
- Generate fresh via `scripts/gen_images.py` (Gemini API, see below).

## Image generation

`scripts/gen_images.py` calls Gemini 2.5 Flash Image (Nano Banana). Requires
`GEMINI_API_KEY` set in env (we keep it in `.env.local`, gitignored).

Usage:
```bash
set -a && source .env.local && set +a
python3 scripts/gen_images.py
```

Generated images land in `assets/sp-*.png` and are wired into sections via
the `fallback_asset` block setting (e.g. `sp-ingredients` block:
`fallback_asset: "sp-ing-black-maca.png"`).

**Don't generate** advisor headshots, customer faces, or press logos — for a
health brand, AI faces are a credibility risk if discovered. Real photos
(or licensed stock with model releases) only for those slots.

## Project structure

```
assets/                  CSS, JS, generated images (sp-ing-*.png)
config/                  Theme settings (settings_schema, settings_data)
layout/theme.liquid      Loads Fraunces + IBM Plex Sans, sp-base.css
locales/                 English locale data (non-EN dropped from baseline)
sections/sp-*.liquid     Custom SoftPauses sections (20 of them)
snippets/                Dawn snippets, mostly untouched
templates/
  product.softpauses.json   Composes the sp-* sections into a PDP
  product.json               Default Dawn product template (untouched)
releases/                Packaged .zip of the theme, committed for download
scripts/preflight.py     Pre-package validation (range alignment, etc.)
scripts/gen_images.py    Image generation via Gemini API
```

## Variants + subscriptions setup (Shopify admin)

The `sp-buybox` section auto-discovers product variants for the qty-tier
selector and selling plans for subscribe & save. Both are configured in
the Shopify admin, not in theme code.

### Variants (qty tiers)

In **Products → SoftPauses product → Variants**:

1. Add an option called **Supply** with values `1 Month`, `3 Months`, `6 Months`.
2. For each variant set its price (e.g. $40 / $108 / $194), SKU, inventory.
3. Save. Reload the storefront PDP — the qty tier row populates from
   `product.variants` in order. First variant becomes the default.

### Subscribe & save (selling plans)

Shopify Subscriptions is a free first-party app:

1. Apps → Shopify App Store → search "Shopify Subscriptions" → install.
2. Subscriptions app → **Create plan**. Pick frequency (every 30 days),
   discount (20% off), payment terms.
3. Apply the plan to the SoftPauses product (Plans → Apply to products).
4. Save. Reload the PDP — the buybox shows two radio plans: subscribe
   (with 20% discount applied automatically by Shopify) and one-time.

### Graceful degradation

If neither variants nor selling plans are configured, `sp-buybox` falls
back to a plain "add to cart" button using the default variant. No
errors, just a simpler buybox. Same applies to `sp-pdp-hero` and
`sp-sticky-cta`.

## Build + ship workflow

```bash
# 1. Edit sections/templates as needed
# 2. Run pre-flight
python3 scripts/preflight.py

# 3. Lint
shopify theme check --fail-level error

# 4. Bump version in config/settings_schema.json (theme_version field)
# 5. Package
rm -f releases/SoftPauses-*.zip
shopify theme package
mv SoftPauses-*.zip releases/

# 6. Commit + push
git add -A
git commit -m "..."
git push origin claude/shopify-theme-setup-pyjWK
```

## CRO architecture (PDP)

`product.softpauses.json` orders sections in a tested funnel:

```
promo-bar -> hero -> pain -> mechanism -> ingredients -> clinical
           -> outcome-stats -> buybox -> cost-calc -> comparison
           -> timeline -> qualify -> advisors -> press
           -> ugc -> risk-free -> faq -> email -> footer
           -> sticky-cta
```

Don't reorder without a reason — this matches the source HTML mockup the
client provided and follows: pain → mechanism → ingredients → proof →
offer → reversal → followup → social proof → objection handling → close.

# CLAUDE.md — sptheme

Context for any AI agent (or human) working on this Shopify theme.

## What this is

OS 2.0 Shopify theme for **SoftPauses**, a perimenopause support patch brand.
Scaffolded from Dawn 15.4.1, with custom `sp-*` sections layered on top.

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

### 6. Image attachments dropped in chat aren't on disk

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

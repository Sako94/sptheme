# SoftPauses theme — team workflow & onboarding

Hand this to anyone (designer, dev, or AI agent) joining the SoftPauses theme
work. It captures the entire workflow: from a fresh laptop to a published
PDP, including the Shopify gotchas that ate cycles the first time around.

> Companion file: `CLAUDE.md` at the repo root is the runtime context for
> the AI assistant. This file is the *human-facing* onboarding guide.

---

## What you're inheriting

- **Repo**: `sako94/sptheme`, branch `claude/shopify-theme-setup-pyjWK`
- **Theme**: SoftPauses (Shopify OS 2.0), based on Dawn 15.4.1
- **Brand**: cream `#FAF1EA` ground, poppy red `#ED1B28` for CTAs, ink `#2A1410` for type. Fonts: Fraunces (display) + IBM Plex Sans (body)
- **Custom sections**: 25 `sp-*` sections covering a high-converting PDP funnel
- **Custom template**: `templates/product.softpauses.json` composing 24 of those sections in tested order
- **AI ingredient/lifestyle images** generated via Gemini 2.5 Flash Image ("Nano Banana") in `assets/sp-*.png`
- **Tooling**: `scripts/preflight.py` (Shopify-validator-mirroring lint) and `scripts/gen_images.py` (Gemini image gen)
- **Releases**: each version packaged to `releases/SoftPauses-X.Y.Z.zip` and committed for direct download from GitHub

---

## Phase 0 — One-time environment setup (per developer)

### 0.1 Accounts

- **GitHub**: access to `sako94/sptheme` (ask the owner)
- **Shopify Partners**: free at partners.shopify.com → create a development store
- **Google AI Studio**: free Gemini API key at https://aistudio.google.com/apikey (only needed if you'll generate images)

### 0.2 Local tools

```bash
# Node 18+ (CLI is built on Node)
node -v   # if missing, install via nvm or nodejs.org

# Shopify CLI (free)
npm install -g @shopify/cli@latest @shopify/theme

# Verify
shopify version
```

### 0.3 Clone the repo

```bash
git clone https://github.com/sako94/sptheme.git
cd sptheme
git checkout claude/shopify-theme-setup-pyjWK
```

### 0.4 Set up Gemini API key (only if you'll generate images)

```bash
# Save key to .env.local (gitignored — never commit)
echo "GEMINI_API_KEY=YOUR_KEY_HERE" > .env.local
chmod 600 .env.local
```

### 0.5 Optional: live theme dev server

```bash
shopify theme dev --store your-dev-store.myshopify.com
```

This boots a hot-reloading preview at `http://127.0.0.1:9292`. First run opens a browser to authenticate against your Partners account.

---

## Phase 1 — Receiving a design

Designs from a client typically arrive as one of:

| Format | What to ask for |
|---|---|
| **Figma file** | View link with comment access. Export images as PNG/JPG. Note exact hex colors and font names. |
| **HTML mockup** | Full HTML + CSS file. This is best — the page styling is fully captured. |
| **Static images** | Multiple high-res screenshots showing every section. Plus a brand board (palette, type, logo). |
| **Brand board only** | Type system, colors, logo, photography mood. Then we design from scratch. |

The original SoftPauses brief was an HTML mockup + 5 brand board PNGs.
That's the gold standard — it gave us exact pixel/copy fidelity.

### Always extract upfront:
- **Palette** (hex values for every used color)
- **Type pairing** (display + body fonts, weights, italic usage)
- **Voice** (sentence case? lowercase? sentence-final periods?)
- **Conversion structure** (the section order in the funnel)
- **Image strategy** (which slots need real photos vs decorative)

---

## Phase 2 — Briefing the AI assistant

Whoever is doing the build (human or AI) needs context. The first prompt you
give Claude/Cursor/etc. when starting work in this repo should read the
two context files:

```
Read CLAUDE.md and docs/WORKFLOW.md before doing anything else.
The Shopify gotchas in CLAUDE.md are non-negotiable — every section
schema you write must pass scripts/preflight.py.

The task is: <state the task plainly>.
```

If the AI is starting from scratch (no repo yet), use this prompt instead:

```
We're building a Shopify OS 2.0 theme for <BRAND>. Base it on Dawn
15.4.1. Brand:
- Display font: <FONT>
- Body font: <FONT>
- Palette: cream <#HEX>, primary CTA <#HEX>, accent <#HEX>, ink <#HEX>
- Voice: <lowercase | sentence case | etc.>

Section convention: prefix every custom section with sp- (e.g.
sp-pdp-hero) so it sorts together in the Theme Editor.

Hard rules from prior bad experience with Shopify's validator:
1. Range setting defaults MUST satisfy (default - min) % step == 0,
   else Shopify silently rejects the section schema and any template
   using it errors with 'does not refer to an existing section file'.
2. JSON templates max 25 sections in their `sections` object.
3. Avoid → ← − – characters in schema info/label/header.content/default
   fields. Theme-check doesn't catch these but Shopify rejects them.
4. Pre-package: run a script that checks both rules across every section.

Start by setting up the brand foundation: assets/sp-base.css with CSS
variables for the palette, body { font-size: 22px } if we want a larger
default body, Dawn class overrides for .button .card .field__input so
the rest of the storefront inherits the brand.
```

---

## Phase 3 — Building custom sections

### The pattern every `sp-*` section follows

```liquid
{%- comment -%}
  One-line description of what this section does.
{%- endcomment -%}

<style>
  /* Scoped styles using #shopify-section-{{ section.id }} as the root */
</style>

<section class="sp-foo"
  style="--sp-pad-top: {{ section.settings.pad_top }}px; --sp-pad-bottom: {{ section.settings.pad_bottom }}px;">
  <div class="sp-wrap">
    <!-- content using section.settings.* and block iteration -->
  </div>
</section>

{% schema %}
{
  "name": "Section name",
  "tag": "section",
  "class": "sp-foo-section",
  "settings": [...],
  "blocks": [...],
  "max_blocks": N,
  "presets": [...]
}
{% endschema %}
```

### Prompt template — build one section from a HTML mockup snippet

```
Build a Shopify section called sp-<NAME> from this HTML/CSS:

<paste the HTML for the section, including its style block>

Requirements:
- Outer wrapper: <section class="sp-<NAME>"> with --sp-pad-top
  and --sp-pad-bottom CSS variables driven by schema range settings.
- Use the brand CSS vars from sp-base.css (--sp-cream, --sp-poppy,
  etc.) instead of hex values.
- Repeating items become blocks (max_blocks set sensibly).
- Singular content (heading, lede, footnote) becomes section settings.
- Always include a presets array so the section is addable from the
  Theme Editor.
- Range settings: default MUST satisfy (default - min) % step == 0.
- No → ← − – characters anywhere in the schema.
- Add a {% if block.type == '<TYPE>' %} guard around block rendering
  for parity with other sp-* sections.

Write only the file. Don't bump the theme version yet.
```

### Prompt template — add the new section to the product template

```
Add the new sp-<NAME> section to templates/product.softpauses.json.
Slot it between <X> and <Y> in the order array. Pre-populate it with
copy from the brief.

Then run scripts/preflight.py and shopify theme check. If both pass,
bump theme_version in config/settings_schema.json by patch (X.Y.Z+1)
and run `shopify theme package` and move the zip to releases/.
```

---

## Phase 4 — Image generation (Nano Banana)

We use Gemini 2.5 Flash Image (model id: `gemini-2.5-flash-image`) for:
- ingredient close-ups (real plants/roots)
- lifestyle shots (hands, wrists, mood photography)
- product packaging mockups

We do NOT use it for:
- **advisor headshots** for production (credibility risk if a real "Dr. X"
  doesn't exist — placeholders are OK but tag them clearly)
- **customer testimonials / UGC** for production (same — discoverable as
  fake)
- **press logos** (use real publication logos with permission)

### Workflow

```bash
set -a && source .env.local && set +a
python3 scripts/gen_images.py     # generates ingredients
# Or copy gen_images.py to gen_<topic>.py with new JOBS list
```

The script saves PNGs into `assets/sp-*.png`. They're then wired into
sections via the `fallback_asset` block setting (see `sp-ingredients`,
`sp-ugc-reviews`, `sp-advisors` for examples).

### Prompt template — generate brand-aligned imagery

```
Add new entries to scripts/gen_images.py for: <list>
Each prompt should:
- Be 4-6 sentences describing subject, mood, lighting, palette,
  composition (1:1 or 4:5), photo style (editorial wellness brand)
- Specify a warm cream/blush background (#FAF1EA / #FED9D1 family)
- Include "Photorealistic, high resolution, no text or labels"
- Match the SoftPauses brand boards' soft, warm, premium aesthetic

Run the script. Save the outputs to assets/. Show me each image
before wiring it into a section so I can approve.
```

### Specs cheat sheet

| Slot | Aspect | Min size | Style note |
|---|---|---|---|
| Ingredients | 1:1 | 800×800 | Single subject, plain background, macro |
| UGC review | 1:1 | 1200×1200 | Lifestyle, woman 40s+, warm light |
| Advisor headshot | 1:1 | 1000×1000 | Studio, neutral background, head + shoulders |
| Hero | 4:5 | 1600×2000 | Editorial lifestyle, person not patch |
| Product packaging | 4:5 or 1:1 | 1200×1500 | Pouch on seamless paper, soft shadow |

---

## Phase 5 — Shopify error gotchas (the back-and-forth eaters)

These are the lessons from the SoftPauses build. **Every one of them cost a
push cycle the first time around.** Read them before writing any schema.

### Gotcha 1 — Range default step alignment

```
"min": M, "step": S, "default": D     →    (D - M) % S MUST == 0
```

Bad: `min: 0, max: 200, step: 8, default: 60`     (60 / 8 = 7.5)
Fix: `default: 56` or `default: 64`

Surface error: `Invalid schema: setting with id="X" default must be a step in the range`

Cascading error in template editor: `Section type 'sp-X' does not refer to an existing section file`

`shopify theme check` does NOT catch this. `scripts/preflight.py` does.

### Gotcha 2 — Section rejection cascades to template error

When Shopify rejects a section schema for ANY reason (range, unknown setting
type, default-type mismatch, banned Unicode chars), the file stays on disk
but the section type isn't registered. Templates using it then error with the
misleading "does not refer to an existing section file."

**Diagnostic move when you see that error:**
1. Open the Shopify admin → Online Store → Themes → SoftPauses → ⋯ → Edit code
2. Click on the offending `sections/sp-X.liquid`
3. Hit Save (no edits needed)
4. Shopify's file-save validator will surface the *real* error message

Always pull the specific error before guessing.

### Gotcha 3 — Banned Unicode chars

These break Shopify's section-schema validator when present in `info`,
`label`, `header.content`, or `default` fields:

| Char | Codepoint | Replace with |
|---|---|---|
| `→` | U+2192 | `->` |
| `←` | U+2190 | `<-` |
| `−` | U+2212 | `-` (hyphen) |
| `–` | U+2013 | `-` (hyphen) |
| `©` | U+00A9 | `(c)` (precaution) |

Safe: `·` (middle dot), `—` (em-dash), `®`, `™`, `★`.

Preflight catches the banned ones.

### Gotcha 4 — Per-theme rejection cache

Shopify caches its rejection decision per theme record. Re-uploading the
*fixed* zip on top of an already-rejected theme can leave the cache stale.

The clean re-upload ritual:
1. **Online Store → Themes → Theme library** → for each old SoftPauses
   card, ⋯ → **Remove**.
2. The currently-published one can't be removed yet — it'll move to library
   after step 4.
3. **Add theme → Upload zip** → upload the new release. Always **open the
   GitHub raw zip URL in incognito** to bust browser cache.
4. **Actions → Publish** on the new card. The previous live theme moves to
   library — now remove it.
5. Refresh the product → Theme template → confirm `softpauses` is selectable.

### Gotcha 5 — 25-section template cap

JSON templates max 25 sections in their `sections` object. Adding more
produces:

```
FileSaveError: sections: must have a maximum of 25
```

The cap counts everything in `sections`, even if not in `order`. Preflight
catches this too. The SoftPauses PDP runs at 24 to leave headroom.

### Gotcha 6 — GitHub raw URL caches

Browsers (and CDNs) cache GitHub raw zip URLs aggressively. After we push
a new `releases/SoftPauses-X.Y.Z.zip`, opening the link in a normal tab
may serve the old zip. **Always open the link in incognito for upload.**

### Gotcha 7 — Chat-attached images don't land on disk

When a designer drops images into a chat with the AI, those images are
visible to the model but NOT saved to the filesystem. To get them into
the theme, the human must either:
- Upload via Theme Editor's `image_picker` (best — Shopify CDN handles it)
- Commit to `assets/` via GitHub web UI
- Have the AI regenerate via Gemini

---

## Phase 6 — Ship cycle (every change)

```bash
# 1. Edit sections, templates, assets
# 2. Run preflight (catches Shopify-only validation rules)
python3 scripts/preflight.py

# 3. Lint with theme-check
shopify theme check --fail-level error

# 4. Bump theme_version in config/settings_schema.json
#    Use semver: patch for fixes, minor for new sections, major for
#    breaking template restructures.

# 5. Package to a versioned zip
rm -f releases/SoftPauses-*.zip
shopify theme package
mv SoftPauses-*.zip releases/

# 6. Commit + push
git add -A
git commit -m "Concise summary

Bullet list of meaningful changes. Note any new validator rule learned
so the next person catches it before push.
"
git push origin claude/shopify-theme-setup-pyjWK

# 7. Hand the merchant the new download URL:
# https://github.com/sako94/sptheme/raw/claude/shopify-theme-setup-pyjWK/releases/SoftPauses-X.Y.Z.zip
```

---

## Phase 7 — Variants + subscriptions (admin-side)

Both are configured in the Shopify admin, NOT in theme code. The buy box
section (`sp-buybox`) auto-discovers them and degrades gracefully if
they're missing.

### Variants (qty tier selector)

**Products → SoftPauses product → Variants:**

1. Add an option called **Supply** with values `1 Month`, `3 Months`, `6 Months`.
2. Set price/SKU/inventory per variant.
3. Save. The qty-tier row in the buy box populates from `product.variants`.

### Subscribe & save (selling plans)

1. Apps → Shopify App Store → install **Shopify Subscriptions** (free).
2. Subscriptions app → **Create plan**. Frequency: every 30 days. Discount: 20% off.
3. Plans → Apply to the SoftPauses product.
4. The buy box's two-radio plan toggle (subscribe vs one-time) appears automatically.

---

## Phase 8 — Prompt library

Copy-paste prompts that mirror what worked for the SoftPauses build.

### Prompt: brief Claude on a fresh repo

```
Read CLAUDE.md and docs/WORKFLOW.md.
Today's task: <task description>.
```

### Prompt: build a section from HTML

```
From the HTML below, create sections/sp-<NAME>.liquid following the pattern in
sections/sp-promo-bar.liquid (closest stable example). All copy should be
editable via schema settings or blocks. Use brand CSS vars from sp-base.css.
Run preflight before declaring done.

<HTML>
```

### Prompt: generate brand imagery

```
Add a job to scripts/gen_images.py for: <subject>.
Aspect: 1:1, 1200x1200. Style: editorial wellness, soft warm light, cream
background (#FAF1EA), subject only, photorealistic.
Run the script. Show me the output before wiring it as a fallback_asset.
```

### Prompt: diagnose a "section file not found" error

```
The Shopify admin gives me 'Section type sp-X does not refer to an existing
section file' when I try to save the template. The file IS in sections/
folder. Run scripts/preflight.py and surface what's wrong with the
sp-X schema. Then have me try saving the file directly in admin Edit code
to confirm the underlying validation error.
```

### Prompt: add a section to the PDP template

```
Add sp-<NAME> to templates/product.softpauses.json. Slot it between <X>
and <Y> in the order array. Pre-populate copy from the brief. Then verify
the template still has 25 or fewer sections (Shopify cap). If we're at
25, swap one out instead of adding.
```

### Prompt: ship a release

```
Run preflight + theme-check. If both pass, bump the theme_version (patch),
package via shopify theme package, move the zip to releases/, commit with
a tight summary, push. Give me the new download URL.
```

### Prompt: respond to a Shopify FileSaveError

```
Shopify gave me this error: <paste exact error>.
Look it up against the gotchas in CLAUDE.md. If it's a known one, fix it
and ship. If it's new, find the root cause first (manually save the
offending file in admin Edit code to surface the real error message),
then add the new rule to scripts/preflight.py and CLAUDE.md so it
never bites again.
```

---

## Appendix — File map

```
.
├── CLAUDE.md                    AI runtime context (gotchas, conventions)
├── docs/WORKFLOW.md             this file
├── README.md                    public-facing readme
├── .env.local                   gitignored: GEMINI_API_KEY
├── assets/
│   ├── sp-base.css              brand foundation (vars, typography, Dawn overrides)
│   ├── sp-ing-*.png             AI-generated ingredient close-ups
│   ├── sp-ugc-*.png             AI-generated UGC placeholders
│   ├── sp-advisor-*.png         AI-generated advisor placeholders
│   ├── sp-patch-on-wrist.png    AI-generated lifestyle shot
│   └── sp-pouch-hero.png        AI-generated pouch hero alt
├── config/
│   ├── settings_data.json       theme settings (brand colors, fonts, radii)
│   └── settings_schema.json     theme settings schema (theme_version lives here)
├── layout/theme.liquid          loads Fraunces + IBM Plex Sans, sp-base.css
├── locales/                     en.default + en.default.schema (rest dropped)
├── releases/SoftPauses-*.zip    packaged theme zips
├── scripts/
│   ├── preflight.py             pre-package validation (Shopify-rule mirror)
│   └── gen_images.py            Gemini Nano Banana image generator
├── sections/sp-*.liquid         25 custom SoftPauses sections
├── snippets/                    Dawn snippets, mostly untouched
└── templates/
    ├── product.softpauses.json  composed PDP, 24 sections
    └── product.json             default Dawn product template (untouched)
```

---

## Hand-off checklist

Before you consider a feature done:

- [ ] `python3 scripts/preflight.py` → "Pre-flight clean"
- [ ] `shopify theme check --fail-level error` → no errors
- [ ] `theme_version` bumped in `config/settings_schema.json`
- [ ] New zip in `releases/` matching the version
- [ ] Commit message summarizes WHY (not just what)
- [ ] Pushed to `claude/shopify-theme-setup-pyjWK`
- [ ] If a new Shopify validator rule was learned, it's in `CLAUDE.md`
      AND `scripts/preflight.py` so the next person doesn't hit it
- [ ] Merchant has been given the new download URL with re-upload ritual
      reminder if anything that affects the section registry changed

# SoftPauses Homepage — CRO Spec

A traffic-arriving-to-add-to-cart-or-email-capture funnel using Aeon's
native section catalog. 17 sections, optimized for women 38–55 landing on
the homepage cold. Hand this to a dev to assemble in `templates/index.json`.

## Design system (apply globally, no per-section overrides needed)

| Token | Value | Aeon setting |
|---|---|---|
| Primary brand | `#ED1B28` poppy | `colors_accent_2` |
| Ink (type, dark surfaces) | `#2A1410` | `colors_accent_1`, `colors_text` |
| Cream (page bg) | `#FAF1EA` | `colors_background_1` |
| Blush soft (alt bg) | `#FEE5DE` | `colors_background_2` |
| Blush (cards) | `#FED9D1` | n/a |
| Display font | Fraunces (italic for emphasis) | `type_header_font: fraunces_n5` |
| Body font | IBM Plex Sans medium | `type_body_font: ibm_plex_sans_n5` |
| Buttons | pill (`buttons_radius: 40`) | global setting |
| Cards | 8px corners | global setting |
| Body size | 18px desktop / 16px mobile | global setting |

**Voice**: lowercase headlines, `<em>italic poppy</em>` on key words, sentence-case body. No exclamation points. No "hey besties." Speak to a tired 45-year-old who knows something is wrong.

---

## Section-by-section funnel

### 1. Announcement bar (`announcement-bar`)
*Why first: persistent trust on every page; sets the offer.*

- Rotating 3 messages (~5s each):
  1. **"save 20% on your first order — limited time"**
  2. **"free shipping on all US orders"**
  3. **"30-day money-back guarantee"**
- Design: thin band, ink background `#2A1410`, cream text. Center-aligned. Dot pagination on mobile.

---

### 2. Hero (`image-banner` or `slideshow-hero`)
*Why second: above-the-fold promise + CTA + immediate trust. Most expensive real estate.*

- Eyebrow: `for women in perimenopause`
- Headline: **`you're not losing your mind. you're losing your <em>estrogen</em>.`**
- Subhead: `one patch a day. 24-hour transdermal release of organic triple-source maca. not a drug. not HRT. just steady support, made simple.`
- Primary CTA: **`shop the patch — $39`** → links to product page
- Secondary CTA: `learn how it works` → anchor scrolls to section 8
- Trust line under CTA: `★ 4.8/5 · 12,000+ verified reviews · made in USA`
- Design: 60/40 split. **Left**: copy + CTAs. **Right**: lifestyle hero image (woman mid-40s, calm domestic moment, natural light — use `sp-patch-on-wrist.png` or upload a new shot). Cream bg. Padding-top 80px, padding-bottom 96px.

---

### 3. Press / "as featured in" (`logo-list`)
*Why early: third-party credibility on first scroll, before they're invested.*

- Label: **`as featured in`** (small caps, ink-muted)
- 6 logos (greyscale, hover restores color): Vogue · Forbes · Women's Health · Goop · The Cut · BYRDIE
- Design: thin band, no border, 50px vertical padding. Replace placeholder logos with real ones once you have press.

> **Note for dev**: if you don't have real press placements yet, omit this section entirely rather than fake it. Press logos are easy to disprove and erode trust if discovered.

---

### 4. Trust strip (`icon-bar`)
*Why here: 5 differentiators, easy to scan, lands the "this isn't just another supplement" message.*

- 5 columns, simple icon + 2 lines each:
  1. **USDA Organic** · `triple-source maca, no fillers`
  2. **Doctor-Backed** · `reviewed by menopause-trained MDs`
  3. **HSA / FSA Eligible** · `covered at checkout via TrueMed`
  4. **30-Day Money-Back** · `no questions, no forms`
  5. **Free U.S. Shipping** · `every order`
- Design: cream bg, ink icons (24px), Fraunces small caps headings. No dividers between columns.

---

### 5. Pain identification (`image-with-text` + 6 small cards via blocks)
*Why now: validates the buyer's experience before pitching anything. Resonance.*

**Left column (text)**:
- Heading: **`you've felt it for months. they keep telling you you're <em>fine</em>.`**
- Body: `the 3am wakings. the rage out of nowhere. the brain fog. the labs that come back "normal." it's not in your head — it's in your hormones.`

**Right column (6 dismissive-quote cards)**:
- `"it's just stress."` → `it isn't just stress.`
- `"your labs are normal."` → `labs miss perimenopause.`
- `"you're too young for that."` → `it can start at 38.`
- `"have you tried yoga?"` → `yoga is not a hormone.`
- `"maybe try an antidepressant."` → `it's not depression.`
- `"it's just part of getting older."` → `it doesn't have to be.`

Design: 2-column layout. Right side is a 3×2 grid of small cards (blush background, 8px radius, italic gray quote on top, ink reframe on bottom). Padding-block 80px.

---

### 6. The stat / scope of problem (`results`)
*Why: scale up from individual pain to "you are not alone." Anchors the 47M market.*

- Eyebrow: `the truth`
- Heading: **`one in three women are dismissed at the first visit.`**
- 3 big numbers (poppy):
  - **47M** — `women in the US are in perimenopause right now`
  - **1 in 3** — `dismissed by their doctor at the first visit`
  - **10 yrs** — `is how long perimenopause can last — most assume it's months`
- Closing line (centered under stats): `you deserve better than waiting it out.`
- Design: Cream bg, big serif numbers (Fraunces, ~140px desktop). Padding-block 96px.

---

### 7. Featured product / primary CTA (`featured-product`)
*Why here: now they're emotionally invested — give them the product. Primary homepage conversion point.*

- **Left**: product image gallery (3-4 SoftPauses pouch shots — use existing brand-board photos)
- **Right**:
  - Eyebrow: `the daily patch`
  - Title: **`Soft Pauses Daily Perimenopause Patch`**
  - Price block: **`$32 / month on subscribe & save`** (with `$40 one-time` strikethrough next to it)
  - 3 benefit pills (poppy outline, pill-shaped):
    - `24-hour release`
    - `doctor-backed`
    - `organic maca`
  - Primary CTA: **`see the patch →`** → links to product page
  - Secondary line: `cancel anytime · 30-day money-back · HSA/FSA eligible`
- Design: 50/50 layout. Sticky scroll behavior on desktop (image gallery stays visible while right side scrolls). Card style: ink-on-cream, 12px radius. Padding-block 96px.

---

### 8. How it works (`icons-with-content` or `multicolumn`)
*Why: kills the "is this a hassle?" objection. Simplicity is the conversion lever for a patch.*

- Heading: **`three steps. <em>one decision</em> a day.`**
- Subhead: `peel, stick, forget about it. the only thing simpler than this routine is not having one.`
- 3 columns:
  1. **STEP 01 · PEEL** — `peel one patch from the daily strip. takes about three seconds. no water, no swallowing.`
  2. **STEP 02 · STICK** — `place it on the inside of your forearm or shoulder. anywhere with thin, clean skin works. rotate placement daily.`
  3. **STEP 03 · SUPPORT** — `the patch delivers organic triple-source maca through the skin for 24 hours. swap for a fresh one tomorrow morning.`
- Design: 3 columns, soft circular icon at top of each (~120px), step number small caps, headline Fraunces, body 16px. Blush-soft bg. Padding-block 96px.
- Connect the columns with thin poppy horizontal lines between them on desktop (subtle journey visual).

---

### 9. Four ingredients (`product-features`)
*Why: transparency = trust. Visible, named, dosed.*

- Heading: **`four ingredients. clinical doses. <em>nothing else.</em>`**
- Subhead: `no fillers, no flavor agents, no proprietary blends, no marketing math. each patch delivers the same dose. every day.`
- 4 cards (each with image from `assets/sp-ing-*.png`):
  - **black maca** · `organic · andean` · `the most-studied of the three. supports mental energy and focus.`
  - **red maca** · `organic · andean` · `traditionally used for hormonal balance and hot-flash relief.`
  - **yellow maca** · `organic · andean` · `supports overall stamina. rounds out the full-spectrum extract.`
  - **BioPerine** · `black pepper extract · standardized` · `multiplies maca absorption. without it, your body uses a fraction.`
- Design: 4-column grid (2×2 on mobile). Card: image top (square, 1:1), ingredient name (Fraunces medium 24px), kicker (small caps poppy), 2-sentence description. Cream bg with cards on white. Padding-block 96px.

---

### 10. Before vs after (`comparison-slider` OR a `results`-style stats block)
*Why: transformation visualization. If you have real before/after content, slider wins. Otherwise stats.*

**Option A (slider — recommended if you have real journey content)**:
- Heading: **`the shape of a <em>30-day reset</em>.`**
- Subhead: `self-reported scores at day 0 and day 30. same questions, same women, 30 days apart.`
- Drag-to-reveal slider between two illustrations or photos.

**Option B (stats — fallback)**:
- Same heading + subhead
- 3 big stats: `+87% energy · +73% sleep · +81% mood balance`
- Footnote: `self-reported, 500 women, 30+ days of daily use.`

Design: Full-width section. Blush-soft bg. Padding-block 96px.

---

### 11. Testimonials / reviews (`testimonials`)
*Why: social proof at maximum impact moment — they've seen the science, now they need to see real women.*

- Heading: **`loved by <em>12,000+</em> women in perimenopause.`**
- 3 review cards (replace with real customers + photos before launch):
  - `Sarah K., 47` · ★★★★★ · `i used to wake up at 3am every night. now i sleep through. one decision a day.` · *verified buyer*
  - `Jen R., 44` · ★★★★★ · `not a younger version. just myself. soft pauses gave me back the version of me i missed.` · *verified buyer*
  - `Maria L., 49` · ★★★★★ · `after 4 supplements and 3 doctors, this is the first thing that actually shifted anything.` · *verified buyer*
- Below: `★★★★★ 4.8 / 5 · based on 12,432 verified reviews` + CTA `read all reviews →`
- Design: 3-column card grid. Each card: photo top (square, 1:1), star row, italic Fraunces quote, name + age + verified badge. Cream bg with cards on white. Padding-block 96px.

> **Important**: AI-generated faces are a credibility risk on a health brand. Replace `sp-ugc-1.png` etc. with real customers (with model releases) before launching.

---

### 12. Comparison vs alternatives (`comparison-table`)
*Why: differentiation. Direct comparison settles the "why not just try a maca capsule?" question.*

- Heading: **`not all perimenopause solutions are created equal.`**
- 3-column table:

| | **Soft Pauses** | **Typical Capsule** | **HRT** |
|---|:---:|:---:|:---:|
| Triple-source organic maca | ✓ | single-source | — |
| Transdermal (no pill) | ✓ | — | varies |
| BioPerine for absorption | ✓ | — | n/a |
| Drug-free / non-hormonal | ✓ | ✓ | — |
| Doctor-backed | ✓ | varies | yes (prescription) |
| Once-daily, no food required | ✓ | 2-3 caps with food | varies |
| 30-day money-back guarantee | ✓ | — | n/a |
| HSA/FSA eligible | ✓ | — | yes |

- Design: Soft Pauses column highlighted with poppy accent header. Check marks in poppy, dashes in ink-muted. Padding-block 96px.

---

### 13. Subscribe & save value prop (`pricing-table` or `icons-with-content`)
*Why: subscription is the high-LTV outcome. Educate the buyer on why subscribing is the smart choice.*

- Heading: **`subscribe & save. <em>cancel anytime.</em>`**
- 3 pricing cards (middle one — Subscribe — highlighted with poppy outline + "most popular" tag):

| One-time | **Subscribe** ⭐ | 3-month bundle |
|---|---|---|
| $40 / month | **$32 / month** | $86 / 3 months |
| ship once | save 20% | save 28% |
| | free shipping | free shipping |
| | skip or pause anytime | priority support |
| | never run out | best price per patch |
| `try once →` | **`subscribe →`** | `bundle → ` |

- Design: 3 columns. Subscribe card has thick poppy border, slight elevation. CTAs match button system. Padding-block 96px.

---

### 14. Risk-free guarantee (`image-with-text` or `section-group`)
*Why: removes the last objection right before they're asked to convert. Standard subscription playbook.*

- Eyebrow: `our promise`
- Heading: **`try it for 30 days. on us.`**
- Body: `if it doesn't feel like it's doing something for you, send it back. no questions, no forms, no friction. that's the offer.`
- 3 badge pills (icon + text):
  - `30-day money-back guarantee`
  - `HSA / FSA eligible`
  - `free U.S. shipping`
- CTA: `start your 30 days →`
- Design: Centered card on cream. Blush-soft card bg, 12px radius. Max-width 720px. Padding-block 64px.

---

### 15. FAQ (`content-tabs`)
*Why: handles objections without bloating the page. Tabbed so users self-select their question type.*

- Heading: **`questions, <em>asked honestly</em>.`**
- 4 tabs:

**product**
- `is this HRT?` → `no. soft pauses is not a hormone and not a drug. it is a daily plant-based support.`
- `how long until i feel something?` → `most women report a difference in energy and mood within 2-4 weeks of daily use. give it a full 30 days.`
- `why a patch and not a pill?` → `pills require a digestive system, a routine, and a memory. a patch is once a day, on the skin, done.`

**subscription**
- `how does the subscription work?` → `first order ships free with 20% off. a fresh 30-day supply arrives every 30 days. pause, skip, or cancel from your account in one click.`
- `how do i cancel?` → `log in, click cancel. takes 10 seconds. no phone calls.`

**medical**
- `is maca safe for me?` → `maca has been used for centuries and is well-tolerated. if you are pregnant, breastfeeding, on thyroid meds, or in cancer treatment, consult your doctor first.`
- `can i use this with HRT?` → `most women on HRT can use soft pauses as a daily floor of support. confirm with your prescribing physician.`

**shipping**
- `when will my order ship?` → `orders before 1pm ET ship same business day. delivery 2-5 business days in the US.`
- `what if it doesn't work for me?` → `send it back within 30 days for a full refund. no forms, no friction.`

- Design: Tabs centered (pill-shaped tabs, active = poppy bg). Accordion items below. Plus/minus indicators in poppy. Padding-block 96px.

---

### 16. Founder note (`image-with-text`)
*Why: humanizes the brand. Closes the "who is behind this?" loop.*

- **Left**: founder portrait (placeholder until real)
- **Right**:
  - Eyebrow: `from the founder`
  - Heading: **`i made the first batch on a kitchen counter at 4am.`**
  - Body: `i started soft pauses after three doctors and six supplements. nothing worked. so i made my own — for my sister, my mom, and the woman i used to be at 3am wondering why her body was doing what it was doing. one patch a day. it isn't magic. it's daily support, taken consistently. — [Founder Name]`
  - Signature image (handwritten name)
- Design: 50/50 layout. Cream bg. Portrait in 1:1 frame with soft drop shadow. Padding-block 96px.

---

### 17. Email capture (`email-signup-banner` or `newsletter`)
*Why last: catches the visitors who didn't convert. Lower-friction ask = high yield.*

- Heading: **`get $5 off your first order.`**
- Subhead: `plus a short, honest weekly note on perimenopause from our medical advisors. no fluff, no spam. you can unsubscribe with one click.`
- Form: email input + button
- Button label: `get my code`
- Below form (small): `we never share your email. unsubscribe anytime.`
- Design: Ink bg (`#2A1410`), cream text. Centered, inline form. Padding-block 80px.

---

### Footer (already exists)
Standard footer-group, no homepage-specific changes.

---

## Order summary (17 sections)

```
1.  announcement-bar      promo + trust rotating bar
2.  image-banner          hero w/ headline + CTA
3.  logo-list             press / "as featured in"  (skip if no real press)
4.  icon-bar              5 trust signals strip
5.  image-with-text       pain identification + 6 dismissive cards
6.  results               3 stats: 47M / 1 in 3 / 10 yrs
7.  featured-product      product showcase + primary CTA
8.  icons-with-content    how it works 3 steps (peel / stick / support)
9.  product-features      4 ingredients with photos
10. comparison-slider     before/after 30 days  (or results fallback)
11. testimonials          3 customer reviews with photos
12. comparison-table      vs typical capsule vs HRT
13. pricing-table         one-time / subscribe / bundle
14. image-with-text       30-day guarantee card
15. content-tabs          FAQ (product/sub/medical/shipping)
16. image-with-text       founder note + portrait
17. email-signup-banner   $5 off + nurture signup
```

Plus the existing footer-group, header-group, and announcement-bar.

---

## CRO rationale — why this order works

**The funnel mirrors a tested DTC pattern**: emotional resonance → scale of problem → product → simplicity → ingredients → transformation → social proof → comparison → pricing → risk reversal → objection handling → brand authenticity → exit capture.

Key mechanics:
- **Pain before product** (sections 5-6 before 7): we earn the buyer's trust by showing we understand their problem before pitching anything.
- **Featured product mid-page** (7) rather than only at top: lets emotional buyers convert immediately AND gives scrollers a second chance.
- **Subscription benefits AFTER comparison** (13 after 12): we've already proven we're worth it before asking for the higher commitment.
- **Risk-free + FAQ both AFTER pricing** (14-15): they handle the two objections that arise right after seeing the price — "what if it doesn't work" and "how does this actually work."
- **Founder note near the end** (16): warm close. Buyers who reached this far want to feel like they're buying from a person, not a brand.
- **Email capture as the final ask** (17): for everyone who didn't add to cart, lowest-friction conversion possible. Feeds a 7-day nurture sequence in Klaviyo.

---

## Dev implementation notes

1. **Build in `templates/index.json`**, replacing the current Aeon demo content there.
2. **Use only Aeon's native section types listed above** — no custom sections needed.
3. **All section settings must respect Aeon's range limits** — run `python3 scripts/preflight.py` before packaging. Common traps:
   - `speed` (horizontal-ticker) max 5
   - `badge_corner_radius` max 40
   - `buttons_radius` max 40
   - All `padding_*` and `spacing_*` must align to their step (usually 4 or 8)
4. **Clear all `shopify://shop_images/*` references to empty string** — the merchant uploads images via Theme Editor. Leaving Aeon demo paths in causes broken image previews.
5. **Section count must stay ≤ 25** — current spec has 17, leaving headroom.
6. **Avoid `section-group` sections** — they reference other sections by hardcoded template instance IDs that don't survive cross-store uploads. Use direct sections in `order` instead.
7. **No `→` `←` `−` `–` characters** in schema `info`, `label`, `header.content`, or `default` strings — Shopify silently rejects sections containing them. Use `->`, `<-`, `-`.

After building, ship cycle:
```bash
python3 scripts/preflight.py        # must report "clean"
shopify theme check --fail-level error
# bump theme_version in config/settings_schema.json
shopify theme package
mv SoftPauses-*.zip releases/
git add -A && git commit && git push
```

---

## What images / assets the dev needs

| Slot | Spec | Source |
|---|---|---|
| Hero image | 4:5, 1600×2000+, warm lifestyle | upload via Theme Editor; `sp-patch-on-wrist.png` available |
| Press logos × 6 | PNG transparent, 200×60 grayscale | only if real press; otherwise omit section |
| Product gallery × 3-4 | square or 4:5, 1200×1200+ | merchant uploads SoftPauses pouch shots |
| How-it-works icons × 3 | SVG or 240×240 PNG | dev creates simple line icons (peel / stick / clock) |
| Ingredient cards × 4 | 1:1, 800×800 | `assets/sp-ing-{black,red,yellow}-maca.png` and `sp-ing-bioperine.png` already in theme |
| Before/after pair × 2 | matched 1:1 | optional, replace with stats if not available |
| Testimonial photos × 3 | 1:1, 1200×1200, real customers | `sp-ugc-1/2/3.png` available as placeholders only |
| Founder portrait | 1:1, 1200×1200, professional but warm | merchant photo, replace `[Founder Name]` |

---

## What this homepage is NOT

- Not the place to deep-dive the patch anatomy or 24hr release diagram — those are PDP-only (in `shield2`). Homepage keeps it surface-level and drives to PDP.
- Not the place for the wake-up call's 6 Q+A in full detail — pulled forward as a compressed 6-tile validation, not the editorial format on the PDP.
- Not a buy box. The featured-product section drives to the PDP for actual purchase decisions.
- Not a place to list every advisor — that's PDP territory. Homepage uses the founder note instead.

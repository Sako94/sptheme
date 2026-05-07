# sptheme

A Shopify Online Store 2.0 theme, scaffolded from [Shopify Dawn](https://github.com/Shopify/dawn) (v15.4.1) as a reference baseline. Custom sections, snippets, and styles are layered on top of Dawn conventions.

## Project structure

```
assets/      CSS, JS, fonts, and image files served from the theme
config/      Theme settings (settings_schema.json, settings_data.json)
layout/      theme.liquid, password.liquid (top-level wrappers)
locales/     Translations (en.default.json is the source of truth)
sections/    OS 2.0 sections, including section groups (header/footer)
snippets/    Reusable Liquid partials
templates/   JSON templates that compose sections per page
```

## Local development

Install [Shopify CLI](https://shopify.dev/docs/themes/tools/cli/install):

```bash
npm install -g @shopify/cli @shopify/theme
```

Connect to a development store and start the local dev server:

```bash
shopify theme dev --store your-store.myshopify.com
```

Lint the theme:

```bash
shopify theme check
```

## Layering Dawn updates

This repo was initialized from Dawn 15.4.1. To pull upstream Dawn improvements later:

```bash
git remote add upstream https://github.com/Shopify/dawn.git
git fetch upstream
git merge upstream/main   # resolve conflicts as needed
```

## Conventions

- **Sections + blocks**: every section exposes a full `{% schema %}` so merchants can configure it in the Theme Editor (text, images, colors, toggles, ranges).
- **No hard-coded copy**: user-facing strings live in `locales/en.default.json` and are referenced via `{{ 'key.path' | t }}`.
- **Performance first**: minimal JS (web components / progressive enhancement), Liquid-rendered HTML, lazy-loaded media. Avoid jQuery / heavy frameworks.
- **Color schemes**: use `color-scheme-N` classes (defined in `settings_schema.json`) instead of hardcoded colors so merchants can rebrand.

## Notes on this initial commit

The first commit contains the Dawn 15.4.1 source as a baseline reference. As we customize sections from designs, new files will be added and Dawn defaults overwritten. The `locales/en.default.schema.json` and other Dawn artifacts can be edited freely — this is your theme now, not a fork.

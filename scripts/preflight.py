#!/usr/bin/env python3
"""
Pre-package validation for sptheme.

Catches Shopify schema issues that `shopify theme check` misses but the
admin upload validator catches — most notably range setting defaults
that don't align to the step boundary.

Exits 0 if clean, 1 if any issues found.

Usage:
    python3 scripts/preflight.py
"""

import json, os, re, sys

SECTIONS_DIR = "sections"
TEMPLATES_DIR = "templates"

# Documented Shopify schema setting types.
# https://shopify.dev/docs/storefronts/themes/architecture/settings/input-settings
VALID_SETTING_TYPES = {
    # Basic
    "text", "textarea", "richtext", "inline_richtext", "html", "paragraph", "header",
    # Specialized
    "checkbox", "color", "color_scheme", "color_background", "color_scheme_group",
    "font_picker", "image_picker", "video", "video_url",
    "link_list", "url",
    "page", "blog", "article", "product", "product_list",
    "collection", "collection_list",
    "number", "range", "radio", "select",
    "liquid", "metaobject", "metaobject_list",
    "style.font_picker", "style.layout", "style.size",
}


def check_schema(schema, file):
    issues = []

    def walk(obj, path=""):
        if isinstance(obj, dict):
            t = obj.get("type")
            if t and "id" in obj and t not in VALID_SETTING_TYPES and "options" not in obj:
                # Settings have type+id; block defs have type+name; preset blocks have type+settings.
                # Only flag actual setting nodes (best-effort heuristic).
                pass  # other type fields are fine

            # Setting-level checks
            if t == "range" and "default" in obj:
                mn, mx = obj.get("min", 0), obj.get("max")
                st, df = obj.get("step", 1), obj["default"]
                if (df - mn) % st != 0:
                    issues.append(
                        f"{path}: range '{obj.get('id')}' default={df} doesn't align to step={st} "
                        f"(min={mn}). Use min + N*step. Nearest valid: {mn + round((df-mn)/st)*st}"
                    )
                if mx is not None and df > mx:
                    issues.append(f"{path}: range '{obj.get('id')}' default={df} > max={mx}")
                if df < mn:
                    issues.append(f"{path}: range '{obj.get('id')}' default={df} < min={mn}")

            if t == "number" and "default" in obj and not isinstance(obj["default"], (int, float)):
                issues.append(f"{path}: number '{obj.get('id')}' has non-numeric default")

            if t == "checkbox" and "default" in obj and not isinstance(obj["default"], bool):
                issues.append(f"{path}: checkbox '{obj.get('id')}' has non-bool default")

            if t == "select":
                opts = obj.get("options", [])
                values = [o.get("value") for o in opts]
                if "default" in obj and obj["default"] not in values:
                    issues.append(
                        f"{path}: select '{obj.get('id')}' default={obj['default']!r} "
                        f"not in options {values}"
                    )

            if t == "radio":
                opts = obj.get("options", [])
                values = [o.get("value") for o in opts]
                if "default" in obj and obj["default"] not in values:
                    issues.append(
                        f"{path}: radio '{obj.get('id')}' default={obj['default']!r} "
                        f"not in options {values}"
                    )

            for k, v in obj.items():
                walk(v, f"{path}.{k}" if path else k)

        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]")

    walk(schema)
    return issues


def main():
    all_issues = []

    # 1. Validate every section schema
    section_types = {}
    for f in sorted(os.listdir(SECTIONS_DIR)):
        if not f.endswith(".liquid"):
            continue
        path = os.path.join(SECTIONS_DIR, f)
        content = open(path).read()
        m = re.search(r"\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}", content, re.DOTALL)
        if not m:
            # No schema is fine for some files
            continue
        try:
            schema = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            all_issues.append(f"{path}: SCHEMA NOT VALID JSON — {e}")
            continue
        issues = check_schema(schema, path)
        if issues:
            for i in issues:
                all_issues.append(f"  {f}: {i}")
        # Track section type (filename without .liquid)
        section_types[f[:-len(".liquid")]] = path

    # 2. Validate every template's section references + 25-section cap
    for f in sorted(os.listdir(TEMPLATES_DIR)):
        if not f.endswith(".json"):
            continue
        path = os.path.join(TEMPLATES_DIR, f)
        try:
            tpl = json.load(open(path))
        except json.JSONDecodeError as e:
            all_issues.append(f"{path}: NOT VALID JSON — {e}")
            continue
        sections_obj = tpl.get("sections", {})
        if len(sections_obj) > 25:
            all_issues.append(
                f"  {f}: has {len(sections_obj)} sections; Shopify caps "
                f"templates at 25. Remove {len(sections_obj) - 25} or move "
                f"to a section group."
            )
        for sec_id, sec in sections_obj.items():
            sec_type = sec.get("type")
            if sec_type and sec_type not in section_types:
                if not os.path.exists(os.path.join(SECTIONS_DIR, f"{sec_type}.liquid")):
                    all_issues.append(
                        f"  {f}: section '{sec_id}' references type '{sec_type}' "
                        f"but no sections/{sec_type}.liquid exists"
                    )

    if all_issues:
        print("PRE-FLIGHT FAILED:\n")
        for i in all_issues:
            print(i)
        sys.exit(1)
    else:
        print(f"Pre-flight clean: {len(section_types)} sections, schemas valid.")


if __name__ == "__main__":
    main()

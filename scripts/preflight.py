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
                # Float-safe step check: compute steps from min, compare with epsilon
                steps_from_min = (df - mn) / st if st else 0
                if abs(steps_from_min - round(steps_from_min)) > 1e-6:
                    issues.append(
                        f"{path}: range '{obj.get('id')}' default={df} doesn't align to step={st} "
                        f"(min={mn}). Use min + N*step. Nearest valid: {mn + round(steps_from_min)*st}"
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
    section_range_limits = {}  # sec_type -> {setting_id: (min, max)}
    for f in sorted(os.listdir(SECTIONS_DIR)):
        if not f.endswith(".liquid"):
            continue
        path = os.path.join(SECTIONS_DIR, f)
        content = open(path).read()
        m = re.search(r"\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}", content, re.DOTALL)
        if not m:
            # No schema is fine for some files
            continue
        schema_str = m.group(1)
        try:
            schema = json.loads(schema_str)
        except json.JSONDecodeError:
            # Shopify accepts trailing commas; strict JSON doesn't. Strip them.
            cleaned = re.sub(r",(\s*[}\]])", r"\1", schema_str)
            try:
                schema = json.loads(cleaned)
            except json.JSONDecodeError as e:
                all_issues.append(f"{path}: SCHEMA NOT VALID JSON — {e}")
                continue
        issues = check_schema(schema, path)
        if issues:
            for i in issues:
                all_issues.append(f"  {f}: {i}")
        sec_name = f[:-len(".liquid")]
        section_types[sec_name] = path
        # Record range limits for template value validation
        limits = {}
        def collect_ranges(obj):
            if isinstance(obj, dict):
                if obj.get("type") == "range" and "id" in obj and "max" in obj:
                    limits[obj["id"]] = (obj.get("min", 0), obj["max"])
                for v in obj.values():
                    collect_ranges(v)
            elif isinstance(obj, list):
                for v in obj:
                    collect_ranges(v)
        collect_ranges(schema)
        section_range_limits[sec_name] = limits

    # 2. Validate every template's section references + 25-section cap
    for f in sorted(os.listdir(TEMPLATES_DIR)):
        if not f.endswith(".json"):
            continue
        path = os.path.join(TEMPLATES_DIR, f)
        if os.path.getsize(path) == 0:
            # Aeon ships empty template files for templates rendered via section groups
            continue
        raw = open(path).read()
        # Strip C-style comments (Aeon ships them at the top of some templates)
        raw_clean = re.sub(r'/\*.*?\*/', '', raw, flags=re.DOTALL)
        try:
            tpl = json.loads(raw_clean) if raw_clean.strip() else {}
        except json.JSONDecodeError as e:
            all_issues.append(f"{path}: NOT VALID JSON — {e}")
            continue
        if not tpl:
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
            # Validate template setting values against schema range min/max
            limits = section_range_limits.get(sec_type, {})
            for setting_id, val in sec.get("settings", {}).items():
                if setting_id in limits and isinstance(val, (int, float)):
                    mn, mx = limits[setting_id]
                    if val > mx:
                        all_issues.append(
                            f"  {f}: section '{sec_id}' setting '{setting_id}'={val} "
                            f"exceeds schema max={mx} (Shopify rejects on save)"
                        )
                    if val < mn:
                        all_issues.append(
                            f"  {f}: section '{sec_id}' setting '{setting_id}'={val} "
                            f"below schema min={mn}"
                        )
            # Flag section-group sections that hardcode a template instance ID
            if sec_type == "section-group":
                for k, v in sec.get("settings", {}).items():
                    if isinstance(v, str) and "shopify-section-template--" in v:
                        all_issues.append(
                            f"  {f}: section-group '{sec_id}' setting '{k}' hardcodes a "
                            f"template instance ID ({v[:50]}...) — won't resolve in other "
                            f"stores. Remove the section-group or re-point in Theme Editor."
                        )

    if all_issues:
        print("PRE-FLIGHT FAILED:\n")
        for i in all_issues:
            print(i)
        sys.exit(1)
    else:
        # Also check global settings_data.json
        gs_issues = check_global_settings()
        if gs_issues:
            print("PRE-FLIGHT FAILED:\n")
            for i in gs_issues:
                print(i)
            sys.exit(1)
        print(f"Pre-flight clean: {len(section_types)} sections, schemas valid.")


def check_global_settings():
    """Validate config/settings_data.json values against config/settings_schema.json range constraints."""
    issues = []
    try:
        schema = json.load(open("config/settings_schema.json"))
        data = json.load(open("config/settings_data.json"))
    except (FileNotFoundError, json.JSONDecodeError):
        return issues

    range_limits = {}
    def walk(obj):
        if isinstance(obj, dict):
            if obj.get("type") == "range" and "id" in obj:
                range_limits[obj["id"]] = (obj.get("min"), obj.get("max"), obj.get("step"))
            for v in obj.values(): walk(v)
        elif isinstance(obj, list):
            for v in obj: walk(v)
    walk(schema)

    cur = data.get("current", {})
    if isinstance(cur, str):
        cur = data.get("presets", {}).get(cur, {})
    for k, v in cur.items():
        if k in range_limits and isinstance(v, (int, float)):
            mn, mx, st = range_limits[k]
            if mx is not None and v > mx:
                issues.append(f"  settings_data.json: '{k}'={v} > schema max={mx} (Shopify rejects on save)")
            if mn is not None and v < mn:
                issues.append(f"  settings_data.json: '{k}'={v} < schema min={mn}")
            if st and mn is not None:
                steps = (v - mn) / st
                if abs(steps - round(steps)) > 1e-6:
                    issues.append(f"  settings_data.json: '{k}'={v} doesn't align to step={st} from min={mn}")
    return issues


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate UGC + advisor PLACEHOLDER images via Gemini.

These are NOT for production. They're stand-ins so the merchant can
preview the design with realistic faces in the slots before swapping
in real customers / advisors.
"""

import base64, os, sys
import requests

API_KEY = os.environ["GEMINI_API_KEY"]
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"
OUT = "/home/user/sptheme/assets"

JOBS = [
    # UGC review thumbnails — women, 40s/50s, lifestyle, warm light
    {"name": "sp-ugc-1", "prompt": (
        "Editorial lifestyle photograph. A woman, mid-40s, soft natural makeup, "
        "looking calmly to camera while sitting at a bright kitchen counter with "
        "morning sunlight. Wearing a soft cream cardigan. Warm window light, soft "
        "shadows. Square 1:1 composition. Premium wellness brand mood. Cream and "
        "blush palette. Photorealistic, high resolution, no logos or text."
    )},
    {"name": "sp-ugc-2", "prompt": (
        "Editorial lifestyle photograph. A woman, late 40s, gentle smile, brown "
        "hair, soft shoulders visible, in a softly lit bedroom near a window with "
        "sheer linen curtains. Casual cream loungewear. Warm morning light, soft "
        "shadows. Square 1:1 composition. Premium wellness brand mood, cream "
        "and blush palette. Photorealistic, high resolution, no logos or text."
    )},
    {"name": "sp-ugc-3", "prompt": (
        "Editorial lifestyle photograph. A woman, early 50s, silver-streaked hair "
        "in a relaxed wave, holding a ceramic mug, sitting in a sunlit garden "
        "chair with greenery softly out of focus behind. Cream sweater. Warm "
        "natural light, soft shadows, golden hour. Square 1:1 composition. "
        "Photorealistic, high resolution, no logos or text."
    )},
    # Advisor headshots — placeholder physicians, white coats, neutral backgrounds
    {"name": "sp-advisor-1", "prompt": (
        "Professional editorial headshot. A woman in her late 40s, blonde wavy "
        "hair, warm smile, wearing a clean white medical coat over a soft beige "
        "top, simple gold pendant necklace. Plain warm beige seamless paper "
        "background. Soft even studio lighting, slight shadow. Editorial wellness "
        "brand mood, not LinkedIn-stiff. Square 1:1 composition, head and "
        "shoulders. Photorealistic, high resolution, no name tag or text."
    )},
    {"name": "sp-advisor-2", "prompt": (
        "Professional editorial headshot. A South Asian woman in her early 40s, "
        "long dark hair, warm gentle smile, wearing a white medical coat over a "
        "soft blush top, small gold hoop earrings. Plain warm beige seamless "
        "paper background. Soft even studio lighting, slight shadow. Editorial "
        "wellness brand mood. Square 1:1 composition, head and shoulders. "
        "Photorealistic, high resolution, no name tag or text."
    )},
    {"name": "sp-advisor-3", "prompt": (
        "Professional editorial headshot. An East Asian woman in her late 30s, "
        "short bob haircut, warm bright smile, wearing a soft cream cashmere "
        "sweater (no medical coat), small gold pendant. Plain warm sage-green "
        "seamless paper background. Soft even studio lighting, slight shadow. "
        "Editorial wellness brand mood. Square 1:1 composition, head and "
        "shoulders. Photorealistic, high resolution, no text."
    )},
    {"name": "sp-advisor-4", "prompt": (
        "Professional editorial headshot. A Black woman in her 40s, natural "
        "curly hair, warm bright smile, wearing a clean white medical coat over "
        "a soft beige top, gold hoop earrings and small gold ring necklace. "
        "Plain warm beige seamless paper background. Soft even studio lighting, "
        "slight shadow. Editorial wellness brand mood. Square 1:1 composition, "
        "head and shoulders. Photorealistic, high resolution, no text."
    )},
]


def gen(job):
    body = {"contents": [{"parts": [{"text": job["prompt"]}]}]}
    r = requests.post(URL, params={"key": API_KEY},
                      headers={"Content-Type": "application/json"},
                      json=body, timeout=120)
    if r.status_code != 200:
        print(f"  ERROR {r.status_code}: {r.text[:200]}")
        return False
    data = r.json()
    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            img = base64.b64decode(inline["data"])
            mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
            ext = "jpg" if "jpeg" in mime else "png"
            out = os.path.join(OUT, f"{job['name']}.{ext}")
            with open(out, "wb") as f:
                f.write(img)
            print(f"  saved {out} ({len(img):,} bytes)")
            return True
    print("  no image returned")
    return False


for job in JOBS:
    print(f"generating {job['name']}...")
    gen(job)

#!/usr/bin/env python3
"""Generate ingredient close-ups via Gemini 2.5 Flash Image (Nano Banana)."""

import base64, json, os, sys
import requests

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    sys.exit("GEMINI_API_KEY not set")

MODEL = "gemini-2.5-flash-image"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

OUT_DIR = "/home/user/sptheme/assets"

JOBS = [
    {
        "name": "sp-ing-black-maca",
        "prompt": (
            "A close-up macro photograph of a single fresh black maca root "
            "(Lepidium meyenii), dark brown, almost black, with subtle texture "
            "and earthy details. Soft warm natural lighting, slight shadows, "
            "centered on a plain warm cream-colored seamless paper background. "
            "Editorial product photography, square 1:1 composition, shallow depth "
            "of field. Soft, premium, apothecary aesthetic. Color palette: warm "
            "cream background (#FAF1EA), root in deep brown/black tones. "
            "Photorealistic, high resolution, no text or labels."
        ),
    },
    {
        "name": "sp-ing-red-maca",
        "prompt": (
            "A close-up macro photograph of a single fresh red maca root "
            "(Lepidium meyenii), distinct rosy/burgundy/coral color with subtle "
            "earthy texture. Soft warm natural lighting, slight shadows, centered "
            "on a plain warm cream-colored seamless paper background. Editorial "
            "product photography, square 1:1 composition, shallow depth of field. "
            "Soft, premium, apothecary aesthetic. Color palette: warm cream "
            "background (#FAF1EA), root in coral/red tones (#ED1B28 / #FE756F). "
            "Photorealistic, high resolution, no text or labels."
        ),
    },
    {
        "name": "sp-ing-yellow-maca",
        "prompt": (
            "A close-up macro photograph of a single fresh yellow maca root "
            "(Lepidium meyenii), pale cream/yellow color with subtle earthy "
            "texture. Soft warm natural lighting, slight shadows, centered on a "
            "plain warm blush-colored seamless paper background. Editorial "
            "product photography, square 1:1 composition, shallow depth of field. "
            "Soft, premium, apothecary aesthetic. Color palette: warm cream/blush "
            "background, root in pale yellow tones. Photorealistic, high "
            "resolution, no text or labels."
        ),
    },
    {
        "name": "sp-ing-bioperine",
        "prompt": (
            "A close-up macro photograph of a small pile of whole black "
            "peppercorns scattered on a plain warm cream-colored seamless paper "
            "background. Soft warm natural lighting, slight shadows. Editorial "
            "product photography, square 1:1 composition, shallow depth of field. "
            "Soft, premium, apothecary aesthetic. Color palette: warm cream "
            "background (#FAF1EA), peppercorns in deep brown/black. Photorealistic, "
            "high resolution, no text or labels."
        ),
    },
]


def generate_one(job):
    body = {
        "contents": [
            {"parts": [{"text": job["prompt"]}]}
        ]
    }
    r = requests.post(
        URL,
        params={"key": API_KEY},
        headers={"Content-Type": "application/json"},
        json=body,
        timeout=120,
    )
    if r.status_code != 200:
        print(f"  ERROR {r.status_code}: {r.text[:300]}")
        return False
    data = r.json()
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            img_bytes = base64.b64decode(inline["data"])
            mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
            ext = "jpg" if "jpeg" in mime else ("png" if "png" in mime else mime.split("/")[-1])
            out_path = os.path.join(OUT_DIR, f"{job['name']}.{ext}")
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            print(f"  saved {out_path} ({len(img_bytes):,} bytes, {mime})")
            return True
    print(f"  no image in response: {json.dumps(data)[:300]}")
    return False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for job in JOBS:
        print(f"generating {job['name']}...")
        generate_one(job)


if __name__ == "__main__":
    main()

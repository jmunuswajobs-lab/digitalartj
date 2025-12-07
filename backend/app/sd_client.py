
import base64
import os
import uuid
from typing import Tuple

import requests

from .config import settings

def ensure_output_dir() -> str:
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    return settings.OUTPUT_DIR

def _automatic1111_img2img(
    input_image_path: str,
    prompt: str,
    negative_prompt: str,
) -> str:
    """Call Automatic1111 /sdapi/v1/img2img API.

    Requires a running Automatic1111 instance with NSFW-capable model loaded.
    The user can manage models / LoRAs from CivitAI directly inside that UI.
    """
    url = settings.SD_API_URL.rstrip("/") + "/sdapi/v1/img2img"

    with open(input_image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "init_images": [img_b64],
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "denoising_strength": 0.6,
        "cfg_scale": 7,
        "sampler_name": "Euler a",
        "steps": 28,
        "width": 768,
        "height": 1024,
    }

    resp = requests.post(url, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("images"):
        raise RuntimeError("Automatic1111 returned no images")

    out_b64 = data["images"][0]
    out_bytes = base64.b64decode(out_b64.split(",", 1)[-1])

    ensure_output_dir()
    out_name = f"gen_{uuid.uuid4().hex}.png"
    out_path = os.path.join(settings.OUTPUT_DIR, out_name)
    with open(out_path, "wb") as f:
        f.write(out_bytes)

    return out_path

def generate_image(
    input_image_path: str,
    prompt: str,
    negative_prompt: str,
) -> str:
    """Main entrypoint for generation.

    Currently supports:
    - Automatic1111 (img2img)
    - mock mode for local testing without a model
    """
    mode = settings.SD_API_MODE

    if mode == "automatic1111":
        return _automatic1111_img2img(input_image_path, prompt, negative_prompt)

    # Mock: just copy input image to outputs
    ensure_output_dir()
    out_name = f"mock_{uuid.uuid4().hex}.png"
    out_path = os.path.join(settings.OUTPUT_DIR, out_name)
    with open(input_image_path, "rb") as src, open(out_path, "wb") as dst:
        dst.write(src.read())
    return out_path

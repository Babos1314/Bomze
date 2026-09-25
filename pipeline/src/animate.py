"""Animation stage: turns a still plan image into a short video clip
(the visible motion described in the plan: a hand pressing a button, a
zoom, a head shake, etc.). Providers here are image-to-video models.
"""
from __future__ import annotations

import os

from models import Plan


def _stub(image_path: str, plan: Plan, out_path: str, api_key: str | None, model: str) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path + ".motion.txt", "w", encoding="utf-8") as f:
        f.write(f"source_image={image_path}\nmotion_hint={plan.image}\nduration={plan.duration}")
    return out_path + ".motion.txt"


def _runway(image_path: str, plan: Plan, out_path: str, api_key: str | None, model: str) -> str:
    """Example real adapter sketch for Runway's image-to-video API. Requires
    an API key and the `requests` package; check Runway's current API docs
    for the exact endpoint/payload before using this in production."""
    if not api_key:
        raise RuntimeError("Runway adapter needs an API key")
    import requests

    with open(image_path, "rb") as f:
        image_bytes = f.read()
    resp = requests.post(
        "https://api.runwayml.com/v1/image_to_video",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"image": image_bytes},
        data={"prompt": plan.image, "model": model or "gen-3"},
        timeout=120,
    )
    resp.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    return out_path


PROVIDERS = {
    "stub": _stub,
    "runway": _runway,
}


def animate_plan(image_path: str, plan: Plan, out_path: str, provider: str, api_key: str | None, model: str) -> str:
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown animate provider {provider!r}. Known: {sorted(PROVIDERS)}")
    return PROVIDERS[provider](image_path, plan, out_path, api_key, model)

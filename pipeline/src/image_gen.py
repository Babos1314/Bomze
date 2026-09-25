"""Image generation stage: turns a PlanPrompt into a still image on disk.

Adapters are intentionally thin. Add a new provider by writing a function
with the same signature as `_stub` and registering it in PROVIDERS.
"""
from __future__ import annotations

import os

from prompts import PlanPrompt


def _stub(prompt: PlanPrompt, out_path: str, api_key: str | None, model: str) -> str:
    """No API key configured: write the prompt text next to where the image
    would go, so the manifest is still inspectable end to end."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path + ".prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt.prompt)
    return out_path + ".prompt.txt"


def _openai_images(prompt: PlanPrompt, out_path: str, api_key: str | None, model: str) -> str:
    """Example real adapter using the OpenAI Images API. Requires the
    `openai` package and OPENAI_API_KEY (or config.providers.image.api_key_env)."""
    if not api_key:
        raise RuntimeError("OPENAI image adapter needs an API key")
    from openai import OpenAI  # local import: optional dependency

    client = OpenAI(api_key=api_key)
    result = client.images.generate(model=model or "gpt-image-1", prompt=prompt.prompt, size="1792x1024")
    import base64

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(result.data[0].b64_json))
    return out_path


PROVIDERS = {
    "stub": _stub,
    "openai": _openai_images,
}


def generate_image(prompt: PlanPrompt, out_path: str, provider: str, api_key: str | None, model: str) -> str:
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown image provider {provider!r}. Known: {sorted(PROVIDERS)}")
    return PROVIDERS[provider](prompt, out_path, api_key, model)

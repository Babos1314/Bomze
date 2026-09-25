"""Voice generation stage: turns a plan's subtitle line into a spoken audio
clip. The voice used follows the charter's subtitle color rule: white lines
are read by the "human" voice, yellow lines by the "object_or_presenter"
voice, so the two speakers in a dialogue-style series stay distinct.
"""
from __future__ import annotations

import os

from models import Plan


def _stub(plan: Plan, out_path: str, api_key: str | None, voice_id: str) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path + ".line.txt", "w", encoding="utf-8") as f:
        f.write(f"[voice={voice_id or 'default'}] {plan.subtitle}")
    return out_path + ".line.txt"


def _elevenlabs(plan: Plan, out_path: str, api_key: str | None, voice_id: str) -> str:
    """Example real adapter using ElevenLabs' text-to-speech API. Requires
    the `requests` package and an API key."""
    if not api_key:
        raise RuntimeError("ElevenLabs adapter needs an API key")
    import requests

    text = plan.subtitle.strip("« »").strip()
    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={"text": text, "model_id": "eleven_multilingual_v2"},
        timeout=60,
    )
    resp.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    return out_path


PROVIDERS = {
    "stub": _stub,
    "elevenlabs": _elevenlabs,
}


def voice_for_plan(plan: Plan, voices: dict) -> str:
    return voices.get("object_or_presenter" if plan.subtitle_color == "yellow" else "human", "")


def generate_voice(plan: Plan, out_path: str, provider: str, api_key: str | None, voices: dict) -> str:
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown voice provider {provider!r}. Known: {sorted(PROVIDERS)}")
    return PROVIDERS[provider](plan, out_path, api_key, voice_for_plan(plan, voices))

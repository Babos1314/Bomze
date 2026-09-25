"""Builds an .ass subtitle file for a video, following the charter: white
text for the human character, yellow for an object/presenter, one cue per
plan, timed against the plan's own "0-3 s" duration range. The whole track
is shifted by `offset_s` so it lines up after the intro jingle in the final
assembly.
"""
from __future__ import annotations

import re

from models import Video

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: White,Arial,72,&H00FFFFFF,&H00000000,&H00000000,1,4,0,2,80,80,120,1
Style: Yellow,Arial,72,&H0000FFFF,&H00000000,&H00000000,1,4,0,2,80,80,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

DURATION_RE = re.compile(r"(\d+)\s*-\s*(\d+)\s*s")


def _parse_range(duration: str) -> tuple[float, float]:
    m = DURATION_RE.search(duration)
    if not m:
        return (0.0, 0.0)
    return (float(m.group(1)), float(m.group(2)))


def _fmt_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def build_ass(video: Video, offset_s: float = 2.0) -> str:
    """offset_s defaults to the charter's 2 s intro jingle."""
    lines = [ASS_HEADER]
    for plan in video.plans:
        start, end = _parse_range(plan.duration)
        if end <= start:
            continue
        style = "Yellow" if plan.subtitle_color == "yellow" else "White"
        text = plan.subtitle.replace("\n", "\\N")
        lines.append(
            f"Dialogue: 0,{_fmt_ts(start + offset_s)},{_fmt_ts(end + offset_s)},{style},,0,0,0,,{text}\n"
        )
    return "".join(lines)


def write_ass(video: Video, out_path: str, offset_s: float = 2.0) -> str:
    content = build_ass(video, offset_s=offset_s)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path

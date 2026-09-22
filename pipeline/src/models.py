"""Plain data classes shared by every pipeline stage.

These mirror the schema written by the storyboards/*.yaml files and the
characters/expressions/*.json + characters/poses/*.json prompt libraries.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Plan:
    plan: int
    duration: str
    image: str
    sound: str
    subtitle: str
    subtitle_color: str  # "white" (human) or "yellow" (object/presenter)


@dataclass
class Video:
    id: str
    series: int
    num: int
    title: str
    character: str  # "pince-sans-rire" or "clown"
    duration_s: int
    text_lines: list[str]
    plans: list[Plan]


@dataclass
class Series:
    series: int
    key: str
    name: str
    character: str
    video_count: int
    videos: list[Video] = field(default_factory=list)

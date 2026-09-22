"""Loads storyboards/*.yaml and characters/{expressions,poses}/*.json into
the dataclasses defined in models.py, and gives every stage a single place
to look a video or a prompt up by id.
"""
from __future__ import annotations

import glob
import json
import os

import yaml

from models import Plan, Series, Video


def load_series(storyboards_dir: str) -> dict[str, Series]:
    series_by_key: dict[str, Series] = {}
    for path in sorted(glob.glob(os.path.join(storyboards_dir, "series-*.yaml"))):
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        videos = [
            Video(
                id=v["id"],
                series=v["series"],
                num=v["num"],
                title=v["title"],
                character=v["character"],
                duration_s=v["duration_s"],
                text_lines=v.get("text_lines", []),
                plans=[Plan(**p) for p in v["plans"]],
            )
            for v in raw["videos"]
        ]
        series = Series(
            series=raw["series"],
            key=raw["key"],
            name=raw["name"],
            character=raw["character"],
            video_count=raw["video_count"],
            videos=videos,
        )
        series_by_key[series.key] = series
    return series_by_key


def load_all_videos(storyboards_dir: str) -> dict[str, Video]:
    videos: dict[str, Video] = {}
    for series in load_series(storyboards_dir).values():
        for v in series.videos:
            videos[v.id] = v
    return videos


def find_video(storyboards_dir: str, video_id: str) -> Video:
    videos = load_all_videos(storyboards_dir)
    if video_id not in videos:
        raise KeyError(f"Unknown video id: {video_id!r}. Known ids: {sorted(videos)}")
    return videos[video_id]


def load_prompt_library(characters_dir: str, character: str, kind: str) -> dict:
    """kind is "expressions" or "poses"."""
    path = os.path.join(characters_dir, kind, f"{character}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_charter(storyboards_dir: str) -> dict:
    with open(os.path.join(storyboards_dir, "charte.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

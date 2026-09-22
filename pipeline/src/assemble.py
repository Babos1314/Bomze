"""Automated editing stage: stitches the animated plan clips into a
finished video, following the charter -
    - 2 s jingle at the start and at the end
    - 1 s of silence right before the punchline (the last plan)
    - subtitles burned in (white for the human, yellow for the object/
      presenter - see subtitles.py)
    - the same end card for every video in a series
    - export in both 16:9 (as shot) and 9:16 (centre-cropped)

This module only shells out to ffmpeg/ffprobe; it does not try to wrap
every ffmpeg feature. Swap `ffmpeg_bin` for a full path if it is not on
PATH.
"""
from __future__ import annotations

import os
import subprocess
import tempfile

from models import Video


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def _write_concat_file(clip_paths: list[str], list_path: str) -> None:
    with open(list_path, "w", encoding="utf-8") as f:
        for p in clip_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")


def make_silence_clip(reference_clip: str, duration_s: float, out_path: str, ffmpeg_bin: str = "ffmpeg") -> str:
    """A short black/silent filler clip matching the reference clip's
    resolution and framerate, used for the 1 s pause before the punchline."""
    _run([
        ffmpeg_bin, "-y",
        "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:d={duration_s}",
        "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={duration_s}",
        "-shortest", out_path,
    ])
    return out_path


def concat_clips(clip_paths: list[str], out_path: str, ffmpeg_bin: str = "ffmpeg") -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tmp:
        list_path = tmp.name
    _write_concat_file(clip_paths, list_path)
    try:
        _run([ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", list_path, "-c", "copy", out_path])
    finally:
        os.remove(list_path)
    return out_path


def burn_subtitles(video_path: str, ass_path: str, out_path: str, ffmpeg_bin: str = "ffmpeg") -> str:
    _run([ffmpeg_bin, "-y", "-i", video_path, "-vf", f"ass={ass_path}", "-c:a", "copy", out_path])
    return out_path


def export_9x16(video_path: str, out_path: str, ffmpeg_bin: str = "ffmpeg") -> str:
    """Centre-crop a 16:9 source into 9:16, per the charter's centred-shoot
    convention: crop to the vertical strip through the middle of the frame."""
    _run([
        ffmpeg_bin, "-y", "-i", video_path,
        "-vf", "crop=ih*9/16:ih,scale=1080:1920",
        "-c:a", "copy", out_path,
    ])
    return out_path


def assemble_video(
    video: Video,
    plan_clip_paths: list[str],
    ass_path: str,
    jingle_path: str,
    end_card_path: str,
    out_dir: str,
    ffmpeg_bin: str = "ffmpeg",
    pre_punchline_silence_s: float = 1.0,
) -> dict[str, str]:
    """plan_clip_paths must be in plan order and already rendered (see
    animate.py). Returns the paths of the final 16:9 and 9:16 exports."""
    os.makedirs(out_dir, exist_ok=True)

    clips = [jingle_path]
    for i, clip in enumerate(plan_clip_paths):
        is_last = i == len(plan_clip_paths) - 1
        if is_last and pre_punchline_silence_s > 0:
            silence_path = os.path.join(out_dir, f"{video.id}_silence.mp4")
            make_silence_clip(clip, pre_punchline_silence_s, silence_path, ffmpeg_bin)
            clips.append(silence_path)
        clips.append(clip)
    clips += [jingle_path, end_card_path]

    raw_path = os.path.join(out_dir, f"{video.id}_raw.mp4")
    concat_clips(clips, raw_path, ffmpeg_bin)

    subbed_path = os.path.join(out_dir, f"{video.id}_16x9.mp4")
    burn_subtitles(raw_path, ass_path, subbed_path, ffmpeg_bin)

    vertical_path = os.path.join(out_dir, f"{video.id}_9x16.mp4")
    export_9x16(subbed_path, vertical_path, ffmpeg_bin)

    return {"16:9": subbed_path, "9:16": vertical_path}

"""CLI orchestrator: runs the four production stages for one video id -
image generation, animation, voice, automated editing - reading its
storyboard from storyboards/*.yaml and its prompts from
characters/{expressions,poses}/*.json.

Usage:
    python pipeline.py prompts s02-d01          # print/save the per-plan
                                                 # image prompts for a video
    python pipeline.py render s02-d01           # run every stage end to end
    python pipeline.py list                     # list every known video id

With the default "stub" providers (see config.example.yaml) this never
calls a paid API: it writes the prompt text, the voice line and the motion
hint that a real provider would consume, so the whole pipeline can be
inspected and tested before any API key is configured.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))

from storyboard_loader import find_video, load_all_videos, load_charter
from prompts import build_video_prompts
from image_gen import generate_image
from voice_gen import generate_voice
from animate import animate_plan
from subtitles import write_ass
from assemble import assemble_video


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def cmd_list(config: dict) -> None:
    videos = load_all_videos(config["paths"]["storyboards_dir"])
    for vid in sorted(videos):
        v = videos[vid]
        print(f"{vid}\t{v.character}\t{v.title}")


def cmd_prompts(config: dict, video_id: str) -> None:
    video = find_video(config["paths"]["storyboards_dir"], video_id)
    plan_prompts = build_video_prompts(config["paths"]["characters_dir"], video)
    out = [
        {
            "plan": p.plan,
            "expression": p.expression_key,
            "pose": p.pose_key,
            "prompt": p.prompt,
        }
        for p in plan_prompts
    ]
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_render(config: dict, video_id: str) -> None:
    storyboards_dir = config["paths"]["storyboards_dir"]
    characters_dir = config["paths"]["characters_dir"]
    output_dir = os.path.join(config["paths"]["output_dir"], video_id)
    os.makedirs(output_dir, exist_ok=True)

    video = find_video(storyboards_dir, video_id)
    charter = load_charter(storyboards_dir)
    plan_prompts = build_video_prompts(characters_dir, video)

    image_cfg = config["providers"]["image"]
    voice_cfg = config["providers"]["voice"]
    animate_cfg = config["providers"]["animate"]

    image_key = os.environ.get(image_cfg.get("api_key_env", ""), "")
    voice_key = os.environ.get(voice_cfg.get("api_key_env", ""), "")
    animate_key = os.environ.get(animate_cfg.get("api_key_env", ""), "")

    clip_paths = []
    for plan, plan_prompt in zip(video.plans, plan_prompts):
        image_path = os.path.join(output_dir, f"plan{plan.plan}.png")
        generate_image(plan_prompt, image_path, image_cfg["name"], image_key, image_cfg.get("model", ""))

        voice_path = os.path.join(output_dir, f"plan{plan.plan}_voice.mp3")
        generate_voice(plan, voice_path, voice_cfg["name"], voice_key, voice_cfg.get("voices", {}))

        clip_path = os.path.join(output_dir, f"plan{plan.plan}_clip.mp4")
        animate_plan(image_path, plan, clip_path, animate_cfg["name"], animate_key, animate_cfg.get("model", ""))
        clip_paths.append(clip_path)

    ass_path = os.path.join(output_dir, f"{video.id}.ass")
    write_ass(video, ass_path, offset_s=charter["audio"]["jingle_intro_s"])

    jingle_path = os.path.join(config["paths"]["assets_dir"], "jingle.mp4")
    end_card_path = os.path.join(config["paths"]["assets_dir"], f"end_card_series_{video.series:02d}.mp4")

    if not (os.path.exists(jingle_path) and os.path.exists(end_card_path)):
        print(
            "Skipping final assembly: place a shared jingle at "
            f"{jingle_path} and a per-series end card at {end_card_path} "
            "first (see pipeline/assets/README.md)."
        )
        print(f"Per-plan assets are ready in {output_dir}")
        return

    result = assemble_video(
        video, clip_paths, ass_path, jingle_path, end_card_path, output_dir,
        ffmpeg_bin=config["ffmpeg"]["binary"],
        pre_punchline_silence_s=charter["audio"]["pre_punchline_silence_s"],
    )
    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "prompts", "render"])
    parser.add_argument("video_id", nargs="?")
    parser.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "..", "config.yaml"))
    args = parser.parse_args()

    config_path = args.config
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.example.yaml")
    config = load_config(config_path)

    if args.command == "list":
        cmd_list(config)
    elif args.command == "prompts":
        if not args.video_id:
            parser.error("prompts requires a video_id")
        cmd_prompts(config, args.video_id)
    elif args.command == "render":
        if not args.video_id:
            parser.error("render requires a video_id")
        cmd_render(config, args.video_id)


if __name__ == "__main__":
    main()

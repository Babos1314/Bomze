"""Turns a storyboard plan into a ready-to-send image-generation prompt by
combining the character reference description with the closest entry from
the expression/pose libraries, plus the plan's own scene description.

This is intentionally a simple, inspectable keyword match rather than an
LLM call: the prompt libraries are small (8 expressions + ~20 poses per
character), so a human can always override the pick in the generated
manifest before it is sent to image_gen.py.
"""
from __future__ import annotations

from dataclasses import dataclass

from models import Plan, Video
from storyboard_loader import load_prompt_library

BASE_SCENE_SUFFIX = (
    "Scene context: {scene}. Keep the character design, outfit and framing "
    "identical to the reference sheet; only the pose, expression and props "
    "described here should change."
)


@dataclass
class PlanPrompt:
    video_id: str
    plan: int
    character: str
    expression_key: str | None
    pose_key: str | None
    prompt: str


def _best_match(text: str, entries: list[dict], text_field: str) -> dict | None:
    """Scores each library entry by how many of its own French label words
    appear in the plan's image description, and returns the best match."""
    text_lower = text.lower()
    best, best_score = None, 0
    for entry in entries:
        label = entry.get("label_fr", "")
        words = [w.strip(",;.:") for w in label.lower().split() if len(w) > 3]
        score = sum(1 for w in words if w in text_lower)
        if score > best_score:
            best, best_score = entry, score
    return best if best_score > 0 else None


def build_plan_prompt(characters_dir: str, video: Video, plan: Plan) -> PlanPrompt:
    expressions = load_prompt_library(characters_dir, video.character, "expressions")["expressions"]
    poses = load_prompt_library(characters_dir, video.character, "poses")["poses"]

    pose_match = _best_match(plan.image, poses, "label_fr")
    expr_match = _best_match(plan.image, expressions, "label_fr")

    if pose_match:
        base_prompt = pose_match["prompt"]
        pose_key = pose_match["key"]
    elif expr_match:
        base_prompt = expr_match["prompt"]
        pose_key = None
    else:
        # Fall back to a neutral deadpan/first expression so every plan still
        # gets a usable starting prompt.
        base_prompt = expressions[0]["prompt"]
        pose_key = None

    expr_key = expr_match["key"] if expr_match else None

    prompt = base_prompt + " " + BASE_SCENE_SUFFIX.format(scene=plan.image)

    return PlanPrompt(
        video_id=video.id,
        plan=plan.plan,
        character=video.character,
        expression_key=expr_key,
        pose_key=pose_key,
        prompt=prompt,
    )


def build_video_prompts(characters_dir: str, video: Video) -> list[PlanPrompt]:
    return [build_plan_prompt(characters_dir, video, plan) for plan in video.plans]

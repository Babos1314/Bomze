# Assets needed for automated assembly

The `assemble` stage (see `src/assemble.py`) expects two shared assets per
the charter (`storyboards/charte.yaml`):

- `jingle.mp4` — the 2-second jingle used identically at the start and end
  of every video (1920x1080, with audio).
- `end_card_series_XX.mp4` (or `.png`, converted to a short clip) — one end
  card per series, `XX` zero-padded (`end_card_series_01.mp4` for
  "Vannes courtes", etc.), showing the series name and episode number as
  described in the charter.

Until these exist, `pipeline.py render` still generates every per-plan
image/voice/clip and stops before final assembly, so the rest of the
pipeline can be tested without them.

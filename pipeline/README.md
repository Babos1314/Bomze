# Pipeline

Turns a storyboard entry from `../storyboards/*.yaml` into a finished,
subtitled, dual-format (16:9 + 9:16) video, in four stages:

1. **Image generation** (`src/image_gen.py`) — one still per plan, built
   from the matching character reference + expression/pose prompt (see
   `../characters/`) plus the plan's own scene description
   (`src/prompts.py` picks the closest expression/pose automatically).
2. **Voice** (`src/voice_gen.py`) — one line per plan, read by the "human"
   voice for white subtitles or the "object/presenter" voice for yellow
   ones, per the charter.
3. **Animation** (`src/animate.py`) — turns each still into a short clip
   using the plan's own motion description.
4. **Automated editing** (`src/assemble.py`, `src/subtitles.py`) —
   concatenates the clips, adds the 2 s intro/outro jingle, inserts the 1 s
   silence before the punchline, burns in the subtitles, appends the
   series' end card, and exports both aspect ratios.

## Setup

```bash
cd pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yaml config.yaml   # then edit provider names/keys
```

Each provider (`image`, `voice`, `animate`) defaults to a `stub` adapter
that writes the prompt/line/motion-hint as text instead of calling a paid
API, so the whole pipeline is runnable and inspectable with zero
configuration. Swap `name: stub` for a real provider (see the adapters
already sketched in each module - OpenAI Images, ElevenLabs, Runway) and
set the matching API key environment variable once you're ready to
generate real media. `ffmpeg`/`ffprobe` must be installed and on PATH for
the final assembly step.

## Usage

```bash
python src/pipeline.py list                 # every video id across all 54 videos
python src/pipeline.py prompts s02-d01       # inspect the per-plan image prompts
python src/pipeline.py render s02-d01        # run all four stages for one video
```

Video ids follow `s<series>-<kind><num>`, e.g. `s01-v03` (series 1, video
3), `s02-d05` (series 2, dialogue 5), `s04-s07` (series 4, sketch 7),
`s05-c02` (series 5, conseil 2), `s06-m01` (series 6, mot 1).

## Data sources

- `../storyboards/*.yaml` — one file per series, all 54 videos, extracted
  from the reference storyboard document (plan/duration/image/sound/subtitle
  per plan, plus each dialogue's lines).
- `../characters/*.md` — the two character bibles and reference-sheet prompts.
- `../characters/expressions/*.json` — the 8 required expressions per
  character, filled prompts ready to send to an image generator.
- `../characters/poses/*.json` — the curated hand-visible pose library per
  character, each entry mapped to the storyboards that use it.

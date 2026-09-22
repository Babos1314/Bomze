# Bomze

Production kit for a series of short, humorous social videos (16:9, 8 to
20 seconds each) built around two recurring semi-realistic animated
characters.

## Contents

- `characters/` — the two character bibles (`pince-sans-rire.md`,
  `clown.md`), each with its reference-sheet prompt, and:
  - `characters/expressions/*.json` — the 8 required expressions per
    character (deadpan, pensive, offended, triumphant, embarrassed,
    resigned, exhausted, oversold salesman smile), filled and ready to send
    to an image generator.
  - `characters/poses/*.json` — a curated, hand-visible pose library per
    character, each entry mapped to the storyboards that use it.
- `storyboards/` — all 54 videos across the 6 written series, one YAML
  file per series (`series-01-vannes-courtes.yaml` … `series-06-dico-du-coin.yaml`),
  plus `charte.yaml` (subtitle colors, jingle/silence timing, end card,
  publishing checklist) and `manifest.yaml` (series index).
- `pipeline/` — the production pipeline: image generation → voice →
  animation → automated editing (subtitles, jingle, end card, 16:9/9:16
  export). See `pipeline/README.md`.

## The two characters

1. **Le pince-sans-rire** — series 2 (Dialogues avec un objet), 4 (Le
   monde politique), 5 (Le conseil de l'expert).
2. **Le clown** — series 1 (Vannes courtes), 3 (Fausses pubs), 6 (Le Dico
   du coin).

## Series overview

| # | Série | Personnage | Vidéos |
| --- | --- | --- | --- |
| 1 | Vannes courtes | Clown | 12 |
| 2 | Dialogues avec un objet | Pince-sans-rire | 8 |
| 3 | Fausses pubs | Clown | 8 |
| 4 | Le monde politique | Pince-sans-rire | 10 |
| 5 | Le conseil de l'expert | Pince-sans-rire | 6 |
| 6 | Le Dico du coin | Clown | 10 |

**Total: 54 videos.**

## Quick start

```bash
cd pipeline
pip install -r requirements.txt
cp config.example.yaml config.yaml
python src/pipeline.py list                # every video id
python src/pipeline.py prompts s02-d01      # per-plan image-gen prompts
python src/pipeline.py render s02-d01       # run the full pipeline (stub providers by default)
```

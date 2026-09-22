# Personnage 1 — Le pince-sans-rire (validé)

Homme d'environ 40 ans, cheveux courts en désordre, barbe de deux jours,
sourcils très mobiles (principal outil d'expression), paupières lourdes,
regard direct vers la caméra, pull en laine vert bouteille, pantalon gris,
chaussures en cuir marron. Ton sobre, mauvaise foi assumée, sympathique.

Aucune ressemblance avec une personne réelle. Joue dans les séries
2 (Dialogues avec un objet), 4 (Le monde politique) et 5 (Le conseil de
l'expert).

## Tenues par série

| Série | Tenue |
| --- | --- |
| 2 (dialogues) | Pull vert bouteille, pantalon gris |
| 4 (monde politique) | Même pull sous une veste sombre, cravate desserrée |
| 5 (conseil de l'expert) | Veste sombre sur le pull vert bouteille |

## Prompt de planche de référence

```
Semi-realistic animated character, man around 40, short messy dark hair,
two-day stubble, very expressive mobile eyebrows with heavy eyelids, deadpan
look, bottle-green wool sweater, grey trousers, brown leather shoes, soft
studio lighting, plain light-grey background. Three views side by side:
front, three-quarter, side. Consistent proportions, original face, 16:9
```

## Garder le même personnage d'une image à l'autre

1. Créer d'abord la planche de référence ci-dessus (face, trois-quarts, profil).
2. Générer la planche des 8 expressions (`expressions/pince-sans-rire.json`).
3. Générer la bibliothèque de poses mains visibles (`poses/pince-sans-rire.json`).
4. Utiliser ces planches comme image de référence pour chaque nouvelle scène,
   sans jamais changer la description de base ci-dessus.

## Modèles de prompt (à réutiliser tels quels)

Expression :
```
Same character as the reference image: semi-realistic animated man around 40,
short messy dark hair, two-day stubble, very expressive mobile eyebrows with
heavy eyelids, bottle-green wool sweater. Expression: [EXPRESSION], exaggerated
expression with strongly emphasized eyebrows, eyes looking directly into the
lens. Chest-up framing, soft studio lighting, plain light-grey background, 16:9
```

Pose :
```
Same character as the reference image: semi-realistic animated man around 40,
short messy dark hair, two-day stubble, very expressive mobile eyebrows with
heavy eyelids, bottle-green wool sweater, grey trousers, brown leather shoes.
Pose: [POSE], exaggerated expression, eyes looking directly into the lens.
Three-quarter body framing, both hands clearly visible with five fingers each,
soft studio lighting, plain light-grey background, 16:9
```

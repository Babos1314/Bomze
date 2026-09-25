# Personnage 2 — Le clown (validé, v2 : animateur de cirque)

Homme d'environ 40 ans, visage chaleureux (entièrement inventé, sans
ressemblance avec une personne réelle), maquillage blanc classique de
clown, petit nez rond rouge, grande perruque bouclée multicolore façon
arc-en-ciel, large sourire. Redingote rouge façon maître de piste avec
galons dorés, nœud papillon à pois, pantalon bleu, chaussures bicolores
rouge-blanc-bleu, gants blancs. Tient souvent un micro vintage.
Personnalité d'animateur/présentateur de spectacle, chaleureux et un peu
too much.

Remplace l'ancienne version du clown (combinaison rayée noir et blanc).
Aucune ressemblance avec une personne réelle. Joue dans les séries
1 (Vannes courtes), 3 (Fausses pubs, dans le rôle du client ravi) et
6 (Le Dico du coin).

## Prompt de planche de référence (validé)

```
3D rendered CGI character, Pixar-style animated movie character: man around
40, warm friendly face (entirely invented, not based on any real person),
soft volumetric shading, subsurface scattering skin, classic white clown
face paint, small red round nose, big colorful curly rainbow afro wig, wide
cheerful smile. Wearing a red velvet ringmaster-style tailcoat with gold
braid trim, a polka-dot bow tie, blue trousers, two-tone red-white-blue
clown shoes, white gloves. Holding a vintage microphone. Three views side
by side: front, three-quarter, side. Soft studio lighting, plain
light-grey background, consistent proportions, semi-realistic 3D animated
style, high quality character turnaround. No text, no labels, no title, no
watermark, no annotations, no measurements.
```

## Garder le même personnage d'une image à l'autre

1. Créer d'abord la planche de référence ci-dessus (face, trois-quarts, profil).
2. Générer la planche des 8 expressions (`expressions/clown.json`).
3. Générer la bibliothèque de poses mains visibles (`poses/clown.json`).
4. Utiliser ces planches comme image de référence pour chaque nouvelle scène,
   sans jamais changer la description de base ci-dessus.

## Modèles de prompt (à réutiliser tels quels)

Expression :
```
Same character as the reference image: 3D rendered CGI Pixar-style animated
character, man around 40, warm friendly face, white clown face paint, small
red round nose, big colorful curly rainbow afro wig, red velvet
ringmaster-style tailcoat with gold braid trim, polka-dot bow tie. Expression:
[EXPRESSION], exaggerated expression with strongly emphasized eyebrows and
mouth, eyes looking directly into the lens. Chest-up framing, soft studio
lighting, plain light-grey background, 16:9. No text, no labels, no watermark.
```

Pose :
```
Same character as the reference image: 3D rendered CGI Pixar-style animated
character, man around 40, warm friendly face, white clown face paint, small
red round nose, big colorful curly rainbow afro wig, red velvet
ringmaster-style tailcoat with gold braid trim, polka-dot bow tie, blue
trousers, two-tone red-white-blue clown shoes, white gloves. Pose: [POSE],
exaggerated expression, eyes looking directly into the lens. Three-quarter
body framing, both hands clearly visible with five fingers each, soft studio
lighting, plain light-grey background, 16:9. No text, no labels, no watermark.
```

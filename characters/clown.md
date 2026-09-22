# Personnage 2 — Le clown (validé)

Homme d'environ 40 ans, visage rond et chaleureux, sans maquillage, nez
légèrement rouge, cheveux en bataille, combinaison rayée noir et blanc,
chaussures marron usées. Sourire large, énergie joyeuse et un peu
maladroite.

Aucune ressemblance avec une personne réelle. Joue dans les séries
1 (Vannes courtes), 3 (Fausses pubs, dans le rôle du client ravi) et
6 (Le Dico du coin).

## Prompt de planche de référence

```
Character reference sheet of a cheerful comedic animated character: man
around 40, chubby build, big round friendly face, large expressive eyes,
bushy eyebrows, tousled messy dark hair, small round red-tinted nose, warm
wide open-mouthed smile, no face paint. Wearing a black and white
horizontally striped jumpsuit, worn brown boots. Warm, friendly, slightly
goofy personality, original cartoon character design. Three views side by
side: front, three-quarter, side. Soft studio lighting, plain light-grey
background, consistent proportions, 16:9
```

Variante à proportions plus exagérées (utilisable pour la planche
d'expressions si un rendu plus cartoon est souhaité) :
```
Character reference sheet of a comedic animated character: man around 40,
exaggerated cartoon proportions, very big rubbery expressive face, oversized
bushy eyebrows, large round nose, wide mouth, big ears, messy dark hair,
playful expressive eyes, bottle-green wool sweater, grey trousers, brown
leather shoes. Three views side by side: front, three-quarter, side. Soft
studio lighting, plain light-grey background, consistent proportions,
original face, 16:9
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
Same character as the reference image: cheerful comedic animated man around
40, chubby build, big round friendly face, bushy eyebrows, tousled messy dark
hair, small round red-tinted nose, black and white horizontally striped
jumpsuit. Expression: [EXPRESSION], exaggerated expression with strongly
emphasized eyebrows and mouth, eyes looking directly into the lens. Chest-up
framing, soft studio lighting, plain light-grey background, 16:9
```

Pose :
```
Same character as the reference image: cheerful comedic animated man around
40, chubby build, big round friendly face, bushy eyebrows, tousled messy dark
hair, small round red-tinted nose, black and white horizontally striped
jumpsuit, worn brown boots. Pose: [POSE], exaggerated expression, eyes looking
directly into the lens. Three-quarter body framing, both hands clearly visible
with five fingers each, soft studio lighting, plain light-grey background, 16:9
```

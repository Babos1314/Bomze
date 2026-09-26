export type Recipe = {
  title: string;
  ingredients: string[];
  steps: string[];
};

const ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001';

const SYSTEM_PROMPT = `Tu es un chef cuisinier qui aide les gens a cuisiner un plat simple avec ce qu'il leur reste au frigo.
A partir de la liste d'ingredients donnee par l'utilisateur, propose UNE recette simple et realiste (temps de preparation raisonnable, etapes claires).
Tu peux supposer que des ingredients de base (sel, poivre, huile, eau) sont disponibles meme si l'utilisateur ne les mentionne pas.
Reponds UNIQUEMENT avec un objet JSON valide, sans texte autour, au format exact :
{"title": "Nom du plat", "ingredients": ["ingredient 1", "ingredient 2"], "steps": ["etape 1", "etape 2"]}`;

export async function generateRecipeFromIngredients(apiKey: string, ingredients: string): Promise<Recipe> {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: ANTHROPIC_MODEL,
      max_tokens: 1024,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: `Voici ce qu'il me reste : ${ingredients}` }],
    }),
  });

  if (response.status === 401) {
    throw new Error('Cle API invalide. Verifie ta cle Anthropic.');
  }
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Erreur de l'API (${response.status}) : ${body}`);
  }

  const data = await response.json();
  const text: string | undefined = data?.content?.[0]?.text;
  if (!text) {
    throw new Error("Reponse inattendue de l'IA.");
  }

  try {
    return JSON.parse(text) as Recipe;
  } catch {
    throw new Error("Impossible de lire la recette generee. Reessaie.");
  }
}

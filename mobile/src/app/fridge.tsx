import { useEffect, useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  TextInput,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, MaxContentWidth, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { clearStoredApiKey, getStoredApiKey, setStoredApiKey } from '@/lib/apiKeyStorage';
import { generateRecipeFromIngredients, type Recipe } from '@/lib/recipeAi';

export default function FridgeScreen() {
  const theme = useTheme();

  const [apiKey, setApiKey] = useState<string | null>(null);
  const [apiKeyInput, setApiKeyInput] = useState('');
  const [checkingApiKey, setCheckingApiKey] = useState(true);

  const [ingredients, setIngredients] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recipe, setRecipe] = useState<Recipe | null>(null);

  useEffect(() => {
    getStoredApiKey()
      .then(setApiKey)
      .finally(() => setCheckingApiKey(false));
  }, []);

  async function handleSaveApiKey() {
    const trimmed = apiKeyInput.trim();
    if (!trimmed) return;
    await setStoredApiKey(trimmed);
    setApiKey(trimmed);
    setApiKeyInput('');
  }

  async function handleChangeApiKey() {
    await clearStoredApiKey();
    setApiKey(null);
    setRecipe(null);
    setError(null);
  }

  async function handleGenerate() {
    if (!apiKey || !ingredients.trim()) return;
    setLoading(true);
    setError(null);
    setRecipe(null);
    try {
      const result = await generateRecipeFromIngredients(apiKey, ingredients.trim());
      setRecipe(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Une erreur est survenue.");
    } finally {
      setLoading(false);
    }
  }

  const inputStyle = [
    styles.input,
    { color: theme.text, backgroundColor: theme.backgroundElement, borderColor: theme.backgroundSelected },
  ];

  if (checkingApiKey) {
    return (
      <ThemedView style={styles.container}>
        <SafeAreaView style={styles.safeArea}>
          <ActivityIndicator />
        </SafeAreaView>
      </ThemedView>
    );
  }

  if (!apiKey) {
    return (
      <ThemedView style={styles.container}>
        <SafeAreaView style={styles.safeArea}>
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <ThemedText type="title">Reste du frigo</ThemedText>
            <ThemedText type="default" themeColor="textSecondary" style={styles.subtitle}>
              Colle ta cle API Anthropic pour activer la generation de recettes par IA.
            </ThemedText>
            <TextInput
              value={apiKeyInput}
              onChangeText={setApiKeyInput}
              placeholder="sk-ant-..."
              placeholderTextColor={theme.textSecondary}
              secureTextEntry
              autoCapitalize="none"
              autoCorrect={false}
              style={inputStyle}
            />
            <Pressable
              onPress={handleSaveApiKey}
              style={({ pressed }) => [styles.button, { backgroundColor: theme.text }, pressed && styles.pressed]}>
              <ThemedText type="smallBold" themeColor="background">
                Enregistrer la cle
              </ThemedText>
            </Pressable>
          </ScrollView>
        </SafeAreaView>
      </ThemedView>
    );
  }

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <ScrollView contentContainerStyle={styles.scrollContent}>
          <ThemedText type="title">Reste du frigo</ThemedText>
          <ThemedText type="default" themeColor="textSecondary" style={styles.subtitle}>
            Indique ce qu&apos;il te reste, l&apos;IA te propose une recette.
          </ThemedText>

          <TextInput
            value={ingredients}
            onChangeText={setIngredients}
            placeholder="ex: 2 oeufs, des courgettes, du riz"
            placeholderTextColor={theme.textSecondary}
            multiline
            style={[inputStyle, styles.multilineInput]}
          />

          <Pressable
            onPress={handleGenerate}
            disabled={loading || !ingredients.trim()}
            style={({ pressed }) => [
              styles.button,
              { backgroundColor: theme.text },
              (pressed || loading || !ingredients.trim()) && styles.pressed,
            ]}>
            {loading ? (
              <ActivityIndicator color={theme.background} />
            ) : (
              <ThemedText type="smallBold" themeColor="background">
                Proposer une recette
              </ThemedText>
            )}
          </Pressable>

          {error && (
            <ThemedView type="backgroundElement" style={styles.card}>
              <ThemedText type="default">{error}</ThemedText>
            </ThemedView>
          )}

          {recipe && (
            <ThemedView type="backgroundElement" style={styles.card}>
              <ThemedText type="subtitle">{recipe.title}</ThemedText>

              <ThemedText type="smallBold" style={styles.sectionTitle}>
                Ingredients
              </ThemedText>
              {recipe.ingredients.map((item, index) => (
                <ThemedText key={index} type="default">
                  {'• '}
                  {item}
                </ThemedText>
              ))}

              <ThemedText type="smallBold" style={styles.sectionTitle}>
                Etapes
              </ThemedText>
              {recipe.steps.map((step, index) => (
                <ThemedText key={index} type="default" style={styles.step}>
                  {index + 1}. {step}
                </ThemedText>
              ))}
            </ThemedView>
          )}

          <Pressable onPress={handleChangeApiKey} style={styles.changeKeyLink}>
            <ThemedText type="link" themeColor="textSecondary">
              Changer la cle API
            </ThemedText>
          </Pressable>
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'row',
  },
  safeArea: {
    flex: 1,
    width: '100%',
  },
  scrollContent: {
    paddingHorizontal: Spacing.four,
    paddingBottom: BottomTabInset + Spacing.three,
    gap: Spacing.three,
    alignSelf: 'center',
    width: '100%',
    maxWidth: MaxContentWidth,
  },
  subtitle: {
    marginBottom: Spacing.two,
  },
  input: {
    borderWidth: 1,
    borderRadius: Spacing.three,
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.two,
    fontSize: 16,
  },
  multilineInput: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  button: {
    borderRadius: Spacing.three,
    paddingVertical: Spacing.three,
    alignItems: 'center',
    justifyContent: 'center',
  },
  pressed: {
    opacity: 0.7,
  },
  card: {
    borderRadius: Spacing.three,
    padding: Spacing.three,
    gap: Spacing.one,
  },
  sectionTitle: {
    marginTop: Spacing.two,
  },
  step: {
    marginTop: Spacing.half,
  },
  changeKeyLink: {
    alignItems: 'center',
    marginTop: Spacing.two,
  },
});

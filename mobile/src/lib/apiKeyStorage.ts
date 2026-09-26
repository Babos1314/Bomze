import AsyncStorage from '@react-native-async-storage/async-storage';

const API_KEY_STORAGE_KEY = 'eco-chef.anthropic-api-key';

export async function getStoredApiKey(): Promise<string | null> {
  return AsyncStorage.getItem(API_KEY_STORAGE_KEY);
}

export async function setStoredApiKey(apiKey: string): Promise<void> {
  await AsyncStorage.setItem(API_KEY_STORAGE_KEY, apiKey);
}

export async function clearStoredApiKey(): Promise<void> {
  await AsyncStorage.removeItem(API_KEY_STORAGE_KEY);
}

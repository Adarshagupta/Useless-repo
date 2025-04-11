import { useEffect, useState } from 'react';
import { Stack, SplashScreen } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useFrameworkReady } from '@/hooks/useFrameworkReady';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Keep the splash screen visible while we fetch resources
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [isReady, setIsReady] = useState(false);
  const [initialRoute, setInitialRoute] = useState<string | null>(null);

  useFrameworkReady();

  useEffect(() => {
    async function prepare() {
      try {
        // Check if user is logged in
        const token = await AsyncStorage.getItem('userToken');

        // Set initial route based on authentication status
        if (token) {
          setInitialRoute('/(tabs)');
        } else {
          setInitialRoute('/splash');
        }
      } catch (e) {
        console.warn('Error preparing app:', e);
        setInitialRoute('/splash');
      } finally {
        // Tell the application to render
        setIsReady(true);
        SplashScreen.hideAsync();
      }
    }

    prepare();
  }, []);

  if (!isReady || !initialRoute) {
    return null;
  }

  return (
    <>
      <Stack screenOptions={{ headerShown: false, animation: 'fade' }}>
        <Stack.Screen name="splash" />
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="(auth)" />
        <Stack.Screen name="+not-found" options={{ presentation: 'modal' }} />
      </Stack>
      <StatusBar style="auto" />
    </>
  );
}
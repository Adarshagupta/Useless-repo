import React from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useFrameworkReady } from '@/hooks/useFrameworkReady';
import { AuthProvider } from './context/AuthContext';

export default function RootLayout() {
  useFrameworkReady();

  return (
    <AuthProvider>
      <>
        <Stack screenOptions={{ headerShown: false }}>
          <Stack.Screen name="+not-found" />
          <Stack.Screen name="(tabs)" />
          <Stack.Screen name="login" />
          <Stack.Screen name="forgot-password" />
          <Stack.Screen name="reset-password" />
          <Stack.Screen
            name="profile"
            options={{
              animation: 'slide_from_right',
            }}
          />
        </Stack>
        <StatusBar style="light" />
      </>
    </AuthProvider>
  );
}

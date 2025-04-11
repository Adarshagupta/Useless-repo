import { Stack } from 'expo-router';

export default function ProfileLayout() {
  return (
    <Stack>
      <Stack.Screen name="addresses" options={{ headerShown: true, title: 'Addresses & Payments' }} />
      <Stack.Screen name="notifications" options={{ headerShown: true, title: 'Notifications' }} />
      <Stack.Screen name="settings" options={{ headerShown: true, title: 'Settings & Help' }} />
    </Stack>
  );
}
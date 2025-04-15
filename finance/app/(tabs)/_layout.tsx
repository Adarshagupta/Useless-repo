import { useEffect } from 'react';
import { Tabs, useRouter } from 'expo-router';
import { TrendingUp, ChartLine as LineChart, Newspaper, Brain, Settings, Briefcase, Search } from 'lucide-react-native';
import { useAuth } from '../context/AuthContext';

export default function TabLayout() {
  const router = useRouter();
  const { isSignedIn, isLoading } = useAuth();

  // Check if the user is signed in
  useEffect(() => {
    if (!isLoading && !isSignedIn) {
      // Redirect to login if not signed in
      router.replace('/login');
    }
  }, [isSignedIn, isLoading, router]);

  // Don't render the tabs until we've checked authentication
  if (isLoading) {
    return null;
  }

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: '#1C1C1E',
          borderTopColor: '#2C2C2E',
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#8E8E93',
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Markets',
          tabBarIcon: ({ size, color }) => (
            <TrendingUp size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="stocks"
        options={{
          title: 'Stocks',
          tabBarIcon: ({ size, color }) => (
            <Search size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="portfolio"
        options={{
          title: 'Portfolio',
          tabBarIcon: ({ size, color }) => (
            <Briefcase size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="analysis"
        options={{
          title: 'Analysis',
          tabBarIcon: ({ size, color }) => (
            <LineChart size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="news"
        options={{
          title: 'News',
          tabBarIcon: ({ size, color }) => (
            <Newspaper size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="ai-insights"
        options={{
          title: 'AI',
          tabBarIcon: ({ size, color }) => (
            <Brain size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          tabBarIcon: ({ size, color }) => (
            <Settings size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
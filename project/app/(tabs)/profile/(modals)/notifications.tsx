import { StyleSheet, Text, View, ScrollView, Switch } from 'react-native';
import { Bell, Tag, Truck, CreditCard } from 'lucide-react-native';
import { useState } from 'react';

const notificationSettings = [
  {
    id: 'orders',
    title: 'Order Updates',
    description: 'Get notified about your order status',
    icon: Truck,
    iconColor: '#4F46E5',
  },
  {
    id: 'promotions',
    title: 'Promotions',
    description: 'Receive offers and promotional updates',
    icon: Tag,
    iconColor: '#059669',
  },
  {
    id: 'payments',
    title: 'Payment Updates',
    description: 'Get notified about payment confirmations',
    icon: CreditCard,
    iconColor: '#D97706',
  },
];

export default function NotificationsScreen() {
  const [settings, setSettings] = useState({
    orders: true,
    promotions: false,
    payments: true,
  });

  const toggleSetting = (id: string) => {
    setSettings(prev => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Notifications</Text>
      </View>

      <ScrollView style={styles.content}>
        {notificationSettings.map((setting) => {
          const Icon = setting.icon;
          return (
            <View key={setting.id} style={styles.settingCard}>
              <View style={[styles.iconContainer, { backgroundColor: `${setting.iconColor}10` }]}>
                <Icon size={24} color={setting.iconColor} />
              </View>
              <View style={styles.settingInfo}>
                <Text style={styles.settingTitle}>{setting.title}</Text>
                <Text style={styles.settingDescription}>{setting.description}</Text>
              </View>
              <Switch
                value={settings[setting.id]}
                onValueChange={() => toggleSetting(setting.id)}
                trackColor={{ false: '#D1D5DB', true: '#FF2E56' }}
                thumbColor="#FFFFFF"
              />
            </View>
          );
        })}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Email Preferences</Text>
          <Text style={styles.sectionDescription}>
            Choose the types of email notifications you'd like to receive
          </Text>

          <View style={styles.settingCard}>
            <View style={[styles.iconContainer, { backgroundColor: '#EF444410' }]}>
              <Bell size={24} color="#EF4444" />
            </View>
            <View style={styles.settingInfo}>
              <Text style={styles.settingTitle}>Marketing Emails</Text>
              <Text style={styles.settingDescription}>Receive marketing and promotional emails</Text>
            </View>
            <Switch
              value={false}
              onValueChange={() => {}}
              trackColor={{ false: '#D1D5DB', true: '#FF2E56' }}
              thumbColor="#FFFFFF"
            />
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  header: {
    padding: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    color: '#111827',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  settingCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
  },
  settingInfo: {
    flex: 1,
    marginLeft: 16,
    marginRight: 16,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 4,
  },
  settingDescription: {
    fontSize: 14,
    color: '#6B7280',
  },
  section: {
    marginTop: 24,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 8,
  },
  sectionDescription: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 16,
  },
});
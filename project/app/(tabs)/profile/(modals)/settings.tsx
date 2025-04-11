import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Switch } from 'react-native';
import { Globe, Moon, Bell, Shield, ChevronRight, MessageCircle, Phone, Mail, FileText, CircleHelp as HelpCircle } from 'lucide-react-native';
import { useState } from 'react';

export default function SettingsScreen() {
  const [darkMode, setDarkMode] = useState(false);

  const helpSections = [
    {
      title: 'FAQs',
      description: 'Find answers to common questions',
      icon: FileText,
      color: '#4F46E5',
    },
    {
      title: 'Live Chat',
      description: 'Chat with our support team',
      icon: MessageCircle,
      color: '#059669',
    },
    {
      title: 'Call Us',
      description: 'Speak with a representative',
      icon: Phone,
      color: '#D97706',
    },
  ];

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Settings & Help</Text>
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Preferences</Text>

          <View style={styles.settingCard}>
            <View style={[styles.iconContainer, { backgroundColor: '#4F46E510' }]}>
              <Globe size={24} color="#4F46E5" />
            </View>
            <View style={styles.settingInfo}>
              <Text style={styles.settingTitle}>Language</Text>
              <Text style={styles.settingValue}>English</Text>
            </View>
            <ChevronRight size={20} color="#6B7280" />
          </View>

          <View style={styles.settingCard}>
            <View style={[styles.iconContainer, { backgroundColor: '#6B728010' }]}>
              <Moon size={24} color="#6B7280" />
            </View>
            <View style={styles.settingInfo}>
              <Text style={styles.settingTitle}>Dark Mode</Text>
              <Text style={styles.settingDescription}>Toggle dark theme</Text>
            </View>
            <Switch
              value={darkMode}
              onValueChange={setDarkMode}
              trackColor={{ false: '#D1D5DB', true: '#FF2E56' }}
              thumbColor="#FFFFFF"
            />
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Privacy</Text>

          <TouchableOpacity style={styles.settingCard}>
            <View style={[styles.iconContainer, { backgroundColor: '#05966910' }]}>
              <Shield size={24} color="#059669" />
            </View>
            <View style={styles.settingInfo}>
              <Text style={styles.settingTitle}>Privacy Settings</Text>
              <Text style={styles.settingDescription}>Manage your data and privacy preferences</Text>
            </View>
            <ChevronRight size={20} color="#6B7280" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.settingCard}>
            <View style={[styles.iconContainer, { backgroundColor: '#EF444410' }]}>
              <Bell size={24} color="#EF4444" />
            </View>
            <View style={styles.settingInfo}>
              <Text style={styles.settingTitle}>Notifications</Text>
              <Text style={styles.settingDescription}>Configure notification preferences</Text>
            </View>
            <ChevronRight size={20} color="#6B7280" />
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Help & Support</Text>

          {helpSections.map((section, index) => {
            const Icon = section.icon;
            return (
              <TouchableOpacity key={index} style={styles.settingCard}>
                <View style={[styles.iconContainer, { backgroundColor: `${section.color}10` }]}>
                  <Icon size={24} color={section.color} />
                </View>
                <View style={styles.settingInfo}>
                  <Text style={styles.settingTitle}>{section.title}</Text>
                  <Text style={styles.settingDescription}>{section.description}</Text>
                </View>
                <ChevronRight size={20} color="#6B7280" />
              </TouchableOpacity>
            );
          })}

          <View style={styles.contactCard}>
            <View style={styles.contactItem}>
              <Text style={styles.contactLabel}>Customer Service</Text>
              <Text style={styles.contactValue}>1-800-123-4567</Text>
            </View>
            <View style={styles.divider} />
            <View style={styles.contactItem}>
              <Text style={styles.contactLabel}>Email</Text>
              <Text style={styles.contactValue}>support@example.com</Text>
            </View>
          </View>
        </View>

        <TouchableOpacity style={styles.dangerButton}>
          <Text style={styles.dangerButtonText}>Delete Account</Text>
        </TouchableOpacity>
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
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 16,
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
  },
  settingDescription: {
    fontSize: 14,
    color: '#6B7280',
    marginTop: 2,
  },
  settingValue: {
    fontSize: 14,
    color: '#6B7280',
  },
  contactCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginTop: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  contactItem: {
    paddingVertical: 8,
  },
  contactLabel: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 4,
  },
  contactValue: {
    fontSize: 16,
    fontWeight: '500',
    color: '#111827',
  },
  divider: {
    height: 1,
    backgroundColor: '#E5E7EB',
    marginVertical: 8,
  },
  dangerButton: {
    backgroundColor: '#FEE2E2',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginTop: 16,
    marginBottom: 24,
  },
  dangerButtonText: {
    color: '#EF4444',
    fontSize: 16,
    fontWeight: '600',
  },
});
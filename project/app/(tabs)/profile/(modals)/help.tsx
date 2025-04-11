import { StyleSheet, Text, View, ScrollView, TouchableOpacity } from 'react-native';
import { MessageCircle, Phone, Mail, FileText, ChevronRight } from 'lucide-react-native';

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
  {
    title: 'Email Support',
    description: 'Send us an email',
    icon: Mail,
    color: '#EF4444',
  },
];

export default function HelpScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Help & Support</Text>
      </View>

      <ScrollView style={styles.content}>
        <Text style={styles.subtitle}>How can we help you?</Text>

        {helpSections.map((section, index) => {
          const Icon = section.icon;
          return (
            <TouchableOpacity key={index} style={styles.card}>
              <View style={[styles.iconContainer, { backgroundColor: `${section.color}10` }]}>
                <Icon size={24} color={section.color} />
              </View>
              <View style={styles.cardInfo}>
                <Text style={styles.cardTitle}>{section.title}</Text>
                <Text style={styles.cardDescription}>{section.description}</Text>
              </View>
              <ChevronRight size={20} color="#6B7280" />
            </TouchableOpacity>
          );
        })}

        <View style={styles.contactSection}>
          <Text style={styles.contactTitle}>Contact Information</Text>
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
            <View style={styles.divider} />
            <View style={styles.contactItem}>
              <Text style={styles.contactLabel}>Hours</Text>
              <Text style={styles.contactValue}>Mon-Fri, 9AM-6PM EST</Text>
            </View>
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
  subtitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 16,
  },
  card: {
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
  cardInfo: {
    flex: 1,
    marginLeft: 16,
    marginRight: 16,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 2,
  },
  cardDescription: {
    fontSize: 14,
    color: '#6B7280',
  },
  contactSection: {
    marginTop: 24,
  },
  contactTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 12,
  },
  contactCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
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
    paddingVertical: 12,
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
  },
});
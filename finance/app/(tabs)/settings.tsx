import { View, Text, StyleSheet, ScrollView, Switch, TouchableOpacity, Alert, Image } from 'react-native';
import { Bell, Lock, Eye, Moon, CircleHelp as HelpCircle, LogOut, User, ChevronRight, Edit, Shield } from 'lucide-react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '../context/AuthContext';

export default function SettingsScreen() {
  const router = useRouter();
  const { user, signOut } = useAuth();

  const handleLogout = async () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: async () => {
            try {
              await signOut();
              router.replace('/login');
            } catch (error) {
              Alert.alert('Error', 'Failed to logout. Please try again.');
            }
          },
        },
      ]
    );
  };

  const navigateToProfile = () => {
    // Make sure we're using the correct path to the profile screen
    router.push('/profile');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Settings</Text>
      </View>

      {/* Profile Section */}
      <TouchableOpacity style={styles.profileSection} onPress={navigateToProfile}>
        <View style={styles.profileInfo}>
          <View style={styles.avatarContainer}>
            {user?.profile_image_url ? (
              <Image
                source={{ uri: user.profile_image_url }}
                style={styles.avatar}
              />
            ) : (
              <View style={styles.avatarPlaceholder}>
                <User color="#FFFFFF" size={32} />
              </View>
            )}
          </View>
          <View style={styles.userInfo}>
            <Text style={styles.userName}>{user?.full_name || 'Your Name'}</Text>
            <Text style={styles.userEmail}>{user?.email}</Text>
          </View>
        </View>
        <ChevronRight color="#8E8E93" size={20} />
      </TouchableOpacity>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account</Text>

        <TouchableOpacity style={styles.settingItem} onPress={navigateToProfile}>
          <View style={styles.settingLeft}>
            <User color="#FFFFFF" size={24} />
            <Text style={styles.settingText}>Edit Profile</Text>
          </View>
          <ChevronRight color="#8E8E93" size={20} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingLeft}>
            <Shield color="#FFFFFF" size={24} />
            <Text style={styles.settingText}>Account Security</Text>
          </View>
          <ChevronRight color="#8E8E93" size={20} />
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Preferences</Text>

        <View style={styles.settingItem}>
          <View style={styles.settingLeft}>
            <Bell color="#FFFFFF" size={24} />
            <Text style={styles.settingText}>Notifications</Text>
          </View>
          <Switch />
        </View>

        <View style={styles.settingItem}>
          <View style={styles.settingLeft}>
            <Moon color="#FFFFFF" size={24} />
            <Text style={styles.settingText}>Dark Mode</Text>
          </View>
          <Switch />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Security</Text>

        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingLeft}>
            <Lock color="#FFFFFF" size={24} />
            <Text style={styles.settingText}>Change Password</Text>
          </View>
          <ChevronRight color="#8E8E93" size={20} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingLeft}>
            <Eye color="#FFFFFF" size={24} />
            <Text style={styles.settingText}>Privacy Settings</Text>
          </View>
          <ChevronRight color="#8E8E93" size={20} />
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Support</Text>

        <TouchableOpacity style={styles.settingItem}>
          <View style={styles.settingLeft}>
            <HelpCircle color="#FFFFFF" size={24} />
            <Text style={styles.settingText}>Help Center</Text>
          </View>
          <ChevronRight color="#8E8E93" size={20} />
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutButtonText}>Logout</Text>
      </TouchableOpacity>

      <View style={styles.footer}>
        <Text style={styles.version}>Version 1.0.0</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  header: {
    padding: 20,
    paddingTop: 60,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  profileSection: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#1C1C1E',
    padding: 20,
    borderRadius: 12,
    marginHorizontal: 20,
    marginBottom: 20,
  },
  profileInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatarContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    overflow: 'hidden',
    marginRight: 15,
  },
  avatar: {
    width: '100%',
    height: '100%',
  },
  avatarPlaceholder: {
    width: '100%',
    height: '100%',
    backgroundColor: '#333333',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 30,
  },
  userInfo: {
    justifyContent: 'center',
  },
  userName: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 14,
    color: '#8E8E93',
  },
  section: {
    marginTop: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#8E8E93',
    marginLeft: 20,
    marginBottom: 10,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#1C1C1E',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#2C2C2E',
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingText: {
    color: '#FFFFFF',
    fontSize: 16,
    marginLeft: 15,
  },
  logoutButton: {
    backgroundColor: '#1C1C1E',
    marginHorizontal: 20,
    marginTop: 30,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  logoutButtonText: {
    color: '#FF3B30',
    fontSize: 16,
    fontWeight: 'bold',
  },
  footer: {
    padding: 20,
    alignItems: 'center',
  },
  version: {
    color: '#8E8E93',
    fontSize: 14,
  },
  logoutText: {
    color: '#FF3B30',
  },
});
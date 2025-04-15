import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, ActivityIndicator, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useAuth } from './context/AuthContext';
import { userAPI } from './api';

export default function ProfileScreen() {
  const router = useRouter();
  const { user, refreshUser, signOut } = useAuth();
  
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Check for authentication
  useEffect(() => {
    const checkAuth = async () => {
      const token = await AsyncStorage.getItem('token');
      if (!token) {
        // Redirect to login if not authenticated
        Alert.alert('Session Expired', 'Please login again');
        router.replace('/login');
      }
    };
    
    checkAuth();
  }, [router]);
  
  // Update local state when user data changes
  useEffect(() => {
    if (user) {
      setFullName(user.full_name || '');
      setEmail(user.email || '');
      setUsername(user.username || '');
      
      // Store user info in AsyncStorage for mock data
      if (user.email) AsyncStorage.setItem('userEmail', user.email);
      if (user.full_name) AsyncStorage.setItem('userName', user.full_name);
    }
  }, [user]);
  
  const handleUpdateProfile = async () => {
    // Validate inputs
    if (password && password !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }
    
    try {
      setIsLoading(true);
      
      // Create update data object
      const updateData: { 
        full_name?: string; 
        email?: string; 
        password?: string 
      } = {};
      
      if (fullName !== user?.full_name) updateData.full_name = fullName;
      if (email !== user?.email) updateData.email = email;
      if (password) updateData.password = password;
      
      // If there are no changes, don't make the API call
      if (Object.keys(updateData).length === 0) {
        Alert.alert('Info', 'No changes to update');
        setIsLoading(false);
        return;
      }
      
      // Update profile
      const updatedUser = await userAPI.updateProfile(updateData);
      
      // Store updated user info in AsyncStorage for mock data
      if (updatedUser.email) AsyncStorage.setItem('userEmail', updatedUser.email);
      if (updatedUser.full_name) AsyncStorage.setItem('userName', updatedUser.full_name);
      
      // Refresh user data
      await refreshUser();
      
      // Clear password fields
      setPassword('');
      setConfirmPassword('');
      
      Alert.alert('Success', 'Profile updated successfully');
    } catch (error: any) {
      console.error('Error updating profile:', error);
      
      // Check if it's an authentication error
      if (error.response && error.response.status === 401) {
        Alert.alert('Session Expired', 'Please login again', [
          { text: 'OK', onPress: async () => {
            await signOut();
            router.replace('/login');
          }}
        ]);
      } else {
        Alert.alert('Error', 'Failed to update profile. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };
  
  if (!user) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }
  
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Profile Settings</Text>
        <Text style={styles.subtitle}>Update your personal information</Text>
      </View>
      
      <View style={styles.form}>
        <Text style={styles.label}>Username</Text>
        <View style={styles.disabledInput}>
          <Text style={styles.disabledText}>{username}</Text>
        </View>
        
        <Text style={styles.label}>Full Name</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your full name"
          placeholderTextColor="#8E8E93"
          value={fullName}
          onChangeText={setFullName}
          autoCapitalize="words"
        />
        
        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your email"
          placeholderTextColor="#8E8E93"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        
        <Text style={styles.label}>New Password (leave blank to keep current)</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter new password"
          placeholderTextColor="#8E8E93"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        
        <Text style={styles.label}>Confirm New Password</Text>
        <TextInput
          style={styles.input}
          placeholder="Confirm new password"
          placeholderTextColor="#8E8E93"
          value={confirmPassword}
          onChangeText={setConfirmPassword}
          secureTextEntry
        />
        
        <TouchableOpacity
          style={styles.button}
          onPress={handleUpdateProfile}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <Text style={styles.buttonText}>Update Profile</Text>
          )}
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
    padding: 20,
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    marginTop: 40,
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#8E8E93',
  },
  form: {
    width: '100%',
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: '#FFFFFF',
    marginBottom: 6,
    marginTop: 15,
  },
  input: {
    backgroundColor: '#1C1C1E',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    color: '#FFFFFF',
    fontSize: 16,
  },
  disabledInput: {
    backgroundColor: '#1C1C1E',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    opacity: 0.7,
  },
  disabledText: {
    color: '#8E8E93',
    fontSize: 16,
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 10,
    padding: 15,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
}); 
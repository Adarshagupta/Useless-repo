import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { useRouter, useLocalSearchParams, Link } from 'expo-router';
import api from './api';

export default function ResetPasswordScreen() {
  const router = useRouter();
  const { token } = useLocalSearchParams<{ token: string }>();
  
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  
  if (!token) {
    // If no token provided, this is an invalid access
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>Invalid Link</Text>
          <Text style={styles.subtitle}>
            Your password reset link is invalid or has expired.
          </Text>
        </View>
        
        <Link href="/forgot-password" asChild>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Request New Link</Text>
          </TouchableOpacity>
        </Link>
      </View>
    );
  }
  
  const handleSubmit = async () => {
    if (!newPassword || !confirmPassword) {
      Alert.alert('Error', 'Please enter and confirm your new password');
      return;
    }
    
    if (newPassword !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }
    
    if (newPassword.length < 8) {
      Alert.alert('Error', 'Password must be at least 8 characters long');
      return;
    }
    
    setIsLoading(true);
    
    try {
      await api.auth.resetPassword(token, newPassword);
      setIsSuccess(true);
    } catch (error: any) {
      console.error('Reset password error:', error);
      
      // Extract error message
      let errorMessage = 'An error occurred. Please try again.';
      
      if (error.response && error.response.data) {
        errorMessage = error.response.data.detail || errorMessage;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      Alert.alert('Error', errorMessage);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Reset Password</Text>
        <Text style={styles.subtitle}>
          {isSuccess
            ? 'Your password has been reset successfully'
            : 'Enter your new password'}
        </Text>
      </View>
      
      {!isSuccess ? (
        <View style={styles.form}>
          <TextInput
            style={styles.input}
            placeholder="New Password"
            placeholderTextColor="#8E8E93"
            value={newPassword}
            onChangeText={setNewPassword}
            secureTextEntry
            editable={!isLoading}
          />
          
          <TextInput
            style={styles.input}
            placeholder="Confirm Password"
            placeholderTextColor="#8E8E93"
            value={confirmPassword}
            onChangeText={setConfirmPassword}
            secureTextEntry
            editable={!isLoading}
          />
          
          <TouchableOpacity
            style={styles.button}
            onPress={handleSubmit}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.buttonText}>Reset Password</Text>
            )}
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.successContainer}>
          <Text style={styles.successText}>
            Your password has been reset successfully. You can now log in with your new password.
          </Text>
          
          <Link href="/login" asChild>
            <TouchableOpacity style={[styles.button, styles.successButton]}>
              <Text style={styles.buttonText}>Log In</Text>
            </TouchableOpacity>
          </Link>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
    padding: 20,
  },
  header: {
    marginTop: 100,
    marginBottom: 50,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#8E8E93',
  },
  form: {
    width: '100%',
  },
  input: {
    backgroundColor: '#1C1C1E',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    color: '#FFFFFF',
    fontSize: 16,
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 10,
    padding: 15,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  switchButton: {
    marginTop: 20,
    alignItems: 'center',
  },
  switchButtonText: {
    color: '#007AFF',
    fontSize: 14,
  },
  successContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  successText: {
    color: '#FFFFFF',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 30,
  },
  successButton: {
    width: '100%',
  },
}); 
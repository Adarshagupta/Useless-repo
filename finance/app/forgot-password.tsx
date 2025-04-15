import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { useRouter, Link } from 'expo-router';
import api from './api';

export default function ForgotPasswordScreen() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  
  const handleSubmit = async () => {
    if (!email) {
      Alert.alert('Error', 'Please enter your email address');
      return;
    }
    
    setIsLoading(true);
    
    try {
      await api.auth.forgotPassword(email);
      setIsSuccess(true);
    } catch (error: any) {
      console.error('Forgot password error:', error);
      
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
            ? 'Check your email for reset instructions'
            : 'Enter your email to receive a password reset link'}
        </Text>
      </View>
      
      {!isSuccess ? (
        <View style={styles.form}>
          <TextInput
            style={styles.input}
            placeholder="Email"
            placeholderTextColor="#8E8E93"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
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
              <Text style={styles.buttonText}>Send Reset Link</Text>
            )}
          </TouchableOpacity>
          
          <Link href="/login" asChild>
            <TouchableOpacity style={styles.switchButton} disabled={isLoading}>
              <Text style={styles.switchButtonText}>Back to Login</Text>
            </TouchableOpacity>
          </Link>
        </View>
      ) : (
        <View style={styles.successContainer}>
          <Text style={styles.successText}>
            If your email exists in our system, you'll receive instructions to reset your password shortly.
          </Text>
          
          <Link href="/login" asChild>
            <TouchableOpacity style={[styles.button, styles.successButton]}>
              <Text style={styles.buttonText}>Return to Login</Text>
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
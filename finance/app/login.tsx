import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TextInput, 
  TouchableOpacity, 
  ActivityIndicator, 
  Alert,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  StatusBar
} from 'react-native';
import { useRouter, Link } from 'expo-router';
import { useAuth } from './context/AuthContext';
import { Ionicons } from '@expo/vector-icons';

export default function LoginScreen() {
  const router = useRouter();
  const { signIn, signUp, isLoading } = useAuth();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [secureTextEntry, setSecureTextEntry] = useState(true);
  
  const toggleSecureEntry = () => {
    setSecureTextEntry(!secureTextEntry);
  };
  
  const handleSubmit = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter both email and password');
      return;
    }
    
    if (isSignUp && !fullName) {
      Alert.alert('Error', 'Please enter your full name');
      return;
    }
    
    try {
      if (isSignUp) {
        await signUp(email, password, fullName);
      } else {
        await signIn(email, password);
      }
      
      // Navigate to the main app
      router.replace('/');
    } catch (error: any) {
      console.error('Authentication error:', error);
      
      // Extract error message
      let errorMessage = 'An error occurred during authentication';
      
      if (error.response && error.response.data) {
        // API error with response
        errorMessage = error.response.data.detail || errorMessage;
      } else if (error.message) {
        // JavaScript error with message
        errorMessage = error.message;
      }
      
      Alert.alert('Error', errorMessage);
    }
  };
  
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <Text style={styles.logo}>F.</Text>
        
        <View style={styles.formContainer}>
          <Text style={styles.title}>
            {isSignUp ? 'Create Account' : 'Welcome Back'}
          </Text>
          <Text style={styles.subtitle}>
            {isSignUp 
              ? 'Sign up to get started' 
              : 'Enter your credentials to continue'}
          </Text>
          
          <View style={styles.form}>
            {isSignUp && (
              <View style={styles.inputWrapper}>
                <Text style={styles.inputLabel}>FULL NAME</Text>
                <View style={styles.inputContainer}>
                  <TextInput
                    style={styles.input}
                    placeholder="Your name"
                    placeholderTextColor="#666"
                    value={fullName}
                    onChangeText={setFullName}
                    autoCapitalize="words"
                  />
                </View>
              </View>
            )}
            
            <View style={styles.inputWrapper}>
              <Text style={styles.inputLabel}>EMAIL</Text>
              <View style={styles.inputContainer}>
                <TextInput
                  style={styles.input}
                  placeholder="Your email"
                  placeholderTextColor="#666"
                  value={email}
                  onChangeText={setEmail}
                  keyboardType="email-address"
                  autoCapitalize="none"
                />
              </View>
            </View>
            
            <View style={styles.inputWrapper}>
              <Text style={styles.inputLabel}>PASSWORD</Text>
              <View style={styles.inputContainer}>
                <TextInput
                  style={styles.input}
                  placeholder="Your password"
                  placeholderTextColor="#666"
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry={secureTextEntry}
                />
                <TouchableOpacity onPress={toggleSecureEntry} style={styles.eyeIcon}>
                  <Ionicons 
                    name={secureTextEntry ? 'eye-outline' : 'eye-off-outline'} 
                    size={20} 
                    color="#666" 
                  />
                </TouchableOpacity>
              </View>
            </View>
            
            {!isSignUp && (
              <Link href="/forgot-password" asChild>
                <TouchableOpacity style={styles.forgotPasswordButton} disabled={isLoading}>
                  <Text style={styles.forgotPasswordText}>Forgot Password?</Text>
                </TouchableOpacity>
              </Link>
            )}
            
            <TouchableOpacity
              style={styles.button}
              onPress={handleSubmit}
              disabled={isLoading}
            >
              {isLoading ? (
                <ActivityIndicator color="#FFFFFF" />
              ) : (
                <Text style={styles.buttonText}>{isSignUp ? 'Create Account' : 'Sign In'}</Text>
              )}
            </TouchableOpacity>
            
            <TouchableOpacity
              style={styles.switchButton}
              onPress={() => setIsSignUp(!isSignUp)}
              disabled={isLoading}
            >
              <Text style={styles.switchButtonText}>
                {isSignUp ? 'Already have an account? ' : 'Don\'t have an account? '}
                <Text style={styles.switchButtonTextHighlight}>
                  {isSignUp ? 'Sign In' : 'Sign Up'}
                </Text>
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  keyboardView: {
    flex: 1,
    justifyContent: 'center',
    padding: 24,
  },
  logo: {
    fontSize: 42,
    fontWeight: '700',
    color: '#007AFF',
    marginBottom: 48,
    textAlign: 'center',
  },
  formContainer: {
    width: '100%',
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#888',
    marginBottom: 32,
  },
  form: {
    width: '100%',
  },
  inputWrapper: {
    marginBottom: 20,
  },
  inputLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#888',
    marginBottom: 8,
    letterSpacing: 0.5,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#333',
    height: 48,
  },
  input: {
    flex: 1,
    color: '#FFFFFF',
    fontSize: 16,
    paddingVertical: 8,
  },
  eyeIcon: {
    padding: 8,
  },
  forgotPasswordButton: {
    alignSelf: 'flex-end',
    marginTop: 8,
    marginBottom: 24,
  },
  forgotPasswordText: {
    color: '#666',
    fontSize: 14,
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    height: 52,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  switchButton: {
    alignItems: 'center',
    padding: 16,
  },
  switchButtonText: {
    color: '#888',
    fontSize: 14,
  },
  switchButtonTextHighlight: {
    color: '#007AFF',
    fontWeight: '600',
  }
});

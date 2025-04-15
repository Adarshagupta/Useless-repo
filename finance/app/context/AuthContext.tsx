import React, { createContext, useState, useEffect, useContext } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authAPI } from '../api';

// Define the shape of the user object
interface User {
  username: string;
  email?: string;
  full_name?: string;
  disabled?: boolean;
}

// Define the shape of the auth context
interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isSignedIn: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, fullName: string) => Promise<void>;
  signOut: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

// Create the auth context
const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: true,
  isSignedIn: false,
  signIn: async () => {},
  signUp: async () => {},
  signOut: async () => {},
  refreshUser: async () => {},
});

// Create a provider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if the user is signed in on mount
  useEffect(() => {
    const bootstrapAsync = async () => {
      try {
        // Check if we have a token
        const token = await AsyncStorage.getItem('token');
        
        if (token) {
          // If we have a token, fetch the user data
          const userData = await authAPI.getCurrentUser();
          setUser(userData);
        }
      } catch (error) {
        console.error('Error bootstrapping auth:', error);
        // If there's an error, clear the token
        await AsyncStorage.removeItem('token');
      } finally {
        setIsLoading(false);
      }
    };

    bootstrapAsync();
  }, []);

  // Sign in function
  const signIn = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      // Call the login API
      await authAPI.login(email, password);
      // Fetch the user data
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Error signing in:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Sign up function
  const signUp = async (email: string, password: string, fullName: string) => {
    try {
      setIsLoading(true);
      // Call the register API
      await authAPI.register(email, password, fullName);
      // Sign in the user
      await signIn(email, password);
    } catch (error) {
      console.error('Error signing up:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Sign out function
  const signOut = async () => {
    try {
      setIsLoading(true);
      // Call the logout API
      await authAPI.logout();
      // Clear the user data
      setUser(null);
    } catch (error) {
      console.error('Error signing out:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const refreshUser = async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Error refreshing user:', error);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isSignedIn: !!user,
        signIn,
        signUp,
        signOut,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Create a hook to use the auth context
export const useAuth = () => useContext(AuthContext);

export default AuthContext;

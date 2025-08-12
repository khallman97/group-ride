import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiService, UserInfo, AuthResponse } from '../services/api';

interface AuthContextType {
  user: UserInfo | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name?: string) => Promise<void>;
  signOut: () => void;
  refreshAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user;

  const saveTokens = (authResponse: AuthResponse) => {
    localStorage.setItem('access_token', authResponse.access_token);
    localStorage.setItem('refresh_token', authResponse.refresh_token);
  };

  const clearTokens = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  const signIn = async (email: string, password: string) => {
    try {
      const authResponse = await apiService.signIn(email, password);
      saveTokens(authResponse);
      
      // Get user info
      const userInfo = await apiService.getCurrentUser();
      setUser(userInfo);
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const signUp = async (email: string, password: string, name?: string) => {
    try {
      await apiService.signUp(email, password, name);
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const signOut = () => {
    clearTokens();
    setUser(null);
  };

  const refreshAuth = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const authResponse = await apiService.refreshToken(refreshToken);
      saveTokens(authResponse);
      
      const userInfo = await apiService.getCurrentUser();
      setUser(userInfo);
    } catch (error) {
      console.error('Token refresh error:', error);
      signOut();
    }
  };

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const userInfo = await apiService.getCurrentUser();
          setUser(userInfo);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        // Try to refresh token
        try {
          await refreshAuth();
        } catch (refreshError) {
          console.error('Token refresh failed:', refreshError);
          signOut();
        }
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    signIn,
    signUp,
    signOut,
    refreshAuth,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 
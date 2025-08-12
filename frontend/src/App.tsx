/**
 * Group Fitness App - Main Application Component
 * 
 * This is the root component that handles the overall application state and routing.
 * It manages the authentication flow, onboarding process, and main application UI.
 * 
 * Flow:
 * 1. Unauthenticated users see login/signup forms
 * 2. After signup, users must confirm their email
 * 3. After login, users complete onboarding if they haven't already
 * 4. Authenticated users with complete profiles see the main app
 */

import React, { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LoginForm } from './components/auth/LoginForm';
import { SignUpForm } from './components/auth/SignUpForm';
import { ConfirmEmailForm } from './components/auth/ConfirmEmailForm';
import { OnboardingForm } from './components/onboarding/OnboardingForm';
import { apiService } from './services/api';
import './App.css';

/**
 * AppContent - Main application logic component
 * 
 * This component handles the complex state management for the authentication
 * and onboarding flow. It's separated from the main App component to ensure
 * it has access to the AuthContext.
 */
const AppContent: React.FC = () => {
  const { user, isAuthenticated, isLoading, signOut } = useAuth();
  
  // UI state management
  const [showSignUp, setShowSignUp] = useState(false);              // Toggle between login/signup
  const [showOnboarding, setShowOnboarding] = useState(false);      // Show onboarding flow
  const [hasProfile, setHasProfile] = useState(false);             // Track if user has completed profile
  const [showConfirmEmail, setShowConfirmEmail] = useState(false); // Show email confirmation
  const [signUpEmail, setSignUpEmail] = useState('');              // Store email for confirmation

  React.useEffect(() => {
    const checkProfile = async () => {
      if (isAuthenticated && user) {
        try {
          await apiService.getUserProfile();
          setHasProfile(true);
        } catch (error) {
          // Profile doesn't exist, show onboarding
          setHasProfile(false);
        }
      }
    };

    checkProfile();
  }, [isAuthenticated, user]);

  const handleOnboardingComplete = () => {
    setShowOnboarding(false);
    setHasProfile(true);
  };

  const handleSignOut = () => {
    signOut();
    setHasProfile(false);
    setShowOnboarding(false);
    setShowConfirmEmail(false);
    setSignUpEmail('');
  };

  const handleSignUpSuccess = (email: string) => {
    setSignUpEmail(email);
    setShowSignUp(false);
    setShowConfirmEmail(true);
  };

  const handleEmailConfirmed = () => {
    setShowConfirmEmail(false);
    setSignUpEmail('');
    // Don't auto-login, let user sign in manually
  };

  const handleBackToSignUp = () => {
    setShowConfirmEmail(false);
    setShowSignUp(true);
  };

  if (isLoading) {
    return (
      <div className="container">
        <div className="form-container">
          <div className="card">
            <div className="text-center">Loading...</div>
          </div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    if (showConfirmEmail) {
      return (
        <div className="container">
          <div className="form-container">
            <ConfirmEmailForm 
              email={signUpEmail}
              onConfirmed={handleEmailConfirmed}
              onBack={handleBackToSignUp}
            />
          </div>
        </div>
      );
    }

    return (
      <div className="container">
        <div className="form-container">
          {showSignUp ? (
            <SignUpForm 
              onSwitchToLogin={() => setShowSignUp(false)}
              onSignUpSuccess={handleSignUpSuccess}
            />
          ) : (
            <LoginForm onSwitchToSignUp={() => setShowSignUp(true)} />
          )}
        </div>
      </div>
    );
  }

  if (isAuthenticated && !hasProfile && !showOnboarding) {
    return (
      <div className="container">
        <div className="form-container">
          <div className="card">
            <h2 className="text-center mb-20">Welcome to Group Fitness!</h2>
            <p className="text-center mb-20">
              Let's set up your profile to help you find the perfect group rides and runs.
            </p>
            <button
              className="btn btn-primary btn-block"
              onClick={() => setShowOnboarding(true)}
            >
              Start Setup
            </button>
            <div className="text-center mt-20">
              <button
                className="btn btn-secondary"
                onClick={handleSignOut}
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (showOnboarding) {
    return (
      <div className="container">
        <div className="form-container">
          <OnboardingForm onComplete={handleOnboardingComplete} />
        </div>
      </div>
    );
  }

  // Main app (user is authenticated and has profile)
  return (
    <div className="container">
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h1>Group Fitness App</h1>
          <button className="btn btn-secondary" onClick={handleSignOut}>
            Sign Out
          </button>
        </div>
        
        <div className="card">
          <h2>Welcome, {user?.name || user?.email}!</h2>
          <p>Your profile is set up and ready to go.</p>
          <p>This is where the main app features will be implemented.</p>
        </div>

        <div className="card">
          <h3>Coming Soon:</h3>
          <ul>
            <li>Browse and create events</li>
            <li>Find group rides and runs</li>
            <li>Chat with event participants</li>
            <li>Track your activities</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;

import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';

interface SignUpFormProps {
  onSwitchToLogin: () => void;
  onSignUpSuccess: (email: string) => void;
}

export const SignUpForm: React.FC<SignUpFormProps> = ({ onSwitchToLogin, onSignUpSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { signUp } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setIsLoading(true);

    try {
      await signUp(email, password, name || undefined);
      setSuccess('Account created successfully! Redirecting to email confirmation...');
      
      // Redirect to confirmation step after a short delay
      setTimeout(() => {
        onSignUpSuccess(email);
      }, 1500);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Sign up failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-center mb-20">Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name (Optional)</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={isLoading}
            minLength={8}
          />
        </div>

        <div className="form-group">
          <label htmlFor="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            disabled={isLoading}
          />
        </div>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        <button
          type="submit"
          className="btn btn-primary btn-block"
          disabled={isLoading}
        >
          {isLoading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>

      <div className="text-center mt-20">
        <button
          type="button"
          className="btn btn-secondary"
          onClick={onSwitchToLogin}
          disabled={isLoading}
        >
          Already have an account? Sign In
        </button>
      </div>
    </div>
  );
}; 
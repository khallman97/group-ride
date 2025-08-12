import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';

interface LoginFormProps {
  onSwitchToSignUp: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSwitchToSignUp }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { signIn } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await signIn(email, password);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Sign in failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-center mb-20">Sign In</h2>
      <form onSubmit={handleSubmit}>
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
          />
        </div>

        {error && <div className="error">{error}</div>}

        <button
          type="submit"
          className="btn btn-primary btn-block"
          disabled={isLoading}
        >
          {isLoading ? 'Signing In...' : 'Sign In'}
        </button>
      </form>

      <div className="text-center mt-20">
        <button
          type="button"
          className="btn btn-secondary"
          onClick={onSwitchToSignUp}
          disabled={isLoading}
        >
          Need an account? Sign Up
        </button>
      </div>
    </div>
  );
}; 
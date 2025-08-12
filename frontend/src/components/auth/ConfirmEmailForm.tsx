import React, { useState } from 'react';
import { apiService } from '../../services/api';

interface ConfirmEmailFormProps {
  email: string;
  onConfirmed: () => void;
  onBack: () => void;
}

export const ConfirmEmailForm: React.FC<ConfirmEmailFormProps> = ({ 
  email, 
  onConfirmed, 
  onBack 
}) => {
  const [confirmationCode, setConfirmationCode] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isResending, setIsResending] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!confirmationCode.trim()) {
      setError('Please enter the confirmation code');
      return;
    }

    setIsLoading(true);

    try {
      await apiService.confirmSignUp(email, confirmationCode.trim());
      setSuccess('Email confirmed successfully! You can now sign in.');
      setTimeout(() => {
        onConfirmed();
      }, 2000);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Confirmation failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendCode = async () => {
    setError('');
    setSuccess('');
    setIsResending(true);

    try {
      // Note: AWS Cognito doesn't have a direct resend confirmation API
      // In a real app, you might need to implement this on your backend
      // For now, we'll show a message to the user
      setSuccess('If you need a new code, please try signing up again.');
    } catch (error) {
      setError('Failed to resend code');
    } finally {
      setIsResending(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-center mb-20">Confirm Your Email</h2>
      
      <div className="mb-20">
        <p className="text-center">
          We've sent a confirmation code to:
        </p>
        <p className="text-center" style={{ fontWeight: 'bold', color: '#007bff' }}>
          {email}
        </p>
        <p className="text-center" style={{ fontSize: '14px', color: '#666' }}>
          Please check your email and enter the 6-digit code below.
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="confirmationCode">Confirmation Code</label>
          <input
            type="text"
            id="confirmationCode"
            value={confirmationCode}
            onChange={(e) => setConfirmationCode(e.target.value)}
            placeholder="Enter 6-digit code"
            required
            disabled={isLoading}
            maxLength={6}
            style={{ 
              textAlign: 'center', 
              fontSize: '18px', 
              letterSpacing: '2px',
              fontFamily: 'monospace'
            }}
          />
        </div>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        <button
          type="submit"
          className="btn btn-primary btn-block"
          disabled={isLoading || !confirmationCode.trim()}
        >
          {isLoading ? 'Confirming...' : 'Confirm Email'}
        </button>
      </form>

      <div className="text-center mt-20">
        <button
          type="button"
          className="btn btn-secondary"
          onClick={handleResendCode}
          disabled={isResending || isLoading}
          style={{ marginRight: '10px' }}
        >
          {isResending ? 'Sending...' : 'Resend Code'}
        </button>
        
        <button
          type="button"
          className="btn btn-secondary"
          onClick={onBack}
          disabled={isLoading}
        >
          Back to Sign Up
        </button>
      </div>

      <div className="mt-20" style={{ 
        padding: '15px', 
        backgroundColor: '#f8f9fa', 
        borderRadius: '8px',
        fontSize: '14px',
        color: '#666'
      }}>
        <p style={{ margin: '0', textAlign: 'center' }}>
          <strong>Note:</strong> Check your spam/junk folder if you don't see the email.
          The code expires after a few minutes.
        </p>
      </div>
    </div>
  );
}; 
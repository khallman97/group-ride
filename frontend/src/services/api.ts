/**
 * API Service for Group Fitness App
 * 
 * This service handles all HTTP communication with the FastAPI backend.
 * It includes authentication, user management, and error handling.
 * 
 * Features:
 * - Automatic token management (stored in localStorage)
 * - Error handling with user-friendly messages
 * - TypeScript interfaces for type safety
 * - Consistent API response handling
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserInfo {
  user_id: string;
  email: string;
  name?: string;
}

export interface UserProfile {
  id: number;
  user_id: string;
  email: string;
  name?: string;
  bio?: string;
  location_lat?: number;
  location_lng?: number;
  location_name?: string;
  created_at: string;
  updated_at: string;
}

export interface UserPreferences {
  id: number;
  user_id: string;
  preferred_pace?: string;
  created_at: string;
  updated_at: string;
}

class ApiService {
  /**
   * Get headers for authenticated requests
   * Automatically includes the JWT token if available
   */
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  /**
   * Handle HTTP responses consistently
   * Extracts JSON data and throws user-friendly errors
   */
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  // Auth endpoints
  async signUp(email: string, password: string, name?: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
    });
    return this.handleResponse(response);
  }

  async confirmSignUp(email: string, confirmationCode: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/auth/confirm-signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, confirmation_code: confirmationCode }),
    });
    return this.handleResponse(response);
  }

  async signIn(email: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return this.handleResponse<AuthResponse>(response);
  }

  async getCurrentUser(): Promise<UserInfo> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<UserInfo>(response);
  }

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    return this.handleResponse<AuthResponse>(response);
  }

  // User endpoints
  async autoCreateProfile(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/users/profile/auto-create`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse(response);
  }

  async getUserProfile(): Promise<UserProfile> {
    const response = await fetch(`${API_BASE_URL}/users/profile`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<UserProfile>(response);
  }

  async updateUserProfile(profileData: Partial<UserProfile>): Promise<UserProfile> {
    const response = await fetch(`${API_BASE_URL}/users/profile`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(profileData),
    });
    return this.handleResponse<UserProfile>(response);
  }

  async getUserPreferences(): Promise<UserPreferences> {
    const response = await fetch(`${API_BASE_URL}/users/preferences`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<UserPreferences>(response);
  }

  async updateUserPreferences(preferencesData: Partial<UserPreferences>): Promise<UserPreferences> {
    const response = await fetch(`${API_BASE_URL}/users/preferences`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(preferencesData),
    });
    return this.handleResponse<UserPreferences>(response);
  }

  async completeOnboarding(profileData: Partial<UserProfile>, preferencesData: Partial<UserPreferences>): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/users/onboarding`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({
        profile: profileData,
        preferences: preferencesData,
      }),
    });
    return this.handleResponse(response);
  }
}

export const apiService = new ApiService(); 
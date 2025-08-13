import React, { useState } from 'react';
import { apiService, UserProfile, UserPreferences } from '../../services/api';
import LocationOnIcon from '@mui/icons-material/LocationOn';

interface OnboardingFormProps {
  onComplete: () => void;
}

export const OnboardingForm: React.FC<OnboardingFormProps> = ({ onComplete }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Profile data
  const [name, setName] = useState('');
  const [bio, setBio] = useState('');
  const [locationName, setLocationName] = useState('');
  const [locationLat, setLocationLat] = useState<number | null>(null);
  const [locationLng, setLocationLng] = useState<number | null>(null);
  const [isGettingLocation, setIsGettingLocation] = useState(false);

  // Preferences data
  const [preferredPace, setPreferredPace] = useState('');

  const paceOptions = ['casual', 'moderate', 'fast'];

  const getCurrentLocation = () => {
    setIsGettingLocation(true);
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocationLat(position.coords.latitude);
          setLocationLng(position.coords.longitude);
          
          // Try to get location name using reverse geocoding
          fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${position.coords.latitude}&lon=${position.coords.longitude}&zoom=10`)
            .then(response => response.json())
            .then(data => {
              if (data.display_name) {
                setLocationName(data.display_name.split(',')[0] + ', ' + data.display_name.split(',')[1]);
              }
            })
            .catch(() => {
              // If reverse geocoding fails, just use coordinates
              setLocationName(`${position.coords.latitude.toFixed(4)}, ${position.coords.longitude.toFixed(4)}`);
            })
            .finally(() => {
              setIsGettingLocation(false);
            });
        },
        (error) => {
          console.log('Geolocation error:', error);
          setIsGettingLocation(false);
          setError('Could not get your location. You can enter it manually.');
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000 // 5 minutes
        }
      );
    } else {
      setIsGettingLocation(false);
      setError('Geolocation is not supported by your browser. Please enter your location manually.');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Auto-create profile first
      await apiService.autoCreateProfile();

      // Complete onboarding
      const profileData: Partial<UserProfile> = {
        name: name || undefined,
        bio: bio || undefined,
        location_name: locationName || undefined,
        location_lat: locationLat || undefined,
        location_lng: locationLng || undefined,
      };

      const preferencesData: Partial<UserPreferences> = {
        preferred_pace: preferredPace || undefined,
      };

      await apiService.completeOnboarding(profileData, preferencesData);
      onComplete();
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Onboarding failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-center mb-20">Complete Your Profile</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Your name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="bio">Bio</label>
          <textarea
            id="bio"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            placeholder="Tell us about yourself..."
            rows={3}
          />
        </div>

        <div className="form-group">
          <label htmlFor="location">Location</label>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-end' }}>
            <div style={{ flex: 1 }}>
              <input
                type="text"
                id="location"
                value={locationName}
                onChange={(e) => setLocationName(e.target.value)}
                placeholder="Your city or use current location"
              />
            </div>
            <button
              type="button"
              onClick={getCurrentLocation}
              disabled={isGettingLocation}
              className="btn btn-secondary"
              style={{ 
                whiteSpace: 'nowrap',
                padding: '12px 16px',
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              {isGettingLocation ? 'Getting...' : (
                <>
                  <LocationOnIcon style={{ fontSize: 16 }} />
                  Use Current
                </>
              )}
            </button>
          </div>
          {locationLat && locationLng && (
            <small style={{ color: 'var(--accent-medium)', fontSize: '12px', marginTop: '4px', display: 'block' }}>
              Location saved: {locationLat.toFixed(4)}, {locationLng.toFixed(4)}
            </small>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="pace">Preferred Pace</label>
          <select
            id="pace"
            value={preferredPace}
            onChange={(e) => setPreferredPace(e.target.value)}
          >
            <option value="">Select pace</option>
            {paceOptions.map(pace => (
              <option key={pace} value={pace}>
                {pace.charAt(0).toUpperCase() + pace.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
        >
          {isLoading ? 'Completing...' : 'Complete Setup'}
        </button>

        {error && <div className="error mt-20">{error}</div>}
      </form>
    </div>
  );
}; 
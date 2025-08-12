import React, { useState } from 'react';
import { apiService, UserProfile, UserPreferences } from '../../services/api';

interface OnboardingFormProps {
  onComplete: () => void;
}

export const OnboardingForm: React.FC<OnboardingFormProps> = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Profile data
  const [name, setName] = useState('');
  const [bio, setBio] = useState('');
  const [locationName, setLocationName] = useState('');

  // Preferences data
  const [sports, setSports] = useState<string[]>([]);
  const [preferredPace, setPreferredPace] = useState('');
  const [rideType, setRideType] = useState('');
  const [distanceMin, setDistanceMin] = useState('');
  const [distanceMax, setDistanceMax] = useState('');
  const [availability, setAvailability] = useState<string[]>([]);

  const sportsOptions = ['running', 'cycling'];
  const paceOptions = ['casual', 'moderate', 'fast'];
  const rideTypeOptions = ['casual', 'drop_ride', 'competitive'];
  const dayOptions = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

  const handleSportToggle = (sport: string) => {
    setSports(prev => 
      prev.includes(sport) 
        ? prev.filter(s => s !== sport)
        : [...prev, sport]
    );
  };

  const handleDayToggle = (day: string) => {
    setAvailability(prev => 
      prev.includes(day) 
        ? prev.filter(d => d !== day)
        : [...prev, day]
    );
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
      };

      const preferencesData: Partial<UserPreferences> = {
        sports: sports.length > 0 ? sports : undefined,
        preferred_pace: preferredPace || undefined,
        ride_type: rideType || undefined,
        distance_range_min: distanceMin ? parseInt(distanceMin) : undefined,
        distance_range_max: distanceMax ? parseInt(distanceMax) : undefined,
        availability: availability.length > 0 ? availability : undefined,
      };

      await apiService.completeOnboarding(profileData, preferencesData);
      onComplete();
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Onboarding failed');
    } finally {
      setIsLoading(false);
    }
  };

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  const renderStep1 = () => (
    <div>
      <h3>Basic Information</h3>
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
        <input
          type="text"
          id="location"
          value={locationName}
          onChange={(e) => setLocationName(e.target.value)}
          placeholder="City, State/Province"
        />
      </div>

      <button type="button" className="btn btn-primary" onClick={nextStep}>
        Next
      </button>
    </div>
  );

  const renderStep2 = () => (
    <div>
      <h3>Sports & Preferences</h3>
      
      <div className="form-group">
        <label>Sports</label>
        <div>
          {sportsOptions.map(sport => (
            <label key={sport} style={{ display: 'block', marginBottom: '10px' }}>
              <input
                type="checkbox"
                checked={sports.includes(sport)}
                onChange={() => handleSportToggle(sport)}
                style={{ marginRight: '8px' }}
              />
              {sport.charAt(0).toUpperCase() + sport.slice(1)}
            </label>
          ))}
        </div>
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

      <div className="form-group">
        <label htmlFor="rideType">Ride Type</label>
        <select
          id="rideType"
          value={rideType}
          onChange={(e) => setRideType(e.target.value)}
        >
          <option value="">Select ride type</option>
          {rideTypeOptions.map(type => (
            <option key={type} value={type}>
              {type.replace('_', ' ').charAt(0).toUpperCase() + type.replace('_', ' ').slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="distanceMin">Distance Range (km)</label>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="number"
            placeholder="Min"
            value={distanceMin}
            onChange={(e) => setDistanceMin(e.target.value)}
            min="1"
            style={{ flex: 1 }}
          />
          <input
            type="number"
            placeholder="Max"
            value={distanceMax}
            onChange={(e) => setDistanceMax(e.target.value)}
            min="1"
            style={{ flex: 1 }}
          />
        </div>
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button type="button" className="btn btn-secondary" onClick={prevStep}>
          Back
        </button>
        <button type="button" className="btn btn-primary" onClick={nextStep}>
          Next
        </button>
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div>
      <h3>Availability</h3>
      
      <div className="form-group">
        <label>Available Days</label>
        <div>
          {dayOptions.map(day => (
            <label key={day} style={{ display: 'block', marginBottom: '10px' }}>
              <input
                type="checkbox"
                checked={availability.includes(day)}
                onChange={() => handleDayToggle(day)}
                style={{ marginRight: '8px' }}
              />
              {day.charAt(0).toUpperCase() + day.slice(1)}
            </label>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button type="button" className="btn btn-secondary" onClick={prevStep}>
          Back
        </button>
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
        >
          {isLoading ? 'Completing...' : 'Complete Setup'}
        </button>
      </div>
    </div>
  );

  return (
    <div className="card">
      <h2 className="text-center mb-20">Complete Your Profile</h2>
      
      <div className="mb-20">
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
          {[1, 2, 3].map(stepNumber => (
            <div
              key={stepNumber}
              style={{
                width: '30px',
                height: '30px',
                borderRadius: '50%',
                backgroundColor: step >= stepNumber ? '#007bff' : '#ddd',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 10px',
                fontWeight: 'bold'
              }}
            >
              {stepNumber}
            </div>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}

        {error && <div className="error mt-20">{error}</div>}
      </form>
    </div>
  );
}; 
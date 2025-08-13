import React, { useState, useEffect } from 'react';
import { apiService, UserProfile } from '../../services/api';
import MapIcon from '@mui/icons-material/Map';
import EventIcon from '@mui/icons-material/Event';
import PersonIcon from '@mui/icons-material/Person';
import AddIcon from '@mui/icons-material/Add';
import LocationOnIcon from '@mui/icons-material/LocationOn';

interface MapViewProps {
  onSignOut: () => void;
  userName?: string;
}

export const MapView: React.FC<MapViewProps> = ({ onSignOut, userName }) => {
  const [activeTab, setActiveTab] = useState<'map' | 'events' | 'profile'>('map');
  const [showCreateEvent, setShowCreateEvent] = useState(false);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [isLoadingLocation, setIsLoadingLocation] = useState(true);

  // Default position (New York City) - fallback
  const defaultLat = 40.7128;
  const defaultLng = -74.0060;

  useEffect(() => {
    const getUserLocation = async () => {
      try {
        // First, try to get user's saved location from preferences
        const userProfile = await apiService.getUserProfile();
        
        if (userProfile.location_lat && userProfile.location_lng) {
          setUserLocation({
            lat: userProfile.location_lat,
            lng: userProfile.location_lng
          });
          setIsLoadingLocation(false);
          return;
        }

        // If no saved location, try to get current location from browser
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              setUserLocation({
                lat: position.coords.latitude,
                lng: position.coords.longitude
              });
              setIsLoadingLocation(false);
            },
            (error) => {
              console.log('Geolocation error:', error);
              // Fall back to default location
              setUserLocation({ lat: defaultLat, lng: defaultLng });
              setIsLoadingLocation(false);
            },
            {
              enableHighAccuracy: true,
              timeout: 10000,
              maximumAge: 300000 // 5 minutes
            }
          );
        } else {
          // Browser doesn't support geolocation, use default
          setUserLocation({ lat: defaultLat, lng: defaultLng });
          setIsLoadingLocation(false);
        }
      } catch (error) {
        console.log('Error getting user profile:', error);
        // Try geolocation as fallback
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              setUserLocation({
                lat: position.coords.latitude,
                lng: position.coords.longitude
              });
              setIsLoadingLocation(false);
            },
            (error) => {
              console.log('Geolocation error:', error);
              setUserLocation({ lat: defaultLat, lng: defaultLng });
              setIsLoadingLocation(false);
            }
          );
        } else {
          setUserLocation({ lat: defaultLat, lng: defaultLng });
          setIsLoadingLocation(false);
        }
      }
    };

    getUserLocation();
  }, []);

  const handleCreateEvent = () => {
    setShowCreateEvent(true);
    // TODO: Implement create event modal/form
    console.log('Create event clicked');
  };

  const renderMap = () => {
    if (isLoadingLocation) {
      return (
        <div className="map-container loading-container">
          <div style={{ textAlign: 'center' }}>
            <LocationOnIcon className="icon" style={{ fontSize: 48, color: 'var(--accent-medium)' }} />
            <p>Getting your location...</p>
          </div>
        </div>
      );
    }

    const { lat, lng } = userLocation || { lat: defaultLat, lng: defaultLng };
    const bboxSize = 0.01; // Adjust this to control zoom level

    return (
      <div className="map-container">
        <iframe
          title="Group Ride Map"
          src={`https://www.openstreetmap.org/export/embed.html?bbox=${lng-bboxSize},${lat-bboxSize},${lng+bboxSize},${lat+bboxSize}&layer=mapnik&marker=${lat},${lng}`}
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
            borderRadius: '0'
          }}
          allowFullScreen
        />
        
        {/* Floating Action Button */}
        <button
          onClick={handleCreateEvent}
          className="fab"
          title="Create Group Event"
        >
          <AddIcon style={{ fontSize: 24 }} />
        </button>
      </div>
    );
  };

  const renderEvents = () => (
    <div style={{ padding: '20px', height: 'calc(100vh - 120px)', overflowY: 'auto' }}>
      <h2>Group Events</h2>
      <p>This is where you'll see all available group events.</p>
      <div style={{ textAlign: 'center', marginTop: '50px' }}>
        <p>No events available yet.</p>
        <button 
          className="btn btn-primary"
          onClick={handleCreateEvent}
        >
          Create First Event
        </button>
      </div>
    </div>
  );

  const renderProfile = () => (
    <div style={{ padding: '20px', height: 'calc(100vh - 120px)', overflowY: 'auto' }}>
      <h2>Profile</h2>
      <div className="card">
        <h3>Welcome, {userName || 'User'}!</h3>
        <p>Your profile information will be displayed here.</p>
        <button className="btn btn-secondary" onClick={onSignOut}>
          Sign Out
        </button>
      </div>
    </div>
  );

  const renderTabBar = () => (
    <div className="tab-bar">
      <button
        onClick={() => setActiveTab('map')}
        className={`tab-button ${activeTab === 'map' ? 'active' : ''}`}
      >
        <MapIcon className="icon" />
        Map
      </button>
      <button
        onClick={() => setActiveTab('events')}
        className={`tab-button ${activeTab === 'events' ? 'active' : ''}`}
      >
        <EventIcon className="icon" />
        Events
      </button>
      <button
        onClick={() => setActiveTab('profile')}
        className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
      >
        <PersonIcon className="icon" />
        Profile
      </button>
    </div>
  );

  return (
    <div style={{ height: '100vh', overflow: 'hidden' }}>
      {/* Header */}
      <div className="app-header">
        <h1>Group Ride</h1>
        <button
          onClick={onSignOut}
          className="header-signout"
        >
          Sign Out
        </button>
      </div>

      {/* Content Area */}
      <div className="content-area">
        {activeTab === 'map' && renderMap()}
        {activeTab === 'events' && renderEvents()}
        {activeTab === 'profile' && renderProfile()}
      </div>

      {/* Tab Bar */}
      {renderTabBar()}
    </div>
  );
};

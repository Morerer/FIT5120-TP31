import { useState, useMemo } from 'react';
import {
  GoogleMap,
  LoadScript,
  TrafficLayer,
  Marker
} from '@react-google-maps/api';

const containerStyle = { width: '100%', height: '80vh' };
const MELBOURNE_CBD = { lat: -37.8136, lng: 144.9631 };

export default function TrafficMap() {
  const [showTraffic, setShowTraffic] = useState(true);

  // Map UI/behavior options
  const mapOptions = useMemo(
    () => ({
      disableDefaultUI: false,
      zoomControl: true,
      streetViewControl: false,
      mapTypeControl: false,
      fullscreenControl: true,
      gestureHandling: 'greedy',
      styles: [
        // Subtle declutter: dim POIs a bit
        { featureType: 'poi', stylers: [{ visibility: 'simplified' }] },
        { featureType: 'transit', stylers: [{ visibility: 'off' }] }
      ]
    }),
    []
  );

  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

  return (
    <div className="w-full px-4 py-6">
      <div className="mb-4 flex items-center gap-3">
        <h1 className="text-xl font-semibold">Melbourne CBD – Live Traffic</h1>
        <label className="inline-flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            className="accent-blue-600"
            checked={showTraffic}
            onChange={(e) => setShowTraffic(e.target.checked)}
          />
          Show traffic
        </label>
      </div>

      <LoadScript googleMapsApiKey={apiKey}>
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={MELBOURNE_CBD}
          zoom={14}
          options={mapOptions}
        >
          {showTraffic && <TrafficLayer />}
          <Marker position={MELBOURNE_CBD} title="Melbourne CBD" />
        </GoogleMap>
      </LoadScript>
    </div>
  );
}

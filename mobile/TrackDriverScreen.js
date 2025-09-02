import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import io from 'socket.io-client';

export default function TrackDriverScreen() {
  const [location, setLocation] = useState(null);

  useEffect(() => {
    const socket = io('http://localhost:3000');
    socket.on('location_update', setLocation);
    return () => socket.disconnect();
  }, []);

  return (
    <View style={{ flex: 1 }}>
      <MapView style={{ flex: 1 }}>
        {location && (
          <Marker coordinate={{ latitude: location.lat, longitude: location.lon }} />
        )}
      </MapView>
    </View>
  );
}

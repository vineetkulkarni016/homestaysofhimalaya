import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';

export default function RequestRideScreen() {
  const [pickup, setPickup] = useState('');
  const [dropoff, setDropoff] = useState('');

  const requestRide = () => {
    // placeholder for API call
    console.log('request ride', pickup, dropoff);
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>Request Ride</Text>
      <TextInput
        placeholder="Pickup lat,lon"
        value={pickup}
        onChangeText={setPickup}
        style={{ borderWidth: 1, marginBottom: 10 }}
      />
      <TextInput
        placeholder="Dropoff lat,lon"
        value={dropoff}
        onChangeText={setDropoff}
        style={{ borderWidth: 1, marginBottom: 10 }}
      />
      <Button title="Request" onPress={requestRide} />
    </View>
  );
}

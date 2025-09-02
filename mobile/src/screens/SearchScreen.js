import React, { useEffect, useState } from 'react';
import { View, Text, Button } from 'react-native';
import { getHomestays } from '../api';
import { getCurrentLocation } from '../device';

export default function SearchScreen({ navigate }) {
  const [homes, setHomes] = useState([]);

  useEffect(() => {
    getHomestays().then(setHomes);
    getCurrentLocation(() => {});
  }, []);

  return (
    <View>
      {homes.map(h => (
        <View key={h.id}>
          <Text>{h.name}</Text>
          <Button title="Book" onPress={() => navigate('booking')} />
        </View>
      ))}
    </View>
  );
}

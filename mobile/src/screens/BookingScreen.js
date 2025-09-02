import React, { useEffect, useState } from 'react';
import { View, Text, Button } from 'react-native';
import { getBookings } from '../api';

export default function BookingScreen({ navigate }) {
  const [booking, setBooking] = useState(null);

  useEffect(() => {
    getBookings().then(setBooking);
  }, []);

  return (
    <View>
      <Text>{JSON.stringify(booking)}</Text>
      <Button title="Pay" onPress={() => navigate('payment')} />
    </View>
  );
}

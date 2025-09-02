import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import { getPayments } from '../api';

export default function PaymentScreen() {
  const [payment, setPayment] = useState(null);

  useEffect(() => {
    getPayments().then(setPayment);
  }, []);

  return (
    <View>
      <Text>{JSON.stringify(payment)}</Text>
    </View>
  );
}

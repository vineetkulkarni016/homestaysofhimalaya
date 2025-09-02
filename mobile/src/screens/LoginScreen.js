import React from 'react';
import { View, Button } from 'react-native';
import { login } from '../api';
import { registerForPush, captureDocument } from '../device';

export default function LoginScreen({ navigate }) {
  const handleLogin = async () => {
    await login();
    registerForPush();
    await captureDocument();
    navigate('search');
  };

  return (
    <View>
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}

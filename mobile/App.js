import React, { useState } from 'react';
import SearchScreen from './src/screens/SearchScreen';
import BookingScreen from './src/screens/BookingScreen';
import LoginScreen from './src/screens/LoginScreen';
import PaymentScreen from './src/screens/PaymentScreen';

export default function App() {
  const [screen, setScreen] = useState('login');
  const screens = {
    search: SearchScreen,
    booking: BookingScreen,
    login: LoginScreen,
    payment: PaymentScreen,
  };
  const ScreenComponent = screens[screen] || LoginScreen;
  return <ScreenComponent navigate={setScreen} />;
}

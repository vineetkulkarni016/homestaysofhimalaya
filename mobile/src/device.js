import PushNotification from '@react-native-community/push-notification-ios';
import Geolocation from '@react-native-community/geolocation';
import { launchCamera } from 'react-native-image-picker';

export function registerForPush() {
  PushNotification.requestPermissions();
}

export function getCurrentLocation(success) {
  Geolocation.getCurrentPosition(
    pos => success(pos.coords),
    err => console.warn('Location error', err),
    { enableHighAccuracy: true }
  );
}

export async function captureDocument() {
  return launchCamera({ mediaType: 'photo' });
}

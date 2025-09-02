import React, { useState } from 'react';
import { View, Button, Text, Alert } from 'react-native';
import { launchImageLibrary } from 'react-native-image-picker';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000';
const API_KEY = process.env.API_KEY || 'dev-key';

export default function DocumentUploadScreen() {
  const [fileName, setFileName] = useState(null);

  const pickAndUpload = async () => {
    const result = await launchImageLibrary({ mediaType: 'photo' });

    if (result.didCancel || result.errorCode || !result.assets?.length) {
      return;
    }

    const asset = result.assets[0];
    setFileName(asset.fileName || 'document');

    const formData = new FormData();
    formData.append('document', {
      uri: asset.uri,
      name: asset.fileName || 'document',
      type: asset.type || 'application/octet-stream',
    });

    try {
      const res = await fetch(
        `${API_BASE_URL}/bike-rentals/documents/upload`,
        {
          method: 'POST',
          headers: {
            'x-api-key': API_KEY,
          },
          body: formData,
        }
      );

      if (!res.ok) {
        throw new Error('Upload failed');
      }

      Alert.alert('Upload successful');
    } catch (err) {
      Alert.alert('Upload failed', err.message);
    }
  };

  return (
    <View>
      <Button title="Select Document" onPress={pickAndUpload} />
      {fileName && <Text>Selected: {fileName}</Text>}
    </View>
  );
}

import React, { useState } from 'react';
import { View, Button, Image, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function DocumentUploadScreen() {
  const [license, setLicense] = useState(null);
  const [aadhar, setAadhar] = useState(null);

  const pickImage = async (setter) => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
    });
    if (!result.canceled) {
      setter(result.assets[0]);
    }
  };

  const upload = async () => {
    if (!license || !aadhar) {
      Alert.alert('Please select both documents');
      return;
    }

    const formData = new FormData();
    formData.append('driving_license', {
      uri: license.uri,
      name: 'license.jpg',
      type: 'image/jpeg',
    });
    formData.append('aadhar_card', {
      uri: aadhar.uri,
      name: 'aadhar.jpg',
      type: 'image/jpeg',
    });

    try {
      const response = await fetch('http://localhost:8000/documents/upload', {
        method: 'POST',
        body: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (response.ok) {
        Alert.alert('Uploaded successfully');
      } else {
        Alert.alert('Upload failed');
      }
    } catch (err) {
      Alert.alert('Upload error');
    }
  };

  return (
    <View>
      <Button title="Pick Driving License" onPress={() => pickImage(setLicense)} />
      {license && <Image source={{ uri: license.uri }} style={{ width: 100, height: 100 }} />}
      <Button title="Pick Aadhar Card" onPress={() => pickImage(setAadhar)} />
      {aadhar && <Image source={{ uri: aadhar.uri }} style={{ width: 100, height: 100 }} />}
      <Button title="Upload" onPress={upload} />
    </View>
  );
}

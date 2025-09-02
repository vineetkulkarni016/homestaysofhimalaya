const API_URL = 'http://localhost:3000';
const headers = { 'x-api-key': 'dev-key' };

export async function getHomestays() {
  const res = await fetch(`${API_URL}/homestays`, { headers });
  return res.json();
}

export async function getBookings() {
  const res = await fetch(`${API_URL}/bookings`, { headers });
  return res.json();
}

export async function login() {
  const res = await fetch(`${API_URL}/users`, { headers });
  return res.json();
}

export async function getPayments() {
  const res = await fetch(`${API_URL}/payments`, { headers });
  return res.json();
}

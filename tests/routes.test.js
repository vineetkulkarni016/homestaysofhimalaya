const test = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const app = require('../index');

if (!globalThis.fetch) {
  globalThis.fetch = (...args) =>
    import('node-fetch').then(({ default: fetch }) => fetch(...args));
}

let server;

const baseUrl = () => `http://localhost:${server.address().port}`;

// Start server before tests

test.before(() => {
  server = http.createServer(app);
  return new Promise((resolve) => server.listen(0, resolve));
});

// Close server after tests

test.after(() => {
  return new Promise((resolve) => server.close(resolve));
});

test('rejects unauthorized requests', async () => {
  const res = await fetch(`${baseUrl()}/homestays`);
  assert.equal(res.status, 401);
});

test('allows requests with valid API key', async () => {
  const res = await fetch(`${baseUrl()}/homestays`, {
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' }
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, [
    { id: 1, name: 'Sample Homestay', location: 'Himalaya' }
  ]);
});

test('allows requests with valid bearer token', async () => {
  const res = await fetch(`${baseUrl()}/homestays`, {
    headers: { Authorization: `Bearer ${process.env.OAUTH_TOKEN || 'dev-token'}` }
  });
  assert.equal(res.status, 200);
});

test('returns stub data for bookings service', async () => {
  const res = await fetch(`${baseUrl()}/bookings`, {
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' }
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'booking', message: 'Hello World' });
});

test('returns stub data for users service', async () => {
  const res = await fetch(`${baseUrl()}/users`, {
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' }
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'user', message: 'Hello World' });
});

test('returns stub data for payments service', async () => {
  const res = await fetch(`${baseUrl()}/payments`, {
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' }
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'payment', message: 'Hello World' });
});

test('returns stub data for hosts service', async () => {
  const res = await fetch(`${baseUrl()}/hosts`, {
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' }
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'hosts', message: 'Hello World' });
});

test('returns stub data for bike rentals service', async () => {
  const res = await fetch(`${baseUrl()}/bike-rentals`, {
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' }
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'bike-rentals', message: 'Hello World' });
});

test('returns stub data for bike rentals availability', async () => {
  const res = await fetch(`${baseUrl()}/bike-rentals/availability`, {
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' }
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'bike-rentals', message: 'Hello World' });
});

test('returns stub data for bike rentals booking', async () => {
  const res = await fetch(`${baseUrl()}/bike-rentals/book`, {
    method: 'POST',
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' },
    body: JSON.stringify({})
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'bike-rentals', message: 'Hello World' });
});

test('returns stub data for bike rentals return', async () => {
  const res = await fetch(`${baseUrl()}/bike-rentals/return`, {
    method: 'POST',
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' },
    body: JSON.stringify({})
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'bike-rentals', message: 'Hello World' });
});

test('returns stub data for bike rentals document upload', async () => {
  const form = new FormData();
  form.append('file', new Blob(['test'], { type: 'text/plain' }), 'test.txt');
  const res = await fetch(`${baseUrl()}/bike-rentals/documents/upload`, {
    method: 'POST',
    headers: { 'x-api-key': process.env.API_KEY || 'dev-key' },
    body: form
  });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepStrictEqual(body, { service: 'bike-rentals', message: 'Hello World' });
});

try {
  require('dd-trace').init();
  console.log('Datadog tracer initialized');
} catch (err) {
  console.warn('Datadog tracer not initialized:', err.message);
}

const express = require('express');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const swaggerUi = require('swagger-ui-express');
const { Readable } = require('stream');
const http = require('http');
const { Server } = require('socket.io');
const { createClient } = require('redis');

if (!globalThis.fetch) {
  globalThis.fetch = (...args) =>
    import('node-fetch').then(({ default: fetch }) => fetch(...args));
}

const app = express();
app.use(express.json());

const spec = yaml.load(
  fs.readFileSync(path.join(__dirname, 'api/openapi.yaml'), 'utf8')
);

const API_KEY = process.env.API_KEY || 'dev-key';
const OAUTH_TOKEN = process.env.OAUTH_TOKEN || 'dev-token';

// Simple API key / bearer auth
app.use((req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  const auth = req.headers['authorization'];
  if (apiKey === API_KEY || (auth && auth === `Bearer ${OAUTH_TOKEN}`)) {
    return next();
  }
  res.status(401).json({ error: 'Unauthorized' });
});

app.use('/docs', swaggerUi.serve, swaggerUi.setup(spec));

app.get('/homestays', (req, res) => {
  res.json([{ id: 1, name: 'Sample Homestay', location: 'Himalaya' }]);
});

async function proxyOrStub(serviceUrl, serviceName) {
  if (serviceUrl) {
    try {
      const response = await fetch(serviceUrl);
      if (response.ok) {
        return await response.json();
      }
    } catch (err) {
      console.warn(`Failed to proxy ${serviceName} service:`, err.message);
    }
  }
  return { service: serviceName, message: 'Hello World' };
}

async function proxyStreamOrStub(req, res, serviceUrl, serviceName) {
  if (serviceUrl) {
    try {
      const url = new URL(req.originalUrl.replace(/^\/bike-rentals/, ''), serviceUrl);
      const headers = { ...req.headers };
      delete headers.host;
      const response = await fetch(url, {
        method: req.method,
        headers,
        body: ['GET', 'HEAD'].includes(req.method) ? undefined : req,
        duplex: 'half',
      });
      res.status(response.status);
      response.headers.forE

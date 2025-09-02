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
const http = require('http');
const { Server } = require('socket.io');
const { createClient } = require('redis');

if (!globalThis.fetch) {
  globalThis.fetch = (...args) =>
    import('node-fetch').then(({ default: fetch }) => fetch(...args));
}

const app = express();
app.use(express.json());
const spec = yaml.load(fs.readFileSync(path.join(__dirname, 'api/openapi.yaml'), 'utf8'));

const API_KEY = process.env.API_KEY || 'dev-key';
const OAUTH_TOKEN = process.env.OAUTH_TOKEN || 'dev-token';

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

app.get('/bookings', async (req, res) => {
  const data = await proxyOrStub(process.env.BOOKINGS_URL, 'booking');
  res.json(data);
});

app.get('/users', async (req, res) => {
  const data = await proxyOrStub(process.env.USERS_URL, 'user');
  res.json(data);
});

app.get('/payments', async (req, res) => {
  const data = await proxyOrStub(process.env.PAYMENTS_URL, 'payment');
  res.json(data);
});

app.get('/cabs', async (req, res) => {
  const data = await proxyOrStub(process.env.CABS_URL, 'cabs');
  res.json(data);
});

app.post('/cabs/rides', async (req, res) => {
  if (process.env.CABS_URL) {
    try {
      const response = await fetch(`${process.env.CABS_URL}/rides`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req.body)
      });
      const body = await response.json();
      return res.status(response.status).json(body);
    } catch (err) {
      console.warn('Failed to proxy cabs service:', err.message);
    }
  }
  res.status(501).json({ error: 'Cabs service unavailable' });
});

const port = process.env.PORT || 3000;

function startServer() {
  const server = http.createServer(app);
  const io = new Server(server, { cors: { origin: '*' } });
  const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';
  const sub = createClient({ url: redisUrl });
  sub
    .connect()
    .then(() =>
      sub.subscribe('driver_locations', (message) => {
        io.emit('location_update', JSON.parse(message));
      })
    )
    .catch((err) =>
      console.warn('Redis subscription failed:', err.message)
    );

  server.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
}

if (require.main === module) {
  startServer();
}

module.exports = app;

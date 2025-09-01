const express = require('express');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const swaggerUi = require('swagger-ui-express');

const app = express();
const spec = yaml.load(fs.readFileSync(path.join(__dirname, 'service/openapi.yaml'), 'utf8'));

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

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

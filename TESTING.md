# Testing Guide

## API
1. Install dependencies:
   ```bash
   pip install -r services/requirements.txt
   cd api
   npm install
   ```
   Alternatively, install each service dependency separately:
   ```bash
   pip install -r services/booking/requirements.txt -r services/users/requirements.txt -r services/payments/requirements.txt
   ```
2. Run unit tests:
   ```bash
   npm test
   ```
3. Run integration tests:
   ```bash
   npm run test:integration
   ```

## UI Tests
1. Install dependencies:
   ```bash
   cd ui
   npm install
   npx playwright install chromium
   ```
2. Run UI tests:
   ```bash
   npm test
   ```

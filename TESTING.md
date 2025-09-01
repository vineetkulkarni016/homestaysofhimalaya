# Testing Guide

## Service
1. Install dependencies:
   ```bash
   cd service
   npm install
   ```
2. Run unit tests:
   ```bash
   npm test
   ```
3. Run integration tests:
   ```bash
   npm run test:integration
   ```
4. Run contract tests:
   ```bash
   npm run test:contract
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

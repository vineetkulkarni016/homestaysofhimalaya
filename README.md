# HomestaysOfHimalaya

Himalayan Homestays, bike & car rentals booking and management.

## Services
- Booking service
- User service
- Payment service

## Single-click local launch

To run all services locally in one step:

1. Copy `.env.example` to `.env` and fill in the required values.
2. Execute `./scripts/setup_local.sh`.

The script installs Docker and Docker Compose if needed and then brings up the stack using `docker compose` with the environment configuration from `.env`.

## Development

Install dependencies and start the server:

```
npm install
npm start
```

The server runs from `index.js` on port `3000` by default and exposes API docs at `http://localhost:3000/docs`.


## Scripts

The `scripts/start_service.sh` script requires the AWS CLI and Python with the `PyYAML` package installed.

### Requirements

This project requires **Node.js 18 or later** for native `fetch` support. For older Node versions, `node-fetch` is automatically loaded as a polyfill when `fetch` is unavailable.


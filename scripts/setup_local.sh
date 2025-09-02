#!/usr/bin/env bash
set -euo pipefail

# Install Docker if missing
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Installing..."
  curl -fsSL https://get.docker.com | sh
fi

# Install Docker Compose plugin if missing
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin not found. Installing..."
  apt-get update && apt-get install -y docker-compose-plugin
fi

# Ensure env file exists
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    echo "Creating .env from .env.example"
    cp .env.example .env
  else
    echo "Error: .env file is required." >&2
    exit 1
  fi
fi

echo "Launching services..."
docker compose --env-file .env up --build

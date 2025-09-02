#!/usr/bin/env bash
set -e

echo "Setting up development environment..."

python3 -m venv venv
source venv/bin/activate
pip install -r services/booking/requirements.txt -r services/users/requirements.txt -r services/payments/requirements.txt

echo "Building and starting services with Docker Compose..."
docker compose up --build -d

echo "Environment is ready."

#!/usr/bin/env bash
set -euo pipefail

SERVICE="$1"
shift
APP_ENV="${APP_ENV:-dev-integration}"
CONFIG_FILE="config/${APP_ENV}.yml"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Config file $CONFIG_FILE not found" >&2
  exit 1
fi

fetch_param() {
  local key="$1"
  python - <<PY
import yaml,sys
with open("$CONFIG_FILE") as f:
    data=yaml.safe_load(f)
print(data.get("$SERVICE", {}).get("$key", ""))
PY
}

DB_PARAM=$(fetch_param database_url)
REDIS_PARAM=$(fetch_param redis_url)

if [ -z "$DB_PARAM" ] || [ -z "$REDIS_PARAM" ]; then
  echo "Missing parameter paths for $SERVICE in $CONFIG_FILE" >&2
  exit 1
fi

DB_URL=$(aws ssm get-parameter --name "$DB_PARAM" --with-decryption --output text --query Parameter.Value)
REDIS_URL=$(aws ssm get-parameter --name "$REDIS_PARAM" --with-decryption --output text --query Parameter.Value)

export DB_URL REDIS_URL

echo "Starting $SERVICE with configuration from $CONFIG_FILE"
# Placeholder for actual service command
exec "./$SERVICE" "$@"

#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ENV="${APP_ENV:-dev-integration}"
"${SCRIPT_DIR}/../../scripts/start_service.sh" cabs "$@"

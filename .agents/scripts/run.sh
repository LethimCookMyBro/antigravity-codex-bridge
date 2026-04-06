#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: .agents/scripts/run.sh

Runs validate-skills.py, check-stale.py, and health-check.sh in sequence.
EOF
  exit 0
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[1/3] validate-skills"
python3 "$ROOT_DIR/scripts/validate-skills.py"

echo "[2/3] check-stale"
python3 "$ROOT_DIR/scripts/check-stale.py" --today 2026-04-06

echo "[3/3] health-check"
bash "$ROOT_DIR/scripts/health-check.sh"

echo "PASS run.sh"

#!/usr/bin/env bash
set -u

if [[ "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: .agents/scripts/health-check.sh

Validates repo-local scripts for:
  - shebang presence
  - syntax / py_compile
  - --help behavior
  - no-argument validation for Python scripts
EOF
  exit 0
fi

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATUS=0

check_py() {
  local script="$1"
  local base
  base="$(basename "$script")"

  if ! head -n 1 "$script" | grep -q '^#!'; then
    echo "FAIL $base missing shebang"
    STATUS=1
  fi

  if ! python3 -m py_compile "$script" >/tmp/skill-health.out 2>&1; then
    echo "FAIL $base py_compile"
    sed -n '1,20p' /tmp/skill-health.out
    STATUS=1
  else
    echo "PASS $base py_compile"
  fi

  if ! python3 "$script" --help >/tmp/skill-health.out 2>&1; then
    echo "FAIL $base --help"
    sed -n '1,20p' /tmp/skill-health.out
    STATUS=1
  else
    echo "PASS $base --help"
  fi

  python3 "$script" >/tmp/skill-health.out 2>&1
  local noarg_exit=$?
  if [[ $noarg_exit -eq 0 ]]; then
    echo "PASS $base no-arg"
  elif grep -qiE 'usage:|required|error:' /tmp/skill-health.out; then
    echo "PASS $base no-arg validation"
  else
    echo "FAIL $base no-arg validation"
    sed -n '1,20p' /tmp/skill-health.out
    STATUS=1
  fi
}

check_sh() {
  local script="$1"
  local base
  base="$(basename "$script")"

  if ! head -n 1 "$script" | grep -q '^#!'; then
    echo "FAIL $base missing shebang"
    STATUS=1
  fi

  if ! bash -n "$script" >/tmp/skill-health.out 2>&1; then
    echo "FAIL $base bash -n"
    sed -n '1,20p' /tmp/skill-health.out
    STATUS=1
  else
    echo "PASS $base bash -n"
  fi

  if ! bash "$script" --help >/tmp/skill-health.out 2>&1; then
    echo "FAIL $base --help"
    sed -n '1,20p' /tmp/skill-health.out
    STATUS=1
  else
    echo "PASS $base --help"
  fi
}

for script in "$ROOT_DIR"/*.py; do
  check_py "$script"
done

for script in "$ROOT_DIR"/*.sh; do
  if [[ "$(basename "$script")" == "health-check.sh" ]]; then
    continue
  fi
  check_sh "$script"
done

exit "$STATUS"

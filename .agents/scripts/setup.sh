#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: .agents/scripts/setup.sh [--dry-run]

Installs or previews the core dependency setup flow for the skill system.
EOF
  exit 0
fi

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

run_cmd() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "DRY-RUN: $*"
  else
    eval "$@"
  fi
}

echo "Skill system setup starting (dry-run=$DRY_RUN)"

if command -v apt >/dev/null 2>&1; then
  run_cmd "sudo apt update"
  run_cmd "sudo apt install -y python3 python3-pip jq whois dnsutils curl ripgrep"
elif command -v brew >/dev/null 2>&1; then
  run_cmd "brew install python jq whois ripgrep"
elif command -v winget >/dev/null 2>&1; then
  run_cmd "winget install Python.Python.3.12"
fi

run_cmd "python3 -m pip install --upgrade pip"
run_cmd "python3 -m pip install python-whois requests"

echo "Optional tools to install separately if your workflows need them:"
echo "  - httpx"
echo "  - nuclei"
echo "  - nikto"
echo "  - subfinder"
echo "  - amass"
echo "  - syft"

echo "Wordlists:"
echo "  # Install: sudo apt install seclists"
echo "  # Or clone: git clone https://github.com/danielmiessler/SecLists"

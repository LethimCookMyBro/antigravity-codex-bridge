# Script Index

This index lists repo-local helper scripts used by the `.agents` skill system.

| Script | Purpose | Output | Notes |
|---|---|---|---|
| `auto_preview.py` | Start, stop, and inspect local preview processes | stdout + `.agents/preview.pid` / `.agents/preview.log` | `start`, `stop`, `status` subcommands |
| `checklist.py` | Run the repo validation checklist | stdout, exit code | Supports `--url` for performance checks |
| `check-stale.py` | Report skills whose `next_review` is missing or overdue | stdout summary, exit code | Supports `--today` override |
| `h4cker_ai_log_analysis.py` | Analyze security logs with OpenAI or local heuristics | stdout JSON or `--output` file | Works without `openai` by falling back to local heuristics |
| `h4cker_auth_logalyzer.py` | Correlate Linux auth logs | stdout JSON or text | Accepts plain logs and `.gz` rotations |
| `h4cker_dns_ownership.py` | Resolve DNS and whois ownership hints | stdout JSON | Uses `python-whois` if available, otherwise CLI `whois` |
| `h4cker_tls_cert_audit.py` | Collect TLS cert data and optional weak-cipher findings | stdout JSON | Supports `--port` and `--check-weak-ciphers` |
| `packet_capture_lab.py` | Tiny Scapy-based packet capture helper for owned labs | stdout packet summaries, optional pcap file | Requires `scapy` and capture privileges |
| `run.sh` | Run the production validation chain | stdout PASS/FAIL summary | Executes validate, stale check, and health check |
| `scapy_port_probe.py` | Small TCP port probe helper for lab validation | stdout JSON | Uses standard Python sockets |
| `session_manager.py` | Show project/session metadata | stdout text or JSON | `status` and `info` subcommands |
| `setup.sh` | Install or dry-run the core dependency setup flow | stdout install plan | Supports `--dry-run` |
| `validate-skills.py` | Validate skill metadata, line targets, and shared references | stdout summary, exit code | Supports `--strict` |
| `verify_all.py` | Run the full verification suite | stdout, exit code | Requires `--url` |
| `health-check.sh` | Validate shebangs, syntax, help output, and no-arg behavior for scripts | stdout PASS/FAIL summary | Run from repo root |

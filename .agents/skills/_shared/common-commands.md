# Shared Common Commands

Use these anchors when the same low-risk command patterns would otherwise be duplicated across multiple skills.

## dns-baseline

```bash
# Use on owned or explicitly authorized domains to collect registrar and DNS baseline evidence
whois example.com
dig NS example.com +short
dig MX example.com +short
dig TXT example.com +short
```

## dns-ownership-helper

```bash
# Use the local helper when you want structured DNS + whois context in JSON
python3 .agents/scripts/h4cker_dns_ownership.py example.com
```

## tls-audit-helper

```bash
# WARNING: use only on owned or explicitly authorized TLS endpoints
python3 .agents/scripts/h4cker_tls_cert_audit.py example.com
python3 .agents/scripts/h4cker_tls_cert_audit.py example.com --check-weak-ciphers
```

## verification-helpers

```bash
# Run the curated repo validation stack before release or when checking test/lint health
python3 .agents/scripts/checklist.py .
python3 .agents/scripts/verify_all.py . --url http://localhost:3000
```

## preview-status

```bash
# Check whether the local preview helper currently has a running process recorded
python3 .agents/scripts/auto_preview.py status
```

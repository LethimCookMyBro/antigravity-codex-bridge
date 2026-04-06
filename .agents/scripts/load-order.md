# Recommended Load Order

## Dependency Map

```text
methodology
├── recon
│   ├── osint
│   ├── osint-recon
│   └── web-application-testing
│       └── exploit-development
│           └── post-exploitation
├── dfir
│   ├── threat-hunting
│   └── threat-intelligence
├── capture-the-flag
│   ├── cracking-passwords
│   └── reverse-engineering
└── devsecops
    ├── sbom
    ├── docker-and-k8s-security
    └── cloud-resources
```

## Recommended Task Sequences

- pentest web app:
  `methodology -> recon -> web-application-testing -> exploit-development`
- CTF:
  `capture-the-flag -> cheat-sheets -> reverse-engineering`
- incident response:
  `dfir -> threat-hunting -> threat-intelligence`
- repo security review:
  `devsecops -> sbom -> docker-and-k8s-security`
- host hardening:
  `methodology -> linux-hardening -> windows`

## Notes

- Prefer lower `load_priority` numbers first.
- Avoid circular dependency chains.
- If two skills overlap, load the narrower skill after the broader discovery skill.

#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import socket
import subprocess
from datetime import datetime


MAJOR_CLOUD_PROVIDERS = [
    "Amazon",
    "AWS",
    "Azure",
    "Microsoft",
    "Google",
    "DigitalOcean",
    "Oracle",
    "Alibaba",
    "Cloudflare",
]


def resolve_first_ip(domain: str):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def resolve_rrset(domain: str, record_type: str):
    try:
        import dns.resolver

        answers = dns.resolver.resolve(domain, record_type)
        return [item.to_text() for item in answers]
    except Exception:
        pass

    dig_path = shutil.which("dig")
    if not dig_path:
        return []
    try:
        result = subprocess.run(
            [dig_path, domain, record_type, "+short"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def parse_whois_text(text: str) -> dict:
    def pick(pattern: str):
        match = re.search(pattern, text, re.I | re.M)
        return match.group(1).strip() if match else None

    return {
        "registrar": pick(r"^Registrar:\s*(.+)$"),
        "creation_date": pick(r"^(?:Creation Date|Created On|Created):\s*(.+)$"),
        "org": pick(r"^(?:OrgName|Organization|org-name|descr):\s*(.+)$"),
        "cidr": pick(r"^CIDR:\s*(.+)$"),
        "range": pick(r"^(?:NetRange|inetnum):\s*(.+)$"),
        "raw_available": bool(text.strip()),
    }


def whois_lookup(query: str):
    try:
        import whois

        result = whois.whois(query)
        return {
            "registrar": str(getattr(result, "registrar", "") or "") or None,
            "creation_date": str(getattr(result, "creation_date", "") or "") or None,
            "org": str(getattr(result, "org", "") or "") or None,
            "cidr": str(getattr(result, "cidr", "") or "") or None,
            "range": str(getattr(result, "range", "") or "") or None,
            "raw_available": True,
        }
    except Exception:
        pass

    whois_path = shutil.which("whois")
    if not whois_path:
        return None
    try:
        result = subprocess.run(
            [whois_path, query],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        return parse_whois_text(result.stdout)
    except Exception:
        return None


def detect_cloud_provider(text: str):
    if not text:
        return None
    lowered = text.lower()
    for provider in MAJOR_CLOUD_PROVIDERS:
        if provider.lower() in lowered:
            return provider
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve DNS records, whois ownership, and likely cloud hosting clues."
    )
    parser.add_argument("domain", help="Domain to inspect")
    args = parser.parse_args()

    domain = args.domain
    ip_address = resolve_first_ip(domain)
    mx_records = resolve_rrset(domain, "MX")
    ns_records = resolve_rrset(domain, "NS")
    txt_records = resolve_rrset(domain, "TXT")

    ip_whois = whois_lookup(ip_address) if ip_address else None
    domain_whois = whois_lookup(domain)

    org_text = ip_whois.get("org", "") if ip_whois else ""

    result = {
        "target": domain,
        "collected_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "dns": {
            "a_record": ip_address,
            "mx_records": mx_records,
            "ns_records": ns_records,
            "txt_records": txt_records,
        },
        "whois": {
            "domain_registrar": domain_whois.get("registrar") if domain_whois else None,
            "domain_creation_date": domain_whois.get("creation_date") if domain_whois else None,
            "ip_org": ip_whois.get("org") if ip_whois else None,
            "ip_cidr": ip_whois.get("cidr") if ip_whois else None,
            "ip_range": ip_whois.get("range") if ip_whois else None,
        },
        "hosting_hints": {
            "major_cloud_provider": detect_cloud_provider(org_text),
        },
        "collection_notes": {
            "dns_backend": "dnspython_or_dig",
            "whois_backend": "python-whois_or_cli",
        },
    }

    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

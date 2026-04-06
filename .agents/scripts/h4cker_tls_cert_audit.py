#!/usr/bin/env python3
import argparse
import json
import socket
import ssl
from datetime import datetime


WEAK_CIPHERS = [
    "aNULL",
    "eNULL",
    "EXPORT",
    "DES",
    "MD5",
    "PSK",
    "RC4",
    "SEED",
]


def format_name(entries):
    parts = []
    for item in entries or []:
        if item and isinstance(item, tuple) and item[0]:
            parts.append(f"{item[0][0]}={item[0][1]}")
    return ", ".join(parts)


def get_certificate_info(hostname: str, port: int) -> dict:
    context = ssl.create_default_context()
    with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname) as conn:
        conn.settimeout(5.0)
        conn.connect((hostname, port))
        cert = conn.getpeercert()
        cipher = conn.cipher()

    san = []
    for item in cert.get("subjectAltName", []):
        if len(item) == 2:
            san.append({"type": item[0], "value": item[1]})

    return {
        "subject": format_name(cert.get("subject")),
        "issuer": format_name(cert.get("issuer")),
        "serial_number": cert.get("serialNumber"),
        "version": cert.get("version"),
        "not_before": cert.get("notBefore"),
        "not_after": cert.get("notAfter"),
        "subject_alt_names": san,
        "cipher": {
            "name": cipher[0] if cipher else None,
            "protocol": cipher[1] if cipher else None,
            "bits": cipher[2] if cipher else None,
        },
    }


def check_weak_ciphers(hostname: str, port: int) -> list[dict]:
    findings = []
    for cipher in WEAK_CIPHERS:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        try:
            context.set_ciphers(cipher)
        except ssl.SSLError:
            continue

        try:
            with context.wrap_socket(
                socket.socket(socket.AF_INET), server_hostname=hostname
            ) as conn:
                conn.settimeout(3.0)
                conn.connect((hostname, port))
                active = conn.cipher()
                findings.append(
                    {
                        "requested_cipher": cipher,
                        "negotiated_cipher": active[0] if active else None,
                        "protocol": active[1] if active else None,
                    }
                )
        except Exception:
            continue
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect TLS certificate details and test for weak cipher acceptance."
    )
    parser.add_argument("domain", help="Domain to inspect")
    parser.add_argument("--port", type=int, default=443, help="TLS port, default 443")
    parser.add_argument(
        "--check-weak-ciphers",
        action="store_true",
        help="Attempt a short list of weak cipher families and report successful negotiation.",
    )
    args = parser.parse_args()

    data = {
        "target": args.domain,
        "port": args.port,
        "collected_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "certificate": get_certificate_info(args.domain, args.port),
    }
    if args.check_weak_ciphers:
        data["weak_cipher_findings"] = check_weak_ciphers(args.domain, args.port)

    print(json.dumps(data, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

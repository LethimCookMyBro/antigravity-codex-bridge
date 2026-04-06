#!/usr/bin/env python3
"""
Small authorized port-probe helper.

Usage:
  python3 .agents/scripts/scapy_port_probe.py 10.0.0.5 --ports 22,80,443 --timeout 2
  python3 .agents/scripts/scapy_port_probe.py 10.0.0.5 --port-range 20-25 --timeout 2
"""

import argparse
import json
import socket


def parse_ports(args: argparse.Namespace) -> list[int]:
    ports: list[int] = []
    if args.ports:
        for value in args.ports.split(","):
            value = value.strip()
            if value:
                ports.append(int(value))
    if args.port_range:
        start, end = args.port_range.split("-", 1)
        ports.extend(range(int(start), int(end) + 1))
    if not ports:
        raise SystemExit("Specify --ports or --port-range.")
    return sorted(set(ports))


def probe(target: str, port: int, timeout: float) -> dict:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        code = sock.connect_ex((target, port))
        status = "open" if code == 0 else "closed_or_filtered"
        return {"target": target, "port": port, "status": status, "errno": code}
    except Exception as exc:
        return {"target": target, "port": port, "status": "error", "error": str(exc)}
    finally:
        sock.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a tiny TCP port probe against an owned or authorized host and print JSON results."
    )
    parser.add_argument("target", help="IPv4 address or hostname of the authorized lab target")
    parser.add_argument("--ports", help="Comma-separated TCP port list, e.g. 22,80,443")
    parser.add_argument("--port-range", help="Inclusive TCP port range, e.g. 20-25")
    parser.add_argument("--timeout", type=float, default=2.0, help="Socket timeout in seconds")
    args = parser.parse_args()

    ports = parse_ports(args)
    results = [probe(args.target, port, args.timeout) for port in ports]
    print(json.dumps(results, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

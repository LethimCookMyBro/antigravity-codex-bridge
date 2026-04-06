#!/usr/bin/env python3
"""
Minimal packet capture helper for authorized lab use.

Usage:
  python3 .agents/scripts/packet_capture_lab.py --iface eth0 --count 5 --bpf "tcp"
  python3 .agents/scripts/packet_capture_lab.py --iface eth0 --count 20 --bpf "host 10.0.0.5" --output captured_packets.pcap
"""

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture a small number of packets from an authorized interface and optionally save them to a pcap."
    )
    parser.add_argument("--iface", required=True, help="Network interface to sniff on, e.g. eth0")
    parser.add_argument("--count", type=int, default=5, help="Packet count limit (default: 5)")
    parser.add_argument("--bpf", default="tcp", help="BPF filter string, e.g. 'tcp and port 443'")
    parser.add_argument("--output", help="Optional pcap output path")
    args = parser.parse_args()

    try:
        from scapy.all import sniff, wrpcap
    except Exception as exc:
        raise SystemExit(
            f"Scapy is required for live capture. Install it with 'python3 -m pip install scapy'. Details: {exc}"
        )

    try:
        packets = sniff(iface=args.iface, count=args.count, filter=args.bpf, timeout=10)
    except PermissionError:
        raise SystemExit("Packet capture requires sufficient privileges. Re-run with sudo in an authorized lab.")
    except Exception as exc:
        raise SystemExit(f"Capture failed: {exc}")

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        wrpcap(str(out), packets)

    for packet in packets:
        try:
            print(packet.summary())
        except Exception:
            print(repr(packet))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import argparse
import gzip
import json
import re
from collections import defaultdict
from pathlib import Path


def read_lines(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            yield line.rstrip("\n")


def parse_ip(line: str):
    match = re.search(r"\bfrom\s((?:[0-9]{1,3}\.){3}[0-9]{1,3})\b", line)
    return match.group(1) if match else None


def parse_user(line: str):
    patterns = [
        r"Accepted password for (\S+)",
        r"Failed password for (?:invalid user )?(\S+)",
        r"Invalid user (\S+)",
        r"sudo:\s+(\S+)\s*:",
        r"logname=(\S+)",
        r"user=(\S+)",
        r"USER=(\S+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            return match.group(1)
    return None


def parse_command(line: str):
    match = re.search(r"COMMAND=(.+)$", line)
    return match.group(1).strip() if match else None


def parse_date(line: str):
    match = re.match(r"^[A-Za-z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}", line)
    return match.group(0) if match else None


def update_bucket(bucket, line: str):
    ip = parse_ip(line)
    if ip:
        bucket["ips"].add(ip)

    command = parse_command(line)
    if command:
        bucket["commands"].add(command)

    bucket["logs"].append(line)

    if "Accepted password for" in line:
        bucket["success_logs"].append(line)
    if "Failed password for" in line or "authentication failure" in line or "Invalid user" in line:
        bucket["failure_logs"].append(line)


def analyze_auth_log(path: Path):
    per_user = defaultdict(
        lambda: {
            "ips": set(),
            "commands": set(),
            "logs": [],
            "failure_logs": [],
            "success_logs": [],
            "first_seen": None,
            "last_seen": None,
        }
    )

    for line in read_lines(path):
        user = parse_user(line) or "__unparsed__"
        bucket = per_user[user]
        update_bucket(bucket, line)
        stamp = parse_date(line)
        if stamp and bucket["first_seen"] is None:
            bucket["first_seen"] = stamp
        if stamp:
            bucket["last_seen"] = stamp

    rendered = {}
    for user, bucket in per_user.items():
        rendered[user] = {
            "ips": sorted(bucket["ips"]),
            "commands": sorted(bucket["commands"]),
            "failure_count": len(bucket["failure_logs"]),
            "success_count": len(bucket["success_logs"]),
            "first_seen": bucket["first_seen"],
            "last_seen": bucket["last_seen"],
            "failure_logs": bucket["failure_logs"],
            "success_logs": bucket["success_logs"],
        }
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Correlate Linux auth logs by user, IP, failures, successes, and sudo commands."
    )
    parser.add_argument("logfile", help="Path to auth.log or rotated .gz file")
    parser.add_argument("--user", help="Filter output to a single user")
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format, default json",
    )
    args = parser.parse_args()

    path = Path(args.logfile)
    if not path.exists():
        raise SystemExit(f"Log file not found: {path}")

    results = analyze_auth_log(path)
    if args.user:
        if args.user not in results:
            raise SystemExit(f"User not found in logs: {args.user}")
        results = {args.user: results[args.user]}

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=True))
    else:
        for user, data in results.items():
            print(f"[user] {user}")
            print(f"  first_seen: {data['first_seen']}")
            print(f"  last_seen: {data['last_seen']}")
            print(f"  failure_count: {data['failure_count']}")
            print(f"  success_count: {data['success_count']}")
            print(f"  ips: {', '.join(data['ips']) or '-'}")
            print(f"  commands: {', '.join(data['commands']) or '-'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

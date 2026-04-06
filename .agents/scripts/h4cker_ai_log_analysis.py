#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path


SYSTEM_PROMPT = """You are a cybersecurity analyst specializing in incident response and log analysis.
Analyze the provided logs and return valid JSON with this shape:
{
  "summary": "brief overview",
  "threat_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "malicious_activity_detected": true,
  "findings": [
    {
      "type": "finding_type",
      "severity": "LOW|MEDIUM|HIGH|CRITICAL",
      "description": "what happened",
      "indicators": ["indicator"],
      "recommendations": ["action"]
    }
  ],
  "iocs": {
    "ip_addresses": [],
    "domains": [],
    "file_hashes": [],
    "user_accounts": []
  },
  "recommendations": ["action"]
}
Focus on failed authentication, privilege escalation, suspicious network behavior, malware indicators, anomalous user activity, and compromise evidence."""


def read_log(path: Path, max_chars: int) -> str:
    content = path.read_text(encoding="utf-8", errors="replace")
    return content[:max_chars]


def heuristic_analysis(log_text: str) -> dict:
    ips = sorted(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", log_text)))
    domains = sorted(
        {
            value
            for value in re.findall(
                r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", log_text
            )
            if not value.replace(".", "").isdigit()
        }
    )
    hashes = sorted(
        set(
            re.findall(
                r"\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b",
                log_text,
            )
        )
    )
    users = sorted(
        set(
            re.findall(
                r"(?:Accepted password for|Failed password for|Invalid user|sudo:\s+)([A-Za-z0-9_.-]+)",
                log_text,
            )
        )
    )

    findings = []
    failed_count = len(re.findall(r"Failed password|authentication failure", log_text))
    sudo_count = len(re.findall(r"\bsudo:\b|COMMAND=", log_text))
    suspicious_net = len(re.findall(r"curl|wget|nc |nmap|masscan|powershell", log_text, re.I))

    threat_level = "LOW"
    malicious = False

    if failed_count:
        findings.append(
            {
                "type": "failed_authentication",
                "severity": "MEDIUM" if failed_count < 10 else "HIGH",
                "description": f"Detected {failed_count} failed authentication indicator(s).",
                "indicators": ips[:10] + users[:10],
                "recommendations": [
                    "Review the affected accounts and source IPs.",
                    "Correlate with successful logins or privilege changes.",
                ],
            }
        )
    if sudo_count:
        findings.append(
            {
                "type": "privilege_activity",
                "severity": "MEDIUM",
                "description": f"Detected {sudo_count} privilege-related log entry or command indicator(s).",
                "indicators": users[:10],
                "recommendations": [
                    "Confirm whether the commands were expected for the account and time window.",
                    "Preserve command history and related auth events.",
                ],
            }
        )
    if suspicious_net:
        findings.append(
            {
                "type": "network_or_tooling_indicator",
                "severity": "HIGH",
                "description": f"Detected {suspicious_net} suspicious network or tooling keyword match(es).",
                "indicators": ips[:10] + domains[:10],
                "recommendations": [
                    "Cross-check the destination domains and source hosts.",
                    "Collect related proxy, DNS, or EDR telemetry.",
                ],
            }
        )

    if failed_count >= 10 or suspicious_net:
        threat_level = "HIGH"
        malicious = True
    elif failed_count or sudo_count:
        threat_level = "MEDIUM"

    summary_parts = []
    if failed_count:
        summary_parts.append(f"{failed_count} failed-auth indicators")
    if sudo_count:
        summary_parts.append(f"{sudo_count} privilege-related indicators")
    if suspicious_net:
        summary_parts.append(f"{suspicious_net} suspicious network/tooling indicators")
    if not summary_parts:
        summary_parts.append("No strong malicious indicators detected by local heuristics")

    recommendations = [
        "Validate all findings against raw evidence before containment decisions.",
        "Promote weak indicators to confirmed findings only after timestamp and entity correlation.",
    ]
    if not findings:
        recommendations.append("Collect a larger time window or richer log sources if the investigation remains inconclusive.")

    return {
        "summary": "; ".join(summary_parts),
        "threat_level": threat_level,
        "malicious_activity_detected": malicious,
        "analysis_mode": "local-heuristic",
        "findings": findings,
        "iocs": {
            "ip_addresses": ips,
            "domains": domains,
            "file_hashes": hashes,
            "user_accounts": users,
        },
        "recommendations": recommendations,
    }


def analyze_logs(log_text: str, model: str) -> dict:
    try:
        from openai import OpenAI
    except Exception:
        return heuristic_analysis(log_text)

    if not os.getenv("OPENAI_API_KEY"):
        return heuristic_analysis(log_text)

    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Analyze the following security logs. Return JSON only.\n\n"
                        f"{log_text}"
                    ),
                },
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        result.setdefault("analysis_mode", "openai")
        return result
    except Exception:
        return heuristic_analysis(log_text)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze security logs with an OpenAI model and emit structured JSON."
    )
    parser.add_argument("logfile", help="Path to a log file to analyze")
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        help="OpenAI model name. Defaults to OPENAI_MODEL or gpt-4.1-mini.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=30000,
        help="Maximum number of log characters to send to the model.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write the JSON result.",
    )
    args = parser.parse_args()

    path = Path(args.logfile)
    if not path.exists():
        raise SystemExit(f"Log file not found: {path}")

    log_text = read_log(path, args.max_chars)
    if not log_text.strip():
        raise SystemExit("Log file is empty.")

    result = analyze_logs(log_text, args.model)
    rendered = json.dumps(result, indent=2, ensure_ascii=True)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

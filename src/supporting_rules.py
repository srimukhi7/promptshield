"""
supporting_rules.py

Purpose:
Provides narrowly scoped deterministic rules that supplement the
pretrained ML detector.

These rules detect structured values that a general-purpose PII model
may miss, including:

- API keys
- Access tokens
- Employee IDs
- Volunteer IDs
- Client IDs
- Explicit confidentiality markers

The ML model remains the primary detection engine.
"""

from __future__ import annotations

import re
from typing import Any


STRUCTURED_PATTERNS: list[dict[str, Any]] = [
    {
        "label": "API_KEY",
        "pattern": re.compile(
            r"\b(sk-(?:test-|live-)?[A-Za-z0-9_-]{16,})\b",
            re.IGNORECASE,
        ),
        "value_group": 1,
    },
    {
        "label": "ACCESS_TOKEN",
        "pattern": re.compile(
            r"\b(?:access[_ -]?token|bearer)"
            r"\s*[:=]?\s*"
            r"([A-Za-z0-9._~+/=-]{12,})\b",
            re.IGNORECASE,
        ),
        "value_group": 1,
    },
    {
        "label": "EMPLOYEE_ID",
        "pattern": re.compile(
            r"\b(EMP(?:LOYEE)?[-_ ]?\d{3,10})\b",
            re.IGNORECASE,
        ),
        "value_group": 1,
    },
    {
        "label": "VOLUNTEER_ID",
        "pattern": re.compile(
            r"\b(VOL(?:UNTEER)?[-_ ]?\d{3,10})\b",
            re.IGNORECASE,
        ),
        "value_group": 1,
    },
    {
        "label": "CLIENT_ID",
        "pattern": re.compile(
            r"\b((?:CLI|CLIENT)[-_ ]?\d{3,10})\b",
            re.IGNORECASE,
        ),
        "value_group": 1,
    },
]


CONFIDENTIALITY_PATTERN = re.compile(
    r"\b(?:"
    r"strictly confidential"
    r"|confidential"
    r"|internal only"
    r"|do not distribute"
    r"|not for external sharing"
    r"|restricted information"
    r")\b",
    re.IGNORECASE,
)


def detect_structured_values(
    text: str,
) -> list[dict[str, Any]]:
    """Detect structured credentials and organizational identifiers."""
    findings: list[dict[str, Any]] = []

    for rule in STRUCTURED_PATTERNS:
        pattern = rule["pattern"]
        value_group = int(rule["value_group"])

        for match in pattern.finditer(text):
            start, end = match.span(value_group)

            findings.append(
                {
                    "label": str(rule["label"]),
                    "text": text[start:end],
                    "start": start,
                    "end": end,
                    "score": 1.0,
                    "source": "supporting_rule",
                }
            )

    return findings


def detect_confidentiality_markers(
    text: str,
) -> list[dict[str, Any]]:
    """
    Detect explicit confidentiality language.

    Ordinary words such as "project", "roadmap", or "internal" alone
    are deliberately not flagged.
    """
    findings: list[dict[str, Any]] = []

    for match in CONFIDENTIALITY_PATTERN.finditer(text):
        findings.append(
            {
                "label": "CONFIDENTIAL_INFORMATION",
                "text": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "score": 1.0,
                "source": "supporting_rule",
            }
        )

    return findings


def detect_supporting_rules(
    text: str,
) -> list[dict[str, Any]]:
    """Run all deterministic supporting rules."""
    if not text.strip():
        return []

    findings = (
        detect_structured_values(text)
        + detect_confidentiality_markers(text)
    )

    return sorted(
        findings,
        key=lambda finding: int(finding["start"]),
    )


def main() -> None:
    """Run synthetic smoke tests for all supporting rules."""
    risky_text = (
        "STRICTLY CONFIDENTIAL\n"
        "Employee Maya Patel has employee ID EMP-4821.\n"
        "Volunteer Elena Cruz has volunteer ID VOL-7284.\n"
        "Client Daniel Lee has client ID CLI-7934.\n"
        "Temporary API key: sk-test-4f92a8d71c6b3e50.\n"
        "Access token: abcdef1234567890xyz."
    )

    safe_text = (
        "The internal team will meet tomorrow to discuss "
        "the project roadmap."
    )

    for title, text in [
        ("Risky example", risky_text),
        ("Safe example", safe_text),
    ]:
        findings = detect_supporting_rules(text)

        print("\n" + "=" * 70)
        print(title.upper())
        print("=" * 70)
        print(text)
        print("\nSupporting-rule findings:")

        if not findings:
            print("None")
            continue

        for finding in findings:
            print(
                f"- {finding['label']:<28}"
                f" | {finding['text']}"
                f" | Source: {finding['source']}"
            )


if __name__ == "__main__":
    main()
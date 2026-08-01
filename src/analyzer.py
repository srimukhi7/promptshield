"""
analyzer.py

Purpose:
Coordinates the complete privacy analysis pipeline.

Responsibilities:
- Run ML-first detection
- Generate redacted text
- Calculate a simple heuristic privacy-risk score
- Return one unified analysis report
"""

from __future__ import annotations

from typing import Any

from detector import detect_sensitive_information
from redactor import redact_text


HIGH_RISK_LABELS = {
    "US_SSN",
    "PASSWORD",
    "API_KEY",
    "ACCESS_TOKEN",
    "CREDIT_CARD",
    "US_BANK_NUMBER",
    "IBAN_CODE",
    "US_PASSPORT",
    "US_DRIVER_LICENSE",
    "US_ITIN",
}

MEDIUM_RISK_LABELS = {
    "EMPLOYEE_ID",
    "VOLUNTEER_ID",
    "CLIENT_ID",
    "CONFIDENTIAL_INFORMATION",
    "FINANCIAL",
    "IP_ADDRESS",
}

LOWER_RISK_LABELS = {
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "LOCATION",
    "ORGANIZATION",
    "TITLE",
}


def calculate_risk(
    findings: list[dict[str, Any]],
) -> tuple[int, str]:
    """
    Calculate a simple heuristic privacy-risk score.

    This score is a user-facing summary and is not a formal security,
    legal, privacy, or compliance assessment.
    """
    score = 0

    for finding in findings:
        label = str(finding["label"])

        if label == "US_SSN":
            score += 40
        elif label in HIGH_RISK_LABELS:
            score += 35
        elif label in MEDIUM_RISK_LABELS:
            score += 25
        elif label in LOWER_RISK_LABELS:
            score += 15
        else:
            score += 10

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


def analyze_text(
    text: str,
    detector: Any,
) -> dict[str, Any]:
    """Run the complete privacy-analysis pipeline."""
    findings = detect_sensitive_information(
        text,
        detector,
    )

    redacted_text = redact_text(
        text,
        findings,
    )

    risk_score, risk_level = calculate_risk(findings)

    return {
        "original_text": text,
        "findings": findings,
        "redacted_text": redacted_text,
        "entity_count": len(findings),
        "risk_score": risk_score,
        "risk_level": risk_level,
    }
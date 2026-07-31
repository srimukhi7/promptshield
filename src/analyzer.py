"""
analyzer.py

Purpose:
Coordinates the complete privacy analysis pipeline.

Responsibilities:
- Run ML detection
- Generate redacted text
- Calculate a simple privacy risk score
- Return one unified report

The UI should only call:

    analyze_text(...)
"""

from __future__ import annotations

from typing import Any

from detector import detect_sensitive_information
from redactor import redact_text


def calculate_risk(
    findings: list[dict[str, Any]],
) -> tuple[int, str]:
    """
    Calculate a simple heuristic privacy-risk score.

    This score is not a formal security or compliance assessment.
    It is a user-facing summary based on the sensitivity of the
    detected entity types.
    """
    score = 0

    for finding in findings:
        label = str(finding["label"])

        if label == "US_SSN":
            score += 40

        elif label in {
            "PASSWORD",
            "CREDIT_CARD",
            "FINANCIAL",
            "IBAN_CODE",
            "US_BANK_NUMBER",
            "US_PASSPORT",
            "US_DRIVER_LICENSE",
            "US_ITIN",
        }:
            score += 30

        elif label in {
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "PERSON",
            "IP_ADDRESS",
        }:
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
    """
    Run the complete end-to-end privacy analysis.

    Returns:
        A dictionary containing the original text, findings,
        redacted text, finding count, risk score, and risk level.
    """
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
"""
redactor.py

Purpose:
Generates a safer version of text by replacing detected sensitive
information with readable placeholder labels.

Responsibilities:
- Map model labels to user-friendly redaction labels
- Replace sensitive spans without changing safe text
- Handle findings from right to left so character positions remain valid

This module does NOT:
- Run the ML model
- Build the user interface
- Decide whether a model prediction is correct
"""

from __future__ import annotations

from typing import Any


REDACTION_LABELS = {
    "PERSON": "[NAME]",
    "EMAIL_ADDRESS": "[EMAIL]",
    "PHONE_NUMBER": "[PHONE]",
    "LOCATION": "[LOCATION]",
    "ORGANIZATION": "[ORGANIZATION]",
    "TITLE": "[JOB TITLE]",
    "PASSWORD": "[PASSWORD]",
    "CREDIT_CARD": "[CREDIT CARD]",
    "FINANCIAL": "[FINANCIAL INFORMATION]",
    "IBAN_CODE": "[IBAN]",
    "US_BANK_NUMBER": "[BANK ACCOUNT]",
    "US_DRIVER_LICENSE": "[DRIVER LICENSE]",
    "US_ITIN": "[ITIN]",
    "US_PASSPORT": "[PASSPORT]",
    "US_SSN": "[SSN]",
    "IP_ADDRESS": "[IP ADDRESS]",
}


def get_redaction_label(entity_label: str) -> str:
    """
    Return a readable placeholder for a detected entity label.

    Unknown labels receive a generic placeholder so the function
    remains safe if the detector later supports additional labels.
    """
    return REDACTION_LABELS.get(entity_label, "[SENSITIVE INFORMATION]")


def redact_text(
    text: str,
    findings: list[dict[str, Any]],
) -> str:
    """
    Replace detected sensitive spans with placeholder labels.

    Findings are processed from right to left. This prevents an earlier
    replacement from changing the character positions of later findings.
    """
    if not text:
        return ""

    if not findings:
        return text

    redacted_text = text

    sorted_findings = sorted(
        findings,
        key=lambda finding: int(finding["start"]),
        reverse=True,
    )

    for finding in sorted_findings:
        start = int(finding["start"])
        end = int(finding["end"])
        entity_label = str(finding["label"])

        if start < 0 or end > len(text) or start >= end:
            continue

        placeholder = get_redaction_label(entity_label)

        redacted_text = (
            redacted_text[:start]
            + placeholder
            + redacted_text[end:]
        )

    return redacted_text


def main() -> None:
    """
    Run a small synthetic smoke test.
    """
    sample_text = (
        "Employee Maya Patel can be reached at "
        "maya.patel@example.com. Her SSN is 123-45-6789."
    )

    sample_findings = [
        {
            "label": "PERSON",
            "text": "Maya Patel",
            "start": 9,
            "end": 19,
            "score": 0.781,
        },
        {
            "label": "EMAIL_ADDRESS",
            "text": "maya.patel@example.com",
            "start": 38,
            "end": 60,
            "score": 0.982,
        },
        {
            "label": "US_SSN",
            "text": "123-45-6789",
            "start": 73,
            "end": 84,
            "score": 0.947,
        },
    ]

    redacted = redact_text(sample_text, sample_findings)

    print("Original:")
    print(sample_text)

    print("\nRedacted:")
    print(redacted)


if __name__ == "__main__":
    main()
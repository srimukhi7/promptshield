"""
redactor.py

Purpose:
Generates a safer version of text by replacing detected sensitive
information with readable placeholder labels.

Responsibilities:
- Map detection labels to user-friendly redaction labels
- Replace sensitive spans without changing safe text
- Process spans from right to left so offsets remain valid
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
    "API_KEY": "[API KEY]",
    "ACCESS_TOKEN": "[ACCESS TOKEN]",
    "CREDIT_CARD": "[CREDIT CARD]",
    "FINANCIAL": "[FINANCIAL INFORMATION]",
    "IBAN_CODE": "[IBAN]",
    "US_BANK_NUMBER": "[BANK ACCOUNT]",
    "US_DRIVER_LICENSE": "[DRIVER LICENSE]",
    "US_ITIN": "[ITIN]",
    "US_PASSPORT": "[PASSPORT]",
    "US_SSN": "[SSN]",
    "IP_ADDRESS": "[IP ADDRESS]",
    "EMPLOYEE_ID": "[EMPLOYEE ID]",
    "VOLUNTEER_ID": "[VOLUNTEER ID]",
    "CLIENT_ID": "[CLIENT ID]",
    "CONFIDENTIAL_INFORMATION": "[CONFIDENTIAL INFORMATION]",
}


def get_redaction_label(entity_label: str) -> str:
    """Return a readable placeholder for a detected entity label."""
    return REDACTION_LABELS.get(
        entity_label,
        "[SENSITIVE INFORMATION]",
    )


def redact_text(
    text: str,
    findings: list[dict[str, Any]],
) -> str:
    """
    Replace detected sensitive spans with placeholder labels.

    Findings are processed from right to left so replacements do not
    invalidate character offsets for findings earlier in the text.
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
    """Run a synthetic redaction smoke test."""
    sample_text = (
        "STRICTLY CONFIDENTIAL. "
        "Employee Maya Patel has employee ID EMP-4821. "
        "Temporary API key: sk-test-4f92a8d71c6b3e50."
    )

    sample_findings = [
        {
            "label": "CONFIDENTIAL_INFORMATION",
            "text": "STRICTLY CONFIDENTIAL",
            "start": 0,
            "end": 21,
            "score": 1.0,
            "source": "supporting_rule",
        },
        {
            "label": "PERSON",
            "text": "Maya Patel",
            "start": 32,
            "end": 42,
            "score": 0.90,
            "source": "ml",
        },
        {
            "label": "EMPLOYEE_ID",
            "text": "EMP-4821",
            "start": 59,
            "end": 67,
            "score": 1.0,
            "source": "supporting_rule",
        },
        {
            "label": "API_KEY",
            "text": "sk-test-4f92a8d71c6b3e50",
            "start": 88,
            "end": 114,
            "score": 1.0,
            "source": "supporting_rule",
        },
    ]

    print("Original:")
    print(sample_text)

    print("\nRedacted:")
    print(redact_text(sample_text, sample_findings))


if __name__ == "__main__":
    main()
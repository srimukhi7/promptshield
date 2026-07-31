"""
demo.py

Purpose:
Demonstrates the complete privacy-auditor pipeline.

Flow:

Input Text
      ↓
ML Detection
      ↓
Detected Findings
      ↓
Redaction
      ↓
Safe Output
"""

from detector import (
    load_detector,
    detect_sensitive_information,
)

from redactor import (
    redact_text,
)


def main():

    detector = load_detector()

    text = (
        "Employee Maya Patel can be reached at "
        "maya.patel@example.com. "
        "Her SSN is 123-45-6789."
    )

    print("=" * 70)
    print("ORIGINAL TEXT")
    print("=" * 70)

    print(text)

    findings = detect_sensitive_information(
        text,
        detector,
    )

    print("\n")
    print("=" * 70)
    print("DETECTED FINDINGS")
    print("=" * 70)

    if not findings:
        print("No sensitive information detected.")

    else:

        for finding in findings:

            print(
                f"{finding['label']:<20}"
                f"{finding['text']:<30}"
                f"{finding['score']:.3f}"
            )

    redacted = redact_text(
        text,
        findings,
    )

    print("\n")
    print("=" * 70)
    print("REDACTED TEXT")
    print("=" * 70)

    print(redacted)


if __name__ == "__main__":
    main()
"""
demo.py

Purpose:
Demonstrates the complete privacy-auditor pipeline.

Flow:
- Load the ML detector
- Analyze synthetic text
- Display detected findings
- Display the heuristic risk summary
- Display the safer redacted version
"""

from __future__ import annotations

from typing import Any

from analyzer import analyze_text
from detector import load_detector


def print_report(
    title: str,
    text: str,
    detector: Any,
) -> None:
    """Analyze one example and print the complete report."""
    report = analyze_text(text, detector)

    print("\n" + "=" * 70)
    print(title.upper())
    print("=" * 70)

    print("\nOriginal text:")
    print(report["original_text"])

    print("\nDetected findings:")

    if not report["findings"]:
        print("None")
    else:
        for finding in report["findings"]:
            print(
                f"- {finding['label']:<20}"
                f"{finding['text']:<30}"
                f"Confidence: {finding['score']:.3f}"
            )

    print("\nPrivacy summary:")
    print(f"- Findings: {report['entity_count']}")
    print(f"- Risk score: {report['risk_score']}/100")
    print(f"- Risk level: {report['risk_level']}")

    print("\nRedacted text:")
    print(report["redacted_text"])


def main() -> None:
    detector = load_detector()

    risky_text = (
        "Employee Maya Patel can be reached at "
        "maya.patel@example.com. Her SSN is 123-45-6789."
    )

    safe_text = "The project meeting is scheduled for 3:00 PM."

    print("\nModel loaded successfully.")

    print_report(
        title="Risky Example",
        text=risky_text,
        detector=detector,
    )

    print_report(
        title="Safe Example",
        text=safe_text,
        detector=detector,
    )


if __name__ == "__main__":
    main()
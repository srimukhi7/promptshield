"""
detector.py

Purpose:
Runs the pretrained ML model and merges its findings with supporting
deterministic rules for structured sensitive values.

The pretrained model performs primary detection. Specific supporting
rules extend coverage for structured credentials, organizational IDs,
and explicit confidentiality markers.
"""

from __future__ import annotations

from typing import Any

from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    pipeline,
)

from supporting_rules import detect_supporting_rules


MODEL_NAME = "gravitee-io/bert-small-pii-detection"
MIN_CONFIDENCE = 0.60

SUPPORTED_LABELS = {
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "LOCATION",
    "ORGANIZATION",
    "TITLE",
    "PASSWORD",
    "CREDIT_CARD",
    "FINANCIAL",
    "IBAN_CODE",
    "US_BANK_NUMBER",
    "US_DRIVER_LICENSE",
    "US_ITIN",
    "US_PASSPORT",
    "US_SSN",
    "IP_ADDRESS",
}


def load_detector():
    """Load the tokenizer, model, and token-classification pipeline."""
    print(f"Loading model: {MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

    return pipeline(
        task="token-classification",
        model=model,
        tokenizer=tokenizer,
        aggregation_strategy="simple",
    )


def normalize_model_findings(
    text: str,
    raw_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Convert raw model output into clean, exact character spans."""
    findings: list[dict[str, Any]] = []

    for result in sorted(
        raw_results,
        key=lambda item: int(item["start"]),
    ):
        label = str(result["entity_group"])
        score = float(result["score"])

        if label not in SUPPORTED_LABELS or score < MIN_CONFIDENCE:
            continue

        start = int(result["start"])
        end = int(result["end"])

        if findings:
            previous = findings[-1]
            gap = text[int(previous["end"]):start]

            if previous["label"] == label and gap.isspace():
                previous["end"] = end
                previous["text"] = text[int(previous["start"]):end]
                previous["score"] = min(
                    float(previous["score"]),
                    score,
                )
                continue

        findings.append(
            {
                "label": label,
                "text": text[start:end],
                "start": start,
                "end": end,
                "score": score,
                "source": "ml",
            }
        )

    return findings


def findings_overlap(
    first: dict[str, Any],
    second: dict[str, Any],
) -> bool:
    """Return True when two findings overlap in the original text."""
    return (
        int(first["start"]) < int(second["end"])
        and int(second["start"]) < int(first["end"])
    )


def merge_findings(
    ml_findings: list[dict[str, Any]],
    rule_findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Merge ML and supporting-rule findings.

    Specific structured rules take priority when they overlap a broader
    or partial ML prediction. For example, a complete API key replaces
    a PASSWORD prediction covering only the key's suffix.
    """
    merged = list(ml_findings)

    for rule_finding in rule_findings:
        merged = [
            existing
            for existing in merged
            if not findings_overlap(existing, rule_finding)
        ]

        merged.append(rule_finding)

    return sorted(
        merged,
        key=lambda finding: int(finding["start"]),
    )


def detect_sensitive_information(
    text: str,
    detector,
) -> list[dict[str, Any]]:
    """Run the complete ML-first sensitive-information pipeline."""
    if not text.strip():
        return []

    raw_results = detector(text)

    ml_findings = normalize_model_findings(
        text,
        raw_results,
    )

    rule_findings = detect_supporting_rules(text)

    return merge_findings(
        ml_findings,
        rule_findings,
    )


def main() -> None:
    """Run combined risky and safe smoke tests."""
    detector = load_detector()

    examples = [
        (
            "Combined Risky Example",
            (
                "STRICTLY CONFIDENTIAL\n"
                "Employee Maya Patel has employee ID EMP-4821.\n"
                "Volunteer Elena Cruz has volunteer ID VOL-7284.\n"
                "Client Daniel Lee has client ID CLI-7934.\n"
                "Contact Maya at maya.patel@example.com or "
                "415-555-0136.\n"
                "Her fictional SSN is 123-45-6789.\n"
                "Temporary API key: sk-test-4f92a8d71c6b3e50.\n"
                "Access token: abcdef1234567890xyz."
            ),
        ),
        (
            "Safe Example",
            (
                "The internal team will meet tomorrow to discuss "
                "the project roadmap."
            ),
        ),
    ]

    print("\nModel loaded successfully.")

    for title, text in examples:
        findings = detect_sensitive_information(text, detector)

        print("\n" + "=" * 70)
        print(title.upper())
        print("=" * 70)
        print(f"\nInput:\n{text}")
        print("\nDetected entities:")

        if not findings:
            print("None")
            continue

        for finding in findings:
            print(
                f"- {finding['label']:<28}"
                f" | {finding['text']:<35}"
                f" | Confidence: {finding['score']:.3f}"
                f" | Source: {finding['source']}"
            )


if __name__ == "__main__":
    main()
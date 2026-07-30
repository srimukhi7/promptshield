"""
detector.py

Purpose:
Runs the pretrained ML model to detect sensitive information.

Responsibilities:
- Load the Hugging Face model
- Detect sensitive entities
- Normalize model output
- Filter unsupported and low-confidence predictions

This module does NOT:
- Build the UI
- Highlight text
- Redact text
"""

from __future__ import annotations

from typing import Any

from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    pipeline,
)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_NAME = "gravitee-io/bert-small-pii-detection"

# Ignore weak predictions
MIN_CONFIDENCE = 0.60

# Only keep entity labels that are relevant for our hackathon
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


# --------------------------------------------------
# Model Loading
# --------------------------------------------------

def load_detector():
    """
    Loads the tokenizer, model, and Hugging Face
    token-classification pipeline.
    """

    print(f"Loading model: {MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_NAME
    )

    detector = pipeline(
        task="token-classification",
        model=model,
        tokenizer=tokenizer,
        aggregation_strategy="simple",
    )

    return detector


# --------------------------------------------------
# Post-processing
# --------------------------------------------------

def normalize_findings(
    text: str,
    raw_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Converts raw Hugging Face output into a clean format.

    The model sometimes inserts spaces into words
    (especially emails and phone numbers).

    Instead of using the returned "word",
    we use the original character positions.
    """

    findings: list[dict[str, Any]] = []

    for result in sorted(raw_results, key=lambda r: int(r["start"])):

        label = str(result["entity_group"])
        score = float(result["score"])

        # Ignore unsupported labels
        if label not in SUPPORTED_LABELS:
            continue

        # Ignore weak predictions
        if score < MIN_CONFIDENCE:
            continue

        start = int(result["start"])
        end = int(result["end"])

        # Merge consecutive entities
        if findings:

            previous = findings[-1]

            gap = text[previous["end"]:start]

            if (
                previous["label"] == label
                and gap.isspace()
            ):
                previous["end"] = end
                previous["text"] = text[
                    previous["start"]:end
                ]

                # Keep the lower confidence
                previous["score"] = min(
                    previous["score"],
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
            }
        )

    return findings


# --------------------------------------------------
# Public API
# --------------------------------------------------

def detect_sensitive_information(
    text: str,
    detector,
) -> list[dict[str, Any]]:
    """
    Runs the detector on user text.
    """

    if not text.strip():
        return []

    raw_results = detector(text)

    return normalize_findings(
        text,
        raw_results,
    )


# --------------------------------------------------
# Smoke Test
# --------------------------------------------------

def main():

    detector = load_detector()

    examples = [

        (
            "Risky Example",
            (
                "Employee Maya Patel can be reached at "
                "maya.patel@example.com. "
                "Her SSN is 123-45-6789."
            ),
        ),

        (
            "Safe Example",
            (
                "The project meeting is scheduled "
                "for 3:00 PM."
            ),
        ),
    ]

    print("\nModel loaded successfully.")

    for title, text in examples:

        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)

        print(f"\nInput:\n{text}")

        findings = detect_sensitive_information(
            text,
            detector,
        )

        print("\nDetected entities:")

        if not findings:
            print("None")
            continue

        for finding in findings:

            print(
                f"- {finding['label']}"
                f" | {finding['text']}"
                f" | Confidence: {finding['score']:.3f}"
            )


if __name__ == "__main__":
    main()
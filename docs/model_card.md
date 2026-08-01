# PromptShield Model Card

## Model Overview

**Model Name**

gravitee-io/bert-small-pii-detection

**Model Type**

Pretrained BERT Token Classification Model

**Purpose**

The model detects Personally Identifiable Information (PII) in free-form text before it is shared with public AI systems.

PromptShield uses this pretrained model as its primary detection engine.

---

# Why This Model?

The project required an ML-first approach without training a custom model.

This model was selected because it:

- Detects common personally identifiable information.
- Requires no additional model training.
- Runs locally without paid APIs.
- Produces character offsets suitable for highlighting and redaction.
- Integrates easily with Hugging Face Transformers.

---

# Detection Approach

PromptShield follows an ML-first architecture.

The pretrained model performs the primary detection.

Supporting deterministic rules extend the model for structured identifiers that are difficult for general-purpose NER models to detect consistently.

Examples include:

- API Keys
- Access Tokens
- Employee IDs
- Volunteer IDs
- Client IDs
- Confidentiality markers

The supporting rules supplement the model rather than replacing it.

---

# Supported Challenge Categories

PromptShield currently supports five challenge categories.

| Category | Detection Method |
|-----------|------------------|
| Names & Contact Information | ML |
| Government / Financial Identifiers | ML |
| Passwords / API Keys / Credentials | ML + Supporting Rules |
| Employee / Client / Volunteer Information | ML + Supporting Rules |
| Confidential Organizational / Project Information | ML + Supporting Rules |

Medical or clinical information is intentionally outside the current project scope.

---

# Strengths

- ML-first detection pipeline
- Runs locally
- No paid AI services required
- Character-level highlighting
- Automatic redaction
- Explainable detections
- Structured supporting rules for deterministic identifiers

---

# Known Limitations

The pretrained model occasionally produces semantic misclassifications.

Examples observed during evaluation include:

- Generic business phrases being classified as organizations.
- Fictional project codenames being classified as people.

PromptShield intentionally presents these detections for user review rather than silently suppressing them.

Human review is always recommended before sharing sensitive information.

---

# Evaluation Summary

# Evaluation Summary

PromptShield was evaluated using ten synthetic test cases covering all implemented challenge categories.

Evaluation was performed at the entity level.

| Metric | Value |
|----------|------:|
| Total Test Cases | 10 |
| Total Expected Entities | 19 |
| True Positives | 19 |
| False Positives | 1 |
| False Negatives | 0 |
| Precision | 95.0% |
| Recall | 100.0% |
| F1 Score | 97.4% |

One observed false positive occurred when the pretrained model classified the generic business phrase **"sprint planning"** as an organization.

No complete misses were observed for the supported challenge categories.

---

# Future Improvements

Potential future work includes:

- Medical information detection
- Multilingual support
- Browser extension
- Context-aware confidence calibration
- Improved confidential document classification
- User-configurable detection rules
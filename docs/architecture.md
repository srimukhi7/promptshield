# Architecture Overview

> Fill this in **after building**, not before. This documents how your app was actually implemented.
> Compare this against your `planning/planning.md` to reflect on where your plan changed and why.

---

# Final Tech Stack

**Framework**

- Streamlit

**Programming Language**

- Python 3.13

**Machine Learning Model**

- Hugging Face `gravitee-io/bert-small-pii-detection`

**Key Libraries**

- Transformers
- PyTorch
- Streamlit
- Regular Expressions (Python `re` module)

### Changes from the Original Plan

The original plan proposed using a pretrained Hugging Face model combined with regular expressions. During implementation, the architecture evolved into an ML-first pipeline supplemented with lightweight supporting detection rules for structured identifiers such as API keys, access tokens, employee IDs, volunteer IDs, client IDs, and confidentiality markers.

No custom model training or paid AI services were required.

---

# Folder Structure

```text
src/
├── app.py                 # Streamlit user interface
├── analyzer.py            # Coordinates the complete analysis pipeline
├── detector.py            # ML-first sensitive information detection
├── supporting_rules.py    # Structured detection rules for IDs, API keys and confidentiality
├── redactor.py            # Generates the redacted output
└── demo.py                # Local testing/demo script
```

### Component Responsibilities

**app.py**

Provides the Streamlit interface, displays findings, highlights sensitive information, calculates the privacy summary, and presents the redacted text.

**analyzer.py**

Coordinates the complete workflow by executing detection, redaction, and heuristic risk scoring before returning a unified analysis report.

**detector.py**

Runs the pretrained Hugging Face model and performs ML-based entity detection.

**supporting_rules.py**

Provides deterministic detection rules for structured identifiers that are difficult for a general-purpose NER model to detect consistently.

**redactor.py**

Replaces detected sensitive values with descriptive placeholders while preserving surrounding text.

**demo.py**

Used during development to test the detection pipeline before the Streamlit interface was completed.

---

# Detection Design

PromptShield follows an **ML-first detection architecture**.

The pretrained Hugging Face model performs the primary detection for:

- Names
- Email addresses
- Phone numbers
- Government identifiers
- Financial identifiers
- Organizations
- Passwords

Supporting detection rules extend the ML model for structured identifiers including:

- API Keys
- Access Tokens
- Employee IDs
- Volunteer IDs
- Client IDs
- Confidentiality markers

Supported challenge categories:

- Names & Contact Information
- Government or Financial Identifiers
- Passwords, API Keys & Credentials
- Employee, Client & Volunteer Information
- Confidential Organizational / Project Information

### Reducing False Positives

Several techniques were used to reduce false positives:

- Confidence threshold filtering for ML predictions.
- Unsupported ML labels are discarded.
- Supporting rules require highly specific patterns (for example `EMP-4821`, `sk-test-...`) rather than generic keywords.
- Confidential information is detected only when explicit phrases such as "STRICTLY CONFIDENTIAL" or "DO NOT DISTRIBUTE" are present.
- Character offsets from the original text are preserved to avoid incorrect redaction.

### Detection Pipeline

1. User submits text.
2. The pretrained ML model performs entity detection.
3. Supporting detection rules identify structured identifiers.
4. ML findings and supporting-rule findings are merged.
5. Duplicate overlaps are removed.
6. A heuristic privacy risk score is calculated.
7. Sensitive text is highlighted.
8. A redacted version is generated.

---

# AI Integration Design

PromptShield uses a pretrained Hugging Face token-classification model running locally within the application.

Model:

- `gravitee-io/bert-small-pii-detection`

The application does not send user text to paid external AI services such as OpenAI, Gemini, or Claude for detection.

Instead:

- The model runs locally through the Hugging Face Transformers library.
- Supporting detection rules execute locally using Python regular expressions.

This approach minimizes privacy risks because user prompts are processed locally rather than transmitted to external APIs.

No prompt engineering was required because PromptShield uses a pretrained token-classification model instead of an LLM prompt.

---

# What Changed From the Plan

The original planning document proposed using a pretrained Hugging Face model together with regular expressions.

During implementation, the project evolved into a modular architecture with clearly separated responsibilities:

- `detector.py` performs ML-based detection.
- `supporting_rules.py` supplements the model using deterministic rules.
- `analyzer.py` coordinates the complete workflow.
- `redactor.py` generates the safer version of the text.
- `app.py` contains only presentation logic.

Supporting rules were expanded to detect structured identifiers such as API keys, access tokens, employee IDs, volunteer IDs, client IDs, and explicit confidentiality markers because these patterns were not always detected consistently by the pretrained model.

Medical information detection was intentionally excluded after evaluation because the selected pretrained model is optimized for PII detection rather than clinical natural language processing. This decision prioritized reliable performance on five challenge categories over broader but less accurate detection.
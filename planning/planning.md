# Planning Document

> Complete this document **before writing any code**. This is part of the evaluation.
> Your intent here will be compared against what you actually built in `docs/architecture.md`.

---

## Tech Stack

**Framework / Language:**

Python with Streamlit.

I chose Python because it has strong support for machine-learning models and
text processing. Streamlit will allow me to build and deploy a simple web
application quickly without creating separate frontend and backend projects.

**Key Libraries:**

- `streamlit` for the user interface
- `transformers` and `torch` for running the pretrained model
- `pytest` for testing
- Python regular expressions for limited supporting validation

**Detection Approach / AI Provider (if any):**

The main detection engine will use the pretrained
`gravitee-io/bert-small-pii-detection` model.

The model will perform the primary sensitive-information detection. Regular
expressions and contextual rules will only support the model for structured
formats such as API keys, employee IDs, and credit-card validation.

The model will run within the application. No paid AI API will be used, and
user text will not be intentionally stored.

The final solution will be tested using at least 10 fictional labelled cases,
including safe examples. Precision, recall, and F1 will be calculated for the
completed detection pipeline.

---

## Detection Categories

| Category | Detect? | Planned technique |
|----------|---------|-------------------|
| Names & contact information | Yes | ML detection for names, email addresses, phone numbers, and locations |
| Government or financial identifiers | Yes | ML detection for SSNs, passports, credit cards, bank details, and related identifiers |
| Passwords, API keys or credentials | Yes | ML detection for passwords, supported by limited patterns for API keys and tokens |
| Medical or sensitive personal information | No, unless time permits | Conservative model and context-based detection |
| Employee, client or volunteer information | Yes | ML-detected names, organizations, and job titles combined with role context and identifier patterns |
| Confidential organizational or project information | No, unless time permits | Strong confidentiality keywords combined with model-detected organizations |

---

## Phases & Priorities

| Phase | Target Dates | Goals |
|-------|-------------|-------|
| 1 | July 29–30 | Set up the Python project, load the ML model, and confirm that it detects sensitive text |
| 2 | July 31–August 1 | Build the Streamlit interface, highlighting, explanations, review process, and redaction |
| 3 | August 2–3 | Create test cases, calculate evaluation metrics, deploy the application, finish documentation, and record the walkthrough |

The core detection and redaction workflow will be completed before optional
features or visual polish.

---

## What I'll Cut If Time Is Short

I will first remove optional medical and confidential-project detection,
advanced risk scoring, custom rules, multilingual support, and extra visual
features.

I will not cut the four required categories, ML-based detection, highlighting,
explanations, redaction, safe test cases, deployment, documentation, or the
walkthrough video.

---

## Open Questions / Risks

- The model may miss uncommon sensitive-information formats.
- The model may occasionally flag harmless text.
- Employee and volunteer IDs may need limited supporting patterns.
- The deployed application may have a slow first load while the model starts.
- A small synthetic evaluation set will not represent every real-world input.
- All examples must remain fictional and must not contain real sensitive data.
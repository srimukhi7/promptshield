# Reflection

> **Fill this in before submission.**

## What I Built

I built **PromptShield**, a privacy auditing application that detects and redacts sensitive information before users share text with public AI systems.

The application supports the following challenge categories:

- ✅ Names & Contact Information
- ✅ Government or Financial Identifiers
- ✅ Passwords, API Keys & Credentials
- ✅ Employee, Client & Volunteer Information
- ✅ Confidential Organizational / Project Information

The application uses the pretrained Hugging Face model `gravitee-io/bert-small-pii-detection` as the primary detection engine. Supporting detection rules were added for structured identifiers such as API keys, access tokens, employee IDs, volunteer IDs, client IDs, and confidentiality markers.

Completed features include:

- Highlighting detected sensitive information
- Detailed explanations for each finding
- Automatic redaction using descriptive placeholders
- Privacy risk scoring
- Live Streamlit web application
- 10 synthetic evaluation test cases

Known limitations:

- Fictional project codenames may occasionally be classified as PERSON entities by the pretrained model.
- Generic business phrases (for example, "sprint planning") may occasionally be classified as ORGANIZATION entities, resulting in isolated false positives.
- Medical information detection is not currently supported because the selected pretrained model focuses on PII rather than clinical information.

---

## What I'd Do Differently

With more time, I would:

- Add medical information detection using a healthcare-specific NLP model.
- Improve confidential project detection using contextual classification instead of keyword matching.
- Reduce false positives through additional validation and confidence calibration.
- Add multilingual support.
- Build a browser extension that scans prompts directly before submission to AI tools.
- Allow users to create custom detection rules for organization-specific sensitive information.
- Export privacy reports and audit summaries.

---

## AI Tools Used

AI-assisted development was used throughout the project.

ChatGPT was used to:

- Brainstorm the overall system architecture.
- Design the ML-first detection pipeline.
- Refactor the application into modular components.
- Improve code quality and documentation.
- Generate synthetic evaluation test cases.
- Review implementation decisions and identify edge cases.
- Draft technical documentation.

All generated code and documentation were reviewed, tested, and modified during implementation before being included in the final project.
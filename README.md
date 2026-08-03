[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/kIswDrNZ)
# CDF Shadow AI Hackathon
**Live URL:** <https://promptshield-srimukhi.streamlit.app>

Welcome! This is your personal repository for the CDF Shadow AI Hackathon. The problem statement is included in this repo - read it carefully before you start.

## 🛡 Project Summary

PromptShield is an ML-powered privacy auditing application that detects and redacts sensitive information before users share text with public AI tools.

The application uses the pretrained Hugging Face model `gravitee-io/bert-small-pii-detection` together with lightweight supporting detection rules to identify:

- Names & Contact Information
- Government or Financial Identifiers
- Passwords, API Keys & Credentials
- Employee, Client & Volunteer Information
- Confidential Organizational / Project Information

PromptShield highlights sensitive information, explains why it may be risky, generates a privacy risk score, and creates a safer redacted version of the original text.

---

## 📋 Problem Statement
See [`problem_statement.md`](./problem_statement.md) for the full brief.

---

## 🗂️ Repo Structure
```
├── README.md               # This file - live URL and submission checklist
├── problem_statement.md    # Full hackathon brief
├── planning/
│   └── planning.md         # Your planning document (fill this out first)
├── src/                    # Your application code goes here
└── docs/
    ├── walkthrough.md      # Link to your 5-minute walkthrough video
    ├── architecture.md     # Your architecture overview and detection design
    └── reflection.md       # What you built, tradeoffs, AI tools used
```

---

## 🚀 Getting Started

1. **Read the problem statement** - [`problem_statement.md`](./problem_statement.md)
2. **Fill out your planning document** - [`planning/planning.md`](./planning/planning.md) before writing any code
3. **Build your solution** inside the `src/` directory
4. **Deploy** to Vercel, Netlify, Streamlit Cloud, Railway, or similar - set any API keys as environment variables in your hosting dashboard, never in the repo
5. **Update this README** with your live URL and reflections before the deadline

---

## 📦 Submission Checklist

Push to your designated repository before the **5-day deadline**. Your repo state at the deadline is your submission.

- [x] Live deployment URL added at the top of this README - **mandatory**
- [x] Completed planning document in `planning/planning.md`
- [x] Working application in `src/`
- [x] At least **10 test cases** (including safe examples that stay unchanged) documented in `docs/` or `planning/`
- [x] `docs/walkthrough.md` - walkthrough video link filled in
- [x] `docs/architecture.md` - architecture overview and detection design filled in
- [x] `docs/reflection.md` - reflection filled in
- [x] Clean commit history - see note below

---

## 🎥 Video Requirements

Your 5-minute walkthrough video is mandatory. It must cover:

- What you built and why
- How your detection works end to end (patterns, keyword lists, validation)
- A risky example being detected, explained, and safely redacted
- A safe example being correctly left unchanged (no over-redaction)
- Which categories you detect and why each is risky
- How you used AI and what value it adds
- Known limitations and what you would improve next

Link your video in `docs/walkthrough.md` before the deadline.

---

## 📝 A Note on Commit History

Your git commit history is part of the evaluation. Here is what a clean history looks like:

- **Commit regularly** - at least once per meaningful chunk of work (e.g. "Add email and phone detectors", "Build highlight preview", "Add redaction engine")
- **Write descriptive messages** - not "fix", "update", or "asdf". A good message tells someone what changed and why
- **Do not squash everything into one commit** at the end - we should be able to follow your progress through the history
- **Do not commit API keys, `.env` files, or `node_modules`** - use `.gitignore`

Think of your commit history as a log of how you think and work, not just a save button.

---

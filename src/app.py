"""
app.py

Streamlit interface for PromptShield:
an ML-powered privacy auditor for text intended for public AI tools.
"""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from analyzer import analyze_text
from detector import load_detector


st.set_page_config(
    page_title="PromptShield",
    page_icon="🛡️",
    layout="wide",
)


ENTITY_DETAILS = {
    "PERSON": {
        "name": "Person Name",
        "icon": "👤",
        "category": "Names & Contact Information",
        "explanation": (
            "A person's name may identify them, especially when combined "
            "with contact, employment, financial, or organizational data."
        ),
    },
    "EMAIL_ADDRESS": {
        "name": "Email Address",
        "icon": "📧",
        "category": "Names & Contact Information",
        "explanation": (
            "Email addresses directly identify or provide a way to contact "
            "an individual and may expose workplace or account details."
        ),
    },
    "PHONE_NUMBER": {
        "name": "Phone Number",
        "icon": "📱",
        "category": "Names & Contact Information",
        "explanation": (
            "Phone numbers can expose personal contact details and may be "
            "used for unwanted contact or social-engineering attempts."
        ),
    },
    "LOCATION": {
        "name": "Location",
        "icon": "📍",
        "category": "Names & Contact Information",
        "explanation": (
            "A specific location may reveal where a person lives, works, "
            "studies, or can be found."
        ),
    },
    "ORGANIZATION": {
        "name": "Organization",
        "icon": "🏢",
        "category": "Confidential Organizational or Project Information",
        "explanation": (
            "An organization name may expose business relationships, "
            "clients, employers, projects, or internal activities."
        ),
    },
    "TITLE": {
        "name": "Job Title",
        "icon": "💼",
        "category": "Employee, Client or Volunteer Information",
        "explanation": (
            "A job title may reveal an individual's role, authority, "
            "responsibilities, or organizational access."
        ),
    },
    "PASSWORD": {
        "name": "Password",
        "icon": "🔑",
        "category": "Passwords, API Keys or Credentials",
        "explanation": (
            "Passwords provide direct account access and should never be "
            "shared with a public AI system."
        ),
    },
    "API_KEY": {
        "name": "API Key",
        "icon": "🗝️",
        "category": "Passwords, API Keys or Credentials",
        "explanation": (
            "API keys may grant access to services, private data, billing, "
            "or production systems."
        ),
    },
    "ACCESS_TOKEN": {
        "name": "Access Token",
        "icon": "🎟️",
        "category": "Passwords, API Keys or Credentials",
        "explanation": (
            "Access tokens may allow temporary or persistent access to "
            "accounts, applications, or protected resources."
        ),
    },
    "CREDIT_CARD": {
        "name": "Credit Card Number",
        "icon": "💳",
        "category": "Government or Financial Identifiers",
        "explanation": (
            "Credit-card information may enable unauthorized purchases, "
            "financial fraud, or identity theft."
        ),
    },
    "FINANCIAL": {
        "name": "Financial Information",
        "icon": "💰",
        "category": "Government or Financial Identifiers",
        "explanation": (
            "Financial information may reveal account ownership, balances, "
            "transactions, or other private financial activity."
        ),
    },
    "IBAN_CODE": {
        "name": "IBAN",
        "icon": "🏦",
        "category": "Government or Financial Identifiers",
        "explanation": (
            "An IBAN identifies a bank account and should not be exposed "
            "to an untrusted or public AI service."
        ),
    },
    "US_BANK_NUMBER": {
        "name": "Bank Account Number",
        "icon": "🏦",
        "category": "Government or Financial Identifiers",
        "explanation": (
            "Bank-account details may be abused for fraud, unauthorized "
            "transactions, or identity theft."
        ),
    },
    "US_DRIVER_LICENSE": {
        "name": "Driver's License Number",
        "icon": "🪪",
        "category": "Government or Financial Identifiers",
        "explanation": (
            "A driver's license number is a sensitive government identity "
            "identifier used for verification."
        ),
    },
    "US_ITIN": {
        "name": "Taxpayer Identification Number",
        "icon": "🧾",
        "category": "Government or Financial Identifiers",
        "explanation": (
            "An ITIN is a sensitive tax identifier and should not be shared "
            "with a public AI platform."
        ),
    },
    "US_PASSPORT": {
        "name": "Passport Number",
        "icon": "🛂",
        "category": "Government or Financial Identifiers",
        "explanation": (
            "A passport number is a government identity-document identifier "
            "that may be used for identity fraud."
        ),
    },
    "US_SSN": {
        "name": "Social Security Number",
        "icon": "🆔",
        "category": "Government or Financial Identifiers",
        "explanation": (
            "Social Security numbers uniquely identify individuals and may "
            "enable identity theft, fraud, or unauthorized account access."
        ),
    },
    "IP_ADDRESS": {
        "name": "IP Address",
        "icon": "🌐",
        "category": "Passwords, API Keys or Credentials",
        "explanation": (
            "An IP address may reveal network infrastructure, approximate "
            "location, or internal system information."
        ),
    },
    "EMPLOYEE_ID": {
        "name": "Employee ID",
        "icon": "🧑‍💼",
        "category": "Employee, Client or Volunteer Information",
        "explanation": (
            "Employee identifiers may expose internal personnel records or "
            "organizational relationships."
        ),
    },
    "VOLUNTEER_ID": {
        "name": "Volunteer ID",
        "icon": "🤝",
        "category": "Employee, Client or Volunteer Information",
        "explanation": (
            "Volunteer identifiers may expose internal records, assignments, "
            "or personal organizational relationships."
        ),
    },
    "CLIENT_ID": {
        "name": "Client ID",
        "icon": "🧑‍🤝‍🧑",
        "category": "Employee, Client or Volunteer Information",
        "explanation": (
            "Client identifiers may expose customer records, contracts, "
            "accounts, or confidential business relationships."
        ),
    },
    "CONFIDENTIAL_INFORMATION": {
        "name": "Confidential Information Marker",
        "icon": "🔒",
        "category": "Confidential Organizational or Project Information",
        "explanation": (
            "Explicit confidentiality language signals that the surrounding "
            "content may contain internal plans, projects, acquisitions, "
            "roadmaps, or restricted organizational information."
        ),
    },
}


@st.cache_resource
def get_detector():
    """Load and cache the ML model so it is reused across scans."""
    return load_detector()


def get_entity_details(label: str) -> dict[str, str]:
    """Return user-friendly metadata for an entity label."""
    return ENTITY_DETAILS.get(
        label,
        {
            "name": label.replace("_", " ").title(),
            "icon": "⚠️",
            "category": "Sensitive Information",
            "explanation": (
                "This information may be sensitive. Review it carefully "
                "before sharing it with a public AI system."
            ),
        },
    )


def build_highlighted_text(
    text: str,
    findings: list[dict[str, Any]],
) -> str:
    """Return safely escaped HTML with detected spans highlighted."""
    if not findings:
        safe_text = html.escape(text).replace("\n", "<br>")
        return f"<div class='highlight-box'>{safe_text}</div>"

    parts: list[str] = []
    cursor = 0

    for finding in sorted(
        findings,
        key=lambda item: int(item["start"]),
    ):
        start = int(finding["start"])
        end = int(finding["end"])
        details = get_entity_details(str(finding["label"]))

        parts.append(html.escape(text[cursor:start]))

        highlighted_value = html.escape(text[start:end])
        tooltip = html.escape(details["name"])

        parts.append(
            f"<mark title='{tooltip}'>{highlighted_value}</mark>"
        )

        cursor = end

    parts.append(html.escape(text[cursor:]))

    highlighted = "".join(parts).replace("\n", "<br>")

    return f"<div class='highlight-box'>{highlighted}</div>"


def display_finding(finding: dict[str, Any]) -> None:
    """Display one finding with its category and explanation."""
    label = str(finding["label"])
    details = get_entity_details(label)
    source = str(finding.get("source", "ml"))

    with st.container(border=True):
        st.markdown(
            f"### {details['icon']} {details['name']}"
        )

        st.caption(details["category"])
        st.markdown(f"**Detected value:** `{finding['text']}`")

        if source == "ml":
            confidence = float(finding["score"]) * 100
            st.progress(min(float(finding["score"]), 1.0))
            st.caption(
                f"Detection method: ML model · Confidence: {confidence:.1f}%"
            )
        else:
            st.caption(
                "Detection method: Supporting structured/context rule"
            )

        st.markdown("**Why might this be risky?**")
        st.write(details["explanation"])


def display_risk_summary(report: dict[str, Any]) -> None:
    """Display the risk level and summary metrics."""
    risk_level = str(report["risk_level"])

    if risk_level == "HIGH":
        st.error("🔴 High privacy risk")
    elif risk_level == "MEDIUM":
        st.warning("🟡 Medium privacy risk")
    else:
        st.success("🟢 Low privacy risk")

    metric_one, metric_two = st.columns(2)

    metric_one.metric(
        "Risk score",
        f"{report['risk_score']}/100",
    )

    metric_two.metric(
        "Sensitive findings",
        report["entity_count"],
    )

    st.caption(
        "The risk score is a simple heuristic based on detected entity "
        "types. It is not a formal security or compliance assessment."
    )


st.markdown(
    """
    <style>
        .block-container {
            max-width: 1200px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        .hero-subtitle {
            font-size: 1.05rem;
            color: #9ca3af;
            margin-bottom: 1.5rem;
        }

        .privacy-note {
            padding: 0.9rem 1rem;
            border: 1px solid rgba(120, 120, 120, 0.3);
            border-radius: 0.6rem;
            margin-bottom: 1.25rem;
        }

        .highlight-box {
            padding: 1rem;
            border: 1px solid rgba(120, 120, 120, 0.35);
            border-radius: 0.6rem;
            line-height: 1.8;
            overflow-wrap: anywhere;
        }

        mark {
            padding: 0.15rem 0.3rem;
            border-radius: 0.3rem;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛡️ PromptShield")

st.markdown(
    "<div class='hero-subtitle'>"
    "Scan before you share. Detect and redact sensitive information "
    "before sending text to a public AI tool."
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="privacy-note">
        🔒 <strong>Privacy design:</strong> Text is processed within the
        application and is not intentionally stored in a database or sent
        to a paid external AI inference API.
    </div>
    """,
    unsafe_allow_html=True,
)

detector = get_detector()

sample_text = (
    "Employee Maya Patel has employee ID EMP-4821. "
    "Contact her at maya.patel@example.com."
)

text = st.text_area(
    "Paste the text you want to analyze",
    value="",
    height=200,
    placeholder=sample_text,
)

scan_clicked = st.button(
    "🔍 Scan Prompt",
    type="primary",
)

if scan_clicked:
    if not text.strip():
        st.warning("Please enter text before starting the scan.")
        st.stop()

    with st.spinner("Scanning text with the privacy model..."):
        report = analyze_text(text, detector)

    st.divider()

    summary_column, preview_column = st.columns(
        [0.35, 0.65],
        gap="large",
    )

    with summary_column:
        st.subheader("Privacy Summary")
        display_risk_summary(report)

    with preview_column:
        st.subheader("Highlighted Review")

        highlighted_text = build_highlighted_text(
            report["original_text"],
            report["findings"],
        )

        st.markdown(
            highlighted_text,
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("Detected Information")

    if not report["findings"]:
        st.success(
            "No supported sensitive information was detected. "
            "The text remains unchanged."
        )
    else:
        finding_columns = st.columns(2)

        for index, finding in enumerate(report["findings"]):
            with finding_columns[index % 2]:
                display_finding(finding)

    st.divider()
    st.subheader("Safer Version")

    st.caption(
        "Review the redacted version before copying it into another system."
    )

    st.code(
        report["redacted_text"],
        language="text",
    )

    if report["findings"]:
        st.success(
            "Sensitive values were replaced with descriptive placeholders."
        )
    else:
        st.info(
            "No changes were made because no supported sensitive "
            "information was detected."
        )

st.divider()

st.caption(
    "PromptShield uses the pretrained "
    "`gravitee-io/bert-small-pii-detection` model together with narrowly "
    "scoped supporting rules. Automated detection can make mistakes, so "
    "users should always perform a final human review."
)
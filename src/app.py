"""
app.py

Streamlit application for the Shadow AI Privacy Auditor.
"""

from __future__ import annotations

import streamlit as st

from analyzer import analyze_text
from detector import load_detector


st.set_page_config(
    page_title="Shadow AI Privacy Auditor",
    page_icon="🛡",
    layout="wide",
)


@st.cache_resource
def get_detector():
    """Load the ML model only once."""
    return load_detector()


detector = get_detector()

st.title("🛡 Shadow AI Privacy Auditor")

st.write(
    "Detect sensitive information before sharing prompts with public AI tools."
)

text = st.text_area(
    "Paste the text you want to analyze",
    height=220,
    placeholder="Paste your prompt here...",
)

if st.button("🔍 Scan Prompt", type="primary"):

    if not text.strip():
        st.warning("Please enter some text first.")
        st.stop()

    report = analyze_text(
        text,
        detector,
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Privacy Summary")

        risk = report["risk_level"]

        if risk == "HIGH":
            st.error(f"🔴 {risk}")

        elif risk == "MEDIUM":
            st.warning(f"🟡 {risk}")

        else:
            st.success(f"🟢 {risk}")

        st.metric(
            "Risk Score",
            f"{report['risk_score']}/100",
        )

        st.metric(
            "Sensitive Findings",
            report["entity_count"],
        )

    with col2:

        st.subheader("Detected Information")

        if not report["findings"]:
            st.success("No sensitive information detected.")

        else:

            for finding in report["findings"]:

                st.write(
                    f"**{finding['label']}**"
                )

                st.write(
                    f"Value: `{finding['text']}`"
                )

                st.write(
                    f"Confidence: {finding['score']:.3f}"
                )

                st.divider()

    st.subheader("Redacted Text")

    st.code(
        report["redacted_text"],
        language="text",
    )
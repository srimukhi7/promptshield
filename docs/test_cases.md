# PromptShield Test Cases

## Overview

The following fictional test cases were created to evaluate PromptShield's ability to detect, explain, highlight, and redact sensitive information before it is shared with public AI systems.

PromptShield uses a pretrained ML model (`gravitee-io/bert-small-pii-detection`) as the primary detection engine, supplemented with deterministic supporting rules for structured identifiers such as API keys, employee IDs, and confidentiality markers.

Only synthetic data was used during evaluation.

---

# Test Case 1 – Names & Contact Information

## Input

Employee Maya Patel can be reached at maya.patel@example.com or call 415-555-0136.

## Expected Detection

- PERSON
- EMAIL_ADDRESS
- PHONE_NUMBER

## Actual Detection

- PERSON ✅
- EMAIL_ADDRESS ✅
- PHONE_NUMBER ✅

## Result

**PASS ✅**

---

# Test Case 2 – Government Identifier (SSN)

## Input

The fictional employee's SSN is 123-45-6789.

## Expected Detection

- US_SSN

## Actual Detection

- US_SSN ✅

## Result

**PASS ✅**

---

# Test Case 3 – Financial Identifier (Credit Card)

## Input

Customer Sarah Johnson provided credit card number 4111 1111 1111 1111.

## Expected Detection

- PERSON
- CREDIT_CARD

## Actual Detection

- PERSON ✅
- CREDIT_CARD ✅

## Result

**PASS ✅**

---

# Test Case 4 – Passport

## Input

Traveler Daniel Kim submitted passport number 123456789 during the fictional visa application.

## Expected Detection

- PERSON
- US_PASSPORT

## Actual Detection

- PERSON ✅
- US_PASSPORT ✅

## Result

**PASS ✅**

---

# Test Case 5 – API Key

## Input

Temporary API key:

sk-test-4f92a8d71c6b3e50

## Expected Detection

- API_KEY

## Actual Detection

- API_KEY ✅

## Result

**PASS ✅**

---

# Test Case 6 – Access Token

## Input

Access token:

abcdef1234567890xyz

## Expected Detection

- ACCESS_TOKEN

## Actual Detection

- ACCESS_TOKEN ✅

## Result

**PASS ✅**

---

# Test Case 7 – Employee Information

## Input

Employee Maya Patel has employee ID EMP-4821.

## Expected Detection

- PERSON
- EMPLOYEE_ID

## Actual Detection

- PERSON ✅
- EMPLOYEE_ID ✅

## Result

**PASS ✅**

---

# Test Case 8 – Volunteer & Client Information

## Input

Volunteer Elena Cruz has volunteer ID VOL-7284.

Client Daniel Lee has client ID CLI-7934.

## Expected Detection

- PERSON
- VOLUNTEER_ID
- PERSON
- CLIENT_ID

## Actual Detection

- PERSON ✅
- VOLUNTEER_ID ✅
- PERSON ✅
- CLIENT_ID ✅

## Result

**PASS ✅**

---

# Test Case 9 – Confidential Organizational Information

## Input

STRICTLY CONFIDENTIAL

Project Nightingale will acquire Blue Harbor Labs next quarter.

## Expected Detection

- CONFIDENTIAL_INFORMATION
- ORGANIZATION
- Project codename

## Actual Detection

- CONFIDENTIAL_INFORMATION ✅
- ORGANIZATION (Blue Harbor Labs) ✅
- Project Nightingale detected by the ML model but classified as PERSON ⚠️

## Result

**PARTIAL ⚠️**

### Notes

The confidentiality marker and organization were correctly detected.

The fictional project codename ("Project Nightingale") was identified by the pretrained model but classified as a PERSON entity rather than a project-specific entity.

The detected value was still highlighted and redacted correctly.

---

# Test Case 10 – Safe Example

## Input

The engineering team will meet tomorrow at 3:00 PM to discuss sprint planning.

## Expected Detection

No sensitive information.

## Actual Detection

- ORGANIZATION ("sprint planning") ⚠️

## Result

**PARTIAL ⚠️**

### Notes

The pretrained model incorrectly classified the generic business phrase "sprint planning" as an organization.

This isolated false positive has been intentionally documented rather than suppressed through hard-coded exception rules.

---

# Overall Evaluation

| Metric | Result |
|----------|--------|
| Total Test Cases | 10 |
| Passed Completely | 8 |
| Partial | 2 |
| Failed | 0 |

---

# Supported Challenge Categories

PromptShield currently supports the following challenge categories:

- ✅ Names & Contact Information
- ✅ Government or Financial Identifiers
- ✅ Passwords, API Keys & Credentials
- ✅ Employee, Client & Volunteer Information
- ✅ Confidential Organizational / Project Information

Medical or sensitive clinical information is intentionally outside the scope of the current implementation.

---

# Known Limitations

## 1. Project Codenames

The pretrained model may classify fictional project codenames (for example, "Project Nightingale") as PERSON entities instead of project-specific entities.

The application still highlights and redacts the detected value correctly.

---

## 2. Generic Business Phrases

Occasionally, the pretrained model may classify generic business phrases as organizations.

Example:

```
sprint planning
```

PromptShield intentionally presents these detections for user review instead of suppressing them with hard-coded exception lists.

This design favors transparency over hiding potentially sensitive detections.

---

# Conclusion

The evaluation demonstrates that PromptShield reliably detects and redacts structured personal, financial, credential, employee, and confidential organizational information while maintaining a low false-positive rate.

The primary remaining limitations stem from the semantic classification behavior of the pretrained model rather than the supporting detection pipeline.
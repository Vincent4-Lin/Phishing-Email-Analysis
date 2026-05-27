# Phishing Email Analysis Report

## Dataset

- Total emails analyzed: 12
- Dataset type: synthetic sample emails for portfolio demonstration
- Labels: phishing / legitimate

## Method

The detector assigns an explainable risk score using urgency terms, credential requests, financial terms, suspicious calls to action, URL presence, sender-domain mismatch, and lookalike-domain hints.

## Evaluation

- Accuracy: 100.0%
- Precision: 100.0%
- Recall: 100.0%
- True positives: 6
- False positives: 0
- False negatives: 0

## Prediction Distribution

- Predicted phishing: 6
- Predicted legitimate: 6

## Highest-Risk Samples

| ID | Actual | Predicted | Score | Sender | Subject | Main URL Domains |
|---|---|---|---:|---|---|---|
| 1 | phishing | phishing | 21 | security-alert@paypa1-login.com | Immediate action required for your account | paypa1-login.com |
| 3 | phishing | phishing | 15 | it-support@company-reset.net | Mailbox storage exceeded | company-reset.net |
| 7 | phishing | phishing | 12 | hr@careers-global-verify.com | Remote job offer confirmation | careers-global-verify.com |
| 9 | phishing | phishing | 12 | support@microsoft-security-check.com | Microsoft account password expires today | microsoft-security-check.com |
| 11 | phishing | phishing | 10 | invoice@vendor-payments.co | Overdue invoice escalation | vendor-payments.co |

## Analyst Notes

- The strongest phishing signals in this sample are urgency, credential requests, payment-related wording, and unfamiliar login domains.
- Rule-based scoring is explainable, but it may miss subtle phishing emails that avoid obvious pressure language.
- A realistic next version should use a larger public dataset and compare this rule-based baseline with a machine learning classifier.

## Next Research Steps

1. Add a public phishing email dataset and document data provenance.
2. Add URL reputation and domain-age features.
3. Compare rule-based detection with logistic regression or a transformer-based text classifier.
4. Write a short cyber threat intelligence brief for the top phishing patterns.

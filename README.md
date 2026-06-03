# Phishing Email Analysis

This project analyzes phishing email indicators using a small, transparent rule-based pipeline. It is designed as an early cybersecurity portfolio project for graduate school applications, with a focus on phishing, social engineering, suspicious links, sender/domain mismatch, and threat-intelligence style reporting.

## Why This Project Matters

Phishing remains one of the most common entry points for cyber incidents. This project demonstrates how language signals, sender information, and URL patterns can be combined to identify suspicious emails and produce a short security analysis report.

## Research Direction Fit

My current research direction is AI-assisted cybersecurity investigation and threat intelligence analysis for identifying attack patterns and improving incident response.

This project supports that direction by:

- Extracting observable phishing indicators such as sender traits, social engineering language, suspicious links, attachment risk, and possible attacker intent.
- Showing an explainable investigation workflow that can be used as a baseline before adding AI-assisted classification, summarization, or triage.
- Creating a practical starting point for future work where AI helps identify phishing patterns, organize evidence, and produce an initial incident triage summary.

For a fuller explanation, see [Research Direction Fit](docs/research-direction.md).

## Current Scope

The current dataset is synthetic and intentionally small. It is used to demonstrate the analysis workflow without exposing private email content.

The analysis checks for:

- Urgency and pressure language
- Credential or account-verification requests
- Financial or payment-related terms
- Suspicious URL patterns
- Sender domain and URL domain mismatch
- High-risk call-to-action phrasing

## Repository Structure

```text
phishing-email-analysis/
├── data/
│   └── sample_emails.csv
├── docs/
│   └── research-direction.md
├── reports/
│   └── analysis_report.md
│   └── threat-intelligence-brief-001.md
├── src/
│   └── analyze_phishing.py
├── .gitignore
├── github-profile-readme-template.md
├── technical-inventory.md
└── README.md
```

## How To Run

This project uses only the Python standard library.

```bash
python3 src/analyze_phishing.py
```

The script generates:

- `reports/analysis_report.md`
- `reports/scored_emails.csv`

## Example Research Question

How can lightweight linguistic and URL-based indicators help detect phishing emails, and where do rule-based methods fail compared with machine learning or human analyst review?

## Results Summary

The initial rule-based detector is meant to be explainable rather than perfect. Each score can be traced back to concrete indicators, making the output useful for analyst training, security awareness, and early-stage threat intelligence writing.

## Applicant Background

I am preparing for graduate study in cybersecurity and network security in Japan. My academic background is in English, and I am building a cybersecurity portfolio that connects language analysis, phishing, threat intelligence, and networking fundamentals.

- TOEIC: 955
- JLPT: N1
- Certification: Cisco CCNA
- Current focus: phishing email analysis, cyber threat intelligence, and network security fundamentals

## Next Steps

- Replace the synthetic sample with a public phishing corpus.
- Add benign emails from a public dataset for more realistic evaluation.
- Add feature extraction for URL age, domain reputation, and redirect chains.
- Compare the rule-based method with a basic machine learning classifier.
- Write a short English threat intelligence brief based on the highest-risk samples.
- Extend the project into an AI-assisted incident triage workflow that generates incident summaries, ATT&CK mappings, priority scores, and response recommendations.

## Applicant Note

This project connects my English-language analytical background with cybersecurity and networking foundations. It is an initial step toward research interests in phishing, social engineering, cyber threat intelligence, and network/security operations.

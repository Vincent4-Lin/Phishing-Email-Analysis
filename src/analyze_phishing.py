from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_emails.csv"
REPORT_DIR = ROOT / "reports"
REPORT_PATH = REPORT_DIR / "analysis_report.md"
SCORED_CSV_PATH = REPORT_DIR / "scored_emails.csv"

URL_RE = re.compile(r"https?://[^\s)>\"]+")

URGENCY_TERMS = {
    "urgent",
    "immediate",
    "immediately",
    "today",
    "within 24 hours",
    "final notice",
    "disabled",
    "suspension",
    "expires",
    "limited",
}

CREDENTIAL_TERMS = {
    "password",
    "username",
    "credentials",
    "verify",
    "confirm",
    "login",
    "identity",
    "account",
}

FINANCIAL_TERMS = {
    "payment",
    "bank",
    "invoice",
    "fee",
    "scholarship",
    "passport",
    "overdue",
}

CALL_TO_ACTION_TERMS = {
    "click",
    "visit",
    "submit",
    "enter",
    "open",
    "confirm",
    "verify",
}


def normalize(text: str) -> str:
    return text.lower().strip()


def extract_urls(text: str) -> list[str]:
    return URL_RE.findall(text)


def domain_from_email(sender: str) -> str:
    if "@" not in sender:
        return ""
    return sender.split("@", 1)[1].lower()


def domain_from_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower().removeprefix("www.")


def count_terms(text: str, terms: set[str]) -> int:
    normalized = normalize(text)
    return sum(1 for term in terms if term in normalized)


def score_email(row: dict[str, str]) -> dict[str, str | int]:
    subject = row["subject"]
    body = row["body"]
    sender_domain = domain_from_email(row["sender"])
    urls = extract_urls(body)
    url_domains = [domain_from_url(url) for url in urls]
    combined_text = f"{subject} {body}"

    urgency = count_terms(combined_text, URGENCY_TERMS)
    credentials = count_terms(combined_text, CREDENTIAL_TERMS)
    financial = count_terms(combined_text, FINANCIAL_TERMS)
    calls_to_action = count_terms(combined_text, CALL_TO_ACTION_TERMS)
    url_count = len(urls)
    sender_url_mismatch = int(any(domain and domain != sender_domain for domain in url_domains))
    lookalike_hint = int(any(char.isdigit() for char in sender_domain))

    score = (
        urgency * 2
        + credentials * 2
        + financial
        + calls_to_action
        + url_count
        + sender_url_mismatch * 2
        + lookalike_hint * 2
    )

    predicted = "phishing" if score >= 7 else "legitimate"

    return {
        **row,
        "sender_domain": sender_domain,
        "url_domains": ";".join(url_domains) if url_domains else "-",
        "urgency_terms": urgency,
        "credential_terms": credentials,
        "financial_terms": financial,
        "call_to_action_terms": calls_to_action,
        "url_count": url_count,
        "sender_url_mismatch": sender_url_mismatch,
        "lookalike_hint": lookalike_hint,
        "risk_score": score,
        "predicted_label": predicted,
    }


def load_emails() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def evaluate(scored_rows: list[dict[str, str | int]]) -> dict[str, float | int]:
    total = len(scored_rows)
    correct = sum(1 for row in scored_rows if row["label"] == row["predicted_label"])
    true_positive = sum(
        1 for row in scored_rows if row["label"] == "phishing" and row["predicted_label"] == "phishing"
    )
    false_positive = sum(
        1 for row in scored_rows if row["label"] == "legitimate" and row["predicted_label"] == "phishing"
    )
    false_negative = sum(
        1 for row in scored_rows if row["label"] == "phishing" and row["predicted_label"] == "legitimate"
    )

    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    accuracy = correct / total if total else 0.0

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
    }


def write_scored_csv(scored_rows: list[dict[str, str | int]]) -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    fieldnames = list(scored_rows[0].keys())
    with SCORED_CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scored_rows)


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def write_report(scored_rows: list[dict[str, str | int]], metrics: dict[str, float | int]) -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    top_risks = sorted(scored_rows, key=lambda row: int(row["risk_score"]), reverse=True)[:5]
    prediction_counts = Counter(str(row["predicted_label"]) for row in scored_rows)

    lines = [
        "# Phishing Email Analysis Report",
        "",
        "## Dataset",
        "",
        f"- Total emails analyzed: {metrics['total']}",
        "- Dataset type: synthetic sample emails for portfolio demonstration",
        "- Labels: phishing / legitimate",
        "",
        "## Method",
        "",
        "The detector assigns an explainable risk score using urgency terms, credential requests, financial terms, suspicious calls to action, URL presence, sender-domain mismatch, and lookalike-domain hints.",
        "",
        "## Evaluation",
        "",
        f"- Accuracy: {format_percent(float(metrics['accuracy']))}",
        f"- Precision: {format_percent(float(metrics['precision']))}",
        f"- Recall: {format_percent(float(metrics['recall']))}",
        f"- True positives: {metrics['true_positive']}",
        f"- False positives: {metrics['false_positive']}",
        f"- False negatives: {metrics['false_negative']}",
        "",
        "## Prediction Distribution",
        "",
        f"- Predicted phishing: {prediction_counts.get('phishing', 0)}",
        f"- Predicted legitimate: {prediction_counts.get('legitimate', 0)}",
        "",
        "## Highest-Risk Samples",
        "",
        "| ID | Actual | Predicted | Score | Sender | Subject | Main URL Domains |",
        "|---|---|---|---:|---|---|---|",
    ]

    for row in top_risks:
        lines.append(
            f"| {row['id']} | {row['label']} | {row['predicted_label']} | {row['risk_score']} | "
            f"{row['sender']} | {row['subject']} | {row['url_domains']} |"
        )

    lines.extend(
        [
            "",
            "## Analyst Notes",
            "",
            "- The strongest phishing signals in this sample are urgency, credential requests, payment-related wording, and unfamiliar login domains.",
            "- Rule-based scoring is explainable, but it may miss subtle phishing emails that avoid obvious pressure language.",
            "- A realistic next version should use a larger public dataset and compare this rule-based baseline with a machine learning classifier.",
            "",
            "## Next Research Steps",
            "",
            "1. Add a public phishing email dataset and document data provenance.",
            "2. Add URL reputation and domain-age features.",
            "3. Compare rule-based detection with logistic regression or a transformer-based text classifier.",
            "4. Write a short cyber threat intelligence brief for the top phishing patterns.",
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = load_emails()
    scored_rows = [score_email(row) for row in rows]
    metrics = evaluate(scored_rows)
    write_scored_csv(scored_rows)
    write_report(scored_rows, metrics)
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {SCORED_CSV_PATH}")


if __name__ == "__main__":
    main()


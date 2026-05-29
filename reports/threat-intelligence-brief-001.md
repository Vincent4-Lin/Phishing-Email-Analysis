# Threat Intelligence Brief 001

## Title

Common Phishing Indicators in Synthetic Email Samples

## Summary

This brief reviews common phishing indicators found in a small synthetic email dataset. The samples show recurring social engineering patterns: urgent account warnings, credential-verification requests, payment or scholarship claims, and login links hosted on unfamiliar domains.

The dataset is not intended to represent real-world phishing volume or diversity. Its purpose is to demonstrate an analyst workflow: extract indicators, explain suspicious patterns, document limitations, and propose next research steps.

## Observed Indicators

| Indicator Type | Examples Observed | Risk Explanation |
|---|---|---|
| Urgency language | "Immediate action required", "within 24 hours", "expires today", "final notice" | Pressure reduces user verification time and increases click-through risk. |
| Credential requests | "Verify your password", "confirm your username and password", "enter your finance credentials" | Direct credential requests are high-risk when paired with external links. |
| Financial hooks | "Scholarship payment", "processing fee", "overdue invoice" | Payment language can trigger fast action from students or finance staff. |
| Suspicious domains | `paypa1-login.com`, `microsoft-security-check.com`, `vendor-payments.co` | Lookalike or unfamiliar domains can imitate trusted brands or business workflows. |
| Login links | External URLs embedded in account or payment messages | Login links should be verified against official domains before interaction. |

## Common Social Engineering Patterns

1. Account suspension pressure  
   The message claims the account will be limited, disabled, or suspended unless the recipient acts quickly.

2. Authority impersonation  
   The sender pretends to be IT support, a payment office, a large technology provider, or a scholarship administrator.

3. Reward or opportunity framing  
   The message offers a scholarship payment or remote job opportunity to create urgency and lower skepticism.

4. Credential collection  
   The message asks the recipient to verify identity, confirm a password, or enter credentials into an external portal.

## Defensive Recommendations

- Verify login links by manually visiting the official website instead of clicking email links.
- Treat password, payment, passport, or identity-verification requests as high risk.
- Check sender domains and URL domains for lookalike spelling, extra words, or unfamiliar top-level domains.
- Use security awareness training that includes language-based phishing indicators.
- For organizations, route suspicious messages to a reporting mailbox or ticketing workflow.

## Limitations

- The dataset is synthetic and small.
- The analysis uses rule-based scoring, so it may miss subtle phishing messages.
- No domain reputation, WHOIS, DNS, redirect-chain, or attachment analysis is included.
- The project does not yet compare against machine learning methods.

## Next Research Steps

1. Add a public phishing email dataset with documented provenance.
2. Compare rule-based indicators with a simple supervised classifier.
3. Add URL/domain features such as domain age, redirect count, and brand impersonation distance.
4. Write future briefs based on real public threat reports from vendors, CERTs, or security research teams.


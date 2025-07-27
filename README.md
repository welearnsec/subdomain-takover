# 🕵️ Subdomain Takeover Detector

This is a Python tool that detects **subdomain takeover vulnerabilities** by analyzing DNS records of inactive or misconfigured subdomains.

Subdomain takeover occurs when a DNS entry (usually a CNAME) points to a deprovisioned service (like an unclaimed GitHub page, Heroku app, S3 bucket, etc.) — allowing an attacker to **register the service and claim the subdomain**.

---

## ⚙️ Features

- Reads subdomains from a file
- Performs DNS resolution (A/CNAME)
- Matches known takeover signatures (e.g., GitHub, Heroku, AWS, etc.)
- Reports potential takeovers with provider hints (e.g., `unclaimed GitHub Pages`, `Heroku app not found`)
- Optional output to file

---

## 🧰 Requirements

- Python 3.x
- Modules:
  - `dnspython` → `pip install dnspython`
  - `requests`

Install them via:

```bash
pip install dnspython requests

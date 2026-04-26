
# Tokyo Train Alert – Train Delay Monitor

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> A Python automation script that periodically checks train delay status (e.g., Tokyo Metro) and sends email alerts when delays are detected.


---

## Features

- ⏱️ **Scheduled checks** – runs every 5 minutes (configurable).
- 📧 **Email alerts** – sends a notification when a delay occurs.
- 📝 **Logging** – writes all activity to a log file.
- 🔌 **Pluggable API** – easy to adapt for different train companies (Tokyo Metro, JR East, etc.).
- 🌐 **Command‑line interface** – simple to configure and run.

---

## Tech Stack

- **Language**: Python 3.10+
- **Scheduling**: `schedule` library
- **HTTP Requests**: `requests`
- **Email**: `smtplib` (Gmail SMTP)
- **Configuration**: environment variables

---

## Why I Built This

I wanted a reliable way to stay informed about train delays in Tokyo without constantly checking apps.

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- A Gmail account (or any SMTP server)
- API access to a train status source (e.g., public RSS feed, custom API)

### Clone and Install
```bash
git clone https://github.com/tayebmekati37-art/tokyo-train-alert.git
cd tokyo-train-alert
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

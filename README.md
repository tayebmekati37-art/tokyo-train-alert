# Tokyo Train Alert

A Python automation tool that monitors the Yamanote Line for delays using the official ODPT API and sends email alerts.

## Setup Instructions

### 1. Get an ODPT API Key
- Go to [ODPT Developer Portal](https://developer.odpt.org/)
- Register and create an application to obtain an API key (acl:consumerKey).

### 2. Gmail SMTP Setup
- If you use 2-factor authentication, create an **App Password**.
- If not, enable "Less secure app access" (not recommended). Prefer App Password.

### 3. Clone & Configure
```bash
git clone <repo>
cd tokyo-train-alert
cp .env.example .env
# Edit .env with your API key, email credentials, etc.
# 📈 Market Signals

A full-suite monitoring system for assessing market risk, generating alerts, and supporting strategic re-entry into the market. This repo supports retirement or long-term portfolios with both caution and opportunity signals.

---

## 🧠 Scripts Overview

### 🔹 `market_signal_monitor.py`
A command-line script that:
- Downloads VIX, S&P 500, and Treasury yields
- Evaluates risk conditions like:
  - Elevated VIX (> 20)
  - S&P 500 falling below its 200-day moving average
  - Yield curve inversion (10Y < 3M)
- Sends automated **email alerts** when signals are triggered

### 🔹 `reentry_monitor.py`
A command-line script that monitors for **market recovery**:
- ✅ VIX drops below 18
- ✅ S&P 500 recovers above 200-day MA
- ✅ Yield curve normalizes (10Y > 3M)

It prints a clear summary with emojis showing whether it's safe to begin **phased or full portfolio re-entry**.

### 🔹 `stagflation_signal_dashboard.py`
A **Streamlit-powered interactive dashboard** to visualize:
- VIX level
- S&P 500 vs 200-day MA
- Yield curve (10Y - 3M spread)

Displays a real-time defensive allocation recommendation based on how many risk signals are active.

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/vmharrel/market_signals.git
cd market_signals
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Copy the template:

```bash
cp .env.example .env
```

Fill in your `.env` file:

```
EMAIL_ADDRESS=you@example.com
EMAIL_PASSWORD=yourpassword
TO_EMAIL=recipient@example.com
```

---

## 🔁 Run Locally

### Risk Monitoring & Email Alerts
```bash
python market_signal_monitor.py
```

### Market Re-entry Signals
```bash
python reentry_monitor.py
```

### Streamlit Dashboard
```bash
streamlit run stagflation_signal_dashboard.py
```

---

## 🛠 GitHub Actions

The workflow (`.github/workflows/monitor.yml`) runs daily at noon UTC and:
- Evaluates risk (`market_signal_monitor.py`)
- Checks for re-entry signals (`reentry_monitor.py`)

Secrets are securely stored in GitHub → Settings → Secrets:
- `EMAIL_ADDRESS`
- `EMAIL_PASSWORD`
- `TO_EMAIL`

---

## 🌐 Streamlit Cloud Deployment

You can deploy the dashboard for free via [Streamlit Cloud](https://streamlit.io/cloud):
- Use `stagflation_signal_dashboard.py` as the main file
- Add secrets in "Advanced Settings" during app setup

---

## 📂 Files

- `.env.example` — Template for secrets
- `requirements.txt` — Project dependencies
- `.github/workflows/monitor.yml` — Daily automation via GitHub Actions

---

© 2025 | Designed for signal-based market allocation strategies and retirement portfolio protection.

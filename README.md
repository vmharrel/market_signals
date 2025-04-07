# Market Signals

A monitoring suite for market risk and recovery signals using:

- 📉 `market_signal_monitor.py` – Detects elevated risk conditions (VIX, yield curve, S&P trend) and emails alerts.
- 📊 `stagflation_signal_dashboard.py` – Interactive dashboard with real-time defensive allocation signals.
- 🔁 `reentry_monitor.py` – Checks for recovery signals for portfolio re-entry (VIX normalization, trend recovery, yield curve).

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/vmharrel/market_signals.git
   cd market_signals
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Run scripts manually or automate:
   ```bash
   python market_signal_monitor.py
   python reentry_monitor.py
   ```

## GitHub Actions

A GitHub Actions workflow runs daily at noon UTC to check for alerts.

## Dashboard

```bash
streamlit run stagflation_signal_dashboard.py
```

---
© 2025 | Built for monitoring economic risk & re-entry indicators.

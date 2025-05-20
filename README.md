# 📊 Harrell Family Market Signals Dashboard

A unified Streamlit dashboard for monitoring macroeconomic and portfolio-specific signals across nine strategic plans.

---

## 🧭 Included Strategic Plans

| Plan                              | Purpose                                                                 |
|-----------------------------------|-------------------------------------------------------------------------|
| 📑 Portfolio Enhancement Actions  | Reference guide with tactical portfolio actions by strategy             |
| 📊 Market Dashboard               | Combined signal table with visual strategy mapping                      |
| 📘 2025 Market Dynamics Plan      | Stagflation defense, CPI, VIX, 10Y yield, credit spreads                |
| 📙 Tax-Sensitive Defensive Plan   | Downshift after market breakdowns; tax harvesting and short duration    |
| 📗 Re-entry Plan                  | Phased return when conditions normalize (VIX, trend, CPI)               |
| 🇺🇸 U.S.A. Debt Crisis Plan        | Defend against Treasury selloff, USD drop, CDS widening                 |
| 🇨🇳 China Treasury Selloff Monitor| Monitor China’s divestment from Treasuries and USD weakening            |
| 🌍 Trade Regime Shift Tracker     | Tariffs, EM divergence, commodity trends, supply chain fragmentation    |
| 📐 50/30/20 Plan                  | Compares actual vs target allocation using uploadable CSV               |

---

## 📥 Upload Format for 50/30/20 Plan

Use this CSV format to compare your current allocation vs the 50/30/20 target:

```csv
Asset Class,Amount
Stocks,500000
Bonds,300000
Private,100000
```

---

## 🧪 Run Locally

```bash
pip install -r requirements.txt
streamlit run market_signals_dashboard.py
```

---

## 🚀 Deploy to Streamlit Cloud

1. Set main file: `market_signals_dashboard.py`
2. Upload `portfolio_enhancement_actions.html`
3. Add secrets:

```toml
FRED_API_KEY = "your_fred_api_key"
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
TO_EMAIL = "recipient@example.com"
```

---

## 🔁 GitHub Actions Workflows

### ✅ `.github/workflows/streamlit_deploy.yml`
- Deploys dashboard on every push to `main`
- Validates that it launches correctly in headless mode

### ✅ `.github/workflows/weekly_signal_report.yml`
- Sends a plain-text email report of all signal statuses every **Monday**
- Uses `weekly_report.py` to scan VIX, CPI, OAS, GDP, LEI, 10Y, DXY, CDS

---

## 🗂 Legacy Dashboards

Archived legacy files from earlier versions are stored in `/legacy/`

---

© 2025 | Harrell Family Financial Monitor | All rights reserved

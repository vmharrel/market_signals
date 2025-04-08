# 📊 Harrell Family Market Signals Dashboard

This unified Streamlit dashboard tracks all key signals outlined in the **2025 Market Dynamics Plan**, **Tax-Sensitive Defensive Plan**, and **Re-entry Plan** — all in one streamlined interface.

---

## 🚀 Features

- ✅ **Plan Selector**: Toggle between the 3 strategic plans in one dashboard
- 🧠 **Built-in Macroeconomic Signals**:
  - VIX, S&P 500 200-Day MA, Yield Curve
  - CPI (YoY Inflation)
  - High-Yield OAS (credit spreads)
  - Real GDP and Leading Economic Index (LEI)
- 🔁 **On-demand FRED data refresh**
- 🧭 **Clear plan-specific actions embedded into each signal**

---

## 🗺 Strategic Plan Modes

| Plan | Signals Tracked | Action Triggers |
|------|------------------|-----------------|
| 📘 2025 Market Dynamics Plan | VIX > 20, S&P < 200MA, Inverted Curve, CPI > 4%, OAS > 500bps | Begin rotating to real assets, floating-rate, short-duration bonds |
| 📙 Tax-Sensitive Defensive Plan | VIX > 25, LEI < 101, GDP < 0, >10% S&P drop | Tax-loss harvesting, rebalance IRAs, shift to short ETFs |
| 📗 Re-entry Plan | VIX < 18, S&P above MA, Yield Curve normalized, CPI < 3.5% | Phased or full re-entry into core allocation |

---

## 📦 Installation

```bash
git clone https://github.com/vmharrel/market_signals.git
cd market_signals
pip install -r requirements.txt
streamlit run market_signals_dashboard.py
```

---

## 🧪 Run Locally or Deploy

Use [Streamlit Cloud](https://streamlit.io/cloud) and set the main file path to:

```
market_signals_dashboard.py
```

Add this to your **Streamlit Secrets**:
```env
FRED_API_KEY=your_fred_api_key
```

---

## 🗂 Legacy Dashboards

Legacy one-off dashboards and CLI scripts are archived under:
```
/legacy/
```

These include older versions like:
- `reentry_monitor.py`
- `stagflation_signal_dashboard.py`

---

## 🔁 GitHub Actions Deployment

A GitHub Actions workflow is included that:
- Triggers on `dev → main` merges
- Installs dependencies
- Validates the Streamlit app

---

© 2025 | Harrell Family Market Signal Strategy

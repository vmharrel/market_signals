import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
import streamlit.components.v1 as components
from fredapi import Fred

from strategies import (
    plan_2025_dynamics,
    plan_tax_defensive,
    plan_reentry,
    plan_debt_crisis,
    plan_china_selloff,
    plan_trade_shift,
    plan_50_30_20,
    market_dashboard,
    enhancement_actions
)

st.set_page_config(page_title="📊 Market Signals Dashboard", layout="wide")
st.title("📊 Harrell Family Strategic Signal Monitor")

FRED_API_KEY = st.secrets.get("FRED_API_KEY")
if not FRED_API_KEY:
    st.error("❌ Missing FRED_API_KEY in Streamlit secrets.")
    st.stop()
fred = Fred(api_key=FRED_API_KEY)

plan = st.selectbox(
    "Select Strategic Plan to Monitor:",
    [
        "📑 Portfolio Enhancement Actions per Strategy",
        "📊 Market Dashboard",
        "📘 2025 Market Dynamics Plan",
        "📙 Tax-Sensitive Defensive Plan",
        "📗 Re-entry Plan",
        "🇺🇸 U.S.A. Debt Crisis Plan",
        "🇨🇳 China Treasury Selloff Monitor",
        "🌍 Trade Regime Shift Tracker",
        "📐 50/30/20 Plan"
    ]
)

if plan == "📑 Portfolio Enhancement Actions per Strategy":
    enhancement_actions.render()
elif plan == "📊 Market Dashboard":
    market_dashboard.render()
elif plan == "📘 2025 Market Dynamics Plan":
    plan_2025_dynamics.render()
elif plan == "📙 Tax-Sensitive Defensive Plan":
    plan_tax_defensive.render()
elif plan == "📗 Re-entry Plan":
    plan_reentry.render()
elif plan == "🇺🇸 U.S.A. Debt Crisis Plan":
    plan_debt_crisis.render()
elif plan == "🇨🇳 China Treasury Selloff Monitor":
    plan_china_selloff.render()
elif plan == "🌍 Trade Regime Shift Tracker":
    plan_trade_shift.render()
elif plan == "📐 50/30/20 Plan":
    plan_50_30_20.render()

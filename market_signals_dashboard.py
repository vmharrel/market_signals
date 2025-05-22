import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime
from fredapi import Fred

# --- Load FRED API key from Streamlit secrets only ---
FRED_API_KEY = st.secrets.get("FRED_API_KEY")
if not FRED_API_KEY:
    st.error("❌ Missing FRED_API_KEY in Streamlit secrets.")
    st.stop()

fred = Fred(api_key=FRED_API_KEY)

st.set_page_config(page_title="📊 Market Signals Strategy Dashboard", layout="wide")
st.title("📊 Harrell Family Strategic Signal Monitor")

# --- Plan Selection ---
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

st.success(f"✅ Selected: {plan}")
st.info("🚧 Placeholder: full signal logic loads below based on plan selection.")

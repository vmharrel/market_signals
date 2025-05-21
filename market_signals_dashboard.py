import os
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime
from fredapi import Fred
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
FRED_API_KEY = st.secrets.get("FRED_API_KEY", os.getenv("FRED_API_KEY"))
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

# Fallback rendering to test UI
if plan:
    st.success(f"You selected: {plan}")
    st.info("Your full dashboard logic should run here for this strategy.")

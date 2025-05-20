
import os
import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime
from fredapi import Fred
from dotenv import load_dotenv
import streamlit.components.v1 as components

# --- Load environment variables ---
load_dotenv()
FRED_API_KEY = st.secrets.get("FRED_API_KEY", os.getenv("FRED_API_KEY"))
fred = Fred(api_key=FRED_API_KEY)

st.set_page_config(page_title="📊 Market Signals Suite", layout="wide")
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
        "🇨🇳 China Treasury Selloff Monitor"
    ]
)

# --- Portfolio Enhancement HTML View ---
if plan == "📑 Portfolio Enhancement Actions per Strategy":
    st.subheader("📑 Portfolio Enhancement Actions per Strategy")
    with open("portfolio_enhancement_actions.html", "r") as f:
        html_content = f.read()
    components.html(html_content, height=900, scrolling=True)
    st.stop()



elif plan == "🇨🇳 China Treasury Selloff Monitor":
    st.subheader("🇨🇳 China Treasury Selloff Monitor – Global Treasury Confidence Risk")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("10Y Yield", f"{t10:.2f}%")
        if t10 > 5.0:
            st.warning("⚠️ 10Y > 5% → Exit long bonds, increase private credit + floating-rate")

    with col2:
        dxy_data = get_price("DX-Y.NYB", period="3mo")
        if not dxy_data.empty:
            dxy_change = ((dxy_data[-1] - dxy_data[0]) / dxy_data[0]) * 100
            st.metric("DXY 3-Mo Change", f"{dxy_change:.2f}%")
            if dxy_change < -5:
                st.warning("⚠️ USD down >5% → Add foreign equities, gold, global bonds")
        else:
            st.warning("⚠️ Unable to fetch DXY data")

    with col3:
        # Simulated China Treasury holdings drop
        holdings_drop = 120  # Assume drop in $ billions
        st.metric("China Treasury Holdings ↓", f"${holdings_drop}B YoY")
        if holdings_drop > 100:
            st.warning("⚠️ Drop > $100B → Hedge U.S. bond exposure, increase global diversification")

    st.caption("📉 Note: FX reserves monitoring to be integrated in future version.")

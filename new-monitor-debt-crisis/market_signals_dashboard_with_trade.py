
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
        "🇨🇳 China Treasury Selloff Monitor",
        "🌍 Trade Regime Shift Tracker"
    ]
)

# --- Portfolio Enhancement HTML View ---
if plan == "📑 Portfolio Enhancement Actions per Strategy":
    st.subheader("📑 Portfolio Enhancement Actions per Strategy")
    with open("portfolio_enhancement_actions.html", "r") as f:
        html_content = f.read()
    components.html(html_content, height=900, scrolling=True)
    st.stop()



elif plan == "🇨🇳 China Treasury Selloff Monitor",
        "🌍 Trade Regime Shift Tracker":
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



elif plan == "🌍 Trade Regime Shift Tracker":
    st.subheader("🌍 Trade Regime Shift Tracker – Reshoring & Global Supply Chain Pressure")

    col1, col2, col3 = st.columns(3)

    with col1:
        gscpi_index = 1.7  # Simulated index reading
        st.metric("GSCPI (Global SC Pressure)", f"{gscpi_index:.2f}")
        if gscpi_index > 1.5:
            st.warning("⚠️ GSCPI > 1.5 → Add U.S. infrastructure, reshoring assets")

    with col2:
        trade_deficit = 90  # Simulated $B monthly deficit
        st.metric("U.S. Trade Deficit", f"${trade_deficit}B")
        if trade_deficit > 80:
            st.warning("⚠️ Deficit widening → Add exporters, FX hedges, real assets")

    with col3:
        eem = get_price("EEM", period="3mo")
        spy = get_price("SPY", period="3mo")
        if not eem.empty and not spy.empty:
            eem_change = ((eem[-1] - eem[0]) / eem[0]) * 100
            spy_change = ((spy[-1] - spy[0]) / spy[0]) * 100
            delta = eem_change - spy_change
            st.metric("EEM vs SPY (3mo)", f"{delta:.2f}%")
            if delta > 5:
                st.warning("⚠️ EM outperformance → Add EM or reshoring plays")
        else:
            st.warning("⚠️ Could not fetch EEM/SPY for divergence analysis")

    dbc = get_price("DBC", period="3mo")
    if not dbc.empty:
        dbc_change = ((dbc[-1] - dbc[0]) / dbc[0]) * 100
        st.metric("DBC 3-Mo Change", f"{dbc_change:.2f}%")
        if dbc_change > 5:
            st.warning("⚠️ Commodity strength → Add PDBC, DBC, GSG, industrials")
    else:
        st.warning("⚠️ Commodity ETF data unavailable")

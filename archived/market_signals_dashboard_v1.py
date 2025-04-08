
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from fredapi import Fred
import os
from dotenv import load_dotenv

# --- Load environment variable for FRED API ---
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")
fred = Fred(api_key=FRED_API_KEY)

st.set_page_config(page_title="📊 Market Signals Suite", layout="wide")

# --- Sidebar: Refresh Macro Data ---
st.sidebar.title("📡 Macroeconomic Data")
refresh_fred = st.sidebar.button("🔁 Refresh FRED Data")

# --- Helper to fetch FRED data with fallback ---
def fetch_latest_fred(series_id, frequency='m'):
    try:
        data = fred.get_series(series_id)
        df = data.to_frame(name="value").reset_index()
        df.columns = ["Date", "Value"]
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
        if frequency == 'q':
            df = df[df["Date"].dt.month.isin([3, 6, 9, 12])]
        return df.iloc[-1]["Value"]
    except Exception as e:
        st.warning(f"Could not fetch {series_id}: {e}")
        return None

# --- FRED macroeconomic indicators ---
latest_cpi, latest_oas, latest_gdp, latest_lei = None, None, None, None

if refresh_fred:
    latest_cpi = fetch_latest_fred("CPIAUCSL")
    latest_oas = fetch_latest_fred("BAMLH0A0HYM2")
    latest_gdp = fetch_latest_fred("GDP", frequency='q')
    latest_lei = fetch_latest_fred("USSLIND")

# --- Market Signal Fetchers ---
def get_price(ticker, period='6mo'):
    return yf.download(ticker, period=period)['Close']

def get_vix():
    return get_price("^VIX", period="5d").iloc[-1].item()

def get_sp500_vs_ma():
    data = get_price("^GSPC", period='1y')
    current = data.iloc[-1].item()
    ma_200 = data.rolling(window=200).mean().dropna().iloc[-1].item()
    return current, ma_200

def get_yield_curve():
    t10 = get_price("^TNX", period="5d").iloc[-1].item() / 100
    t3m = get_price("^IRX", period="5d").iloc[-1].item() / 100
    return t10, t3m

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🚨 Risk Signal Monitor", "🔁 Re-entry Dashboard", "📊 Stagflation Summary"])

with tab1:
    st.header("🚨 Market Risk Signal Monitor")
    vix = get_vix()
    sp_price, sp_ma = get_sp500_vs_ma()
    t10, t3m = get_yield_curve()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("VIX", f"{vix:.2f}")
    with col2:
        st.metric("S&P vs 200MA", f"{sp_price:.2f} vs {sp_ma:.2f}")
    with col3:
        st.metric("10Y - 3M", f"{t10:.2f}% - {t3m:.2f}%")

    st.divider()

    if latest_cpi:
        st.metric("📈 CPI YoY", f"{latest_cpi:.2f}")
        if latest_cpi > 4.0:
            st.warning("⚠️ CPI YoY above 4% — Inflation risk")
    if latest_oas:
        st.metric("📉 HY OAS", f"{latest_oas:.0f} bps")
        if latest_oas > 500:
            st.warning("⚠️ Credit spreads above 500bps")

with tab2:
    st.header("🔁 Re-entry Signal Dashboard")
    reentry_score = sum([
        vix < 18,
        sp_price > sp_ma,
        t10 > t3m,
        latest_cpi is not None and latest_cpi < 3.5
    ])

    st.metric("Re-entry Score", f"{reentry_score}/4")
    if reentry_score == 4:
        st.success("✅ All clear: Begin full re-entry")
    elif reentry_score >= 2:
        st.info("🟡 Consider phased re-entry")
    else:
        st.warning("🔒 Hold off on re-entry")

with tab3:
    st.header("📊 Stagflation Summary")
    if latest_gdp:
        st.metric("📉 GDP Growth", f"{latest_gdp:.2f}%")
        if latest_gdp < 0:
            st.error("⚠️ Negative GDP — contraction alert")
    if latest_lei:
        st.metric("📉 LEI", f"{latest_lei:.2f}")
        if latest_lei < 101:
            st.error("⚠️ LEI decline — potential economic slowdown")

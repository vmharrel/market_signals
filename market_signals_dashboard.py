
import os
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from fredapi import Fred
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
FRED_API_KEY = st.secrets.get("FRED_API_KEY", os.getenv("FRED_API_KEY"))

st.set_page_config(page_title="📊 Market Signals Strategy Dashboard", layout="wide")
st.title("📊 Harrell Family Strategic Signal Monitor")

# --- Plan Selection ---
plan = st.selectbox(
    "Select Strategic Plan to Monitor:",
    [
        "📘 2025 Market Dynamics Plan",
        "📙 Tax-Sensitive Defensive Plan",
        "📗 Re-entry Plan"
    ]
)

# --- Refresh Macro Data ---
st.sidebar.title("📡 Macroeconomic Data")
refresh_fred = st.sidebar.button("🔁 Refresh FRED Data")

# --- FRED Fetch Helper ---
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

# --- Fetch Macro Data ---
latest_cpi, latest_oas, latest_gdp, latest_lei = None, None, None, None

if refresh_fred:
    latest_cpi = fetch_latest_fred("CPIAUCSL")
    latest_oas = fetch_latest_fred("BAMLH0A0HYM2")
    latest_gdp = fetch_latest_fred("GDP", frequency='q')
    latest_lei = fetch_latest_fred("USSLIND")

# --- Market Signal Functions ---
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

# --- Fetch Market Data ---
vix = get_vix()
sp_price, sp_ma = get_sp500_vs_ma()
t10, t3m = get_yield_curve()

# --- Signal Display Based on Plan ---
st.divider()
if plan == "📘 2025 Market Dynamics Plan":
    st.subheader("📘 Signals for 2025 Market Dynamics Plan")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("VIX", f"{vix:.2f}")
        if vix > 20:
            st.warning("⚠️ VIX > 20 → Rotate into floating-rate, cash, real assets")

    with col2:
        st.metric("S&P vs 200-Day MA", f"{sp_price:.2f} vs {sp_ma:.2f}")
        if sp_price < sp_ma:
            st.warning("⚠️ S&P < 200-day → Shift to value/dividend stocks")

    with col3:
        st.metric("Yield Curve (10Y - 3M)", f"{t10:.2f}% - {t3m:.2f}%")
        if t10 < t3m:
            st.warning("⚠️ Yield Curve Inverted → Add gold, reduce long bonds")

    if latest_cpi and latest_cpi > 4:
        st.warning(f"⚠️ CPI YoY at {latest_cpi:.2f}% → Add TIPS, commodities")

    if latest_oas and latest_oas > 500:
        st.warning(f"⚠️ HY OAS {latest_oas:.0f} bps → Exit high-yield, raise cash")

elif plan == "📙 Tax-Sensitive Defensive Plan":
    st.subheader("📙 Signals for Tax-Sensitive Defensive Plan")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("VIX", f"{vix:.2f}")
        if vix > 25:
            st.warning("⚠️ VIX > 25 → Rebalance IRAs immediately")

    with col2:
        st.metric("S&P Correction", f"{sp_price:.2f}")
        if sp_price < sp_ma * 0.9:
            st.warning("⚠️ >10% drop → Harvest tax losses, shift to short-duration")

    with col3:
        st.metric("LEI", f"{latest_lei if latest_lei else 'N/A'}")
        if latest_lei and latest_lei < 101:
            st.warning("⚠️ LEI drop → Build cash cushion for 24 months expenses")

    if latest_gdp and latest_gdp < 0:
        st.warning(f"⚠️ GDP contracted → Lock in liquidity buffer")

elif plan == "📗 Re-entry Plan":
    st.subheader("📗 Signals for Re-entry Plan")

    conditions_met = 0
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("VIX", f"{vix:.2f}")
        if vix < 18:
            st.success("✅ VIX < 18 → Volatility normalized")
            conditions_met += 1
        else:
            st.info("Still elevated")

    with col2:
        st.metric("S&P vs 200-Day MA", f"{sp_price:.2f} vs {sp_ma:.2f}")
        if sp_price > sp_ma:
            st.success("✅ Trend recovery")
            conditions_met += 1

    with col3:
        st.metric("Yield Curve", f"{t10:.2f}% - {t3m:.2f}%")
        if t10 > t3m:
            st.success("✅ Curve normalized")
            conditions_met += 1

    if latest_cpi and latest_cpi < 3.5:
        st.success(f"✅ CPI stabilized at {latest_cpi:.2f}%")
        conditions_met += 1

    st.divider()
    if conditions_met == 4:
        st.success("🔁 All clear: Begin full portfolio re-entry")
    elif conditions_met >= 2:
        st.info("🟡 Consider phased re-entry — monitor remaining signals")
    else:
        st.warning("🔒 Re-entry not yet advised")


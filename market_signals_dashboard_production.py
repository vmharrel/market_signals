import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime
from fredapi import Fred

# --- Securely load FRED API key ---
FRED_API_KEY = st.secrets.get("FRED_API_KEY")
if not FRED_API_KEY:
    st.error("❌ Missing FRED_API_KEY in Streamlit secrets.")
    st.stop()

fred = Fred(api_key=FRED_API_KEY)

st.set_page_config(page_title="📊 Market Signals Dashboard", layout="wide")
st.title("📊 Harrell Family Strategic Signal Monitor")

# --- Plan Selector ---
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

# --- Signal & Metric Calculators ---
def get_price(ticker, period='6mo'):
    try:
        return yf.download(ticker, period=period)['Close']
    except:
        return pd.Series()

def get_vix():
    return get_price("^VIX", period="5d").iloc[-1]

def get_sp500_vs_ma():
    data = get_price("^GSPC", period="1y")
    current = data.iloc[-1]
    ma_200 = data.rolling(200).mean().dropna().iloc[-1]
    return current, ma_200

def get_yield_curve():
    t10 = get_price("^TNX", period="5d").iloc[-1] / 100
    t3m = get_price("^IRX", period="5d").iloc[-1] / 100
    return t10, t3m

def fetch_fred_series(series_id, frequency="m"):
    try:
        data = fred.get_series(series_id)
        df = data.to_frame(name="value").reset_index()
        df.columns = ["Date", "Value"]
        df = df.sort_values("Date")
        if frequency == "q":
            df = df[df["Date"].dt.month.isin([3, 6, 9, 12])]
        return df.iloc[-1]["Value"]
    except:
        return None

# Fetch common metrics
vix = get_vix()
sp_price, sp_ma = get_sp500_vs_ma()
t10, t3m = get_yield_curve()
cpi = fetch_fred_series("CPIAUCSL")
oas = fetch_fred_series("BAMLH0A0HYM2")
gdp = fetch_fred_series("GDP", frequency="q")
lei = fetch_fred_series("USSLIND")

# Info bar to confirm logic is loaded
st.info("✅ Dashboard logic is initialized. Insert each plan-specific view below this point.")

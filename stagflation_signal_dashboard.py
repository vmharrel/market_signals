import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# --- Set Up ---
st.set_page_config(page_title="Stagflation Signal Dashboard", layout="wide")
st.title("📊 Stagflation & Defensive Allocation Signal Monitor")
st.markdown("Monitor key market indicators before executing the revised retirement allocation strategy.")

# --- Helper Functions ---
def get_price(ticker, period='6mo'):
    return yf.download(ticker, period=period)['Close']

def get_vix():
    return get_price('^VIX').iloc[-1].item()

def get_sp500_vs_ma():
    data = get_price('^GSPC', period='1y')
    current = data.iloc[-1].item()
    ma_200 = data.rolling(window=200).mean().dropna().iloc[-1].item()
    return current, ma_200

def get_yield_curve():
    t10 = get_price('^TNX').iloc[-1].item() / 100  # 10-Year Yield
    t3m = get_price('^IRX').iloc[-1].item() / 100  # 3-Month Yield
    return t10, t3m

# --- Fetch Data ---
vix = get_vix()
sp_price, sp_ma = get_sp500_vs_ma()
t10, t3m = get_yield_curve()

# --- Display Metrics ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("VIX Index (Volatility)", f"{vix:.2f}", delta=None)
    if vix > 20:
        st.warning("Volatility Elevated → Begin Defensive Rotation")

with col2:
    st.metric("S&P 500 vs. 200-Day MA", f"{sp_price:.2f} vs {sp_ma:.2f}")
    if sp_price < sp_ma:
        st.warning("S&P 500 Below 200-Day Moving Avg")

with col3:
    st.metric("Yield Curve (10Y - 3M)", f"{t10:.2f}% - {t3m:.2f}%")
    if t10 < t3m:
        st.warning("Yield Curve Inverted → Recession Signal")

# --- Scoring and Signal ---
signal_count = sum([
    vix > 20,
    sp_price < sp_ma,
    t10 < t3m
])

st.divider()

if signal_count >= 3:
    st.error("🚨 STRONG SIGNAL: Execute full defensive reallocation")
elif signal_count == 2:
    st.warning("⚠️ MODERATE SIGNAL: Begin phased allocation shift + tax strategy")
elif signal_count == 1:
    st.info("🟡 Early Warning: Monitor indicators daily")
else:
    st.success("🟢 No major risk signals. Maintain current positioning")

st.caption("Data powered by Yahoo Finance. Script last updated: April 8, 2025")

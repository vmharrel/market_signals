import streamlit as st
import yfinance as yf

st.set_page_config(page_title="🔁 Re-entry Signal Monitor", layout="wide")
st.title("🔁 Market Re-Entry Signal Dashboard")

# --- Re-entry signal thresholds ---
REENTRY_VIX_THRESHOLD = 18

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
    t10 = get_price('^TNX').iloc[-1].item() / 100
    t3m = get_price('^IRX').iloc[-1].item() / 100
    return t10, t3m

# --- Signal Evaluation ---
vix = get_vix()
sp_price, sp_ma = get_sp500_vs_ma()
t10, t3m = get_yield_curve()

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("VIX Level", f"{vix:.2f}")
    st.success("✅ VIX below 18 — Normalized") if vix < REENTRY_VIX_THRESHOLD else st.error("❌ VIX still elevated")

with col2:
    st.metric("S&P 500 vs 200-Day MA", f"{sp_price:.2f} vs {sp_ma:.2f}")
    st.success("✅ Trend Recovery") if sp_price > sp_ma else st.error("❌ S&P 500 still below 200-day MA")

with col3:
    st.metric("Yield Curve (10Y - 3M)", f"{t10:.2f}% - {t3m:.2f}%")
    st.success("✅ Curve Normalized") if t10 > t3m else st.error("❌ Yield curve still inverted")

# --- Summary ---
st.divider()
conditions_met = sum([
    vix < REENTRY_VIX_THRESHOLD,
    sp_price > sp_ma,
    t10 > t3m
])

if conditions_met == 3:
    st.success("🔁 All conditions met — Ready for full portfolio re-entry")
elif conditions_met == 2:
    st.warning("🟡 Consider phased re-entry — monitor for full signal")
elif conditions_met == 1:
    st.info("⚠️ Early improvement — not yet time to re-enter")
else:
    st.error("🔒 No signals suggest safe re-entry at this time")

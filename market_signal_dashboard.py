import streamlit as st
import yfinance as yf

st.set_page_config(page_title="🚨 Market Signal Alert Monitor", layout="wide")
st.title("🚨 Market Signal Alert Dashboard")

# Thresholds
VIX_ALERT_LEVEL = 20
SP500_MOVING_AVG_DAYS = 200

# --- Utility Functions ---
def get_price(ticker, period='6mo'):
    return yf.download(ticker, period=period)['Close']

def fetch_vix_level():
    vix = get_price("^VIX", period="5d")
    return vix.iloc[-1].item()

def fetch_sp500_vs_moving_avg():
    sp500 = get_price("^GSPC", period="1y")
    current_price = sp500.iloc[-1].item()
    moving_avg = sp500.rolling(window=SP500_MOVING_AVG_DAYS).mean().dropna().iloc[-1].item()
    return current_price, moving_avg

def fetch_yield_curve():
    t10 = get_price("^TNX", period="5d").iloc[-1].item() / 100
    t3m = get_price("^IRX", period="5d").iloc[-1].item() / 100
    return t10, t3m

# --- Evaluation ---
vix = fetch_vix_level()
sp_price, sp_ma = fetch_sp500_vs_moving_avg()
t10, t3m = fetch_yield_curve()

# --- Display Metrics ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("VIX Index (Volatility)", f"{vix:.2f}")
    if vix > VIX_ALERT_LEVEL:
        st.warning("⚠️ VIX elevated: Defensive rotation advised")

with col2:
    st.metric("S&P 500 vs. 200-Day MA", f"{sp_price:.2f} vs {sp_ma:.2f}")
    if sp_price < sp_ma:
        st.warning("📉 S&P 500 below 200-day moving average")

with col3:
    st.metric("Yield Curve (10Y - 3M)", f"{t10:.2f}% - {t3m:.2f}%")
    if t10 < t3m:
        st.warning("📉 Yield curve inversion detected")

# --- Summary ---
st.divider()
signal_count = sum([
    vix > VIX_ALERT_LEVEL,
    sp_price < sp_ma,
    t10 < t3m
])

if signal_count >= 3:
    st.error("🚨 STRONG SIGNAL: Execute full defensive reallocation")
elif signal_count == 2:
    st.warning("⚠️ MODERATE SIGNAL: Begin phased allocation shift + tax strategy")
elif signal_count == 1:
    st.info("🟡 Early Warning: Monitor indicators daily")
else:
    st.success("🟢 No major risk signals. Maintain current positioning")

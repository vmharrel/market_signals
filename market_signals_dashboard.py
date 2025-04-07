import streamlit as st
import yfinance as yf

st.set_page_config(page_title="📊 Market Signals Suite", layout="wide")

# --- Utility Functions ---
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

# --- Tab 1: Risk Signal Monitor ---
with tab1:
    st.header("🚨 Market Risk Signal Monitor")

    VIX_ALERT_LEVEL = 20
    sp_price, sp_ma = get_sp500_vs_ma()
    vix = get_vix()
    t10, t3m = get_yield_curve()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("VIX Level", f"{vix:.2f}")
        if vix > VIX_ALERT_LEVEL:
            st.warning("⚠️ VIX elevated: Defensive rotation advised")

    with col2:
        st.metric("S&P 500 vs 200-Day MA", f"{sp_price:.2f} vs {sp_ma:.2f}")
        if sp_price < sp_ma:
            st.warning("📉 S&P 500 below 200-day moving average")

    with col3:
        st.metric("Yield Curve (10Y - 3M)", f"{t10:.2f}% - {t3m:.2f}%")
        if t10 < t3m:
            st.warning("📉 Yield curve inversion detected")

    signal_count = sum([
        vix > VIX_ALERT_LEVEL,
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

# --- Tab 2: Re-entry Dashboard ---
with tab2:
    st.header("🔁 Re-entry Signal Dashboard")

    REENTRY_VIX_THRESHOLD = 18
    reentry_conditions = []

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("VIX Level", f"{vix:.2f}")
        if vix < REENTRY_VIX_THRESHOLD:
            st.success("✅ VIX normalized")
            reentry_conditions.append(True)
        else:
            st.error("❌ VIX still elevated")
            reentry_conditions.append(False)

    with col2:
        st.metric("S&P 500 vs 200-Day MA", f"{sp_price:.2f} vs {sp_ma:.2f}")
        if sp_price > sp_ma:
            st.success("✅ Trend Recovery")
            reentry_conditions.append(True)
        else:
            st.error("❌ S&P 500 below 200-day MA")
            reentry_conditions.append(False)

    with col3:
        st.metric("Yield Curve (10Y - 3M)", f"{t10:.2f}% - {t3m:.2f}%")
        if t10 > t3m:
            st.success("✅ Curve Normalized")
            reentry_conditions.append(True)
        else:
            st.error("❌ Yield curve still inverted")
            reentry_conditions.append(False)

    st.divider()
    met = sum(reentry_conditions)
    if met == 3:
        st.success("🔁 All conditions met — Ready for full portfolio re-entry")
    elif met == 2:
        st.warning("🟡 Consider phased re-entry — monitor for full signal")
    elif met == 1:
        st.info("⚠️ Early improvement — not yet time to re-enter")
    else:
        st.error("🔒 No signals suggest safe re-entry at this time")

# --- Tab 3: Stagflation Summary (original dashboard logic) ---
with tab3:
    st.header("📊 Stagflation Signal Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("VIX Index (Volatility)", f"{vix:.2f}")
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

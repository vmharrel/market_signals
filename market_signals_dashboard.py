
import os
import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
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
        "📊 Market Dashboard",
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

if plan == "📊 Market Dashboard":
    st.subheader("📊 Combined Market Signal Dashboard")
    st.caption("🧭 Mapping all signals to strategic plans for fast review")

    data = []

    # Collect all signals in a table
    data.append(("VIX > 20", vix > 20, "📘 2025 Market Dynamics Plan", "Begin rotating into real assets and floating-rate instruments"))
    data.append(("VIX > 25", vix > 25, "📙 Tax-Sensitive Defensive Plan", "Rebalance IRAs immediately"))
    data.append(("VIX < 18", vix < 18, "📗 Re-entry Plan", "Volatility normalized – start phased re-entry"))

    data.append(("S&P < 200-Day MA", sp_price < sp_ma, "📘 2025 Market Dynamics Plan", "Rotate into value/dividend stocks"))
    data.append(("S&P Correction >10%", sp_price < sp_ma * 0.9, "📙 Tax-Sensitive Defensive Plan", "Harvest tax losses, shift to short ETFs"))
    data.append(("S&P > 200-Day MA", sp_price > sp_ma, "📗 Re-entry Plan", "Trend recovery confirmed"))

    data.append(("Yield Curve Inverted (10Y < 3M)", t10 < t3m, "📘 2025 Market Dynamics Plan", "Add gold, reduce long bonds"))
    data.append(("Yield Curve Normalized (10Y > 3M)", t10 > t3m, "📗 Re-entry Plan", "Bond market normalization"))

    if latest_cpi:
        data.append((f"CPI YoY > 4% (Currently {latest_cpi:.2f}%)", latest_cpi > 4.0, "📘 2025 Market Dynamics Plan", "Add TIPS, commodities"))
        data.append((f"CPI YoY < 3.5% (Currently {latest_cpi:.2f}%)", latest_cpi < 3.5, "📗 Re-entry Plan", "CPI stabilized – begin re-entry"))

    if latest_oas:
        data.append((f"HY OAS > 500bps (Currently {latest_oas:.0f})", latest_oas > 500, "📘 2025 Market Dynamics Plan", "Exit high-yield, increase cash"))

    if latest_gdp:
        data.append((f"GDP < 0% (Currently {latest_gdp:.2f}%)", latest_gdp < 0, "📙 Tax-Sensitive Defensive Plan", "Lock in cash cushion for 24 months"))

    if latest_lei:
        data.append((f"LEI < 101 (Currently {latest_lei:.2f})", latest_lei < 101, "📙 Tax-Sensitive Defensive Plan", "Build emergency liquidity buffer"))

    df = pd.DataFrame(data, columns=["Signal", "Triggered", "Plan", "Suggested Action"])
    df["Status"] = df["Triggered"].map(lambda x: "🟥 ALERT" if x else "✅ OK")

    st.dataframe(df[["Status", "Signal", "Plan", "Suggested Action"]], use_container_width=True)

    st.markdown("### 📊 Strategy-Specific Signal Overview (Visual)")

    for plan_name in ["📘 2025 Market Dynamics Plan", "📙 Tax-Sensitive Defensive Plan", "📗 Re-entry Plan"]:
        subset = df[df["Plan"] == plan_name]
        if not subset.empty:
            st.markdown(f"#### {plan_name}")
            chart = alt.Chart(subset).mark_bar().encode(
                x=alt.X("Signal", sort="-y"),
                y="Triggered",
                color=alt.Color("Status", scale=alt.Scale(domain=["🟥 ALERT", "✅ OK"], range=["red", "green"]))
            ).properties(width="container", height=200)
            st.altair_chart(chart, use_container_width=True)

    st.stop()

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


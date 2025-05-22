import streamlit as st

def render():
    st.subheader("📘 2025 Market Dynamics Plan")

    # These would be passed into render() normally; using mock values here
    vix = 23.5
    sp_price = 4100
    sp_ma = 4300
    t10 = 4.75
    t3m = 5.00
    cpi = 4.6
    oas = 510

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("VIX", f"{vix:.2f}")
        if vix > 20:
            st.warning("⚠️ VIX > 20 → Rotate into floating-rate, cash, real assets")

    with col2:
        st.metric("S&P vs 200-Day MA", f"{sp_price:.0f} vs {sp_ma:.0f}")
        if sp_price < sp_ma:
            st.warning("⚠️ S&P < 200-day → Shift to value/dividend stocks")

    with col3:
        st.metric("Yield Curve", f"{t10:.2f}% - {t3m:.2f}%")
        if t10 < t3m:
            st.warning("⚠️ Yield Curve Inverted → Add gold, reduce long bonds")

    if cpi and cpi > 4:
        st.warning(f"⚠️ CPI YoY at {cpi:.2f}% → Add TIPS, commodities")

    if oas and oas > 500:
        st.warning(f"⚠️ HY OAS {oas:.0f} bps → Exit high-yield, raise cash")

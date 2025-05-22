import streamlit as st

def render():
    st.subheader("📙 Tax-Sensitive Defensive Plan")

    # Mocked metrics for demonstration
    vix = 27.1
    sp_price = 3950
    sp_ma = 4450
    lei = 100.5
    gdp = -0.4

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("VIX", f"{vix:.2f}")
        if vix > 25:
            st.warning("⚠️ VIX > 25 → Rebalance in tax-advantaged accounts (e.g., IRAs)")

    with col2:
        st.metric("S&P vs 200-Day MA", f"{sp_price:.0f} vs {sp_ma:.0f}")
        if sp_price < sp_ma * 0.9:
            st.warning("⚠️ S&P Correction >10% → Harvest losses, shift to short-duration ETFs")

    with col3:
        st.metric("LEI", f"{lei:.2f}")
        if lei < 101:
            st.warning("⚠️ LEI < 101 → Build cash cushion for 24 months of expenses")

    if gdp < 0:
        st.warning(f"⚠️ GDP Growth < 0% ({gdp:.2f}%) → Lock in liquidity buffer and de-risk portfolio")

import streamlit as st

def render():
    st.subheader("🇨🇳 China Treasury Selloff Monitor")

    # Simulated signal data
    t10 = 5.2
    dxy_change_3mo = -5.8
    china_holdings_drop = 120  # in $B

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("10Y Treasury Yield", f"{t10:.2f}%")
        if t10 > 5.0:
            st.warning("⚠️ 10Y > 5% → Exit long bonds, increase floaters and private credit")

    with col2:
        st.metric("DXY 3-Mo Change", f"{dxy_change_3mo:.2f}%")
        if dxy_change_3mo < -5:
            st.warning("⚠️ USD down >5% → Add gold, FX-hedged global bonds")

    with col3:
        st.metric("China Treasury Holdings ↓ YoY", f"${china_holdings_drop}B")
        if china_holdings_drop > 100:
            st.warning("⚠️ Drop > $100B → Hedge U.S. bond exposure, rotate to global debt")

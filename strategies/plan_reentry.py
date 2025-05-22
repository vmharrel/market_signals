import streamlit as st

def render():
    st.subheader("📗 Re-entry Plan")

    # Example signal values (normally passed in)
    vix = 16.8
    sp_price = 4450
    sp_ma = 4300
    t10 = 4.75
    t3m = 4.30
    cpi = 3.2

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
        st.metric("S&P vs 200-Day MA", f"{sp_price:.0f} vs {sp_ma:.0f}")
        if sp_price > sp_ma:
            st.success("✅ Trend recovery confirmed")
            conditions_met += 1

    with col3:
        st.metric("Yield Curve", f"{t10:.2f}% - {t3m:.2f}%")
        if t10 > t3m:
            st.success("✅ Curve normalized")
            conditions_met += 1

    if cpi < 3.5:
        st.success(f"✅ CPI stabilized at {cpi:.2f}%")
        conditions_met += 1

    st.divider()
    if conditions_met == 4:
        st.success("🔁 All clear: Begin full portfolio re-entry")
    elif conditions_met >= 2:
        st.info("🟡 Consider phased re-entry — monitor remaining signals")
    else:
        st.warning("🔒 Re-entry not yet advised — hold position")

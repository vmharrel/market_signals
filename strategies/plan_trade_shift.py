import streamlit as st

def render():
    st.subheader("🌍 Trade Regime Shift Tracker")

    # Simulated data
    gscpi = 1.8
    trade_deficit = 85  # in billions
    eem_vs_spy_3mo = 6.2  # % outperformance
    dbc_3mo_change = 7.4  # % change

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("GSCPI (Simulated)", f"{gscpi:.2f}")
        if gscpi > 1.5:
            st.warning("⚠️ GSCPI > 1.5 → Add U.S. infra, reshoring, domestic REITs")

    with col2:
        st.metric("U.S. Trade Deficit", f"${trade_deficit}B")
        if trade_deficit > 80:
            st.warning("⚠️ Trade deficit > $80B → Add exporters, FX hedging, real assets")

    with col3:
        st.metric("EEM vs SPY (3-mo)", f"{eem_vs_spy_3mo:.2f}%")
        if eem_vs_spy_3mo > 5:
            st.warning("⚠️ EM > SPY → Add EM exposure, reshoring industrials")

    st.metric("DBC 3-Mo Change", f"{dbc_3mo_change:.2f}%")
    if dbc_3mo_change > 5:
        st.warning("⚠️ Commodities +5% → Add PDBC, GSG, commodity stocks")

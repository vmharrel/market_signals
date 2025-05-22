import streamlit as st
import pandas as pd
import altair as alt

def render():
    st.subheader("📊 Combined Market Signal Dashboard")
    st.caption("🧭 Mapping all signals to strategic plans for fast review")

    # Simulated data
    vix = 23
    sp_price = 4100
    sp_ma = 4400
    t10 = 5.2
    t3m = 5.0
    cpi = 4.5
    oas = 520
    gdp = -0.3
    lei = 100.5
    dxy_change = -6.1
    cds_spread = 55
    gscpi = 1.7
    trade_deficit = 85
    eem_vs_spy_3mo = 6
    dbc_change = 7

    signals = [
        ("VIX > 20", vix > 20, "📘 2025 Market Dynamics Plan", "Rotate into real assets"),
        ("VIX > 25", vix > 25, "📙 Tax-Sensitive Defensive Plan", "Rebalance IRAs"),
        ("VIX < 18", vix < 18, "📗 Re-entry Plan", "Begin phased re-entry"),
        ("S&P < 200-Day MA", sp_price < sp_ma, "📘 2025 Market Dynamics Plan", "Shift to value"),
        ("S&P Drop >10%", sp_price < sp_ma * 0.9, "📙 Tax-Sensitive Defensive Plan", "Harvest losses"),
        ("S&P > 200-Day MA", sp_price > sp_ma, "📗 Re-entry Plan", "Trend recovery"),
        ("Yield Curve Inverted", t10 < t3m, "📘 2025 Market Dynamics Plan", "Add gold"),
        ("Yield Curve Normalized", t10 > t3m, "📗 Re-entry Plan", "Resume intermediate bonds"),
        (f"CPI > 4% ({cpi:.2f})", cpi > 4, "📘 2025 Market Dynamics Plan", "Add TIPS"),
        (f"CPI < 3.5% ({cpi:.2f})", cpi < 3.5, "📗 Re-entry Plan", "Reduce inflation hedges"),
        (f"HY OAS > 500bps ({oas})", oas > 500, "📘 2025 Market Dynamics Plan", "Reduce high yield"),
        (f"GDP < 0 ({gdp:.2f})", gdp < 0, "📙 Tax-Sensitive Defensive Plan", "Increase liquidity"),
        (f"LEI < 101 ({lei})", lei < 101, "📙 Tax-Sensitive Defensive Plan", "Lock in 24mo cushion"),
        (f"CDS > 50bps ({cds_spread})", cds_spread > 50, "🇺🇸 U.S.A. Debt Crisis Plan", "Add private credit"),
        (f"DXY ↓ >5% ({dxy_change:.2f}%)", dxy_change < -5, "🇺🇸 U.S.A. Debt Crisis Plan", "Add gold/foreign assets"),
        (f"GSCPI > 1.5 ({gscpi})", gscpi > 1.5, "🌍 Trade Regime Shift Tracker", "Add U.S. infra"),
        (f"Trade Deficit > $80B ({trade_deficit})", trade_deficit > 80, "🌍 Trade Regime Shift Tracker", "Add exporters"),
        (f"EEM > SPY (3-mo Δ {eem_vs_spy_3mo}%)", eem_vs_spy_3mo > 5, "🌍 Trade Regime Shift Tracker", "Add EM"),
        (f"Commodities +5% ({dbc_change}%)", dbc_change > 5, "🌍 Trade Regime Shift Tracker", "Add DBC/PDBC"),
    ]

    df = pd.DataFrame(signals, columns=["Signal", "Triggered", "Plan", "Suggested Action"])
    df["Status"] = df["Triggered"].map(lambda x: "🟥 ALERT" if x else "✅ OK")

    st.dataframe(df[["Status", "Signal", "Plan", "Suggested Action"]], use_container_width=True)

    st.markdown("### 📊 Strategy-Specific Signal Overview")

    for plan in df["Plan"].unique():
        subset = df[df["Plan"] == plan]
        if not subset.empty:
            st.markdown(f"#### {plan}")
            chart = alt.Chart(subset).mark_bar().encode(
                x=alt.X("Signal", sort="-y"),
                y="Triggered",
                color=alt.Color("Status", scale=alt.Scale(domain=["🟥 ALERT", "✅ OK"], range=["red", "green"]))
            ).properties(height=250)
            st.altair_chart(chart, use_container_width=True)

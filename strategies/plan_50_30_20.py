import streamlit as st
import pandas as pd
import altair as alt

def render():
    st.subheader("📐 50/30/20 Plan – Allocation Comparison")

    st.markdown("Upload your current portfolio allocation as a CSV. Example format:")

    st.code("Asset Class,Amount\nStocks,500000\nBonds,300000\nPrivate,100000", language="csv")

    uploaded_csv = st.file_uploader("Upload your allocation CSV", type="csv")

    if uploaded_csv:
        df = pd.read_csv(uploaded_csv)
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df.dropna(inplace=True)

        total = df["Amount"].sum()
        df["% Allocation"] = df["Amount"] / total * 100

        target_alloc = {"Stocks": 50, "Bonds": 30, "Private": 20}
        df["Target %"] = df["Asset Class"].map(target_alloc)
        df["Deviation"] = df["% Allocation"] - df["Target %"]
        df["Status"] = df["Deviation"].apply(lambda x: "✅ OK" if abs(x) <= 5 else "⚠️ Off Target")

        st.dataframe(df, use_container_width=True)

        chart = alt.Chart(df).transform_fold(
            ["% Allocation", "Target %"]
        ).mark_bar().encode(
            x=alt.X("key:N", title="Metric"),
            y=alt.Y("value:Q", title="Percentage"),
            color=alt.Color("key:N", scale=alt.Scale(domain=["% Allocation", "Target %"], range=["#1f77b4", "#ff7f0e"]))
        ).properties(height=300)

        st.altair_chart(chart, use_container_width=True)

        if any(df["Status"] == "⚠️ Off Target"):
            st.warning("⚠️ Some allocations deviate by more than ±5% from the target.")
        else:
            st.success("✅ All asset classes are within acceptable range.")
    else:
        st.info("Upload a CSV to compare against the 50/30/20 target.")

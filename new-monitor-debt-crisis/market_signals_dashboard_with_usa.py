
import os
import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime
from fredapi import Fred
from dotenv import load_dotenv
import streamlit.components.v1 as components

# --- Load environment variables ---
load_dotenv()
FRED_API_KEY = st.secrets.get("FRED_API_KEY", os.getenv("FRED_API_KEY"))
fred = Fred(api_key=FRED_API_KEY)

st.set_page_config(page_title="📊 Market Signals Suite", layout="wide")
st.title("📊 Harrell Family Strategic Signal Monitor")

# --- Plan Selection ---
plan = st.selectbox(
    "Select Strategic Plan to Monitor:",
    [
        "📑 Portfolio Enhancement Actions per Strategy",
        "📊 Market Dashboard",
        "📘 2025 Market Dynamics Plan",
        "📙 Tax-Sensitive Defensive Plan",
        "📗 Re-entry Plan",
        "🇺🇸 U.S.A. Debt Crisis Plan"
    ]
)

# --- Portfolio Enhancement HTML View ---
if plan == "📑 Portfolio Enhancement Actions per Strategy":
    st.subheader("📑 Portfolio Enhancement Actions per Strategy")
    with open("portfolio_enhancement_actions.html", "r") as f:
        html_content = f.read()
    components.html(html_content, height=900, scrolling=True)
    st.stop()

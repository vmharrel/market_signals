import streamlit as st
import os

# Try both secrets and environment
fred_key_secret = st.secrets.get("FRED_API_KEY", None)
fred_key_env = os.getenv("FRED_API_KEY", None)

st.set_page_config(page_title="🔍 FRED API Key Test", layout="wide")
st.title("🔍 FRED API Key Detection Test")

st.markdown("### st.secrets.get('FRED_API_KEY'):")
st.code(fred_key_secret if fred_key_secret else "❌ Not found in st.secrets")

st.markdown("### os.getenv('FRED_API_KEY'):")
st.code(fred_key_env if fred_key_env else "❌ Not found in environment")

import streamlit as st
import streamlit.components.v1 as components
import os

def render():
    st.subheader("📑 Portfolio Enhancement Actions per Strategy")

    html_path = "portfolio_enhancement_actions.html"

    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=900, scrolling=True)
    else:
        st.error("❌ Could not find 'portfolio_enhancement_actions.html'. Please ensure it's in the project root.")

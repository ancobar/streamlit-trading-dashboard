import streamlit as st

# Main title
st.set_page_config(page_title="Web-Based Trading System", layout="wide")

st.title("📈 Web-Based Trading System")
st.write("Welcome to our automated trading platform. Use the sidebar to navigate.")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.page_link("pages/1_Home.py", label="🏠 Home")
st.sidebar.page_link("pages/2_Live_Trading.py", label="📊 Go Live")
st.sidebar.page_link("pages/3_About_ML.py", label="🧠 ML Model Explanation")
st.sidebar.page_link("pages/4_Backtesting.py", label="🔄 Backtesting Simulator")

st.sidebar.markdown("---")
st.sidebar.write("Developed by Group 2")
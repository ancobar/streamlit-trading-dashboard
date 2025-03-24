import streamlit as st

# ----------------------------
# 🔧 Page configuration
# ----------------------------
st.set_page_config(page_title="Web-Based Trading System", layout="wide")

# ----------------------------
# 🎯 Main title
# ----------------------------
st.title("📈 Web-Based Trading System")
st.write("Welcome to our automated trading platform. Use the sidebar to navigate.")

# ----------------------------
# 📚 Sidebar navigation
# ----------------------------
st.sidebar.title("Navigation")

st.sidebar.page_link("pages/A_Home.py", label="🏠 Home")
st.sidebar.page_link("pages/B_Live_Trading.py", label="📊 Go Live")
st.sidebar.page_link("pages/C_About_ML.py", label="🧠 ML Model Explanation")
st.sidebar.page_link("pages/D_Backtesting.py", label="🧮 Backtesting Simulator")

st.sidebar.markdown("___")
st.sidebar.write("Developed by Group 2")
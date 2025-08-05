st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Unbounded', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# ---- Sidebar ----
st.sidebar.image("https://i.imgur.com/wxI4Z6Z.png", width=150)
st.sidebar.title("🔍 FinDetect")
st.sidebar.markdown("AI-Powered Fraud Detection\n\nBuilt with Streamlit 💡")

# ---- Header ----
st.markdown("# 🧠 Welcome to **FinDetect**")
st.markdown("### AI-powered fraud detection with a simulation of OSI Layer 6 🛡️")
st.write("Upload your financial transactions CSV below:")

# ---- File Upload ----
file = st.file_uploader("📁 Upload your financial transaction CSV", type=["csv"])

if file:
    data = pd.read_csv(file)
    st.subheader("📊 Preview of Your Data")
    st.write(data.head())

    # ---- Fraud Detection ----
    st.subheader("🚨 AI Detection Results")

    model = IsolationForest(contamination=0.1, random_state=42)
    data["fraudulent"] = model.fit_predict(data)
    data["fraudulent"] = data["fraudulent"].map({1: "✅ Safe", -1: "❌ Fraud"})

    st.dataframe(data)

    # ---- Visualization ----
    st.subheader("📈 Fraud Detection Chart")

    fig, ax = plt.subplots()
    colors = np.where(data["fraudulent"] == "❌ Fraud", "red", "green")
    ax.scatter(data["amount"], data["account_age"], c=colors)
    ax.set_xlabel("Transaction Amount")
    ax.set_ylabel("Account Age")
    st.pyplot(fig)

    st.success("✅ Analysis Complete")
else:
    st.info("Please upload a CSV file to begin.")


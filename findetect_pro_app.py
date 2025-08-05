
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Custom Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Varela+Round&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Varela Round', sans-serif;
        background-color: #0F1117;
        color: #FFFFFF;
    }
    .stButton>button {
        color: #FFFFFF;
        background: #1DB954;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        font-weight: bold;
        transition: background 0.3s ease;
    }
    .stButton>button:hover {
        background: #1AA34A;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.image("https://upload.wikimedia.org/wikipedia/commons/6/60/Fraud_detection_concept.jpg", use_container_width=True)
st.title("FinDetect Pro")
st.subheader("🧠 AI-powered Fraud Detection + IFRS-based Financial Review")

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload your financial transaction CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Basic view
    st.write("### 🔍 Raw Data Preview")
    st.dataframe(df.head())

    # Fraud score simulation (mock AI logic)
    st.write("### 🚨 Fraud Risk Detection")
    df["fraud_score"] = np.random.rand(len(df))  # Mocked logic
    risky = df[df["fraud_score"] > 0.8]
    st.write(f"⚠️ Found {len(risky)} potentially risky transactions")
    st.dataframe(risky[["fraud_score"] + [col for col in df.columns if col != "fraud_score"]])

    # IFRS-inspired financial insights
    st.write("### 📊 Financial Health Snapshot (IFRS Style)")
    if {"amount", "type"}.issubset(df.columns):
        income = df[df["type"] == "credit"]["amount"].sum()
        expenses = df[df["type"] == "debit"]["amount"].sum()
        profit = income - expenses

        st.metric("💰 Total Income", f"${income:,.2f}")
        st.metric("💸 Total Expenses", f"${expenses:,.2f}")
        st.metric("📈 Net Profit", f"${profit:,.2f}")

        # Suggestion logic
        st.write("### 💡 AI Suggestions")
        if profit < 0:
            st.error("⚠️ Negative profit detected. Consider reducing expenses or improving revenue streams.")
        elif expenses > income * 0.7:
            st.warning("🧮 Expenses are high relative to income. Try budgeting more effectively.")
        else:
            st.success("✅ Financials look stable. Continue monitoring for anomalies.")

        # Visualization
        fig, ax = plt.subplots()
        ax.bar(["Income", "Expenses", "Net Profit"], [income, expenses, profit], color=["green", "red", "blue"])
        ax.set_title("Financial Overview")
        st.pyplot(fig)
    else:
        st.error("CSV must include 'amount' and 'type' columns.")
else:
    st.info("Please upload a CSV to begin analysis.")

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# ✅ Step 1: Streamlit Page Config
st.set_page_config(
    page_title="FinDetect - AI Fraud Scanner",
    page_icon="💸",
    layout="wide"
)

# ✅ Step 2: Custom Font and Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #0e1117;
        color: white;
    }

    .stButton>button {
        background-color: #00c9a7;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }

    .stFileUploader, .stSlider, .stTextInput {
        background-color: #1f2937;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Step 3: Sidebar Logo (Optional)
st.sidebar.image("https://i.imgur.com/tGbaZCY.png", use_column_width=True)  # Replace with your logo if needed

# ✅ Step 4: Main App Functionality

st.title("💸 FinDetect: AI-Powered Fraud Detection")

st.write("Welcome to FinDetect, your AI assistant for detecting financial anomalies using Isolation Forest and OSI Layer 6 simulation.")

uploaded_file = st.file_uploader("📁 Upload your financial transactions CSV file", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.subheader("🔍 Uploaded Data")
    st.dataframe(data)

    if {'amount', 'time', 'account_age'}.issubset(data.columns):
        X = data[['amount', 'time', 'account_age']]

        model = IsolationForest(contamination=0.05)
        model.fit(X)
        data['anomaly'] = model.predict(X)
        data['anomaly'] = data['anomaly'].apply(lambda x: '🔴 Fraud' if x == -1 else '🟢 Normal')

        st.subheader("🚦 Detection Results")
        st.dataframe(data)

        st.subheader("📊 Visualisation")
        fig, ax = plt.subplots()
        colors = np.where(data['anomaly'] == '🔴 Fraud', 'red', 'green')
        ax.scatter(data['amount'], data['time'], c=colors)
        ax.set_xlabel("Amount")
        ax.set_ylabel("Time")
        st.pyplot(fig)

    else:
        st.error("❌ Your CSV must contain 'amount', 'time', and 'account_age' columns.")
else:
    st.info("👈 Upload a CSV to begin.")



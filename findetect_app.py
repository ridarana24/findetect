
import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import base64
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="FinDetect", page_icon="🔐", layout="wide")

# Custom dark mode CSS
dark_style = """
<style>
body {
    background-color: #0e1117;
    color: #c1c1c1;
}
h1, h2, h3, h4, h5 {
    color: #ffffff;
}
.stButton>button {
    background-color: #1f1f1f;
    color: #00ffae;
    border: 1px solid #00ffae;
    border-radius: 8px;
}
.stDownloadButton>button {
    background-color: #1f1f1f;
    color: #00ffae;
    border: 1px solid #00ffae;
    border-radius: 8px;
}
</style>
"""

st.markdown(dark_style, unsafe_allow_html=True)

st.title("🔐 FinDetect: AI Financial Anomaly Detection")
st.markdown("Welcome to **FinDetect**, your AI-powered fraud detection app with OSI Layer 6 simulation.")

uploaded_file = st.file_uploader("📁 Upload your financial transaction CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Uploaded Data")
    st.dataframe(df.head())

    if st.button("🚨 Run AI Fraud Detection"):
        clf = IsolationForest(contamination=0.1, random_state=42)
        df['anomaly'] = clf.fit_predict(df.select_dtypes(include=['float64', 'int64']))

        df['encoded'] = df.apply(lambda row: base64.b64encode(str(row.values).encode()).decode(), axis=1)
        df['anomaly_label'] = df['anomaly'].apply(lambda x: "🔴 Suspicious" if x == -1 else "🟢 Normal")

        st.success("✅ Detection complete. Scroll down for results.")

        st.subheader("🧾 Results")
        st.dataframe(df[['anomaly_label', 'encoded']])

        st.subheader("📈 Anomaly Trend")

        plt.figure(figsize=(10, 4))
        plt.plot(df['anomaly'], linestyle='--', marker='o')
        plt.title("Anomaly Trend")
        plt.xlabel("Transaction Index")
        plt.ylabel("Anomaly Score")
        st.pyplot(plt)

        # Download button
        csv = df.to_csv(index=False).encode()
        st.download_button(
            label="📥 Download Full Results",
            data=csv,
            file_name='FinDetect_Results.csv',
            mime='text/csv',
        )

        st.markdown("---")
        st.markdown("🔒 Built with Python, Streamlit & AI — by [Your Name]")

import streamlit as st
import pandas as pd
import re

# Page configuration
st.set_page_config(page_title="FinDetect", layout="centered")

# Custom styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        html, body, [class*="css"] {
            font-family: 'Share Tech Mono', monospace;
            background-color: #000080 !important;
            color: white !important;
        }

        .stApp {
            background-color: #000080 !important;
        }

        .stTextInput input {
            background-color: #add8e6 !important; /* Light blue */
            color: black !important;
            border: 1px solid #ffffff !important;
        }

        .stButton>button {
            background-color: #add8e6 !important;
            color: black !important;
        }

        body::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            background: radial-gradient(white 1px, transparent 1px);
            background-size: 30px 30px;
            animation: moveDots 10s linear infinite;
            opacity: 0.05;
        }

        @keyframes moveDots {
            from {
                background-position: 0 0;
            }
            to {
                background-position: 100px 100px;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.title("FinDetect: AI-Powered Financial Analysis")

# Chat input
query = st.text_input("Paste a company's financial data or ask a financial question:")

# Parse basic structure
def parse_financials(text):
    numbers = re.findall(r'\d+[\,\.]?\d*', text.replace(',', ''))
    numbers = [float(n) for n in numbers if n.replace('.', '', 1).isdigit()]

    results = {}
    if len(numbers) >= 5:
        results['Revenue'] = numbers[0]
        results['COGS'] = numbers[1]
        results['Net Income'] = numbers[2]
        results['Total Assets'] = numbers[3]
        results['Total Liabilities'] = numbers[4]
    return results

# Analyze data with detailed reasoning
def analyze(financials):
    if not financials:
        return "❗ Unable to extract enough financial data. Try again with more detail."

    analysis = []

    if 'Revenue' in financials and 'COGS' in financials:
        gpm = (financials['Revenue'] - financials['COGS']) / financials['Revenue'] * 100
        analysis.append(f"✅ Gross Profit Margin: {gpm:.2f}%")

    if 'Net Income' in financials and 'Revenue' in financials:
        npm = financials['Net Income'] / financials['Revenue'] * 100
        analysis.append(f"✅ Net Profit Margin: {npm:.2f}%")

    if 'Total Liabilities' in financials and 'Total Assets' in financials:
        dar = financials['Total Liabilities'] / financials['Total Assets'] * 100
        analysis.append(f"⚠️ Debt to Asset Ratio: {dar:.2f}%")

        if dar > 70:
            analysis.append("🔎 High leverage detected. This may raise red flags for creditors and investors.\n")
            analysis.append("- Consider reviewing **IFRS 9** for credit risk classification and impairment models.\n"
                            "- High leverage can also reflect aggressive expansion, over-reliance on debt financing, or poor asset quality.\n"
                            "- Check liquidity, interest coverage ratios, and ensure covenant compliance.")

    if not analysis:
        return "❗ Not enough data for meaningful analysis."

    return '\n'.join(analysis)

# Show output
if query:
    financial_data = parse_financials(query)
    result = analyze(financial_data)
    st.subheader("📊 Analysis Result")
    st.text(result)


import streamlit as st
import pandas as pd
import re

# Set page config
st.set_page_config(page_title="FinDetect", layout="centered")

# Custom styling with dark navy background and light blue accents
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Share Tech Mono', monospace;
            background-color: #001f3f !important;
            color: #FFFFFF !important;
        }

        .stApp {
            background-color: #001f3f !important;
        }

        .stTextInput input {
            color: #FFFFFF;
            background-color: #005792;
            border: 1px solid #00BFFF;
        }

        .stButton>button {
            background-color: #005792;
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)

st.title("FinDetect: AI-Powered Financial Analysis for Auditors")

# Chat-based input
query = st.text_input("Paste a company's financial data or ask a question:")

# Sample logic for chat analysis
def parse_financials(text):
    # Basic number and keyword extraction
    numbers = re.findall(r'\d+[\,\.]?\d*', text.replace(',', ''))
    numbers = [float(n) for n in numbers if n.replace('.', '', 1).isdigit()]

    # Keyword-based detection
    keywords = {
        'Revenue': ['revenue', 'sales'],
        'COGS': ['cost of goods sold', 'cogs'],
        'Net Income': ['net income', 'profit after tax'],
        'Total Assets': ['total assets'],
        'Total Liabilities': ['total liabilities'],
        'Investment Property': ['investment property'],
        'Intangible Assets': ['intangible'],
        'Cash and Cash Equivalents': ['cash'],
        'Equity': ['equity']
    }

    results = {}
    for key, terms in keywords.items():
        for term in terms:
            if term in text.lower():
                index = text.lower().find(term)
                context = text[index:index+100]
                value_match = re.findall(r'\d+[\,\.]?\d*', context.replace(',', ''))
                if value_match:
                    results[key] = float(value_match[0])
                    break

    if len(results) == 0 and len(numbers) == 1:
        results['Single Value'] = numbers[0]

    return results

def analyze(financials):
    if not financials:
        return "Unable to extract enough financial data. Try again with more detail."

    analysis = []

    if 'Revenue' in financials and 'COGS' in financials:
        gpm = (financials['Revenue'] - financials['COGS']) / financials['Revenue'] * 100
        analysis.append(f"Gross Profit Margin: {gpm:.2f}%")

    if 'Net Income' in financials and 'Revenue' in financials:
        npm = financials['Net Income'] / financials['Revenue'] * 100
        analysis.append(f"Net Profit Margin: {npm:.2f}%")

    if 'Total Liabilities' in financials and 'Total Assets' in financials:
        dar = financials['Total Liabilities'] / financials['Total Assets'] * 100
        analysis.append(f"Debt to Asset Ratio: {dar:.2f}%")

        if dar > 70:
            analysis.append("High leverage detected. Consider IFRS 9 implications: credit risk, impairment provisioning, and going concern risks. Also assess whether the debt structure is sustainable and properly disclosed.")

    if 'Investment Property' in financials:
        analysis.append("Investment property detected. Ensure IFRS 13 (Fair Value Measurement) and IAS 40 (Investment Property) guidance are followed.")

    if 'Intangible Assets' in financials:
        analysis.append("Check if intangible assets comply with IAS 38, particularly regarding amortisation and impairment.")

    if 'Cash and Cash Equivalents' in financials:
        if financials['Cash and Cash Equivalents'] < 0:
            analysis.append("Negative cash balance detected — verify cash flow statement and reconciliation with bank confirmations.")

    if 'Equity' in financials and 'Total Assets' in financials:
        eq_ratio = financials['Equity'] / financials['Total Assets'] * 100
        analysis.append(f"Equity to Asset Ratio: {eq_ratio:.2f}%")

    if 'Single Value' in financials:
        analysis.append("Single figure detected. Please specify the account name (e.g. Investment Property 2024: 500000, 2025: 700000) for a more detailed analysis.")

    if len(analysis) == 0:
        return "Not enough recognizable data for analysis. Try specifying the line items (e.g., Revenue: 100000, Net Income: 25000)."

    return '\n'.join(analysis)

if query:
    financial_data = parse_financials(query)
    result = analyze(financial_data)
    st.subheader("Analysis Result")
    st.text(result)


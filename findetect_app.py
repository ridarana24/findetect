import streamlit as st
import pandas as pd
import re

# Set page config
st.set_page_config(page_title="FinDetect", layout="centered")

# Custom styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Varela+Round&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Varela Round', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }
        .stTextInput input {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("FinDetect: AI-Powered Financial Analysis")

# Chat-based input
query = st.text_input("Paste a company's financial data or ask a question:")

# Sample logic for chat analysis
def parse_financials(text):
    # Basic number extraction
    numbers = re.findall(r'\d+[\,\.]?\d*', text.replace(',', ''))
    numbers = [float(n) for n in numbers if n.replace('.', '', 1).isdigit()]

    # Dummy structure: assume order [Revenue, COGS, Net Income, Total Assets, Total Liabilities]
    results = {}
    if len(numbers) >= 5:
        results['Revenue'] = numbers[0]
        results['COGS'] = numbers[1]
        results['Net Income'] = numbers[2]
        results['Total Assets'] = numbers[3]
        results['Total Liabilities'] = numbers[4]
    return results

def analyze(financials):
    if not financials:
        return "Unable to extract enough financial data. Try again with more details."

    analysis = []
    # Gross Profit Margin
    if 'Revenue' in financials and 'COGS' in financials:
        gpm = (financials['Revenue'] - financials['COGS']) / financials['Revenue'] * 100
        analysis.append(f"Gross Profit Margin: {gpm:.2f}%")

    # Net Profit Margin
    if 'Net Income' in financials and 'Revenue' in financials:
        npm = financials['Net Income'] / financials['Revenue'] * 100
        analysis.append(f"Net Profit Margin: {npm:.2f}%")

    # Debt to Asset Ratio
    if 'Total Liabilities' in financials and 'Total Assets' in financials:
        dar = financials['Total Liabilities'] / financials['Total Assets'] * 100
        analysis.append(f"Debt to Asset Ratio: {dar:.2f}%")

        # IFRS-based suggestion
        if dar > 70:
            analysis.append("⚠️ High leverage detected. Consider reviewing IFRS 9 for credit risk implications.")

    if len(analysis) == 0:
        return "Not enough info for analysis. Please provide more financial details."

    return '\n'.join(analysis)

if query:
    financial_data = parse_financials(query)
    result = analyze(financial_data)
    st.subheader("Analysis Result")
    st.text(result)


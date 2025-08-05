import streamlit as st
import re

# Set custom page config
st.set_page_config(page_title="FinDetect Pro", page_icon="📈", layout="centered")

# Apply custom CSS for background and font
st.markdown("""
    <style>
    body {
        background-color: #001f3f;
        color: white;
        font-family: 'Varela Round', sans-serif;
    }
    .stTextInput>div>div>input {
        background-color: #0074D9;
        color: white;
    }
    .stButton>button {
        background-color: #0074D9;
        color: white;
        border-radius: 8px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #7FDBFF;
    }
    </style>
""", unsafe_allow_html=True)

# Title & description
st.markdown("""
    <h1>📈 FinDetect Pro</h1>
    <p>Advanced Financial Statement Analyzer with IFRS logic, risk scoring, and insights.</p>
    <img src="https://i.imgur.com/2nCt3Sb.png" alt="Finance" width="100%">
""", unsafe_allow_html=True)

# --- Analysis Function ---
def analyze(financials):
    if not financials:
        return "Unable to extract enough financial data. Try again with more details."

    analysis = []
    risk_flags = []

    # Gross Profit Margin
    if 'Revenue' in financials and 'COGS' in financials:
        gpm = (financials['Revenue'] - financials['COGS']) / financials['Revenue'] * 100
        analysis.append(f"Gross Profit Margin: {gpm:.2f}%")
        if gpm < 20:
            risk_flags.append("Low gross margin may indicate pricing pressure or high production costs.")

    # Net Profit Margin
    if 'Net Income' in financials and 'Revenue' in financials:
        npm = financials['Net Income'] / financials['Revenue'] * 100
        analysis.append(f"Net Profit Margin: {npm:.2f}%")
        if npm > 100:
            risk_flags.append("Unusually high net margin — verify if data includes one-off gains or accounting anomalies.")

    # Debt to Asset Ratio
    if 'Total Liabilities' in financials and 'Total Assets' in financials:
        dar = financials['Total Liabilities'] / financials['Total Assets'] * 100
        analysis.append(f"Debt to Asset Ratio: {dar:.2f}%")

        if dar > 70:
            risk_level = "🔴 High Risk"
            explanation = (
                f"{risk_level} – Leverage exceeds 70%, suggesting over-reliance on debt financing. "
                "This increases insolvency risk and reduces financial flexibility. "
                "Per IFRS 9, assess expected credit losses (ECL), especially if assets are under stress. "
                "Entity may move to Stage 2 or 3 under IFRS 9 if there's significant increase in credit risk or default probability. "
                "High leverage may breach loan covenants, trigger refinancing issues, and lead to a downgrade in credit ratings. "
                "Also assess interest coverage and operating cash flow to ensure debt sustainability."
            )
            analysis.append(explanation)

    # Summary
    if len(analysis) == 0:
        return "Not enough info for analysis. Please provide more financial details."

    if risk_flags:
        analysis.append("\n⚠️ Additional Flags:")
        analysis.extend([f"- {flag}" for flag in risk_flags])

    return '\n'.join(analysis)

# --- Input Method ---
st.markdown("### Enter Financial Data:")
user_input = st.text_area("Paste key financial figures (e.g., Revenue: 1000000, Net Income: 200000, COGS: 600000, etc.)")

# --- Extract Numbers ---
def extract_financials(text):
    pattern = r"([A-Za-z ]+):\s*([\d,.]+)"
    matches = re.findall(pattern, text)
    financials = {}
    for key, value in matches:
        key_clean = key.strip()
        value_clean = float(value.replace(",", ""))
        financials[key_clean] = value_clean
    return financials

# --- Analyze Button ---
if st.button("Analyze"):
    data = extract_financials(user_input)
    result = analyze(data)
    st.markdown("### 📊 Analysis Result:")
    st.code(result)
    st.markdown("""
        <img src="https://i.imgur.com/WtXG5pJ.png" alt="Risk Chart" width="100%">
    """, unsafe_allow_html=True)

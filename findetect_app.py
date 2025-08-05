import streamlit as st
import pandas as pd
import re

# Set page config
st.set_page_config(page_title="FinDetect", layout="centered")

# Custom styling with dark navy background and bright text
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Share Tech Mono', monospace;
            background-color: #001f3f !important;
            color: white !important;
        }

        .stApp {
            background-color: #001f3f !important;
        }

        .stTextInput input {
            color: white;
            background-color: #87cefa;
            border: 1px solid white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("FinDetect: AI-Powered Financial Analysis")

query = st.text_input("Paste line items and year-on-year values:")

# IFRS/IAS mapping for advanced analysis
ifrs_guidance = {
    "Investment Property": {
        "standards": ["IAS 40", "IFRS 13"],
        "notes": "Investment property should be measured at fair value. Significant increases may indicate revaluation or acquisition. Check appraisal reports, acquisition records, and ensure fair value hierarchy disclosures are met."
    },
    "Revenue": {
        "standards": ["IFRS 15"],
        "notes": "Revenue changes may stem from volume/price fluctuations, or changes in recognition policy. Cross-check contracts and timing of recognition."
    },
    "COGS": {
        "standards": ["IAS 2"],
        "notes": "Increase in COGS might reflect rising costs or inventory issues. Review inventory valuation, supplier contracts, and pricing trends."
    },
    "Net Income": {
        "standards": ["IAS 1"],
        "notes": "Large fluctuations in net income should be traced to operating, financing, or tax components. Inspect notes, tax returns, and financing costs."
    },
    "Total Assets": {
        "standards": ["IAS 1"],
        "notes": "Check for asset acquisitions, revaluations, or disposals. Trace to non-current asset schedules and revaluation reports."
    },
    "Total Liabilities": {
        "standards": ["IFRS 9", "IAS 1"],
        "notes": "Increase may indicate borrowings or changes in financial liabilities. Check loan agreements, maturities, and classification."
    },
    "PPE": {
        "standards": ["IAS 16"],
        "notes": "Ensure depreciation and revaluation are correctly applied. Large changes should be traced to capex or disposal records."
    }
}

def parse_yearly_change(text):
    lines = re.split(r'[\n,;]+', text)
    results = []
    for line in lines:
        match = re.match(r'(.*?)\s*2024\D*(\d+[.,]?\d*)\D*2025\D*(\d+[.,]?\d*)', line, re.IGNORECASE)
        if match:
            item = match.group(1).strip()
            val_2024 = float(match.group(2).replace(',', ''))
            val_2025 = float(match.group(3).replace(',', ''))
            change_pct = ((val_2025 - val_2024) / val_2024) * 100 if val_2024 else 0
            results.append((item, val_2024, val_2025, change_pct))
    return results

def advanced_analysis(results):
    if not results:
        return "Not enough financial data detected. Please follow format like 'Investment Property 2024: 5000, 2025: 6000'"

    output = []
    for item, y1, y2, change in results:
        formatted_change = f"{change:.2f}%"
        color = "red" if abs(change) > 3 else "white"

        output.append(f"\n**{item}**\n2024: {y1}, 2025: {y2}\n<span style='color:{color}'>Change: {formatted_change}</span>")

        if item in ifrs_guidance:
            standards = ", ".join(ifrs_guidance[item]['standards'])
            output.append(f"Relevant Standards: {standards}")
            output.append(f"Recommendations: {ifrs_guidance[item]['notes']}")
            if abs(change) > 3:
                output.append("⚠️ Significant change detected. Further audit investigation advised.")
        elif abs(change) > 3:
            output.append("⚠️ Unmapped item with large fluctuation. Consider cross-checking related notes or disclosures.")

    return '\n\n'.join(output)

if query:
    parsed = parse_yearly_change(query)
    result = advanced_analysis(parsed)
    st.subheader("Analysis Result")
    st.markdown(result, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
from openai import OpenAI

# Use local LM Studio API
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

# Page config
st.set_page_config(page_title="FinDetect", layout="wide")

# Styling (Share Tech Mono)
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

st.title("FinDetect: AI-Powered Financial Analysis & Audit Engine")

query = st.text_input("Paste financial items with 2024 and 2025 values:")

# Financial Ratios
ratios = {
    "ROCE": lambda data: (data.get("Net Profit", 0) / (data.get("Total Assets", 1) - data.get("Current Liabilities", 0)) * 100),
    "Gross Profit Margin": lambda data: ((data.get("Revenue", 0) - data.get("COGS", 0)) / data.get("Revenue", 1) * 100),
    "Net Profit Margin": lambda data: (data.get("Net Profit", 0) / data.get("Revenue", 1) * 100),
    "Debt to Equity": lambda data: (data.get("Total Liabilities", 0) / max(data.get("Share Capital", 1), 1)),
    "Current Ratio": lambda data: (data.get("Current Assets", 0) / max(data.get("Current Liabilities", 1), 1)),
    "Quick Ratio": lambda data: ((data.get("Current Assets", 0) - data.get("Inventory", 0)) / max(data.get("Current Liabilities", 1), 1)),
    "Asset Turnover": lambda data: (data.get("Revenue", 0) / max(data.get("Total Assets", 1), 1)),
    "Return on Assets (ROA)": lambda data: (data.get("Net Profit", 0) / max(data.get("Total Assets", 1), 1) * 100),
    "Equity Ratio": lambda data: (data.get("Share Capital", 0) / max(data.get("Total Assets", 1), 1) * 100)
}

# IFRS Audit Guidance
ifrs_guidance = {
    "Investment Property": {"standards": ["IAS 40", "IFRS 13"], "notes": "Fair value, revaluation or acquisition reviewed."},
    "Revenue": {"standards": ["IFRS 15"], "notes": "Check recognition timing, volume/price, contracts."},
    "COGS": {"standards": ["IAS 2"], "notes": "Rising COGS may indicate cost or inventory issues."},
    "Net Profit": {"standards": ["IAS 1"], "notes": "Check operating and tax drivers."},
    "Total Assets": {"standards": ["IAS 1"], "notes": "Review acquisitions, disposals, revaluations."},
    "Total Liabilities": {"standards": ["IFRS 9", "IAS 1"], "notes": "Check borrowings, changes in financial liabilities."},
    "PPE": {"standards": ["IAS 16"], "notes": "Capex, disposal, depreciation analysis."},
    "Intangible Assets": {"standards": ["IAS 38"], "notes": "Impairment, amortisation, acquisition review."},
    "Leases": {"standards": ["IFRS 16"], "notes": "Right-of-use and lease liabilities."},
    "Provisions": {"standards": ["IAS 37"], "notes": "Ensure proper recognition and reasonableness."},
    "Deferred Tax": {"standards": ["IAS 12"], "notes": "Correct tax base and recognition."},
    "Financial Instruments": {"standards": ["IFRS 9"], "notes": "Classification, measurement, impairment."},
    "Inventory": {"standards": ["IAS 2"], "notes": "Costing method and write-downs."},
    "Borrowings": {"standards": ["IFRS 9"], "notes": "Check interest rate terms and disclosures."},
    "Goodwill": {"standards": ["IAS 36"], "notes": "Test annually for impairment."},
    "Retained Earnings": {"standards": ["IAS 1"], "notes": "Understand profit movements and dividend payouts."},
    "Share Capital": {"standards": ["IAS 32"], "notes": "Disclosure of share movements and classification."},
    "Cash and Cash Equivalents": {"standards": ["IAS 7"], "notes": "Ensure classification and cash flow alignment."},
    "Other Comprehensive Income": {"standards": ["IAS 1"], "notes": "Reconcile to equity movements and items."},
    "Biological Assets": {"standards": ["IAS 41"], "notes": "Measure at fair value less costs to sell."},
    "Employee Benefits": {"standards": ["IAS 19"], "notes": "Defined benefit obligations and disclosures."}
}

# Parse Input
def parse_yearly_change(text):
    pattern = r'(.*?)\s*(?:2024|in 2024|was in 2024|for 2024)[:\s-]*([\d,.]+)[^\d]+(?:2025|in 2025|was in 2025|for 2025)[:\s-]*([\d,.]+)'
    results = []
    for line in re.split(r'[\n;]+', text):
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            try:
                item = match.group(1).strip().rstrip(':')
                val_2024 = float(match.group(2).replace(',', ''))
                val_2025 = float(match.group(3).replace(',', ''))
                change_pct = ((val_2025 - val_2024) / val_2024) * 100 if val_2024 else 0
                results.append((item, val_2024, val_2025, change_pct))
            except:
                continue
    return results

# AI from Local Model
def get_ai_insight(text):
    try:
        response = client.chat.completions.create(
            model="local-model",  # LM Studio ignores this
            messages=[
                {"role": "system", "content": "You're a forensic audit AI. Assess risk, audit scenarios, ISA relevance and fraud flags."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI engine error: {e}"

# Chart
def show_chart(results):
    if results:
        df = pd.DataFrame(results, columns=["Item", "2024", "2025", "% Change"])
        df.set_index("Item")[["2024", "2025"]].plot(kind='bar')
        st.pyplot(plt.gcf())
        plt.clf()

# Advanced Analysis
def advanced_analysis(results):
    if not results:
        return "<span style='color:red'>⚠️ Not enough data. Try: 'PPE in 2024: 5000, 2025: 4800'</span>"

    output = []
    data_2025 = {item: y2 for item, _, y2, _ in results}

    for item, y1, y2, change in results:
        formatted_change = f"{change:.2f}%"
        color = "red" if abs(change) > 3 else "white"

        output.append(f"\n**{item}**\n2024: {y1}, 2025: {y2}\n<span style='color:{color}'>Change: {formatted_change}</span>")

        if item in ifrs_guidance:
            standards = ", ".join(ifrs_guidance[item]['standards'])
            output.append(f"IFRS Standards: {standards}")
            output.append(f"Audit Checklist: {ifrs_guidance[item]['notes']}")
            if abs(change) > 3:
                output.append("⚠️ Significant fluctuation. Deep audit needed.")
        elif abs(change) > 3:
            output.append("⚠️ Unmapped line with abnormal change. Review manually.")

        ai_advice = get_ai_insight(f"{item} changed from {y1} to {y2}. Provide audit risks, relevant IFRS/IAS, fraud red flags, and checklist items.")
        output.append(f"\n**AI Mastermind Audit Engine:**\n{ai_advice}")

    output.append("\n---\n**📈 Key Financial Ratios for 2025:**")
    for name, func in ratios.items():
        try:
            ratio_val = func(data_2025)
            output.append(f"{name}: {ratio_val:.2f}%")
        except:
            continue

    return '\n\n'.join(output)

# Run
if query:
    parsed = parse_yearly_change(query)
    result = advanced_analysis(parsed)
    st.subheader("📊 Analysis Result")
    st.markdown(result, unsafe_allow_html=True)
    show_chart(parsed)







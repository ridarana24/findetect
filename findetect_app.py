import streamlit as st
from openai import OpenAI
import re

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're an AI-powered expert auditor with full knowledge of IFRS/IAS standards, auditing practices, red flag detection, and financial analysis. You can understand vague inputs like 'sales increased slightly' or 'investment property stayed same', and you compute ratios like ROCE, gross profit margin, debt-equity, etc."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"\n❌ AI Error:\n\n{e}"

def parse_yearly_change(text):
    match = re.search(r"(.*?)\s*2024[\s:,-]*([\d,]+)[^\d]+2025[\s:,-]*([\d,]+)", text, re.IGNORECASE)
    if match:
        item = match.group(1).strip()
        val_2024 = float(match.group(2).replace(",", ""))
        val_2025 = float(match.group(3).replace(",", ""))
        return item, val_2024, val_2025
    return None, None, None

st.set_page_config(page_title="FinDetect AI", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Archivo Black', sans-serif;
        background-color: #001f3f;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff11;
        color: white;
    }
    .stTextInput>div>div>input::placeholder {
        color: #bbb;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 FinDetect AI - Auditing Mastermind")

query = st.text_input("Ask anything about financial data, trends, audit risks, or IFRS standards:")

if query:
    item, val_2024, val_2025 = parse_yearly_change(query)
    if item and val_2024 is not None and val_2025 is not None:
        change = ((val_2025 - val_2024) / val_2024) * 100 if val_2024 != 0 else 0
        color = "red" if abs(change) > 3 else "white"
        st.markdown(f"**{item}** YoY Change: <span style='color:{color}'>**{change:.2f}%**</span>", unsafe_allow_html=True)

        ai_prompt = (
            f"You are reviewing financials. Item: {item}, 2024: {val_2024}, 2025: {val_2025}. Year-over-year change: {change:.2f}%\n"
            f"Provide detailed audit recommendations, flag any red flags, and list potential IFRS/IAS standards affected.\n"
            f"Compute financial ratios where applicable like ROCE, Gross/Net Profit, Debt-Equity.\n"
            f"Also explain audit scenarios for this kind of change, offer controls to test, and give comparative analysis."
        )
        ai_response = ask_ai(ai_prompt)

        st.markdown("---")
        st.subheader("💬 AI Insight:")
        st.markdown(ai_response)
    else:
        vague_prompt = (
            f"{query}\n"
            f"Interpret this vague statement using your auditing intelligence. Identify relevant financial elements, red flags, standards (IFRS/IAS), audit procedures, controls, and risk impact."
        )
        ai_response = ask_ai(vague_prompt)
        st.markdown("---")
        st.subheader("💬 AI Interpretation:")
        st.markdown(ai_response)







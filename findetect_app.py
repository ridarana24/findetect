import streamlit as st
import openai
import re

# ✅ Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ✅ Function to ask OpenAI using new syntax
def ask_ai(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "You're an AI-powered expert auditor with full knowledge of IFRS/IAS standards, "
                    "auditing practices, red flag detection, and financial analysis. "
                    "You understand vague inputs like 'sales increased slightly' or 'investment property stayed same', "
                    "and you compute ratios like ROCE, gross/net profit margin, debt-equity, etc."
                )},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"\n❌ AI Error:\n\n{e}"

# ✅ Function to extract item and year-wise values
def parse_yearly_change(text):
    match = re.search(r"(.*?)\s*2024[\s:,-]*([\d,]+)[^\d]+2025[\s:,-]*([\d,]+)", text, re.IGNORECASE)
    if match:
        item = match.group(1).strip()
        val_2024 = float(match.group(2).replace(",", ""))
        val_2025 = float(match.group(3).replace(",", ""))
        return item, val_2024, val_2025
    return None, None, None

# ✅ Streamlit config and styling
st.set_page_config(page_title="FinDetect AI", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Varela+Round&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Varela Round', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 FinDetect AI - Auditing Mastermind")

# ✅ Main input
query = st.text_input("Ask anything about financial data, trends, audit risks, or IFRS standards:")

if query:
    item, val_2024, val_2025 = parse_yearly_change(query)
    
    if item and val_2024 is not None and val_2025 is not None:
        change = ((val_2025 - val_2024) / val_2024) * 100 if val_2024 != 0 else 0
        color = "red" if abs(change) > 3 else "black"

        st.markdown(f"**{item}** YoY Change: <span style='color:{color}'>**{change:.2f}%**</span>", unsafe_allow_html=True)

        ai_prompt = (
            f"You are reviewing financials. Item: {item}, 2024: {val_2024}, 2025: {val_2025}. "
            f"Year-over-year change: {change:.2f}%\n\n"
            f"👉 Provide audit insights, red flags, IFRS/IAS standards triggered.\n"
            f"👉 Compute ratios like ROCE, Gross/Net Profit, Debt-Equity.\n"
            f"👉 Suggest audit procedures and internal controls.\n"
            f"👉 Provide comparative analysis."
        )
        ai_response = ask_ai(ai_prompt)

        st.markdown("---")
        st.subheader("💬 AI Insight:")
        st.markdown(ai_response)

    else:
        vague_prompt = (
            f"{query}\n\n"
            f"👉 Interpret this vague statement using auditing intelligence.\n"
            f"👉 Identify financial line items, risks, ratios, IFRS/IAS triggers.\n"
            f"👉 Suggest audit procedures, red flags, controls, and advice."
        )
        ai_response = ask_ai(vague_prompt)
        
        st.markdown("---")
        st.subheader("💬 AI Interpretation:")
        st.markdown(ai_response)







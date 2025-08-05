import streamlit as st
import openai
import re

# Set your app title
st.set_page_config(page_title="FinDetect AI - Audit Assistant", page_icon="📊", layout="centered")

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["general"]["OPENAI_API_KEY"]

# Custom styles
st.markdown("""
    <style>
    body {background-color: #0b1a36;}
    .stApp {background-color: #0b1a36; color: white; font-family: 'Varela Round', sans-serif;}
    .stTextInput > div > div > input {background-color: #1f3a5f; color: white; border-radius: 10px;}
    .css-1aumxhk {background-color: #1f3a5f; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 FinDetect AI: Auditor's Intelligence Engine")
st.write("Ask any financial or audit-related question and get smart analysis backed by IFRS & IAS standards.")

# --- AI Chat Function --- #
def ask_financial_ai(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a powerful AI auditing assistant. Interpret vague or exact financial data and give deep insight per IFRS/IAS. Provide recommendations, possible red flags, and what an auditor should check."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# --- Simple Ratio Analysis (Optional Supplement) --- #
def parse_yearly_change(query):
    match = re.search(r"(.+)\s+(2024):\s*(\d+[,.]?\d*)[,\s]+(2025):\s*(\d+[,.]?\d*)", query, re.IGNORECASE)
    if match:
        item = match.group(1).strip()
        val_2024 = float(match.group(3).replace(',', ''))
        val_2025 = float(match.group(5).replace(',', ''))
        percent_change = ((val_2025 - val_2024) / val_2024) * 100 if val_2024 != 0 else 0
        color = "red" if abs(percent_change) > 3 else "white"
        return f"<b style='color:{color}'>{item} YoY Change:</b> {percent_change:.2f}%", item, val_2024, val_2025, percent_change
    else:
        return "⚠️ Not enough data. Try: 'PPE in 2024: 5000, 2025: 4800'", None, None, None, None

# --- User Input --- #
user_input = st.text_input("🔍 Enter financial data or audit question:")

if user_input:
    # Step 1: Try parsing as a financial YoY input
    parse_result, item, v2024, v2025, change = parse_yearly_change(user_input)
    st.markdown(parse_result, unsafe_allow_html=True)

    # Step 2: AI analysis
    st.markdown("### 💬 AI Insight:")
    ai_response = ask_financial_ai(user_input)
    st.write(ai_response)

    # Step 3 (Optional): Additional rule-based logic
    if item:
        if item.lower() == "investment property":
            st.markdown("---")
            st.markdown("**🔎 Additional IFRS Checks for Investment Property**")
            if change > 3:
                st.write("Increase detected in Investment Property. Possible reasons:")
                st.write("- Fair value gains (check revaluation method under IFRS 13).")
                st.write("- Purchase of new property (check capital expenditure records).")
                st.write("- Reclassification from PPE (verify IAS 40 conditions).")
            elif change < -3:
                st.write("Decrease detected. Investigate:")
                st.write("- Disposals (verify sale agreements and derecognition under IFRS 13).")
                st.write("- Impairments (apply IAS 36 impairment review).")
            else:
                st.write("No significant change in Investment Property. Cross-check disclosures and revaluation policy consistency.")

            st.write("Always ensure IFRS 13 (Fair Value Measurement) and IAS 40 are appropriately disclosed and applied.")






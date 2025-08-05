import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re

# Set page config
st.set_page_config(page_title="FinDetect", layout="centered")

# Inject Matrix-style background with falling green code
components.html("""
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: black;
        }

        canvas {
            position: fixed;
            top: 0;
            left: 0;
            z-index: -1;
        }

        .matrix-text {
            font-family: 'Share Tech Mono', monospace;
            color: #00FF41 !important;
        }
    </style>
    <canvas id="matrixCanvas"></canvas>
    <script>
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');

        canvas.height = window.innerHeight;
        canvas.width = window.innerWidth;

        let chars = "アァイィウエカキクケコサシスセソタチッツテトナニヌネノ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        chars = chars.split("");

        let fontSize = 14;
        let columns = canvas.width / fontSize;
        let drops = [];

        for (let x = 0; x < columns; x++)
            drops[x] = 1;

        function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#0F0";
            ctx.font = fontSize + "px 'Share Tech Mono'";

            for (let i = 0; i < drops.length; i++) {
                let text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975)
                    drops[i] = 0;

                drops[i]++;
            }
        }

        setInterval(draw, 33);
        window.onresize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
    </script>
""", height=0)

# Inject font and text input styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        html, body, [class*="css"] {
            font-family: 'Share Tech Mono', monospace !important;
            color: #00FF41 !important;
        }

        .stTextInput input, .stTextArea textarea {
            background-color: #000000 !important;
            color: #00FF41 !important;
            border: 1px solid #00FF41 !important;
        }

        .stTextInput label, .stTextArea label, .stSubheader, .stTitle {
            color: #00FF41 !important;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
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
            analysis.append("High leverage detected. Consider reviewing IFRS 9 for credit risk implications.")

    if len(analysis) == 0:
        return "Not enough info for analysis. Please provide more financial details."

    return '\n'.join(analysis)

if query:
    financial_data = parse_financials(query)
    result = analyze(financial_data)
    st.subheader("Analysis Result")
    st.text(result)

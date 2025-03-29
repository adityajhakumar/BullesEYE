import streamlit as st
import yfinance as yf
import pandas as pd
from openai import OpenAI

# --- Streamlit App Configuration ---
st.set_page_config(page_title="📈 AI Stock Screener", layout="wide")
st.markdown(
    "<h1 style='text-align: center; font-size: 48px;'>🎯 Bullseye AI</h1>", 
    unsafe_allow_html=True
)

# --- Secure API Key (Use Streamlit Secrets) ---
DEEPSEEK_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=DEEPSEEK_API_KEY
)

# --- Fetch Stock Data Function ---
@st.cache_data
def fetch_stock_data(stock_symbol, period="5y"):
    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period=period)
        return hist if not hist.empty else None
    except Exception:
        return None

# --- Fetch Resilient Indian Stocks ---
@st.cache_data
def get_resilient_indian_stocks():
    indian_stocks = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "BAJFINANCE.NS",
                     "HINDUNILVR.NS", "ASIANPAINT.NS", "KOTAKBANK.NS", "LT.NS", "ICICIBANK.NS"]

    stock_data = []

    for stock in indian_stocks:
        df = fetch_stock_data(stock, "10y")
        if df is None:
            continue

        max_price = df["Close"].max()
        min_price = df["Close"].min()
        last_price = df["Close"][-1]
        dip_recovery = ((max_price - min_price) / max_price) * 100
        current_recovery = ((last_price - min_price) / (max_price - min_price)) * 100

        if dip_recovery > 30 and current_recovery > 70:  
            stock_data.append({
                "Stock": stock.replace(".NS", ""),
                "Max Price": round(max_price, 2),
                "Min Price": round(min_price, 2),
                "Current Price": round(last_price, 2),
                "Recovery %": round(current_recovery, 2),
                "Dip %": round(dip_recovery, 2)
            })

    return pd.DataFrame(stock_data)

# --- Sidebar: User Preferences ---
st.sidebar.header("📊 Customize Your AI Analysis")

investor_type = st.sidebar.selectbox("What type of investor are you?", 
                                     ["Long-Term", "Short-Term", "Growth", "Dividend", "Value", "Speculative"])

user_priority = st.sidebar.multiselect("What matters most to you?", 
                                       ["Risk", "Growth", "Valuation", "Dividends", "Market Trends", "Competitor Comparison"])

# --- Sidebar: Stock Selection ---
st.sidebar.header("🔍 Select or Enter a Stock")
resilient_stocks_df = get_resilient_indian_stocks()
stock_list = resilient_stocks_df["Stock"].tolist()

selected_stock = st.sidebar.selectbox("Select a Stock from the List", stock_list)
manual_stock = st.sidebar.text_input("Or Enter a Stock Symbol (e.g., TCS.NS)")

# --- Auto-Select Stock from Table ---
st.subheader("📋 Top Resilient Stocks in India (Last 10 Years)")
st.write("Click a stock to analyze it.")

selected_stock_from_table = st.data_editor(
    resilient_stocks_df,
    use_container_width=True,
    column_config={"Stock": st.column_config.TextColumn("📌 Click to Select")},
    disabled=["Max Price", "Min Price", "Current Price", "Recovery %", "Dip %"],
)

# --- Final Stock Selection Logic (Corrected) ---
if manual_stock.strip():  # If user manually enters a stock
    final_stock = manual_stock.upper().strip()
    if "." not in final_stock:  # Append ".NS" if missing
        final_stock += ".NS"
else:
    if selected_stock_from_table is not None and not selected_stock_from_table.empty:
        selected_stock = selected_stock_from_table["Stock"].iloc[0]
    final_stock = selected_stock + ".NS"

st.sidebar.success(f"✅ Selected Stock: {final_stock}")

# --- AI Stock Analysis Function ---
def analyze_stock_with_ai(stock_symbol, investor_type, user_priority):
    priority_str = ", ".join(user_priority) if user_priority else "General Analysis"

    prompt = f"""
    Analyze the stock {stock_symbol} based on user preferences.

    User is a **{investor_type} investor**. 
    Their top priorities are: **{priority_str}**.

    Perform a deep analysis covering:

    1️⃣ **Historical Performance**
       - Key price trends over the past 5-10 years.
       - Major growth phases and downturns.
       - Dividend history (if applicable).

    2️⃣ **Recent Stock Decline Analysis**
       - Identify reasons for recent price drops.
       - Economic & sector-specific impact.

    3️⃣ **Future Growth Potential**
       - Revenue projections and expected earnings growth.
       - Competitive advantage vs. industry peers.

    4️⃣ **Investment Risks**
       - Market risks, legal risks, macroeconomic factors.

    5️⃣ **Final Investment Recommendation**
       - **BUY, HOLD, or SELL** with a detailed explanation.

    The response should be structured and relevant to the user's investment style.
    """

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI Analysis Error: {str(e)}"

# --- Stock Analysis Button ---
if st.sidebar.button("Analyze Stock"):
    with st.spinner("Fetching stock data and analyzing..."):
        hist_data = fetch_stock_data(final_stock)

        if hist_data is None:
            st.error("❌ Invalid stock symbol or no data available.")
        else:
            st.subheader(f"📊 {final_stock} Stock Performance (Last 5 Years)")
            st.line_chart(hist_data['Close'])

            st.subheader("🤖 AI-Powered Investment Analysis")
            ai_analysis = analyze_stock_with_ai(final_stock, investor_type, user_priority)
            st.write(ai_analysis)

# --- AI Chatbot: Persistent Chat History ---
st.subheader("💬 Chat with AI for More Insights")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": "You are a financial AI assistant helping users analyze stocks."}]

user_query = st.text_input("Ask AI a follow-up question:")

if st.button("Ask AI"):
    if user_query.strip():
        with st.spinner("AI is analyzing..."):
            chat_prompt = f"User asked about {final_stock}: {user_query}"

            chat_response = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=[{"role": "user", "content": chat_prompt}]
            )

            response_text = chat_response.choices[0].message.content
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

            for chat in st.session_state.chat_history[-5:]:  # Display only last 5 messages
                role = "👤" if chat["role"] == "user" else "🤖"
                st.write(f"{role} {chat['content']}")

    else:
        st.warning("Please enter a question before clicking 'Ask AI'.")
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 16px;
            color: gray;
        }
    </style>
    <div class='footer'>Made with ❤️ by <b>ServerSync</b></div>
    """,
    unsafe_allow_html=True
)

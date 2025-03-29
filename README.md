### 📈 Bullseye AI - AI Stock Screener

# Description

**Bullseye AI** is an advanced, user-friendly **AI-powered stock screener** built with **Streamlit**. This app helps investors analyze the performance of Indian stocks over the past decade and generates personalized investment insights using **OpenAI’s GPT model** via **OpenRouter API**.

It allows users to:
- 📊 **Fetch historical stock data** for Indian companies over the last 10 years.
- 🎯 **Identify resilient stocks** based on their recovery from dips and overall growth.
- 🔍 **Perform AI-based stock analysis** based on user preferences such as growth, risk, valuation, dividends, etc.
- 💬 **Interact with an AI chatbot** for continuous and dynamic investment-related discussions.

The app is perfect for investors of all types: **Long-Term, Short-Term, Growth, Dividend, Value, and Speculative**.

---

## Features

- 📈 **Stock Data Fetching:** Retrieve historical stock data via **Yahoo Finance API**.
- 📌 **Top Resilient Indian Stocks:** Automatically detect resilient stocks based on their recovery rate and performance.
- 🤖 **AI-Powered Analysis:** Analyze stocks with **OpenAI’s GPT model** considering user’s investment style and preferences.
- 💬 **AI Chatbot:** Ask follow-up questions to gain deeper insights about your selected stocks.
- ⚙️ **Streamlit Interface:** Interactive, fast, and visually appealing web app.
- 📊 **Dynamic Data Visualization:** View stock performance trends via line charts.
- 🔍 **Customize Analysis:** Choose investment style and priorities to personalize AI-generated insights.
- 📂 **Persistent Chat History:** Continue conversations with the AI for a seamless experience.

---

## Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** OpenAI GPT Model via OpenRouter API
- **Data Source:** Yahoo Finance (`yfinance`)
- **Visualization:** Streamlit's built-in charting tools
- **Environment:** Python 3.x

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/bullseye-ai.git
cd bullseye-ai
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Add your OpenAI API Key to Streamlit Secrets:**
```bash
mkdir -p .streamlit
echo "[secrets]" > .streamlit/secrets.toml
echo "DEEPSEEK_API_KEY = 'sk-xxx...'" >> .streamlit/secrets.toml
```

4. **Run the Streamlit app:**
```bash
streamlit run app.py
```

---

## Usage

1. **Select your investor type:** Choose from Long-Term, Short-Term, Growth, Dividend, Value, or Speculative.
2. **Select stock priorities:** Pick your preferred focus areas like Growth, Risk, Valuation, etc.
3. **Choose or enter a stock symbol:** Either select from a list of resilient stocks or manually input a stock symbol.
4. **Analyze the stock:** Click the 'Analyze Stock' button to view AI-generated insights.
5. **Chat with AI:** Ask follow-up questions for deeper insights.

---

## Requirements

- **Python 3.8+**
- **Streamlit**
- **yfinance**
- **OpenAI (via OpenRouter API)**
- **Pandas**

---

## License

This project is licensed under the **MIT License**.

---

## Future Enhancements

- 📊 **Technical Analysis:** Include common indicators like RSI, MACD, Moving Averages, etc.
- 💼 **Portfolio Analysis:** Allow users to input multiple stocks for overall portfolio assessment.
- 🌍 **Multi-Market Support:** Expand support to include stocks from US, Europe, and other markets.
- 📝 **Export Reports:** Allow users to export analysis as PDFs or Excel files.

---

## Author

Developed with ❤️ by **ServerSync**.  



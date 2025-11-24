# 📈 CAC 40 Sentiment Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B)
![Finance](https://img.shields.io/badge/Finance-CAC40-green)

## ℹ️ About
This project is a financial dashboard built to monitor the sentiment of news regarding **CAC 40** companies. It helps investors gauge the "market mood" by analyzing news headlines using NLP techniques adapted for the French language.

**Key Features:**
- 📊 **Real-time Dashboard:** Built with Streamlit.
- 📰 **News Aggregation:** Fetches latest Google News RSS feeds for major French stocks.
- 🧠 **NLP Engine:** Uses `TextBlob-FR` to score news polarity (-1 to +1).
- 📉 **Market Data:** Integrates price history via `yfinance`.

## 🚀 How to Run

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/TON_USER/cac40-sentiment-analyzer.git](https://github.com/TON_USER/cac40-sentiment-analyzer.git)
   cd cac40-sentiment-analyzer

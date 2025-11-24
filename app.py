import streamlit as st
import pandas as pd
import yfinance as yf
from utils.data_loader import get_stock_data, get_company_news
from utils.sentiment import analyze_sentiment
from utils.visualizer import create_sentiment_gauge, create_candlestick_chart
import plotly.graph_objects as go

# Configuration: Top 10 CAC 40 Tickers
CAC40_TICKERS = {
    "LVMH": "MC.PA",
    "Orange": "OR.PA",
    "TotalEnergies": "TTE.PA",
    "Sanofi": "SAN.PA",
    "Airbus": "AIR.PA",
    "AXA": "CS.PA",
    "BNP Paribas": "BNP.PA",
    "Société Générale": "GLE.PA",
    "Credit Agricole": "ACA.PA",
    "Danone": "BN.PA"
}

# Company names for news search
COMPANY_NAMES = {
    "MC.PA": "LVMH",
    "OR.PA": "Orange",
    "TTE.PA": "TotalEnergies",
    "SAN.PA": "Sanofi",
    "AIR.PA": "Airbus",
    "CS.PA": "AXA",
    "BNP.PA": "BNP Paribas",
    "GLE.PA": "Société Générale",
    "ACA.PA": "Credit Agricole",
    "BN.PA": "Danone"
}

st.set_page_config(
    page_title="CAC 40 Sentiment Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("CAC 40 Sentiment Analyzer")
    
    # Sidebar for company selection
    st.sidebar.header("Sélection de l'entreprise")
    selected_company = st.sidebar.selectbox(
        "Choisissez une entreprise CAC 40",
        list(CAC40_TICKERS.keys())
    )
    
    ticker = CAC40_TICKERS[selected_company]
    
    # Load stock data
    with st.spinner("Chargement des données boursières..."):
        stock_data = get_stock_data([ticker])
    
    if not stock_data.empty:
        latest_data = stock_data.iloc[-1]
        previous_data = stock_data.iloc[-2] if len(stock_data) > 1 else latest_data
        
        current_price = latest_data['Close']
        price_change = ((current_price - previous_data['Close']) / previous_data['Close']) * 100
        
        # Header with company info
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.subheader(selected_company)
        with col2:
            st.metric("Prix actuel", f"€{current_price:.2f}")
        with col3:
            st.metric("Variation 24h", f"{price_change:.2f}%", 
                     delta=f"{price_change:.2f}%",
                     delta_color="normal")
        
        # Load news data
        with st.spinner("Récupération des actualités..."):
            news_data = get_company_news(COMPANY_NAMES[ticker])
        
        # Top row with sentiment gauge and stock chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Analyse de sentiment")
            if news_data:
                # Analyze sentiment for news titles
                sentiments = []
                for article in news_data[:10]:  # Limit to last 10 articles
                    sentiment_score = analyze_sentiment(article['title'])
                    sentiments.append(sentiment_score)
                
                if sentiments:
                    avg_sentiment = sum(sentiments) / len(sentiments)
                    fig_gauge = create_sentiment_gauge(avg_sentiment, selected_company)
                    st.plotly_chart(fig_gauge, use_container_width=True)
                else:
                    st.info("Aucun sentiment à analyser pour le moment.")
            else:
                st.info("Aucune actualité trouvée pour cette entreprise.")
        
        with col2:
            st.subheader("Cours de l'action (5 derniers jours)")
            fig_candlestick = create_candlestick_chart(stock_data)
            st.plotly_chart(fig_candlestick, use_container_width=True)
        
        # Bottom section: Latest news with sentiment analysis
        st.subheader("Dernières actualités & Analyses")
        if news_data:
            # Add sentiment scores to news data
            news_df = pd.DataFrame(news_data[:15])  # Limit to 15 articles
            news_df['sentiment'] = news_df['title'].apply(analyze_sentiment)
            
            # Style the dataframe based on sentiment
            def sentiment_color(sentiment):
                if sentiment > 0.1:
                    return 'background-color: rgba(0, 255, 0, 0.1)'
                elif sentiment < -0.1:
                    return 'background-color: rgba(255, 0, 0, 0.1)'
                else:
                    return 'background-color: rgba(255, 255, 0, 0.1)'
            
            styled_df = news_df.style.applymap(sentiment_color, subset=['sentiment'])
            st.dataframe(styled_df, height=400, use_container_width=True)
        else:
            st.info("Aucune actualité disponible pour cette entreprise.")
    else:
        st.error("Impossible de charger les données boursières. Veuillez réessayer.")

if __name__ == "__main__":
    main()
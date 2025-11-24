import yfinance as yf
import feedparser
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(tickers):
    """
    Fetch last 5 days of history using yfinance and calculate % change.
    
    Args:
        tickers (list): List of ticker symbols
    
    Returns:
        pd.DataFrame: Stock data with percentage change
    """
    if not tickers:
        return pd.DataFrame()
    
    try:
        # Get data for the last 5 days
        data = yf.download(tickers, period="5d", group_by="ticker")
        
        # Handle case where only one ticker is provided
        if len(tickers) == 1:
            df = data.copy()
            ticker = tickers[0]
        else:
            # For multiple tickers, select the first one
            ticker = tickers[0]
            df = data[ticker]
        
        # Reset index to make Date a column
        df.reset_index(inplace=True)
        
        # Calculate percentage change
        df['Percent_Change'] = ((df['Close'] - df['Open']) / df['Open']) * 100
        
        return df
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return pd.DataFrame()

def get_company_news(company_name):
    """
    Fetch RSS headlines from Google News France for a specific company.
    
    Args:
        company_name (str): Name of the company to search for
    
    Returns:
        list: List of dictionaries with news articles
    """
    try:
        # Construct the RSS feed URL for Google News France
        rss_url = f"https://news.google.com/rss/search?q={company_name}&hl=fr&gl=FR&ceid=FR:fr"
        
        # Parse the RSS feed
        feed = feedparser.parse(rss_url)
        
        # Extract relevant information from entries
        news_articles = []
        for entry in feed.entries[:15]:  # Limit to 15 most recent articles
            article = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published if hasattr(entry, 'published') else 'N/A'
            }
            news_articles.append(article)
        
        return news_articles
    except Exception as e:
        print(f"Error fetching news for {company_name}: {e}")
        return []
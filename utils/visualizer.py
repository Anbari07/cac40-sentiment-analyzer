import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_sentiment_gauge(sentiment_score, company_name):
    """
    Create a Gauge Chart showing the average sentiment score for a company.
    
    Args:
        sentiment_score (float): Average sentiment score between -1.0 and +1.0
        company_name (str): Name of the company
    
    Returns:
        plotly.graph_objects.Figure: Gauge chart figure
    """
    # Normalize sentiment score to 0-100 scale for gauge
    normalized_score = (sentiment_score + 1) * 50
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=normalized_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Sentiment pour {company_name}", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': 'red'},
                {'range': [30, 70], 'color': 'yellow'},
                {'range': [70, 100], 'color': 'green'}],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': normalized_score}}))
    
    fig.update_layout(
        font={'color': "black", 'family': "Arial"},
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_candlestick_chart(stock_data):
    """
    Create a Candlestick chart for stock price data.
    
    Args:
        stock_data (pd.DataFrame): DataFrame with stock data including Open, High, Low, Close columns
    
    Returns:
        plotly.graph_objects.Figure: Candlestick chart figure
    """
    fig = go.Figure(data=go.Candlestick(
        x=stock_data['Date'],
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name="Prix de l'action"
    ))
    
    fig.update_layout(
        title="Cours des 5 derniers jours",
        yaxis_title="Prix (EUR)",
        xaxis_title="Date",
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig
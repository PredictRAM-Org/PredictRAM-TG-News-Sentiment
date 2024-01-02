import streamlit as st
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistory
from textblob import TextBlob
import yfinance as yf

# Replace these values with your own Telegram API credentials
api_id = '288143'
api_hash = '81d969845f282ee8487c6c026bc21c3f'
channel_username = 'moneycontrolcom'

# Create a TelegramClient
client = TelegramClient('session_name', api_id, api_hash)

# Function to fetch news for a given stock symbol
def get_stock_news(symbol):
    news = []
    try:
        channel_entity = client.get_entity(channel_username)
        messages = client(GetHistory(channel=channel_entity, limit=10, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        for message in messages.messages:
            if symbol.lower() in message.message.lower():
                news.append(message.message)
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
    return news

# Streamlit app
st.title("Stock Sentiment Analysis App")

# User input for stock symbol
stock_symbol = st.text_input("Enter a stock symbol (e.g., AAPL):")

# Fetch stock data
if stock_symbol:
    stock_data = yf.Ticker(stock_symbol)
    st.write(f"## Stock Information for {stock_symbol}")
    st.write(f"**Company Name:** {stock_data.info['longName']}")
    st.write(f"**Current Price:** {stock_data.info['lastPrice']}")
    st.write(f"**Market Cap:** {stock_data.info['marketCap']}")
    
    # Fetch and display news for the stock
    st.write(f"## News for {stock_symbol}")
    stock_news = get_stock_news(stock_symbol)
    for news_item in stock_news:
        st.write(news_item)

    # Analyze sentiment of news
    st.write(f"## Sentiment Analysis for {stock_symbol}")
    sentiment_scores = [TextBlob(news).sentiment.polarity for news in stock_news]
    average_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

    if average_sentiment > 0:
        st.success(f"The overall sentiment is positive with an average sentiment score of {average_sentiment:.2f}.")
    elif average_sentiment < 0:
        st.error(f"The overall sentiment is negative with an average sentiment score of {average_sentiment:.2f}.")
    else:
        st.info("The sentiment is neutral.")

# Run the Streamlit app
if __name__ == '__main__':
    st.run_app()

import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import date

st.title("Stock Market Volatility Analysis (Interactive)")

# Sidebar for user input
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'SPY']
ticker = st.sidebar.selectbox("Select Ticker", tickers)
start_date = st.sidebar.date_input("Start Date", date(2015, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2025, 1, 1))
plot_type = st.sidebar.selectbox("Plot Type", [
    "Daily Return", "Daily Invest", "Daily High", "Daily Low", "Daily Volume", "Rolling STD", "MA20", "Upper Band", "Lower Band"
])

# Download data
data_load_state = st.text('Loading data...')
df = yf.download(ticker, start=start_date, end=end_date)
data_load_state.text('')

if df.empty:
    st.warning("No data found for the selected ticker and date range.")
else:
    # Calculate columns as needed
    if "Daily Return" in plot_type or "Rolling STD" in plot_type or "MA20" in plot_type or "Upper Band" in plot_type or "Lower Band" in plot_type:
        df['Daily Return'] = df['Close'].pct_change()
    if "Daily Invest" in plot_type:
        df['Daily Invest'] = df['Open'].pct_change()
    if "Daily High" in plot_type:
        df['Daily High'] = df['High'].pct_change()
    if "Daily Low" in plot_type:
        df['Daily Low'] = df['Low'].pct_change()
    if "Daily Volume" in plot_type:
        df['Daily Volume'] = df['Volume'].pct_change()
    if "Rolling STD" in plot_type or "Upper Band" in plot_type or "Lower Band" in plot_type:
        df['Rolling_STD'] = df['Close'].rolling(window=20).std()
    if "MA20" in plot_type or "Upper Band" in plot_type or "Lower Band" in plot_type:
        df['MA20'] = df['Close'].rolling(window=20).mean()
    if "Upper Band" in plot_type:
        df['Upper'] = df['MA20'] + 2*df['Rolling_STD']
    if "Lower Band" in plot_type:
        df['Lower'] = df['MA20'] - 2*df['Rolling_STD']

    # Plot
    plt.figure(figsize=(14, 6))
    if plot_type == "Daily Return":
        sns.lineplot(data=df['Daily Return'], color='blue')
        plt.title(f'{ticker} Daily Returns')
        plt.xlabel('Date')
        plt.ylabel('Daily Return')
    elif plot_type == "Daily Invest":
        sns.lineplot(data=df['Daily Invest'], color='red')
        plt.title(f'{ticker} Daily Invest')
        plt.xlabel('Date')
        plt.ylabel('Daily Invest')
    elif plot_type == "Daily High":
        sns.lineplot(data=df['Daily High'], color='yellow')
        plt.title(f'{ticker} Daily High')
        plt.xlabel('Date')
        plt.ylabel('Daily High')
    elif plot_type == "Daily Low":
        sns.lineplot(data=df['Daily Low'], color='green')
        plt.title(f'{ticker} Daily Low')
        plt.xlabel('Date')
        plt.ylabel('Daily Low')
    elif plot_type == "Daily Volume":
        sns.lineplot(data=df['Daily Volume'], color='black')
        plt.title(f'{ticker} Daily Volume')
        plt.xlabel('Date')
        plt.ylabel('Daily Volume')
    elif plot_type == "Rolling STD":
        sns.lineplot(data=df['Rolling_STD'], color='blue')
        plt.title(f'{ticker} 20-Day Rolling STD')
        plt.xlabel('Date')
        plt.ylabel('STD')
    elif plot_type == "MA20":
        sns.lineplot(data=df['MA20'], color='red')
        plt.title(f'{ticker} 20-Day Moving Average (MA20)')
        plt.xlabel('Date')
        plt.ylabel('MA20')
    elif plot_type == "Upper Band":
        sns.lineplot(data=df['Upper'], color='green')
        plt.title(f'{ticker} Upper Band (MA20 + 2*STD)')
        plt.xlabel('Date')
        plt.ylabel('Upper Band')
    elif plot_type == "Lower Band":
        sns.lineplot(data=df['Lower'], color='purple')
        plt.title(f'{ticker} Lower Band (MA20 - 2*STD)')
        plt.xlabel('Date')
        plt.ylabel('Lower Band')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt) 
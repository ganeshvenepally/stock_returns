import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def get_daily_return_for_multiple_stocks(stock_list, start_date):
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=5)).strftime('%Y-%m-%d')
    results = []

    for stock_name in stock_list:
        data = yf.download(stock_name, start=start_date, end=end_date)
        
        # Ensure we have 5 days of data
        if len(data) != 5:
            results.append([stock_name] + ["No data available"]*5)
            continue

        data['Returns'] = data['Close'].pct_change().fillna(0)
        daily_returns = data['Returns'].tolist()
        results.append([stock_name] + daily_returns)

    return results

st.title('Stock Daily Returns Calculator')
st.write('Calculate daily returns for the next 5 days from the provided start date.')

# User input
stock_names = st.text_input("Enter the list of stock names separated by commas (e.g. AAPL,MSFT,GOOGL):")
start_date = st.date_input("Enter the start date:")

if st.button('Calculate Returns'):
    stock_list = [stock.strip() for stock in stock_names.split(',')]
    results = get_daily_return_for_multiple_stocks(stock_list, start_date.strftime('%Y-%m-%d'))
    
    # Convert results to DataFrame for display in Streamlit
    date_range = [start_date + timedelta(days=i) for i in range(5)]
    columns = ["Stock Name"] + [date.strftime('%Y-%m-%d') for date in date_range]
    df = pd.DataFrame(results, columns=columns)
    st.table(df)


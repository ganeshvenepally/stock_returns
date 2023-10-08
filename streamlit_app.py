import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

def get_day1_return_for_multiple_stocks(stock_list, start_date, end_date):
    results = []

    for stock_name in stock_list:
        data = yf.download(stock_name, start=start_date, end=end_date)
        if data.empty:
            results.append([start_date, end_date, stock_name, "No data available"])
            continue

        # Calculate percent change from open to close for the first day
        first_day_data = data.iloc[0]
        day1_return = (first_day_data['Close'] - first_day_data['Open']) / first_day_data['Open']
        results.append([start_date, end_date, stock_name, f"{day1_return:.2%}"])

    return results

st.title('Stock Day 1 Returns Calculator')
st.write('Calculate returns from open to close for the first day between the provided start and end dates.')

# User input
stock_names = st.text_input("Enter the list of stock names separated by commas (e.g. AAPL,MSFT,GOOGL):")
start_date = st.date_input("Enter the start date:")
end_date = st.date_input("Enter the end date:", start_date)  # Default to start_date

if st.button('Calculate Returns'):
    stock_list = [stock.strip() for stock in stock_names.split(',')]
    results = get_day1_return_for_multiple_stocks(stock_list, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    
    # Convert results to DataFrame for display in Streamlit
    df = pd.DataFrame(results, columns=["Start Date", "End Date", "Stock Name", "Day 1 Returns"])
    st.table(df)

import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def process_stock_names(data):
    lines = data.split("\n")
    stock_names = [line.replace("BSE:", "") + ".BO" for line in lines if "BSE:" in line]
    return stock_names

def get_total_return_for_multiple_stocks(stock_list, start_date):
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=5)).strftime('%Y-%m-%d')
    results = []

    for stock_name in stock_list:
        data = yf.download(stock_name, start=start_date, end=end_date)
        if data.empty:
            results.append([start_date, end_date, stock_name, "No data available"])
            continue

        data['Returns'] = data['Close'].pct_change().fillna(0)
        total_return = (data['Returns'] + 1).prod() - 1
        results.append([start_date, end_date, stock_name, f"{total_return:.2%}"])

    return results

st.title('Stock Returns Calculator')
st.write('Input stock data in the provided format, get processed stock names, and calculate total returns for the next 5 days from the provided start date.')

# Stock name processor
data = st.text_area("Enter stock data:")
if st.button('Process Stock Names'):
    processed_names = process_stock_names(data)
    st.write(", ".join(processed_names))

# Stock returns calculator
start_date = st.date_input("Enter the start date:")
if st.button('Calculate Returns'):
    stock_list = processed_names
    results = get_total_return_for_multiple_stocks(stock_list, start_date.strftime('%Y-%m-%d'))
    
    # Convert results to DataFrame for display in Streamlit
    df = pd.DataFrame(results, columns=["Start Date", "End Date", "Stock Name", "Returns"])
    st.table(df)

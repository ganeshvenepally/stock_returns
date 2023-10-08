import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import io

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
st.write('Calculate total returns for the next 5 days from the provided start date.')

# User input
stock_names = st.text_input("Enter the list of stock names separated by commas (e.g. AAPL,MSFT,GOOGL):")
start_date = st.date_input("Enter the start date:")

if st.button('Calculate Returns'):
    stock_list = [stock.strip() for stock in stock_names.split(',')]
    results = get_total_return_for_multiple_stocks(stock_list, start_date.strftime('%Y-%m-%d'))
    
    # Convert results to DataFrame
    df = pd.DataFrame(results, columns=["Start Date", "End Date", "Stock Name", "Returns"])
    
    # Convert DataFrame to CSV and let the user download it
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="stock_returns.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

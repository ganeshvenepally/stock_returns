import streamlit as st
import yfinance as yf
import pandas as pd

def process_stock_names_India(data):
    lines = data.split("\n")
    # Exclude lines that start with "BSE:5" and process the rest
    stock_names = [line.replace("BSE:", "") + ".BO" for line in lines if "BSE:" in line and not line.startswith("BSE:5")]
    return ", ".join(stock_names)

st.title('Stock Name Processor India')
st.write('Input stock data in the provided format and get processed stock names.')

# User input
data = st.text_area("Enter stock data:")

if st.button('Process Stock Names'):
    processed_names_India = process_stock_names_India(data)
    st.write(processed_names_India)

def process_stock_names_US(data):
    lines = data.split("\n")
    # Extract tickers that start with "NYSE:" or "NASDAQ:" and process the rest
    stock_names = [line.replace("NYSE:", "").replace("NASDAQ:", "") for line in lines if "NYSE:" in line or "NASDAQ:" in line]
    return ", ".join(stock_names)

st.title('Stock Name Processor US')
st.write('Input stock data in the provided format and get processed stock names.')

# User input
data = st.text_area("Enter stock data:")

if st.button('Process Stock Names'):
    processed_names_US = process_stock_names_US(data)
    st.write(processed_names_US)

def get_total_return_for_multiple_stocks(stock_list, start_date, end_date):
    results = []

    for stock_name in stock_list:
        try:
            data = yf.download(stock_name, start=start_date, end=end_date)
            if data.empty:
                results.append([start_date, end_date, stock_name, "No data available"])
                continue

            total_return = ((data['Close'].iloc[-1] - data['Open'].iloc[0]) / data['Open'].iloc[0]) * 100
            results.append([start_date, end_date, stock_name, f"{total_return:.2f}%"])
        except Exception as e:
            results.append([start_date, end_date, stock_name, f"Error: {e}"])

    return results

st.title('Stock Returns Calculator')
st.write('Calculate total returns for a list of stocks between the provided start and end dates.')

# User input
stock_names = st.text_input("Enter the list of stock names separated by commas (e.g. AAPL,MSFT,GOOGL):")
start_date = st.date_input("Enter the start date:")
end_date = st.date_input("Enter the end date:", start_date)  # Default to start_date

if st.button('Calculate Returns'):
    stock_list = [stock.strip() for stock in stock_names.split(',')]
    results = get_total_return_for_multiple_stocks(stock_list, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    
    # Convert results to DataFrame for display in Streamlit
    df = pd.DataFrame(results, columns=["Start Date", "End Date", "Stock Name", "Total Returns"])
    st.table(df)

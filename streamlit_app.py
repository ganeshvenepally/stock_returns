import streamlit as st
import warnings
import yfinance as yf
import quantstats as qs
import os
import pandas as pd
from datetime import datetime

# Suppress all warnings
warnings.filterwarnings('ignore')

# Streamlit app title and description
st.title('QuantStats Report Generator')
st.write('This app generates a QuantStats report for a selected stock.')

# Get the current date
current_date = datetime.today()

# User input for stock symbol
stock_symbol = st.text_input('Enter Stock Symbol (e.g., 0P0000XW4J.BO)', '0P0000XW4J.BO')

# Date inputs for start and end date
start_date = st.date_input('Start Date', value=pd.to_datetime('2000-06-01'))
end_date = st.date_input('End Date', value=current_date)

# Button to generate the report
if st.button('Generate Report'):
    # Download historical data for the selected stock with progress bar disabled
    st.write(f"Downloading data for {stock_symbol} from {start_date} to {end_date}...")
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date, progress=False)
    
    if not stock_data.empty:
        # Extend pandas with QuantStats functions
        qs.extend_pandas()
        
        # Generate the QuantStats report and save it to an HTML file
        report_file_path = f'{stock_symbol}_quantstats_report.html'
        
        # Disable the progress bar when downloading benchmark data
        try:
            qs.reports.html(stock_data['Adj Close'], benchmark='SPY', ou

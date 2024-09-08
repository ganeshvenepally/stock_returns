import streamlit as st
import warnings
import yfinance as yf
import quantstats as qs
import os

# Suppress all warnings
warnings.filterwarnings('ignore')

# Streamlit app title and description
st.title('QuantStats Report Generator')
st.write('This app generates a QuantStats report for a selected stock.')

# User input for stock symbol
stock_symbol = st.text_input('Enter Stock Symbol (e.g., 0P0000XW4J.BO)', '0P0000XW4J.BO')

# Date inputs for start and end date
start_date = st.date_input('Start Date', value=pd.to_datetime('2000-06-01'))
end_date = st.date_input('End Date', value=pd.to_datetime('2010-12-31'))

# Button to generate the report
if st.button('Generate Report'):
    # Download historical data for the selected stock
    st.write(f"Downloading data for {stock_symbol} from {start_date} to {end_date}...")
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    
    if not stock_data.empty:
        # Extend pandas with QuantStats functions
        qs.extend_pandas()
        
        # Generate the QuantStats report and save it to an HTML file
        report_file_path = f'{stock_symbol}_quantstats_report.html'
        qs.reports.html(stock_data['Adj Close'], benchmark='SPY', output=report_file_path)
        
        # Notify the user and display a link to download the report
        st.success(f'Report saved to {report_file_path}')
        with open(report_file_path, 'rb') as f:
            st.download_button('Download Report', f, file_name=os.path.basename(report_file_path))
    else:
        st.error(f'No data found for {stock_symbol} in the selected date range.')

# Note for the user
st.write("This app generates a full QuantStats report, comparing the stock's performance to the S&P 500 benchmark.")

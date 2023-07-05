import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import yfinance as yf
import datetime as dt
import plotly.graph_objects as go
from prophet import Prophet

@st.cache_data
def download_data(tickerSymbol):
    raw_data = yf.download(tickers=tickerSymbol,start='2013-01-01')
    return raw_data

def main():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

    ticker_list = pd.read_csv('TickersList.csv',names=['ticker','company'], header=None)

    option = st.selectbox('Choose your company',ticker_list['ticker'])
    if option:
        st.write('You selected: ', option)    
        st.session_state['tickerSymbol'] = option
        st.session_state['data'] = download_data(option)

    if st.checkbox('Show dataframe'):
        st.write(download_data.head())

if __name__ == '__main__':
    main()
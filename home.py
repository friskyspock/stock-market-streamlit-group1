import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import yfinance as yf
import datetime as dt
import plotly.graph_objects as go
from prophet import Prophet



def main():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

    company_ticker = pd.read_csv('TickersList.csv',names=['ticker','company'], header=None)
    option = st.selectbox('Choose your company',company_ticker['ticker'])
    if option:
        st.write('You selected: ', option)    
        st.session_state['tickerName'] = option

    raw_data = yf.download(tickers="RELIANCE.NS",start='2013-01-01')
    st.session_state['data'] = raw_data

    st.write(st.session_state)


    # if st.checkbox('Show dataframe'):
    #     display_data = load_data().head()
    #     display_data



if __name__ == '__main__':
    main()
"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import yfinance as yf
import datetime as dt
import warnings
import plotly.graph_objects as go
warnings.filterwarnings("ignore")


# Importing prophet
from prophet import Prophet

## Pages
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")



# list of options to select
company_ticker = pd.read_csv('TickersList.csv',names=['ticker','company'], header=None)
option = st.selectbox(
    'Choose your company',
     company_ticker['ticker'])
'You selected: ', option


# downloading data
start_date = '2013-01-01'
raw_data = yf.download(tickers=option,start=start_date,period='1d')

    

# use checkbox to show/hide data
if st.checkbox('Show dataframe'):
    raw_data = raw_data.head()
    raw_data



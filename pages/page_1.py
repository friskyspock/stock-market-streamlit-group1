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

st.markdown("# Page 2 ")
st.sidebar.markdown("# Page 2 ")



# downloading data
start_date = '2013-01-01'
raw_data = yf.download(tickers=option,start=start_date,period='1d')


data = pd.DataFrame()
data['ds'] = raw_data.index
data['y'] = raw_data['Close'].values

st.text_input("No. of days to predict", key="days")



if st.button('train model'):
    model = Prophet(weekly_seasonality=False)
    model.fit(data)
    future = model.make_future_dataframe(periods=int(st.session_state.days))
    forecast = model.predict(future)
   
    #fig,ax=plt.subplots()
    #ax.plot(forecast['ds'][:-30],forecast['yhat'][:-30])
    #ax.plot(forecast['ds'][-30:],forecast['yhat'][-30:])
    #st.pyplot(fig)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast['ds'][:-int(st.session_state.days)],y=forecast['yhat'][:-int(st.session_state.days)]))
    fig.add_trace(go.Scatter(x=forecast['ds'][-int(st.session_state.days):],y=forecast['yhat'][-int(st.session_state.days):]))
    st.plotly_chart(fig)



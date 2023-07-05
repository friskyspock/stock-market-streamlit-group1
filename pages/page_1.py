import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import yfinance as yf
import datetime as dt
import warnings
import plotly.graph_objects as go

from prophet import Prophet


def main():
    st.markdown("# Page 2 ")
    st.sidebar.markdown("# Page 2 ")

    st.write(st.session_state['tickerName'])

    st.write(st.session_state['data'].head())
    # data = pd.DataFrame()
    # data['ds'] = raw_data.index
    # data['y'] = raw_data['Close'].values

    # st.text_input("No. of days to predict", key="days")

    # if st.button('train model'):
    #     model = Prophet(weekly_seasonality=False)
    #     model.fit(data)
    #     future = model.make_future_dataframe(periods=int(st.session_state.days))
    #     forecast = model.predict(future)

    #     fig = go.Figure()
    #     fig.add_trace(go.Scatter(x=forecast['ds'][:-int(st.session_state.days)],y=forecast['yhat'][:-int(st.session_state.days)]))
    #     fig.add_trace(go.Scatter(x=forecast['ds'][-int(st.session_state.days):],y=forecast['yhat'][-int(st.session_state.days):]))
    #     st.plotly_chart(fig)


if __name__ == '__main__':
    main()
import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

@st.cache_data
def download_data(tickerSymbol):
    raw_data = yf.download(tickers=tickerSymbol,start='2013-01-01')
    return raw_data

def main():
    st.sidebar.title("Stock Market Predictor")

    ticker_list = pd.read_csv('TickersList.csv',names=['ticker','company'], header=None)

    option = st.selectbox('Choose a ticker',ticker_list['ticker'])
    if option:
        tickerName = ticker_list[ticker_list['ticker']==option]['company'].values[0]
        raw_data = download_data(option)

        change = raw_data['Close'][-1]-raw_data['Close'][-2]
        percent = " ("+format(abs(change*100/raw_data['Close'][-2]),'.2f')+"%)"
        color = 'Red' if change < 0 else 'Green'
        arrow = "<span style='font-size: 20px; color: Red'>  &#9660;</span>" if change < 0 else "<span style='font-size: 20px; color: Green'>  &#9650;</span>"
        info = "</br><p style='font-size: 20px; line-height: 0.2'>"+tickerName+"</p>"+"<b style='font-size: 50px; line-height: 0.7'>"+format(raw_data['Close'][-1],'.2f')+arrow+"</b><span style='font-size: 25px; color:"+color+"'>"+format(change,'.2f')+percent+"</span>"
        st.markdown(info,unsafe_allow_html=True)

        st.session_state['tickerName'] = tickerName
        st.session_state['data'] = raw_data

    fig = go.Figure(data=[go.Candlestick(x=raw_data.index,
                                     close=raw_data['Close'],
                                     open=raw_data['Open'],
                                     high=raw_data['High'],
                                     low=raw_data['Low'])])
    fig.update_layout(xaxis_rangeslider_visible=False)


    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    tab1.plotly_chart(fig, use_container_width=True)
    tab2.dataframe(raw_data,column_config={'Date':st.column_config.DateColumn('Date')},use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        df = raw_data[['Close']].copy()
        df['year'] = raw_data.index.year
        df = df.groupby('year').sum().reset_index()
        fig = px.pie(df, values='Close', names='year',
                color_discrete_sequence=px.colors.sequential.RdBu,
                title ='Share of total Volume per year')
        st.plotly_chart(fig)

    with col2:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = raw_data['Volume'].mean(),
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Average Volume"},
            gauge = {'axis': {'range': [None, max(raw_data['Volume'])], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "#067FD0",
            }
            ))
        st.plotly_chart(fig)


if __name__ == '__main__':
    main()
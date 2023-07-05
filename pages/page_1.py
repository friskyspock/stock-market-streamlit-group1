import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from prophet import Prophet

@st.cache_resource
def build_model(data):
    df = pd.DataFrame()
    df['ds'] = data.index
    df['y'] = data['Close'].values
    model = Prophet(weekly_seasonality=False)
    model.fit(df)
    return model

def main():
    st.markdown("# Page 2 ")
    st.sidebar.markdown("# Page 2 ")

    st.write(st.session_state['tickerName'])
    raw_data = st.session_state['data']

    n_steps = st.number_input('No. of days to predict')

    if st.button('train model'):
        model = build_model()
        future = model.make_future_dataframe(periods=n_steps)
        forecast = model.predict(future)

        fig = go.Figure(data=[go.Candlestick(x=raw_data.index,
                                     close=raw_data['Close'],
                                     open=raw_data['Open'],
                                     high=raw_data['High'],
                                     low=raw_data['Low'])])
        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)


if __name__ == '__main__':
    main()
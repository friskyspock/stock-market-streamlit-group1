import streamlit as st
import pandas as pd
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
    st.header(st.session_state['tickerSymbol'])
    raw_data = st.session_state['data']

    n_steps = st.number_input('No. of days to predict')

    if st.button('train model'):
        model = build_model(raw_data)
        future = model.make_future_dataframe(periods=int(n_steps))
        forecast = model.predict(future)
        
        fig = go.Figure()
        fig.add_scatter(x=forecast.iloc[-int(n_steps):]["ds"], y=forecast.iloc[-int(n_steps):]["yhat"])
        fig.add_scatter(x=forecast.iloc[:-int(n_steps)]["ds"], y=forecast.iloc[:-int(n_steps)]["yhat"])
        st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
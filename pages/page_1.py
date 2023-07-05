import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from prophet import Prophet

@st.cache_resource
def build_model():
    raw_data = st.session_state['data']
    df = pd.DataFrame()
    df['ds'] = raw_data.index
    df['y'] = raw_data['Close'].values
    model = Prophet(weekly_seasonality=False)
    model.fit(df)
    return model

def main():
    st.markdown("# Page 2 ")
    st.sidebar.markdown("# Page 2 ")

    st.write(st.session_state['tickerName'])
    
    st.text_input("No. of days to predict", key="days")

    if st.button('train model'):
        future = build_model().make_future_dataframe(periods=int(st.session_state.days))
        forecast = model.predict(future)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast['ds'][:-int(st.session_state.days)],y=forecast['yhat'][:-int(st.session_state.days)]))
        fig.add_trace(go.Scatter(x=forecast['ds'][-int(st.session_state.days):],y=forecast['yhat'][-int(st.session_state.days):]))
        st.plotly_chart(fig)


if __name__ == '__main__':
    main()
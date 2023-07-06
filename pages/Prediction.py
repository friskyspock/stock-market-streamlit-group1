import streamlit as st
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from prophet import Prophet

@st.cache_resource
def build_model(data):
    df = pd.DataFrame()
    df['ds'] = data.index
    df['y'] = data['Close'].values
    model = Prophet(weekly_seasonality=False)
    model.fit(df)
    return model

@st.cache_resource
def build_hwes_model(data):
    model = ExponentialSmoothing(data['Close'].values, seasonal_periods=52, trend='add', seasonal='add')
    fitted_model = model.fit()
    return fitted_model

def main():
    st.sidebar.title("Stock Market Predictor")

    if 'tickerName' not in st.session_state:
        st.write("Select ticker from Dashboard")
    
    else:
        st.header(st.session_state['tickerName'])
        raw_data = st.session_state['data']
        train_data = raw_data[raw_data.index>'2020-09-01']

        n_steps = st.number_input('No. of days to predict',step=5)

        if st.button('train model'):
            model = build_model(train_data)
            future = model.make_future_dataframe(periods=int(n_steps))
            forecast = model.predict(future)

            hwes_model = build_hwes_model(train_data)
            hwes_array = hwes_model.forecast(steps=int(n_steps))
            
            fig = go.Figure()
            fig.add_scatter(x=forecast["ds"][-int(n_steps):], y=forecast["yhat_lower"][-int(n_steps):],name='lower limit',line=dict(color='rgba(172,172,92,0.2)'))
            fig.add_scatter(x=forecast["ds"][-int(n_steps):], y=forecast["yhat_upper"][-int(n_steps):],fill='tonexty',name='upper limit',line=dict(color='rgba(172,172,92,0.2)'))

            fig.add_scatter(x=forecast["ds"][-int(n_steps):], y=hwes_array,name='Holts-Winter',line=dict(color='orange', width=3))
            fig.add_scatter(x=forecast["ds"][-int(n_steps):], y=forecast.iloc[-int(n_steps):]["yhat"],name='Prophet',line=dict(color='red', width=3))
            fig.add_scatter(x=train_data.iloc[-120:].index, y=train_data.iloc[-120:]["Close"],name='original')
            fig.update_layout(autosize=False,width=800,height=400,margin=dict(l=50,r=50,b=50,t=10,pad=4))

            
            st.markdown("<h3 style='text-align: center'>Predictions</h3>",unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns([1,3],gap="medium")
            with col1:
                st.markdown("<h3 style='text-align: center'>Predicted Data Points</h3>",unsafe_allow_html=True)
                st.dataframe(forecast[["ds","yhat"]].iloc[-int(n_steps):],use_container_width=True)

            with col2:
                st.markdown("<h3 style='text-align: center'>Seasonal Decomposition</h3>",unsafe_allow_html=True)
                decompose = seasonal_decompose(raw_data['Close'].values,model='additive',period=5)
                fig = make_subplots(rows=2, cols=1)
                fig.add_scatter(x=raw_data.index,y=decompose.trend,row=1,col=1,name='Trend')
                fig.add_scatter(x=raw_data.index[-60:],y=decompose.seasonal[-60:],row=2,col=1,name='Seasonality')
                fig.update_layout(autosize=False,width=500,height=400,margin=dict(l=50,r=50,b=50,t=10,pad=4))
                st.plotly_chart(fig,use_container_width=True)
        


if __name__ == '__main__':
    main()
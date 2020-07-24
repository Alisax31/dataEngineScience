import const
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
const.path = 'train.csv'

def data_formate(df):
    df['Datetime'] = pd.to_datetime(df.Datetime, format="%d-%m-%Y %H:%M")
    df.index = df['Datetime']
    df = df.drop(['ID','Datetime'], axis=1)
    df_daily = df.resample('D').sum()
    df_daily['ds'] = df_daily.index
    df_daily['y'] = df_daily['Count']
    df_daily = df_daily.drop(['Count'], axis=1)
    return df_daily

def prophet_gen(df_daily):
    model = Prophet(yearly_seasonality=True, seasonality_prior_scale=0.1)
    model.fit(df_daily)
    future = model.make_future_dataframe(periods=213)
    forecast = model.predict(future)
    model.plot(forecast)
    plt.show()
    model.plot_components(forecast)
    plt.show()

if __name__ == '__main__':
    df = pd.read_csv(const.path)
    model = data_formate(df)
    prophet_gen(model)
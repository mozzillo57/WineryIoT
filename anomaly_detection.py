import pandas as pd
from requests import get
from fbprophet import Prophet
from fbprophet.plot import plot, plot_components
import matplotlib.pyplot as plt
from datetime import datetime
plt.style.use('fivethirtyeight')
sensors = [ "Temperature", "Humidity", "Distance", "Brightness"]

def fzwait():
    if not False:
        return input("Press Enter to continue.")
    return ' '

# 1. lettura dati
r = get("http://192.168.1.201:4444/lists")
print("Response code: ", r.status_code)
feed = r.json()
print ("Numbers of feed: ", len(feed["feeds"]))


# 2.0 tipi di dato e nomi colonne
df = pd.DataFrame(feed["feeds"])
print(df.dtypes)
print(df.head(5))
df["value"] = pd.to_numeric(df["value"])
df['timestamp'] = pd.to_datetime(df["timestamp"])
df['timestamp'] = df['timestamp'].dt.tz_localize(None)


#3.0 show data
df[df["sensor_id"]==0]
for w in df["winery_id"].unique().tolist():
    for s in df["sensor_id"].unique().tolist():
        new_df = df[(df.winery_id == w) & (df.sensor_id == s) ]
        
        ax = plt.gca()
        ax.set_xticks([0, len(new_df)-1])
        ax.set_xticklabels([new_df.iloc[0]['timestamp'], new_df.iloc[-1]['timestamp']])
       
        new_df.plot(kind='line', x='timestamp', y='value', ax=ax, figsize=(15,5))
        
        plt.title('Winery id:' + str(w) + ' - Sensor: ' + sensors[s])
        plt.xlabel('Timestamp')
        plt.ylabel('Value')
        plt.show()
        fzwait()


df = df.rename({'timestamp': 'ds', 'value': 'y'}, axis='columns')
for s in df["sensor_id"].unique().tolist():
    sensor_df = df[df.sensor_id == s]
    
    #4.0 model creation
    my_model = Prophet(interval_width=0.95, weekly_seasonality=True)

    #5.0 fit the data
    my_model.fit(sensor_df)

    #6.0 creation of future dataframe
    future_dates = my_model.make_future_dataframe(periods=10, freq='1min', include_history=True)
    print(future_dates.tail())
    
    #7.0 forecast
    values = my_model.predict(future_dates)
    values[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    
    #8.0 plot of the forecast
    plot(my_model, values, uncertainty=True, xlabel="Time", ylabel="Value")
    plt.title(" " + sensors[s])
    plt.show()
    fzwait()
    
    plot_components(my_model, values)
    plt.show()
    fzwait()

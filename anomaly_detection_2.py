from numpy.random.mtrand import choice
import pandas as pd
import numpy as np
from requests import get
from fbprophet import Prophet
from fbprophet.plot import plot, plot_components
import matplotlib.pyplot as plt
from datetime import datetime
import json 
from config import Config
from views import winery
from winerys import WineryManager
from flask_template import db

plt.style.use('fivethirtyeight')
sensors_type = ["T", "H", "D", "B"]

wm = WineryManager(db)

def fzwait():
    if not False:
        return input("Press Enter to continue.")
    return ' '
# 1. lettura dati 
df = pd.DataFrame(columns=['timestamp', 'value', 'type', 'winery_id'])

for winery in wm.get_all_winerys():
    sensors = winery.sensors
    for sen in sensors:
        tipo = sen.sensor_type
        for value in sen.values:
            timestamp = value.value_id
            val = value.val
            #print(timestamp, val, tipo, winery.winery_id)
            df = df.append({'timestamp': timestamp, 'value':val, 'type':tipo, 'winery_id':winery.winery_id }, ignore_index=True)

# DATAFRAME
# ['timestamp', 'value', 'type', 'winery_id']

df["value"] = pd.to_numeric(df["value"])
df["winery_id"] = pd.to_numeric(df["winery_id"])
df['timestamp'] = pd.to_datetime(df["timestamp"])
df['timestamp'] = df['timestamp'].dt.tz_localize(None)

sorted_df = df.sort_values(by=['timestamp'])

dt = (sorted_df['timestamp'][(len(sorted_df)-1)] - sorted_df['timestamp'][0] ) /2

periods = dt.seconds//60

df_train = df[df['timestamp']<= sorted_df['timestamp'][0] + dt]
df_test = df[df['timestamp']> sorted_df['timestamp'][0] + dt]

#print(df_test.describe())
#print(df_validate.describe())


#3. show data
for t in sensors_type:
    
    new_df = df_train[(df_train['type']==t)]
    new_df = new_df.drop(columns=['type'])
    
    if len(new_df) > 0:
        ax = plt.gca()
        ax.set_xticks([0, len(new_df)-1])
        ax.set_xticklabels([new_df.iloc[0]['timestamp'], new_df.iloc[len(new_df)-1]['timestamp']])
        new_df.plot(kind='line', x='timestamp', y='value', ax=ax, figsize=(15,5))
        plt.title('Winery id:' + str(winery.winery_id) + ' - Sensor: ' + t)
        plt.xlabel('Timestamp')
        plt.ylabel('Value')
        #plt.show()
        #fzwait()
        new_df = new_df.rename({'timestamp': 'ds', 'value': 'y'}, axis='columns')
        #4.0 model creation
        my_model = Prophet(interval_width=0.95, weekly_seasonality=True)
        #5.0 fit the data
        my_model.fit(new_df)
        #6.0 creation of future dataframe
        future_dates = my_model.make_future_dataframe(periods=periods, freq='1min', include_history=True)
        
        #7.0 forecast
        values = my_model.predict(future_dates)
        
        #8.0 plot of the forecast
        plot(my_model, values, uncertainty=True, xlabel="Time", ylabel="Value")
        plt.title(" " + t)
        #plt.show()
        #fzwait()
        plot_components(my_model, values)
        #plt.show()
        #fzwait()
        # controllare che tra il dataframe values (_df) e il dataframe di test (df_test), se ci sono delle date che
        # differiscono almeno per 1 minuto (per non fare il confronto preciso), se il valore è fuori range, vuol dire che c'è un'anomalia
        # ds: timestamp, yhat_lower < valore < yhat_upper
        _df = values.tail(n=periods)
        _df = _df.reset_index()
        new_df_test = df_test[(df_test['type']==t)]
        new_df_test = new_df_test.reset_index()
        
        print(_df)
        print("########################")
        print(new_df_test)
        
        idx = np.where(_df['ds'] - new_df_test['timestamp'] < np.timedelta64(1, 'm'))[0]
        for i in idx:
            if (_df.iloc[i]['yhat_lower'] > new_df_test.iloc[i]['value']) | (_df.iloc[i]['yhat_upper'] < new_df_test.iloc[i]['value']):
                print("Anomalia")
            print (_df.iloc[i]['yhat_lower'], _df.iloc[i]['yhat_upper'], new_df_test.iloc[i]['value'])
                # anomalia rilevata su 
                # new_df_test.iloc[i]['winery_id]
                # tipo sensore: t
        fzwait()
'''
 se viene detectata un'anomalia, bisogna aggiungere una nuova anomalia al sensore e mandarla

quello che si aspettava il bridge era un messaggio tipo 
allarme su tutti i sensori
 payload = {
    'sensor': "all",
    'winery_id': 0
}

oppure cessato allarme
payload = {
    'sensor': -1,
    'winery_id': 0
}

oppure allarme su una lista di sensori
 payload = {
    'sensor': [1, 3],
    'winery_id': 0
}

 protocollo scambio messaggi per il bridge com'è fatto adesso
 DD win_id id_sensore DE

 per indicare che c'è un anomalia su più sensori
 DD win_id numero_sens id_sens1 id_sens..n DE

 per indicare che tutti i sensori hanno un'anomalia
 DD win_id DC DE

 per cessare le anomalie
 DD win_id DB DE

'''
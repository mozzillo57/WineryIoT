from numpy.random.mtrand import choice
import pandas as pd
import numpy as np
from fbprophet import Prophet
from fbprophet.plot import plot, plot_components
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from config import Config
from requests import post
from random import randint

plt.style.use("fivethirtyeight")


class Anomaly_Detection:
    def __init__(self, wm):
        self.sensors_type = ["T", "H", "D", "B"]
        self.wm = wm

    def post_anomaly(self, sensor_id):
        anomaly = {"sensor_id": sensor_id}
        try:
            r = post(Config.BASE_URL + "/add/anomaly", data=anomaly)
            print(r.status_code)

        except ConnectionError as e:
            print("No connection with server")

    def fzwait(self):
        if not False:
            return input("Press Enter to continue.")
        return " "

    def create_DataFrame(self):
        # 1. lettura dati
        df = pd.DataFrame(
            columns=["timestamp", "value", "type", "winery_id", "sensor_id"]
        )

        for winery in self.wm.get_all_winerys():
            sensors = winery.sensors
            for sen in sensors:
                tipo = sen.sensor_type
                for value in sen.values:
                    timestamp = value.value_id
                    val = value.val
                    if datetime.now() - timestamp <= timedelta(hours=2):
                    # print(timestamp, val, tipo, winery.winery_id)
                        df = df.append(
                            {
                                "timestamp": timestamp,
                                "value": val,
                                "type": tipo,
                                "winery_id": winery.winery_id,
                                "sensor_id": sen.sensor_id,
                            },
                            ignore_index=True,
                        )

        return df

    def prepare_DataFrame(self, df):
        df["value"] = pd.to_numeric(df["value"])
        df["winery_id"] = pd.to_numeric(df["winery_id"])
        df["sensor_id"] = df["sensor_id"].astype(int)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["timestamp"] = df["timestamp"].dt.tz_localize(None)

        start_date = datetime.now() - timedelta(hours=2)

        mask = df["timestamp"] > start_date
        # print(df.loc[mask])
        df = df.loc[mask]
        df = df.reset_index()
        sorted_df = df.sort_values(by=["timestamp"])

        dt = (
            sorted_df.iloc[-1]["timestamp"] - sorted_df.iloc[0]["timestamp"]
        ) / 2

        print('DTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDT')
        print(sorted_df.iloc[-1]["timestamp"])

        df_train = df[df["timestamp"] <= sorted_df["timestamp"][0] + dt]
        df_test = df[df["timestamp"] > sorted_df["timestamp"][0] + dt]

        return df_train, df_test

    def show_DataFrame(self, df_train, sensor_type, sensor_id):
        ax = plt.gca()
        ax.set_xticks([0, len(df_train) - 1])
        ax.set_xticklabels(
            [
                df_train.iloc[0]["timestamp"],
                df_train.iloc[len(df_train) - 1]["timestamp"],
            ]
        )
        df_train.plot(kind="line", x="timestamp", y="value", ax=ax, figsize=(15, 5))

        plt.title("Sensor: " + sensor_type)
        plt.xlabel("Timestamp")
        plt.ylabel("Value")
        # plt.show()
        print("static/img/Sensor{}.png".format(sensor_id))
        plt.savefig("static/img/Sensor{}.png".format(sensor_id))
        plt.close()

    def train_model(self, df, sensor_type, sensor_id, periods=10):
        df = df.rename({"timestamp": "ds", "value": "y"}, axis="columns")

        my_model = Prophet(interval_width=0.95, weekly_seasonality=True)
        my_model.fit(df)

        future_dates = my_model.make_future_dataframe(
            periods=periods, freq='4s', include_history=True
        )

        values = my_model.predict(future_dates)

        plot_components(my_model, values)

        plt.savefig("static/img/components{}.png".format(sensor_id))
        plt.close()

        plot(my_model, values, uncertainty=True, xlabel="Time", ylabel="Value")
        plt.title(" " + sensor_type)
        # plt.savefig('static/img/Future Values Sensor{}.png'.format(sensor_id))
        return values

    def check_anomaly(self, df_predict, df_test, sensor_id):
        # controllare che tra il dataframe values (df_predict) e il dataframe di test (df_test), se ci sono delle date che
        # differiscono almeno per 1 minuto (per non fare il confronto preciso), se il valore è fuori range, vuol dire che c'è un'anomalia
        # ds: timestamp, yhat_lower < valore < yhat_upper

        fig = plt.figure(1)
        print((df_predict["ds"]))
        print('IDXIDXIDXIDXIDXIDX')
        idx = np.where(
            df_predict["ds"] - df_test["timestamp"] < np.timedelta64(1, "m")
        )[0]
        for i in idx:
            plt.plot(
                df_predict.iloc[i]["ds"],
                df_test.iloc[i]["value"],
                "o",
                markersize=8,
                color="green",
            )
            if (df_predict.iloc[i]["yhat_lower"] > df_test.iloc[i]["value"]) | (
                df_predict.iloc[i]["yhat_upper"] < df_test.iloc[i]["value"]
            ):
                print(
                    "Anomalia",
                    df_test.iloc[i]["timestamp"],
                    df_predict.iloc[i]["yhat_lower"],
                    df_predict.iloc[i]["yhat_upper"],
                    df_test.iloc[i]["value"],
                )
                self.post_anomaly(df_test.iloc[i]["sensor_id"])
                # post
                plt.plot(
                    df_predict.iloc[i]["ds"],
                    df_test.iloc[i]["value"],
                    "bo",
                    markersize=8,
                    color="red",
                )
                # plt.savefig('static/img/' + 'Future Values Sensor' + id + '.png')
                # plt.close()

            """ print(
                df_predict.iloc[i]["yhat_lower"],
                df_predict.iloc[i]["yhat_upper"],
                df_test.iloc[i]["value"],
            ) """
            # anomalia rilevata su
            # df_test.iloc[i]['winery_id]
            # tipo sensore: t

        fig.savefig("static/img/" + "Future Values Sensor" + sensor_id + ".png")
        # plt.savefig('static/img/' + 'Future Values Sensor' + id + '.png')
        plt.close()
        # self.fzwait()

    def start(self):
        print("########### Start Check Anomaly ################")
        df = self.create_DataFrame()

        df_train, df_test = self.prepare_DataFrame(df)
        for s_type in self.sensors_type:

            if len(df_train) > 0:
                train = df_train[(df_train["type"] == s_type)]
                train = train.drop(columns=["type"])
                id = str(train.iloc[0]["sensor_id"])
                self.show_DataFrame(df_train=train, sensor_type=s_type, sensor_id=id)

                test = df_test[(df_test["type"] == s_type)]
                test = test.reset_index()

                values = self.train_model(
                    df=train, sensor_type=s_type, sensor_id=id, periods=len(test)
                )

                predicted = values.tail(n=len(test))
                predicted = predicted.reset_index()

                self.check_anomaly(df_predict=predicted, df_test=test, sensor_id=id)
        print(len(df_train), len(df_test))    


if __name__ == "__main__":
    from views import wm

    a = Anomaly_Detection(wm)
    a.start()
"""
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

"""

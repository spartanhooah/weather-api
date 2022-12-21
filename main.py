from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

@app.route("/")
def home():

    return render_template("home.html", data=stations.to_html(index=False))


@app.route("/api/v1/<station>/<date>")
def get_data(station, date):
    station_id = str(station).zfill(6)
    data = pd.read_csv(f"data_small/TG_STAID{station_id}.txt",
                       skiprows=20,
                       parse_dates=["    DATE"])

    temperature = data.loc[data["    DATE"] == date]["   TG"].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True)

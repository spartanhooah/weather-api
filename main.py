from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

@app.route("/")
def home():

    return render_template("home.html", data=stations.to_html(index=False))


@app.route("/api/v1/<station>/<date>")
def station_date(station, date):
    station_id = str(station).zfill(6)
    data = pd.read_csv(f"data_small/TG_STAID{station_id}.txt",
                       skiprows=20,
                       parse_dates=["    DATE"])

    temperature = data.loc[data["    DATE"] == date]["   TG"].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def station_all(station):
    station_id = str(station).zfill(6)
    data = pd.read_csv(f"data_small/TG_STAID{station_id}.txt",
                       skiprows=20,
                       parse_dates=["    DATE"])

    return data.to_dict(orient="records")


@app.route("/api/v1/yearly/<station>/<year>")
def station_year(station, year):
    station_id = str(station).zfill(6)
    data = pd.read_csv(f"data_small/TG_STAID{station_id}.txt", skiprows=20)
    data["    DATE"] = data["    DATE"].astype(str)
    result = data[data["    DATE"].str.startswith(str(year))]

    return result.to_dict(orient="records")


if __name__ == "__main__":
    app.run(debug=True)

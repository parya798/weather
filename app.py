from flask import Flask, request, render_template
import requests

app = Flask(__name__)


API_KEY = "641a1b136c1e23cae53e6366c5a12db3"

CURRENT_WEATHER_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

FORECAST_ENDPOINT = "http://api.openweathermap.org/data/2.5/forecast"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city_name = request.form["city_name"]
        current_weather_data = get_current_weather(city_name)
        forecast_data = get_forecast(city_name)
        return render_template("index.html", city_name=city_name, current_weather_data=current_weather_data, forecast_data=forecast_data)
    return render_template("index.html")

def get_current_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(CURRENT_WEATHER_ENDPOINT, params=params)
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }

def get_forecast(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(FORECAST_ENDPOINT, params=params)
    data = response.json()
    forecast_data = []
    for i in range(5):
        forecast_data.append({
            "date": data["list"][i]["dt_txt"],
            "temperature": data["list"][i]["main"]["temp"],
            "humidity": data["list"][i]["main"]["humidity"],
            "description": data["list"][i]["weather"][0]["description"]
        })
    return forecast_data

if __name__ == "__main__":
    app.run(debug=True)
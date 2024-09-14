from flask import Flask, request, render_template 
import requests 

app = Flask(__name__) 

API_KEY = "641a1b136c1e23cae53e6366c5a12db3" 

FORECAST_ENDPOINT = "http://api.openweathermap.org/data/2.5/forecast" 

def get_forecast(city_name): 
    params = { 
        "q": city_name,
        "appid": API_KEY, 
        "units": "metric" 
    } 
    response = requests.get(FORECAST_ENDPOINT, params=params) 
    data = response.json() 
    forecast_data = [] 
    for forecast in data['list'][:5]: 
        forecast_data.append({ 
            "date": forecast["dt_txt"], 
            "temperature": forecast["main"]["temp"], 
            "humidity": forecast["main"]["humidity"], 
            "description": forecast["weather"][0]["description"] 
        }) 
    return forecast_data 

@app.route("/", methods=["GET", "POST"]) 
def index(): 
    if request.method == "POST": 
        city_name = request.form.get("city_name") 
        forecast_data = get_forecast(city_name) 
        return render_template("forecast.html", city_name=city_name, forecast_data=forecast_data) 
    return render_template("index.html")

if __name__ == "__main__": 
    app.run(debug=True)
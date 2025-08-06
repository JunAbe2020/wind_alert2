import os
import requests
import datetime
from django.shortcuts import render
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

def get_weather_data(city):
    cache_key = f"weather_{city}_{datetime.date.today()}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"
    response = requests.get(url)
    data = response.json()

    cache.set(cache_key, data, timeout=3600)
    return data

def wind_alert_view(request):
    city = "Morioka,JP"  # お住まいの市町村
    data = get_weather_data(city)
    wind_speed = data['wind']['speed']
    alert = wind_speed >= 10

    return render(request, "weather/alert.html", {
        "city": city,
        "wind_speed": wind_speed,
        "alert": alert
    })

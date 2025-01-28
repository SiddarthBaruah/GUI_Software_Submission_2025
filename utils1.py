import pandas as pd
import requests

def get_pod_data():
    """Static pod data for display."""
    return pd.DataFrame({
        "Pod Name": [
            "Avishkar-1 (Chennai to Bangalore)", 
            "Avishkar-2 (Chennai to Hyderabad)", 
            "Avishkar-3 (Chennai to Mumbai)", 
            "Avishkar-4 (Chennai to Goa)", 
            "Avishkar-5 (Chennai to Pune)"
        ],
        "Current Speed (km/h)": [800, 750, 990, 600, 1000],
        "Battery (%)": [85, 70, 65, 56, 99],
        "Status": ["Operational", "Maintenance", "Docked", "Operational", "Operational"]
    })

def get_weather_data(city, api_key):
    """Fetch weather data for a given city from OpenWeatherMap API."""
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(weather_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


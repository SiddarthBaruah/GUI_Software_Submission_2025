import streamlit as st
import requests

st.title("Route Monitoring")

st.header("Weather Conditions")

#Fetch Weather Data
route_weather_api = "http://api.weatherapi.com/v1/current.json?key=992c4a78ed12445c86a72417252601&q=Chennai&aqi=no"
response = requests.get(route_weather_api)

if response.status_code == 200:
    weather_data = response.json()
    condition_text = weather_data["current"]["condition"]["text"]
    st.write(f"Current Weather: {condition_text.capitalize()}")

    if "mist" in condition_text.lower():
        st.warning("Misty Conditions: Suggested speed limit is 800 km/h.")
    elif "rain" in condition_text.lower() or weather_data["current"]["precip_mm"] > 0:
        st.warning("Rainy Conditions: Suggested speed limit is 700 km/h.")
    else:
        st.success("Weather is clear. Proceed at optimal speed.")
else:
    st.error("Failed to fetch weather data.")
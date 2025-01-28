import streamlit as st
import os
from dotenv import load_dotenv
import requests
import pandas as pd
load_dotenv()
weather_api_key = os.getenv("weather_api_key")
weather_api_url = os.getenv("weather_api_url_2")

class weather_api:
	def __init__(self):
		pass
	def get_weather_details(x):
		latitude = st.session_state[f'location{x}'][0][0]
		longitude = st.session_state[f'location{x}'][0][1]
		params = {"key":weather_api_key,"q":f"{latitude},{longitude}"}
		try:			
			response = requests.get(weather_api_url, params = params)
			data = response.json()
			if f'weather_description{x}' not in st.session_state:
				st.session_state[f'weather_description{x}'] = data['current']['condition']['text']
			if f'temperature{x}' not in st.session_state:
				st.session_state[f'temperature{x}'] = data['current']['temp_c']
				st.session_state[f'temperature{x}'] = float(st.session_state[f"temperature{x}"])
		except requests.exceptions.ConnectionError as e:
			st.write("sorry, unable to request your data please try again later ", e)

import streamlit as st
import os
from dotenv import load_dotenv
import requests
import pandas as pd
load_dotenv()
weather_api_key = "580887f5dea34cc095c85509252001"
weather_api_url = "http://api.weatherapi.com/v1/current.json"

class weather_api:
	def __init__(self):
		pass
	def get_weather_details(self, x):
		latitude = st.session_state[f'location{x}'][0][0]
		longitude = st.session_state[f'location{x}'][0][1]
		params = {"key":weather_api_key,"q":f"{latitude},{longitude}"}
		try:			
			response = requests.get(weather_api_url, params = params)
			data = response.json()
			if f'weather_description{x}' not in st.session_state:
				st.session_state[f'weather_description{x}'] = data['current']['condition']['text']
				return st.session_state[f'weather_description{x}']
			if f'temperature{x}' not in st.session_state:
				st.session_state[f'temperature{x}'] = data['current']['temp_c']
				st.session_state[f'temperature{x}'] = float(st.session_state[f"temperature{x}"])
				return st.session_state[f'temperature{x}']
		except requests.exceptions.ConnectionError as e:
			st.write("sorry, unable to request your data please try again later ", e)

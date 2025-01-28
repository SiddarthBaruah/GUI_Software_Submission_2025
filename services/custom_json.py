import streamlit as st
import requests
import random
import os
from dotenv import load_dotenv
load_dotenv()
json_api_url = os.getenv("jsonplaceholder_api_url_2")
class json:
	def __init__(self):
		pass
	def show_random_api(x):
		try:
			response = requests.get(json_api_url)
			response.raise_for_status()
			posts = response.json()
			tip = random.choice(posts)
		
			st.write(tip.get("body"))
		except requests.exceptions.ConnectionError as e:
			st.write("sorry, unable to request your data please try again later ", e)



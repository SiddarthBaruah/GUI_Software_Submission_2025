import streamlit as st
import requests
import numpy as np

st.title("Energy Optimization")

st.header("Tips")

#Fetch Energy Tips
energy_tips_api = "https://jsonplaceholder.typicode.com/posts/" + str(np.random.randint(1, 20))
response = requests.get(energy_tips_api)

if response.status_code == 200:
    energy_tip = response.json()["body"]
    st.info(f"Energy Tip: {energy_tip}")
else:
    st.error("Failed to fetch energy tips.")
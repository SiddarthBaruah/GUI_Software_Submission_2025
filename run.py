import sys
import streamlit as st
import os
import random
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from services.new_pod_creation import new_pod
from services.sidebar import sidebar
import time


def font():
    st.markdown(
        """
        <style>
        *{
            font-family: 'Courier New', monospace;
        }
        </style>
        """,
        unsafe_allow_html = True
    )
font()
load_dotenv()
x = 5
weather_api_key = os.getenv("weather_api_key")
weather_api_url = os.getenv("weather_api_url")
fact_ap_url = os.getenv("jsonplaceholder_api_url")

data = pd.DataFrame(columns= ["name","speed","pod status","battery level","location","maintenance"])

new = new_pod.creation(data,x) # from the new_pod class i've created the creation function which helps us to create a table using the creation(data,x) where x is the number of rows that are to be required
new2 = pd.DataFrame(new)
new2 = sidebar.creation(new2,x)

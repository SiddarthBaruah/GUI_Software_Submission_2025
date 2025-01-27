import streamlit as st
import requests

st.title("Did You Know?")

#Fetch Fun Facts
facts_api = "https://api.api-ninjas.com/v1/facts"
response = requests.get(facts_api, headers={'X-Api-Key': 'WPLDadyUAcI6whIUt43jFQ==Z399KQ7qDgpK6HL5'})

if response.status_code == 200:
    fact = response.json()[0]["fact"]
    st.info(f"Fun Fact: {fact}")
else:
    st.error("Failed to get trivia.")
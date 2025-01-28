import streamlit as st
import requests
import pandas as pd
import numpy as np
import random
import plotly.express as px

#generating data for the pods
def generate_pod_data(num_pods):
    data={
        "Pod Name": [f"Avishkar-{i+1}" for i in range(num_pods)],
        "Current Speed (km/h)" : np.random.uniform(0,1500,num_pods),
        "Battery Percentage (%)" : np.random.uniform(0,100,num_pods),
        "Status" : np.random.choice(["Operational", "Maintenance", "Docked"], num_pods)
    }
    return pd.DataFrame(data)

#sample data
num_pods=10
df=generate_pod_data(num_pods)

#title
st.title("Avishkar Control Dashboard")

#1. Pod Tracker
st.header("Pod Tracker")
#filtering by status
status_filter=st.multiselect(
    "Filter Pods",
    options=["Operational", "Maintenance", "Docked", "All"],
    default="All",
)
if "All" in status_filter:
    filtered_df = df
else:
    filtered_df = df[df["Status"].isin(status_filter)]

#sorting and displaying the data
st.data_editor(filtered_df, use_container_width=True, hide_index=True)

cols=st.columns(2)
#2. Route Monitoring
api_key='aa465a9bcfde4f4f8cf150709251901'

def get_weather(location):
    base_url='http://api.weatherapi.com/v1/current.json'
    url=f'{base_url}?key={api_key}&q={location}'
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        return {
            'location':data['location']['name'],
            'temperature':data['current']['temp_c'],
            'condition':data['current']['condition']['text']
        }
    else:
        return {'error':'could not fetch data'}

#example
locations=['Los Angeles', 'San Francisco', 'Las Vegas', 'New York', 'London']

#dictionary with conditions and speeds
safe_speeds = {"clear": 1000,
    "sunny": 1000,
    "partly cloudy": 950,
    "cloudy": 950,
    "overcast": 950,
    "patchy rain possible": 900,
    "light drizzle": 900,
    "patchy light rain": 900,
    "patchy light drizzle": 900,
    "light rain shower": 850,
    "moderate or heavy rain shower": 850,
    "mist": 850,
    "patchy snow possible": 850,
    "light snow": 850,
    "patchy sleet possible": 850,
    "light sleet": 850,
    "patchy moderate snow": 850,
    "patchy freezing drizzle possible": 850,
    "freezing drizzle": 850,
    "moderate rain": 800,
    "heavy rain at times": 800,
    "moderate snow": 800,
    "heavy snow": 800,
    "moderate or heavy sleet": 800,
    "light freezing rain": 800,
    "fog": 800,
    "freezing fog": 800,
    "light sleet showers": 750,
    "moderate or heavy sleet showers": 750,
    "ice pellets": 750,
    "thundery outbreaks possible": 750,
    "blowing snow": 750,
    "light showers of ice pellets": 750,
    "light snow showers": 750,
    "moderate or heavy snow showers": 750,
    "torrential rain shower": 700,
    "patchy light rain with thunder": 700,
    "patchy heavy snow": 700,
    "blizzard": 700,
    "moderate or heavy freezing rain": 700,
    "heavy freezing drizzle": 700,
    "moderate or heavy showers of ice pellets": 700,
    "patchy light snow with thunder": 700,
    "moderate or heavy rain with thunder": 650,
    "moderate or heavy snow with thunder": 650
} #note: I asked ChatGPT to generate this part

with cols[0]:
    st.header("Route Monitoring")
    location=st.selectbox('Select a location', locations)
    weather=get_weather(location)
    if 'error' in weather:
        st.error(weather['error'])
    else:
        st.subheader(f"Weather in {weather['location']}")
        st.write(f"**Temperature:** {weather['temperature']}C")
        st.write(f"**Condition:** {weather['condition']}")
        st.write(f"**Safe speed limit:** {safe_speeds[weather['condition'].lower()]} km/h")

#3. Energy Optimization
def fetch_random_tip():
    url='https://jsonplaceholder.typicode.com/posts'
    response=requests.get(url)
    data=response.json()
    random_tip=random.choice(data)
    return random_tip['title'], random_tip['body']

tip, description= fetch_random_tip()

with cols[1]:
    st.header("Tip for optimising energy")
    st.write(tip.capitalize())
    st.write(f"**Description:** {description}")

#4. Pod Insights
st.header("Pod Insights")
selected_pods=st.multiselect(
    "Select pods that you want to compare",
    options=[f"Avishkar-{i+1}" for i in range(num_pods)],
    default=["Avishkar-1", "Avishkar-2"]
)
selected_df=df[df["Pod Name"].isin(selected_pods)]

fig=px.scatter(selected_df,x="Current Speed (km/h)", y="Battery Percentage (%)", color="Pod Name",
               hover_data=["Pod Name", "Status"], title="Speed vs Battery Level")

selected_points=st.plotly_chart(fig, use_container_width=True)

cols1=st.columns(2)
fig2 = px.bar(selected_df, x="Pod Name", y="Battery Percentage (%)", color="Pod Name", title="Battery Level Comparison")
with cols1[0]:
    selected_points=st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(selected_df, x="Pod Name", y="Current Speed (km/h)", color="Pod Name", title="Speed Comparison")
with cols1[1]:
    selected_points=st.plotly_chart(fig3, use_container_width=True)

#5. Hyperloop Fun Facts (Bonus):
def did_you_know():
    url='https://opentdb.com/api.php?amount=10&category=28' #for the time being, I couldn't find any facts API
    response=requests.get(url)
    data=response.json()
    return data.get("results")

i_know= did_you_know()
random_fact=random.choice(i_know)
st.info(f"**Did you know?**  \n\n{random_fact['question']}")

#Bonus Features
st.header("Wear Level of Pods")
cols2 = st.columns(2)
def Maintenance_Predictor():
    data2={
        "Pod Name": [f"Avishkar-{i+1}" for i in range(num_pods)],
        "Wear Level (%)" : np.random.uniform(0,100,num_pods),
    }
    return pd.DataFrame(data2)
Wear_Level=Maintenance_Predictor()
with cols2[0]:
    st.data_editor(Wear_Level, hide_index=True)

with cols2[1]:
    maintain_pods=0
    for index, row in Wear_Level.iterrows():
        if row["Wear Level (%)"] > 70:
             st.warning(f"Warning! {row['Pod Name']} requires maintenance. Wear Level = {row['Wear Level (%)']:.2f}%")
             maintain_pods+=1
    if maintain_pods==0:
        st.success("All pods are well maintained!")

def generate_pod_positions(num_pods):
    latitudes = np.random.uniform(low=-69.0, high=69.0, size=num_pods)  
    longitudes = np.random.uniform(low=-69.0, high=69.0, size=num_pods)
    return pd.DataFrame({
        "Pod Name": [f"Avishkar-{i+1}" for i in range(num_pods)],
        "Latitude": latitudes,
        "Longitude": longitudes
    })

#Generate pod positions
pod_positions = generate_pod_positions(num_pods)

st.header("Live Pod Map")
fig = px.scatter_geo(
    pod_positions,
    lat="Latitude",
    lon="Longitude",
    hover_name="Pod Name",
    template="plotly",
    color="Pod Name",
    size_max=10
)

st.plotly_chart(fig, use_container_width=True)

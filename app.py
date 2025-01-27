import streamlit as st
import pandas as pd
import random
import requests

# Constants
WEATHER_API_KEY = "cca9ea1d8fea4e9ba38151713251901"
WEATHER_API_URL = "http://api.weatherapi.com/v1"
FUN_FACTS_API_URL = "https://my-json-server.typicode.com/Someshwar-vp/energy-tips/funFacts"
ENERGY_TIPS_API_URL = "https://my-json-server.typicode.com/Someshwar-vp/energy-tips/energyTips"

# Helper Functions
def fetch_weather(city):
    params = {"q": city, "key": WEATHER_API_KEY, "aqi": "no"}
    response = requests.get(f"{WEATHER_API_URL}/current.json", params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data['current']['condition']['text']
        return weather
    else:
        return "Unknown"


def fetch_energy_tips():
    response = requests.get(ENERGY_TIPS_API_URL)
    if response.status_code == 200:
        try:
            tips = response.json()
            if isinstance(tips, list) and len(tips) > 0:
                random_tip = random.choice(tips)  # Select a random tip object
                return random_tip["body"]  # Extract the "body" from the selected tip
            else:
                return "No energy tips available at the moment."
        except ValueError:
            return "Error processing energy tips data."
    else:
        return "Failed to fetch energy tips. Please try again later."


def fetch_fun_fact():
    response = requests.get(FUN_FACTS_API_URL)
    if response.status_code == 200:
        facts = response.json()  # This will be a list of facts
        if isinstance(facts, list) and len(facts) > 0:
            # Pick a random fact and return the 'fact' field
            random_fact = random.choice(facts)
            return random_fact.get("fact", "Transportation is fascinating!")  # Safe fallback
        else:
            return "No fun facts available at the moment."
    else:
        return "Failed to fetch fun facts. Please try again later."


def generate_random_pod_data():
    pod_data = []  # Create an empty list to store pod information
    
    for i in range(5):  # Loop 5 times to generate data for 5 pods
        pod = {
            "Pod Name": "Avishkar-" + str(i + 1),  # Generate pod name as "Avishkar-1", "Avishkar-2", etc.
            "Current Speed": random.randint(600, 1000),  # Random speed between 600 and 1000
            "Battery Percentage": random.randint(10, 100),  # Random battery percentage between 10 and 100
            "Status": random.choice(["Operational", "Maintenance", "Docked"])  # Random status
        }
        pod_data.append(pod)  # Add the pod dictionary to the list

    return pod_data  # Return the list of pod data

# Streamlit App
st.title("Hyperloop Control Dashboard")
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to", ["Pod Tracker", "Route Monitoring", "Energy Optimization", "Pod Health Insights", "Did You Know?"])

# Initialize session state for pod data
if "pod_data" not in st.session_state:
    st.session_state["pod_data"] = generate_random_pod_data()

# Access the persistent pod data
pod_data = st.session_state["pod_data"]

# Pod Tracker
if section == "Pod Tracker":
    st.header("Pod Tracker")
    pod_df = pd.DataFrame(pod_data)

    # Filters
    status_filter = st.selectbox("Filter by Status", ["All"] + pod_df["Status"].unique().tolist())
    if status_filter != "All":
        pod_df = pod_df[pod_df["Status"] == status_filter]

    # Sort options
    sort_option = st.selectbox("Sort by", ["Pod Name", "Current Speed", "Battery Percentage"])
    pod_df = pod_df.sort_values(by=sort_option, ascending=True if sort_option == "Pod Name" else False)

    st.dataframe(pod_df)

# Route Monitoring
elif section == "Route Monitoring":
    st.header("Route Monitoring")
    city = st.text_input("Enter City for Weather Data", "Chennai")
    weather = fetch_weather(city)
    st.write(f"Current Weather in {city}: {weather}")

    # Suggest safe speed limits based on weather
    safe_speed = 1000  # Default
    if weather == "Rain" or weather =="Overcast":
        safe_speed = 700
    elif weather == "Snow":
        safe_speed = 600
    elif weather == "Thunderstorm" or weather == "Mist":
        safe_speed = 500

    st.write(f"Suggested Safe Speed: {safe_speed} km/h")

# Energy Optimization
elif section == "Energy Optimization":
    st.header("Energy Optimization")
    energy_tip = fetch_energy_tips()
    st.write("**Energy-Saving Tip:**")
    st.write(energy_tip)

# Pod Health Insights
elif section == "Pod Health Insights":
    st.header("Pod Health Insights")
    pod_df = pd.DataFrame(pod_data)

    pod1 = st.selectbox("Select Pod 1", pod_df["Pod Name"])
    pod2 = st.selectbox("Select Pod 2", pod_df["Pod Name"])

    pod1_data = pod_df[pod_df["Pod Name"] == pod1].iloc[0]
    pod2_data = pod_df[pod_df["Pod Name"] == pod2].iloc[0]

    st.write("### Comparison")
    st.write(pd.DataFrame({
        "Metric": ["Current Speed", "Battery Percentage", "Status"],
        pod1: [pod1_data["Current Speed"], pod1_data["Battery Percentage"], pod1_data["Status"]],
        pod2: [pod2_data["Current Speed"], pod2_data["Battery Percentage"], pod2_data["Status"]]
    }))

# Did You Know?
elif section == "Did You Know?":
    st.header("Did You Know?")
    fun_fact = fetch_fun_fact()
    st.write(fun_fact)

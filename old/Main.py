import streamlit as st
import pandas as pd
import numpy as np
import time
import requests

#General
st.set_page_config(page_title="Avishkar Dashboard", initial_sidebar_state="expanded") #sidebar menu is first open

st.title("Avishkar Control")

#Sidebar
st.sidebar.header("Navigation")
sections = ["Pod Tracker", "Route Monitoring", "Energy Optimization", "Pod Health", "Did You Know?"]
selected_section = st.sidebar.radio("", sections) #current selected tab in sidebar
st.sidebar.info("Built with Streamlit by Avishkar Hyperloop") #Giving recognition to Streamlit, footer in sidebar

start_time = time.time()
health_metrics = ["Avg Speed (km/h)", "Battery Health (%)"]

#Pod Tracker Data
pods_data = pd.DataFrame({"Name": ["Avishkar-1", "Avishkar-2", "Avishkar-3"], "Speed (km/h)": [1000, 0, 0],
                          "Battery Level (%)": [40, 60, 80], "Status": ["Operational", "Maintenance", "Docked"],
                          "Pressure (kPa)": [90, 100, 105], "Temperature (°C)": [25, 30, 29],
                          "Battery Health (%)": [70, 20, 90], "Avg Speed (km/h)": [622, 401, 553],
                          "Maintenance Level": [1, 1, 1]})

#Update pod data in real-time
def update_live_data():
    for i in range(len(pods_data["Name"])):
        if pods_data["Status"][i] == "Operational":
            pods_data["Speed (km/h)"][i] += np.random.randint(-100, 100)
            pods_data["Battery Level (%)"][i] -= 0.5
            pods_data["Pressure (kPa)"][i] += np.random.uniform(-10, 10)
            pods_data["Temperature (°C)"][i] += np.random.uniform(-5, 5)
            pods_data["Battery Health (%)"][i] -= 0.5*(time.time()-start_time)**0.5
            pods_data["Maintenance Level"][i] -= 0.06
        else:
            pods_data["Battery Level (%)"][i] += 0.2
            pods_data["Pressure (kPa)"][i] += np.random.uniform(-2, 2)
            pods_data["Temperature (°C)"][i] += np.random.uniform(-2, 2)
            pods_data["Battery Health (%)"][i] -= 0.1
          

#Pod Tracker
if selected_section == "Pod Tracker":
    st.header("Pod Tracker")

    #Display Pod Details
    filter_status = st.selectbox("Filter by Status:", ["All"] + pods_data["Status"].unique().tolist())
    sort_by = st.selectbox("Sort by:", ["Name", "Speed (km/h)", "Battery Level (%)", "Pressure (kPa)",
                                        "Temperature (°C)", "Battery Health (%)"])
    
    placeholder = st.empty()
    for _ in range(20):
        update_live_data()
        if filter_status != "All":
            filtered_pods = pods_data[pods_data["Status"] == filter_status]
        else:
            filtered_pods = pods_data
        
        sorted_pods = filtered_pods.sort_values(by=sort_by, ascending=False)

        with placeholder.container():
            st.table(sorted_pods)

            st.subheader("System Conditions - Avishkar-1")

            #Simulated Alert Conditions
            is_alerts = False
            live_data = {key:pods_data[key][0] for key in pods_data.keys()} #Selects data for Avishkar-1, "Operational" status

            if live_data["Speed (km/h)"] > 1100:
                st.error("High Speed Alert: Reduce speed immediately!")
                is_alerts = True
            if live_data["Pressure (kPa)"] < 75 or live_data["Pressure (kPa)"] > 115:
                st.error("Pod Pressure Out of Range!")
                is_alerts = True
            if live_data["Battery Level (%)"] < 25:
                st.error("Low Battery Level: Recharge or replace batteries soon.")
                is_alerts = True
            if live_data["Temperature (°C)"] > 30:
                st.error("High Temperature: Cooling system required.")
                is_alerts = True

            if is_alerts:
                st.success("All systems operational.")

            #Display info for maintenance level predictor <simulator>
            st.subheader("Maintenance Predictor")
            data = pd.DataFrame({"Name": [name for name in pods_data["Name"]], 
                         "Maintenance Status": ["Not Needed" if m_level>0.5 else ("Needed" if m_level>0 else "Repair Now!") for m_level in pods_data["Maintenance Level"]]})
            st.table(data)
    
        time.sleep(2) #like realtime delays

#Route Monitoring Section
elif selected_section == "Route Monitoring":
    st.header("Route Monitoring")

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

#Energy Optimization Section
elif selected_section == "Energy Optimization":
    st.header("Energy Optimization")

    #Fetch Energy Tips
    energy_tips_api = "https://jsonplaceholder.typicode.com/posts/" + str(np.random.randint(1, 20))
    response = requests.get(energy_tips_api)

    if response.status_code == 200:
        energy_tip = response.json()["body"]
        st.info(f"Energy Tip: {energy_tip}")
    else:
        st.error("Failed to fetch energy tips.")

#Pod Health Section
elif selected_section == "Pod Health":
    st.header("Pod Health")

    pod_1 = st.selectbox("Select Pod 1:", pods_data["Name"].tolist())
    pod_2 = st.selectbox("Select Pod 2:", pods_data["Name"].tolist())

    if pod_1 and pod_2 and pod_1 != pod_2:
        pod_1_data = pods_data[pods_data["Name"] == pod_1].iloc[0]
        pod_2_data = pods_data[pods_data["Name"] == pod_2].iloc[0]

        comparison_data = pd.DataFrame({
            "Metric": health_metrics,
            pod_1: [pod_1_data[i] for i in health_metrics],
            pod_2: [pod_2_data[i] for i in health_metrics],
        })

        st.table(comparison_data)
    else:
        st.warning("Please select two different pods for comparison.")

elif selected_section == "Did You Know?":
    st.header("Fun Facts about Hyperloop!")

    #Fetch Fun Facts
    facts_api = "https://api.api-ninjas.com/v1/facts"
    response = requests.get(facts_api, headers={'X-Api-Key': 'WPLDadyUAcI6whIUt43jFQ==Z399KQ7qDgpK6HL5'})

    if response.status_code == 200:
        fact = response.json()[0]["fact"]
        st.info(f"Fun Fact: {fact}")
    else:
        st.error("Failed to get trivia.")

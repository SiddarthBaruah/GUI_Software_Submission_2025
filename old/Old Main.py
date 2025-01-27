import streamlit as st
import pandas as pd
import numpy as np
import time
import requests

#General
st.set_page_config(page_title="Avishkar Dashboard", initial_sidebar_state="expanded")
st.title("Avishkar Control")

#Sidebar
st.sidebar.header("Navigation")
sections = ["Pod Tracker", "Route Monitoring", "Energy Optimization", "Pod Health Insights", "Alerts"]
selected_section = st.sidebar.radio("Go to:", sections)

#Simulated Data
start_time = time.time()
status_list = ["Operational", "Maintenance", "Docked"]
def generate_live_data(podcode = 1):
    speed = 0 if podcode != 1 else np.random.randint(100, 1200)
    return {"Speed (km/h)": speed, "Pod Pressure (kPa)": np.random.randint(90, 110),
            "Battery Level (%)": podcode*np.random.randint(0,30), "Temperature (°C)": np.random.randint(25, 40),
            "Battery Health (%)": (30*podcode)-0.5*(time.time()-start_time)**0.5, "Status": status_list[podcode]}

#Pod Tracker Data
pods_data = pd.DataFrame({"Pod Name": ["Avishkar-1", "Avishkar-2", "Avishkar-3"], "Current Speed (km/h)": [1000, 0, 0],
                          "Battery Percentage (%)": [40, 60, 80], "Status": ["Operational", "Maintenance", "Docked"]})

#Live Data Section
if selected_section == "Live Data":
    st.header("Live Hyperloop Pod Data")

    #Display live data dynamically
    placeholder = st.empty()
    for _ in range(10):  #Simulate live updates (10 iterations for demo purposes)
        live_data = generate_live_data()
        df_live = pd.DataFrame([live_data])
        
        with placeholder.container():
            st.table(df_live)

        time.sleep(1)  #Realtime update time, adjust here for simulation

#Performance Metrics Section
elif selected_section == "Performance Metrics":
    st.header("Performance Metrics")

    st.subheader("Historical Pod Performance")

    #Simulated Historical Data
    data = pd.DataFrame(
        {
            "Time": pd.date_range(start="2023-01-01", periods=100, freq="min"),
            "Speed (km/h)": np.random.randint(800, 1200, size=100),
            "Pod Pressure (kPa)": np.random.uniform(80, 120, size=100),
            "Battery Level (%)": np.random.uniform(20, 100, size=100),
            "Temperature (°C)": np.random.uniform(15, 35, size=100),
        }
    )

    metric_to_plot = st.selectbox("Select Metric to Visualize:", data.columns[1:])
    st.line_chart(data.set_index("Time")[metric_to_plot])

    #Comparisons
    st.subheader("Comparison Between Metrics")
    comparison_metrics = st.multiselect(
        "Select Metrics to Compare:", data.columns[1:], default=data.columns[1:3]
    )
    if len(comparison_metrics) > 1:
        st.line_chart(data.set_index("Time")[comparison_metrics])

#Alerts Section
elif selected_section == "Alerts":
    st.header("Critical Alerts")

    st.subheader("Current System Status")

    #Simulated Alert Conditions
    alerts = []
    live_data = generate_live_data()

    if live_data["Speed (km/h)"] > 1100:
        alerts.append("High Speed Alert: Reduce speed immediately!")
    if live_data["Pod Pressure (kPa)"] < 75 or live_data["Pod Pressure (kPa)"] > 115:
        alerts.append("Pod Pressure Out of Range!")
    if live_data["Battery Level (%)"] < 25:
        alerts.append("Low Battery Level: Recharge or replace batteries soon.")
    if live_data["Temperature (°C)"] > 30:
        alerts.append("High Temperature: Cooling system required.")

    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("All systems operational.")

    st.subheader("System Logs")
    st.text("Logs not available for this demo.")

#Pod Tracker Section
elif selected_section == "Pod Tracker":
    st.header("Pod Tracker")

    #Display Pod Details
    filter_status = st.selectbox("Filter by Status:", ["All"] + pods_data["Status"].unique().tolist())
    if filter_status != "All":
        filtered_pods = pods_data[pods_data["Status"] == filter_status]
    else:
        filtered_pods = pods_data

    sort_by = st.selectbox("Sort by:", ["Pod Name", "Current Speed (km/h)", "Battery Percentage (%)"])
    sorted_pods = filtered_pods.sort_values(by=sort_by, ascending=False)

    st.table(sorted_pods)

#Route Monitoring Section
elif selected_section == "Route Monitoring":
    st.header("Route Monitoring")

    #Fetch Weather Data (Dummy API Call Example)
    route_weather_api = "http://api.weatherapi.com/v1/current.json?key=992c4a78ed12445c86a72417252601&q=Chennai&aqi=no"
    response = requests.get(route_weather_api)

    if response.status_code == 200:
        weather_data = response.json()
        condition_text = weather_data["current"]["condition"]["text"]
        st.write(f"Current Weather: {condition_text.capitalize()}")

        if "rain" in condition_text.lower() or weather_data["current"]["precip_mm"] > 0:
            st.warning("Rainy Conditions: Suggested speed limit is 700 km/h.")
        elif "mist" in condition_text.lower():
            st.warning("Misty Conditions: Suggested speed limit is 800 km/h.")
        else:
            st.success("Weather is clear. Proceed at optimal speed.")
    else:
        st.error("Failed to fetch weather data.")

#Energy Optimization Section
elif selected_section == "Energy Optimization":
    st.header("Energy Optimization")

    #Fetch Energy Tips (Dummy API Call Example)
    energy_tips_api = "https://jsonplaceholder.typicode.com/posts/" + str(np.random.randint(1, 20))
    response = requests.get(energy_tips_api)

    if response.status_code == 200:
        energy_tip = response.json()["body"]
        st.info(f"Energy Tip: {energy_tip}")
    else:
        st.error("Failed to fetch energy tips.")

#Pod Health Insights Section
elif selected_section == "Pod Health Insights":
    st.header("Pod Health Insights")

    pod_1 = st.selectbox("Select Pod 1:", pods_data["Pod Name"].tolist())
    pod_2 = st.selectbox("Select Pod 2:", pods_data["Pod Name"].tolist())

    if pod_1 and pod_2 and pod_1 != pod_2:
        pod_1_data = pods_data[pods_data["Pod Name"] == pod_1].iloc[0]
        pod_2_data = pods_data[pods_data["Pod Name"] == pod_2].iloc[0]

        comparison_data = pd.DataFrame({
            "Metric": ["Current Speed (km/h)", "Battery Percentage (%)"],
            pod_1: [pod_1_data["Current Speed (km/h)"], pod_1_data["Battery Percentage (%)"]],
            pod_2: [pod_2_data["Current Speed (km/h)"], pod_2_data["Battery Percentage (%)"]],
        })

        st.table(comparison_data)
    else:
        st.warning("Please select two different pods for comparison.")

#Footer in sidebar
st.sidebar.info("Built with Streamlit by Avishkar Hyperloop")

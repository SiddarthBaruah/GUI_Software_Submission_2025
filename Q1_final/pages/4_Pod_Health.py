import streamlit as st
import numpy as np
import pandas as pd
import time

st.title("Pod Health")

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
            pods_data["Battery Health (%)"][i] -= 0.5
            pods_data["Maintenance Level"][i] -= 0.06
        else:
            pods_data["Battery Level (%)"][i] += 0.2
            pods_data["Pressure (kPa)"][i] += np.random.uniform(-2, 2)
            pods_data["Temperature (°C)"][i] += np.random.uniform(-2, 2)
            pods_data["Battery Health (%)"][i] -= 0.1

pod_1 = st.selectbox("Select Pod 1:", pods_data["Name"].tolist())
pod_2 = st.selectbox("Select Pod 2:", pods_data["Name"].tolist())

placeholder = st.empty()

for _ in range(20):
    if pod_1 and pod_2 and pod_1 != pod_2:
        pod_1_data = pods_data[pods_data["Name"] == pod_1].iloc[0]
        pod_2_data = pods_data[pods_data["Name"] == pod_2].iloc[0]

        comparison_data = pd.DataFrame({
            "Metric": health_metrics,
            pod_1: [pod_1_data[i] for i in health_metrics],
            pod_2: [pod_2_data[i] for i in health_metrics],
        })

        with placeholder.container():
            st.table(comparison_data)
    else:
        with placeholder.container():
            st.warning("Please select two different pods for comparison.")

    update_live_data()
    time.sleep(2) #Realtime delays simulation
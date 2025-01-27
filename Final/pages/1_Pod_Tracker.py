import streamlit as st
import numpy as np
import pandas as pd
import time

st.title("Live Hyperloop Pod Tracker")

start_time = time.time()

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
st.header("Pod Tracker")

#Display Pod Details
filter_status = st.selectbox("Filter by Status:", ["All"] + pods_data["Status"].unique().tolist())
sort_by = st.selectbox("Sort by:", ["Name", "Speed (km/h)", "Battery Level (%)", "Pressure (kPa)",
                                    "Temperature (°C)", "Battery Health (%)"])

placeholder_1 = st.empty()
placeholder_2 = st.empty()
placeholder_3 = st.empty()

for _ in range(20):
    update_live_data()
    if filter_status != "All":
        filtered_pods = pods_data[pods_data["Status"] == filter_status]
    else:
        filtered_pods = pods_data
    
    sorted_pods = filtered_pods.sort_values(by=sort_by, ascending=False)

    with placeholder_1.container():
        st.table(sorted_pods)

    with placeholder_2.container():
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

    with placeholder_3.container():
        #Display info for maintenance level predictor <simulator>
        st.subheader("Maintenance Predictor")
        data = pd.DataFrame({"Name": [name for name in pods_data["Name"]], 
                        "Maintenance Status": ["Not Needed" if m_level>0.5 else ("Needed" if m_level>0 else "Repair Now!") for m_level in pods_data["Maintenance Level"]]})
        st.table(data)

        time.sleep(2) #like realtime delays
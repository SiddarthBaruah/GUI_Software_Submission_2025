import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
import time
import folium
from streamlit_folium import st_folium
from groq import Groq

# Setting up the page
st.set_page_config(page_title="Avishkar Hyperloop Control", page_icon="🚄", layout="wide")

# Custom Styling    
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

body {
    background-color: #0a192f;
    color: #64ffda;
}
.big-font {
    font-family: 'Orbitron', sans-serif;
    font-size: 48px !important;
    font-weight: 700;
    color: #64ffda;
    text-shadow: 0 0 10px #64ffda;
}
.sub-font {
    font-family: 'Orbitron', sans-serif;
    font-size: 24px;
    color: #8892b0;
}
.stButton>button {
    font-family: 'Orbitron', sans-serif;
    background-color: #172a45;
    color: #64ffda;
    border: 2px solid #64ffda;
    border-radius: 5px;
    box-shadow: 0 0 10px #64ffda;
}
</style>
""", unsafe_allow_html=True)

# Define routes
routes = [
    {"name": "Ahmedabad to Mumbai", "coords": [(23.0225, 72.5714), (19.0760, 72.8777)], "travel_time": 25},
    {"name": "Delhi to Jaipur", "coords": [(28.6139, 77.2090), (26.9124, 75.7873)], "travel_time": 12},
    {"name": "Chennai to Bangalore", "coords": [(13.0827, 80.2707), (12.9716, 77.5946)], "travel_time": 15},
    {"name": "Kolkata to Bhubaneswar", "coords": [(22.5726, 88.3639), (20.2961, 85.8245)], "travel_time": 19},
    {"name": "Hyderabad to Pune", "coords": [(17.3850, 78.4867), (18.5204, 73.8567)], "travel_time": 20},
    {"name": "Lucknow to Kanpur", "coords": [(26.8467, 80.9462), (26.4499, 80.3319)], "travel_time": 6},
    {"name": "Indore to Bhopal", "coords": [(22.7196, 75.8577), (23.2599, 77.4126)], "travel_time": 10}
]

# Create a new DataFrame for pods with routes
pods = [
    {
        "name": f"Avishkar-{i+1}",
        "route": routes[i]["name"],
        "status": "Operational",
        "position": "Start",
        "trips": 0,
        "speed": random.randint(500, 1000),
        "battery": 100,
        "travel_time": 15
    }
    for i in range(7)
]
df_pods = pd.DataFrame(pods)

def simulate_pods(df):
    for index, pod in df.iterrows():
        route = routes[index]
        if pod['status'] != 'Maintenance':
            if pod['battery'] > 20:
                if pod['position'] == 'Start':
                    df.at[index, 'position'] = 'En route to Destination'
                    df.at[index, 'speed'] = random.randint(500, 1000)
                    df.at[index, 'travel_time'] = route['travel_time']
                elif pod['position'] == 'En route to Destination':
                    df.at[index, 'travel_time'] -= 1
                    if df.at[index, 'travel_time'] <= 0:
                        df.at[index, 'position'] = 'At Destination'
                        df.at[index, 'speed'] = 0
                        df.at[index, 'battery'] -= 10
                elif pod['position'] == 'At Destination':
                    df.at[index, 'position'] = 'En route to Start'
                    df.at[index, 'speed'] = random.randint(500, 1000)
                    df.at[index, 'travel_time'] = route['travel_time']
                elif pod['position'] == 'En route to Start':
                    df.at[index, 'travel_time'] -= 1
                    if df.at[index, 'travel_time'] <= 0:
                        df.at[index, 'position'] = 'Start'
                        df.at[index, 'speed'] = 0
                        df.at[index, 'battery'] -= 10
                        df.at[index, 'trips'] += 1
            else:
                df.at[index, 'status'] = 'Maintenance'
                df.at[index, 'position'] = 'At Start'
                df.at[index, 'speed'] = 0
        else:  # Pod is in Maintenance
            df.at[index, 'status'] = 'Operational'
            df.at[index, 'battery'] = 100
            df.at[index, 'position'] = 'Start'
    return df

def get_position(start_coords, end_coords, elapsed_time, total_time):
    if elapsed_time >= total_time:
        return end_coords
    ratio = elapsed_time / total_time
    lat = start_coords[0] + (end_coords[0] - start_coords[0]) * ratio
    lon = start_coords[1] + (end_coords[1] - start_coords[1]) * ratio
    return [lat, lon]

# Title, logo, and energy tips
col1, col2 = st.columns([3,1])
with col1:
    st.markdown("<p class='big-font'>Avishkar Hyperloop Control</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-font'>Next-Gen Transportation Hub</p>", unsafe_allow_html=True)

with col2:
    st.markdown("<p class='sub-font'>Energy Tip</p>", unsafe_allow_html=True)
    
    def get_energy_tip():
        tips = [
            "Optimize pod aerodynamics to reduce energy consumption",
            "Implement regenerative braking to recover energy during deceleration",
            "Use lightweight materials to reduce overall pod weight",
            "Enhance magnetic levitation efficiency to minimize friction",
            "Optimize climate control systems for energy efficiency"
        ]
        return random.choice(tips)
    
    if 'energy_tip' not in st.session_state or st.button("New Tip"):
        st.session_state.energy_tip = get_energy_tip()
    
    st.info(f"💡 {st.session_state.energy_tip}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pod Tracker", "Route Monitoring", "Pod Health", "Live Tracking", "JARVIS"])

# ---------------------------
#    EXPERIMENTAL FRAGMENT
# ---------------------------
@st.experimental_fragment(run_every=1)
def pod_tracker_fragment():
    st.header("Pod Tracker")
    
    if 'df_pods' not in st.session_state:
        st.session_state.df_pods = df_pods
        st.session_state.last_update = time.time()

    # Simulate pods (runs on every fragment refresh)
    st.session_state.df_pods = simulate_pods(st.session_state.df_pods)

    # Filtering and display
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(st.session_state.df_pods["status"].unique()))
    with col2:
        sort_by = st.selectbox("Sort by", ["Speed", "Battery"])
    
    df_display = st.session_state.df_pods.copy()
    if status_filter != "All":
        df_display = df_display[df_display["status"] == status_filter]
    df_display = df_display.sort_values(sort_by.lower(), ascending=False)
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df_display.columns),
                    fill_color='#172a45',
                    align='left',
                    font=dict(size=16, color='white')),
        cells=dict(values=[df_display[col] for col in df_display.columns],
                   fill_color='#0a192f',
                   align='left',
                   font=dict(size=14, color='#64ffda'))
    )])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

# Tab1 calls the fragment
with tab1:
    pod_tracker_fragment()

with tab2:
    st.header("Route Monitoring")
    
    def get_weather(city):
        api_key = "dbc02e6f06e443ffbb2155649252701"  # Replace with your actual WeatherAPI.com API key
        base_url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": api_key,
            "q": city,
            "aqi": "no"
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                temp_c = data["current"]["temp_c"]
                condition = data["current"]["condition"]["text"]
                wind_kph = data["current"]["wind_kph"]
                return temp_c, condition, wind_kph
            else:
                return None, None, None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None, None, None

    city = st.text_input("Enter city for weather check")
    if city:
        temperature, condition, wind_speed = get_weather(city)
        if temperature is not None:
            st.write(f"Current weather in {city}:")
            st.write(f"Temperature: {temperature}°C")
            st.write(f"Condition: {condition}")
            st.write(f"Wind Speed: {wind_speed} km/h")
            
            if "rain" in condition.lower():
                st.warning("⚠️ Rainy conditions detected. Reduce speed to 700 km/h")
            else:
                st.success("✅ Weather conditions are favorable for maximum speed")
        else:
            st.error("Unable to retrieve weather data. Please check the city name or try again later.")


with tab3:
    st.header("Pod Health Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        pod1 = st.selectbox("Select first pod", st.session_state.df_pods["name"])
    with col2:
        pod2 = st.selectbox("Select second pod", st.session_state.df_pods["name"])
    
    if pod1 and pod2:
        comparison = st.session_state.df_pods[st.session_state.df_pods["name"].isin([pod1, pod2])]
        
        fig = px.bar(
            comparison,
            x="name",
            y=["speed", "battery"],
            barmode="group",
            title="Pod Comparison",
            labels={"value": "Value", "variable": "Metric"}
        )
        fig.update_layout(plot_bgcolor="#0a192f", paper_bgcolor="#0a192f", font_color="#64ffda")
        st.plotly_chart(fig, use_container_width=True)

# ---- Live Tracking Fragment ----
@st.experimental_fragment(run_every=1)
def live_tracking_fragment(df_pods_state):
    """Refreshes only the live tracking portion every 1 second."""
    st.title("Live Pod Tracking")

    # Create a folium map
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    # Add routes to the map
    for route in routes:
        folium.PolyLine(route["coords"], color="blue", weight=2.5, opacity=1).add_to(m)

    # Add dynamic pod markers
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    for index, pod in df_pods_state.iterrows():
        route = routes[index]
        route_coords = route["coords"]
        start_coords = route_coords[0]
        end_coords = route_coords[1]
        total_time = route["travel_time"]  # total time for route

        elapsed_time = (time.time() - st.session_state.start_time) % total_time
        pod_position = get_position(start_coords, end_coords, elapsed_time, total_time)

        folium.Marker(
            location=pod_position,
            popup=f"{pod['name']} - {pod['position']}<br>Status: {pod['status']}<br>Battery: {pod['battery']}%",
            icon=folium.Icon(color="green" if pod["status"] == "Operational" else "red")
        ).add_to(m)

    st_folium(m, width=800, height=600)
    st.write("Updating live positions...")

with tab4:
    # Pass the current DataFrame to the fragment for partial refresh
    live_tracking_fragment(st.session_state.df_pods)

with tab5:
    st.title("JARVIS - Hyperloop Chatbot")

    # Custom styling for chatbot
    st.markdown("""
    <style>
        .stTextInput input {
            font-size: 16px;
            padding: 8px;
            color: #64ffda;
            background-color: #172a45;
            border: 1px solid #64ffda;
            border-radius: 5px;
        }
        .stButton button {
            font-size: 16px;
            padding: 8px 16px;
            background-color: #172a45;
            color: #64ffda;
            border: 1px solid #64ffda;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #000f21;
        }
        .message {
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            color: #64ffda;
        }
        .user-message {
            background-color: #000f21;
            text-align: right;
        }
        .bot-message {
            background-color: #0a192f;
            text-align: left;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize Groq client
    def initialize_groq_client():
        api_key = "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"
        if not api_key:
            st.error("Groq API key not set. Please configure it.")
            st.stop()
        return Groq(api_key=api_key)

    # Initialize chat history with README.md content
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """
You are a hyperloop assistant chatbot built by Siddh Rathod. Your name is JARVIS. Your purpose is to assist users with hyperloop-related queries, including technical details, applications, and innovations. Always respond in a professional and helpful manner. Here's an overview of the Avishkar Hyperloop Control Dashboard:

# Avishkar Hyperloop Control Dashboard

## Overview

The Avishkar Hyperloop Control Dashboard is a comprehensive web application built using Streamlit to monitor and manage a hyperloop transportation system. This dashboard provides real-time tracking of hyperloop pods, route monitoring with weather updates, pod health comparisons, live tracking visualization, and an AI-powered chatbot assistant.

## Features

### 1. Pod Tracker
- Real-time updates of pod status, position, speed, and battery levels
- Filtering and sorting capabilities for easy monitoring
- Dynamic simulation of pod movements and status changes

### 2. Route Monitoring
- Live weather updates for selected cities along routes
- Speed recommendations based on current weather conditions
- Utilizes the python_weather library for real-time weather data

### 3. Pod Health Comparison
- Visual comparison of selected pods' speed and battery levels
- Interactive bar charts for easy analysis

### 4. Live Tracking
- Interactive map showing real-time positions of all pods
- Route visualization with color-coded pod markers
- Automatic updates every second

### 5. JARVIS Chatbot
- AI-powered assistant for hyperloop-related queries
- Utilizes the Groq API for natural language processing
- Maintains conversation history for context-aware responses

## Usage

Navigate through the tabs to access different features of the dashboard.

## Dependencies

- streamlit
- pandas
- plotly
- folium
- streamlit-folium
- groq
- python_weather
- requests
- asyncio

Please assist users with any questions related to this dashboard or hyperloop technology in general.
"""
            },
            {
                "role": "assistant",
                "content": "Hello! I'm JARVIS, your Hyperloop assistant. How can I help you today with the Avishkar Hyperloop Control Dashboard or any hyperloop-related queries?"
            }
        ]

    # Rest of the code for displaying chat history and handling user input remains unchanged
    ...


    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f'<div class="message {msg["role"]}-message">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input box for user message
    user_input = st.chat_input("Type a message for JARVIS here...")
    if user_input:
        # Add user's message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(f'<div class="message user-message">{user_input}</div>', unsafe_allow_html=True)

        with st.spinner("JARVIS is thinking..."):
            try:
                client = initialize_groq_client()
                response = client.chat.completions.create(
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    model="llama-3.3-70b-versatile"  # or any other available model
                )
                bot_content = response.choices[0].message.content
                
                # Add bot response to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_content})

                with st.chat_message("assistant"):
                    st.markdown(f'<div class="message bot-message">{bot_content}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")



# Footer
st.markdown("---")
st.markdown("<p class='sub-font'>Avishkar Hyperloop Control v1.0 | Powered by Streamlit</p>", unsafe_allow_html=True)

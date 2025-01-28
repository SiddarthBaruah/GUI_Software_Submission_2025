import streamlit as st
import requests
import random
import pandas as pd
from PIL import Image
from io import BytesIO
import folium
from folium import Marker
from folium.plugins import MarkerCluster

# OpenWeather API key
api_key = "03b68f9a1d394778bab114109252801"  

# Function to fetch weather data using WeatherAPI by latitude and longitude
def fetch_weather_by_coordinates(lat, lon):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}&aqi=no"
        response = requests.get(url)
        response.raise_for_status()  # Raise error for HTTP issues
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request error: {err}"}

# All pod's data
pods = [
    {"name": "Avishkar-6", "speed": 720, "battery": 85, "status": "Operational"},
    {"name": "Avishkar-5", "speed": 700, "battery": 60, "status": "Operational"},
    {"name": "Avishkar-4", "speed": 650, "battery": 70, "status": "Maintenance"},
    {"name": "Avishkar-3", "speed": 800, "battery": 90, "status": "Docked"},
]

# Function to fetch fun transportation facts
def fetch_transportation_fun_facts():
    fun_facts = [
        "The first trains were powered by horses, but later steam engines were introduced.",
        "The world's longest passenger train is over 4 kilometers long and runs in India.",
        "The world's busiest subway station is located in Tokyo, Japan, with over 3.5 million passengers daily.",
        "The Hyperloop is designed to travel at speeds of up to 760 miles per hour (1,220 km/h).",
        "Electric vehicles (EVs) are becoming more popular, contributing to cleaner air in cities.",
        "The first modern traffic light was installed in 1914 in Salt Lake City, Utah.",
        "The longest road in the world is the Pan-American Highway, stretching over 19,000 miles (30,000 km)."
    ]
    return random.choice(fun_facts)

# Function to crop the top 1/5th of the image
def crop_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    top_crop = height // 5
    crop_box = (0, top_crop, width, height)
    cropped_img = img.crop(crop_box)
    return cropped_img

# The Complete Dashboard begins here.
#Setting page title
st.set_page_config(page_title="Hyperloop Management Dashboard", layout="wide")

# Croping and displaying the Hyperloop image using the function written above
hyperloop_image_url = "https://urbantransportnews.com/assets/uploads/gallary/20200927121331.jpg"
cropped_image = crop_image(hyperloop_image_url)
st.image(cropped_image, use_container_width=True)  # Automatically adjusts to container width

# fetch energy saving tip
def get_energy_tips():
    url = "https://jsonplaceholder.typicode.com/posts"  
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json() 
        return data  
    except requests.exceptions.RequestException as e:
        return [f"Error fetching tips: {str(e)}"]

st.title("Energy-Saving Tip")
tips = get_energy_tips()

if isinstance(tips, list) and tips:
    random_tip = random.choice(tips) 
    st.write(f"Tip: {random_tip['title']}") 
else:
    st.write("No tips available at the moment.")

# Heading for the Hyperloop Management Dashboard
st.markdown("<h1 style='text-align: center; font-size: 40px; font-weight: bold; color: #ff6f61;'>Hyperloop Management Dashboard</h1>", unsafe_allow_html=True)

# 1. Pod Tracker
st.header("Pod Tracker")

# Adding styles to Pod Tracker section
st.markdown("""
    <style>
        .pod-info {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
        }

        .pod-info h4 {
            color: #1f4d58;
            margin-bottom: 10px;
        }
        
    </style>
""", unsafe_allow_html=True)
#filters and sorting options
status_filter = st.selectbox("Filter by Status:", ["All", "Operational", "Maintenance", "Docked"], key="status_filter", index=0, help="Select a status to filter the pods.")
sort_by = st.selectbox("Sort by:", ["None", "Speed", "Battery"], key="sort_by", index=0, help="Sort pods based on speed or battery.")

filtered_pods = pods
if status_filter != "All":
    filtered_pods = [pod for pod in pods if pod["status"] == status_filter]

if sort_by == "Speed":
    filtered_pods = sorted(filtered_pods, key=lambda x: x["speed"], reverse=True)
elif sort_by == "Battery":
    filtered_pods = sorted(filtered_pods, key=lambda x: x["battery"], reverse=True)

# Display filtered and sorted pods
for pod in filtered_pods:
    st.markdown(f"<div class='pod-info'><h4>{pod['name']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Speed:</strong> {pod['speed']} km/h</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Battery:</strong> {pod['battery']}%</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Status: </strong>{pod['status']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Map showing location of all the pods
# Coordinates for the pods
pod_locations = {
    "Avishkar 6 (Mumbai)": [19.0760, 72.8777],  # Mumbai coordinates
    "Avishkar 5 (Delhi)": [28.6139, 77.2090],   # Delhi coordinates
    "Avishkar 4 (Chennai)": [13.0827, 80.2707],  # Chennai coordinates
    "Avishkar 3 (Bangalore)": [12.9716, 77.5946] # Bangalore coordinates
}

# Colors for different pods
pod_colors = {
    "Avishkar 6 (Mumbai)": "red",
    "Avishkar 5 (Delhi)": "blue",
    "Avishkar 4 (Chennai)": "green",
    "Avishkar 3 (Bangalore)": "purple"
}

# Initialize a map centered on India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Add color for each pod location with different colors
for pod, coordinates in pod_locations.items():
    color = pod_colors.get(pod)
    Marker(
        location=coordinates, 
        popup=f"{pod} ({color.capitalize()})", 
        icon=folium.Icon(color=color)
    ).add_to(m)

st.title("All the pod locations")

st.write("Avishkar6: Red")
st.write("Avishkar5: Blue")
st.write("Avishkar4: Green")
st.write("Avishkar3: Purple")
st.components.v1.html(m._repr_html_(), height=600)

# 2. Route Weather Monitoring by Latitude and Longitude
# css styling for this part
st.markdown("""
    <style>
        .stMarkdown h2, .stTextInput input,.stNumberInput label, .stSelectbox label, .stTextArea label{
            font-size: 30px;
            padding: 16px;
            height: 50px;
            width: 17%;
            border: 1px solid #4A90E2;
            border-radius: 8px;
            background-color:	;
            color:grey;
        }
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox select {
            font-size: 22px;
            padding: 12px;
            height: 50px;
            width: 60%;
            border: 2px solid #4A90E2;  /* Soft blue border */
            border-radius: 8px;
            background-color:#E1F9E3 ;  /* Light blue background */
            color:#2C3E50
        }
        /*button styling*/
        .stButton button {
            padding: 12px;
            height: 50px;
            width: 80%;
            border-radius: 10px;
            background-color: #4A90E2;
            cursor: pointer;
        }

        .stButton button:hover {
            background-color: #357ABD;
            border: 2px solid white;
            color: white
        }
            
        .stButton button:active {
            background-color: #357ABD;
            border: 2px solid white;
            color: white
        }
    </style>
""", unsafe_allow_html=True)
# code for weather 
latitude = st.number_input("Enter Latitude:", value=13.0826, step=1.0000, format="%.4f")
longitude = st.number_input("Enter Longitude:", value=80.2707, step=1.0000, format="%.4f")

if st.button("Fetch Weather at Coordinates"):
    weather_data = fetch_weather_by_coordinates(latitude, longitude)

    if "error" in weather_data:
        st.error(weather_data["error"])
    else:
        weather_condition = weather_data["current"]["condition"]["text"]
        temp = weather_data["current"]["temp_c"]
        humidity = weather_data["current"]["humidity"]
        wind_speed = weather_data["current"]["wind_kph"]
        icon_url = "http:" + weather_data["current"]["condition"]["icon"]

        # Display weather icon and details
        st.image(icon_url, width=100)
        st.write(f"**Weather Conditions at {latitude}, {longitude}:**")
        st.write(f"- Condition: {weather_condition}")
        st.write(f"- Temperature: {temp}°C")
        st.write(f"- Humidity: {humidity}%")
        st.write(f"- Wind Speed: {wind_speed} km/h")

        # Safe Speed Recommendations
        if "rain" in weather_condition.lower():
            st.warning("Rainy: Reduce the speed to 500 km/h")
        elif "snow" in weather_condition.lower():
            st.warning("Snowy: Reduce the speed to 400 km/h")
        elif "storm" in weather_condition.lower():
            st.error("Stormy: Reduce the speed to 300 km/h")
        else:
            st.success("Clear weather: Safe speed 800 km/h")


# 4. Comparing pods 
st.header("Pod Comparison")
pod_names = [pod["name"] for pod in pods]

# Default selection for Pod 1 and Pod 2
pod1 = st.selectbox("Select Pod 1:", pod_names, index=0)
pod2 = st.selectbox("Select Pod 2:", pod_names, index=1)

if pod1 and pod2:
    pod1_data = next(pod for pod in pods if pod["name"] == pod1)
    pod2_data = next(pod for pod in pods if pod["name"] == pod2)

    data = {
        "Pod Parameter": ["Speed (km/h)", "Battery (%)", "Status"],
        pod1: [pod1_data["speed"], pod1_data["battery"], pod1_data["status"]],
        pod2: [pod2_data["speed"], pod2_data["battery"], pod2_data["status"]],
    }

    # The comparison table css styles 
    st.markdown("""
        <style>
            .comparison-table th, .comparison-table td {
                padding: 15px;
                text-align: center;
                font-size: 22px;
                color: #333333;
            }
            .comparison-table th {
                background-color: #333333;
                font-weight: bold;
                color: white;
                border: 1px solid #ddd;
            }
            .comparison-table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .comparison-table tr:nth-child(odd) {
                background-color: #e0e0e0;
            }
            .comparison-table tr:hover {
                background-color: #d0d0d0;
            }
            .comparison-table td {
                border: 1px solid #ddd;
            }
        </style>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(data)
    st.markdown(df.to_html(classes='comparison-table', index=False, escape=False), unsafe_allow_html=True)

# 5. Transportation Fun Facts
st.header("Transportation Fun Fact")
fact = fetch_transportation_fun_facts()
st.markdown(f"**🚗 Fun Fact:** {fact}")

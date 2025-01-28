# GUI_Software_Submission_2025_EE24B123
# MANOJ SURYA
import streamlit as st
import requests
import pandas as pd
import random

# Constants
WEATHER_API_KEY = "fce5cf9b64b84340a83111313252601"  # Replace with your WeatherAPI key
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
JSONPLACEHOLDER_API_URL = "https://jsonplaceholder.typicode.com/todos"

# Mock Pod Data
pods = [
    {"name": "Avishkar-1", "speed": 800, "battery": 90, "status": "Operational"},
    {"name": "Avishkar-2", "speed": 700, "battery": 75, "status": "Maintenance"},
    {"name": "Avishkar-3", "speed": 600, "battery": 60, "status": "Docked"},
    {"name": "Avishkar-4", "speed": 850, "battery": 95, "status": "Operational"},
]

# Utility Functions
def fetch_weather_data(city: str):
    """Fetch weather data from WeatherAPI."""
    params = {"key": WEATHER_API_KEY, "q": city}
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("error", {}).get("message", "Unknown error")}
    except Exception as e:
        return {"error": str(e)}

def fetch_energy_tips():
    """Fetch random energy-saving tips from JSONPlaceholder API."""
    try:
        response = requests.get(JSONPLACEHOLDER_API_URL)
        if response.status_code == 200:
            tips = response.json()
            return random.choice(tips).get("title", "No tip available")
        return "No energy tips available at the moment."
    except Exception as e:
        return f"Failed to fetch energy tips: {str(e)}"

# Streamlit App
st.set_page_config(page_title="Hyperloop Control Dashboard", layout="wide", page_icon="🚄")

# App Title and Description
st.title("🚄 Hyperloop Control Dashboard")
st.markdown("""
Welcome to the **Hyperloop Control Dashboard**!  
Monitor pod operations, analyze weather conditions, and access insights to ensure smooth Hyperloop operations.  
**Built for the engineers of the future!**  
""")

# Layout
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pod Tracker 🚦")
    # Sidebar filters
    status_filter = st.selectbox("Filter Pods by Status", ["All", "Operational", "Maintenance", "Docked"])
    sort_option = st.selectbox("Sort Pods by", ["None", "Speed", "Battery"])

    # Filter and sort pods
    filtered_pods = [pod for pod in pods if status_filter == "All" or pod["status"] == status_filter]
    if sort_option == "Speed":
        filtered_pods = sorted(filtered_pods, key=lambda x: x["speed"], reverse=True)
    elif sort_option == "Battery":
        filtered_pods = sorted(filtered_pods, key=lambda x: x["battery"], reverse=True)

    # Display pods
    pod_df = pd.DataFrame(filtered_pods)
    st.dataframe(pod_df.style.highlight_max(subset=["speed", "battery"], color="lightgreen"))

with col2:
    st.subheader("Weather and Safe Speed 🌤️")
    city = st.text_input("Enter a city to fetch weather data:", "Chennai")
    if city:
        weather_data = fetch_weather_data(city)
        if "error" in weather_data:
            st.error(f"Error fetching weather data: {weather_data['error']}")
        else:
            weather_desc = weather_data["current"]["condition"]["text"]
            temp = weather_data["current"]["temp_c"]
            safe_speed = 700 if "rain" in weather_desc.lower() else 800

            # Display weather and speed
            st.metric("City", city)
            st.metric("Weather", weather_desc)
            st.metric("Temperature (°C)", temp)
            st.metric("Safe Speed (km/h)", safe_speed)

st.markdown("---")

col3, col4 = st.columns([2, 1])

with col3:
    st.subheader("Energy Optimization 💡")
    energy_tip = fetch_energy_tips()
    st.info(f"**Tip for Engineers:** {energy_tip}")

    st.subheader("Pod Health Insights ⚙️")
    pod1 = st.selectbox("Select Pod 1", [pod["name"] for pod in pods], index=0)
    pod2 = st.selectbox("Select Pod 2", [pod["name"] for pod in pods], index=1)

    if pod1 != pod2:
        pod1_data = next(pod for pod in pods if pod["name"] == pod1)
        pod2_data = next(pod for pod in pods if pod["name"] == pod2)

        comparison_df = pd.DataFrame(
            {
                "Metric": ["Speed (km/h)", "Battery (%)", "Status"],
                pod1: [pod1_data["speed"], pod1_data["battery"], pod1_data["status"]],
                pod2: [pod2_data["speed"], pod2_data["battery"], pod2_data["status"]],
            }
        )
        st.table(comparison_df)

with col4:
    st.subheader("Fun Facts About Hyperloop 🚀")
    facts = [
        "Hyperloop can reach speeds of up to 1200 km/h.",
        "Elon Musk proposed the first Hyperloop concept in 2013.",
        "Hyperloop uses magnetic levitation for smooth operation.",
        "Energy consumption in Hyperloop is much lower than traditional air travel.",
    ]
    st.write(f"💡 **Did You Know?** {random.choice(facts)}")

st.markdown("---")

# Footer
st.markdown("### Built with ❤️ using Streamlit")


```
Create a fork
Push your code in that repo
Finally create a pull request
```
## docs:

### https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request

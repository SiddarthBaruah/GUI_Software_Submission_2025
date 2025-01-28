import streamlit as st
import plotly.express as px
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
import random
from utils1 import get_weather_data

# Function to render headings in white with smaller font size
def render_white_heading(text):
    return f"<h1 style='color: white; font-size: 18px; text-transform: uppercase; font-weight: normal;'>{text}</h1>"

def pod_tracker_page(pod_data):

    col1, col2 = st.columns([2, 3])

    # Manage map state in session_state to prevent reloading
    if "map_pod" not in st.session_state:
        st.session_state.map_pod = pod_data.sample(1).iloc[0]
    # Right: Pod List and Pie Chart
    with col2:
        st.markdown(render_white_heading("Pod List"), unsafe_allow_html=True)
        status_filter = st.selectbox("Filter by Status", ["All"] + pod_data["Status"].unique().tolist())
        sort_by = st.selectbox("Sort By", ["Pod Name", "Current Speed (km/h)", "Battery (%)"])

         # Apply filters and sorting
        filtered_data = pod_data if status_filter == "All" else pod_data[pod_data["Status"] == status_filter]
        sorted_data = filtered_data.sort_values(by=sort_by, ascending=True)
        st.table(sorted_data)
        
        # Battery Level Bar Chart
        st.markdown(render_white_heading("Battery Levels"), unsafe_allow_html=True)
        battery_fig = px.bar(
            pod_data,
            x="Pod Name",
            y="Battery (%)",
            title="Battery Levels of Pods",
            text="Battery (%)",
            color="Battery (%)",
            color_continuous_scale=["#003300", "#00FF00"]  # Green gradient
        )
        battery_fig.update_traces(textposition="outside")
        st.plotly_chart(battery_fig, use_container_width=True)

# Left: Map with a static random location
    with col1:
        st.markdown(render_white_heading("Pod Location"), unsafe_allow_html=True)
        selected_pod = st.session_state.map_pod
        lat, lon = 20.5937, 78.9629  # Coordinates of India
        m = folium.Map(location=[lat, lon], zoom_start=5)
        folium.Marker([lat, lon], popup=f"Pod: {selected_pod['Pod Name']}").add_to(m)
        st_folium(m, width=700, height=500)
       

        st.markdown(render_white_heading("Pod Status Distribution"), unsafe_allow_html=True)
        status_counts = pod_data["Status"].value_counts()
        pie_fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Status Distribution",
            color_discrete_sequence=["#00FF00", "#007700", "#003300"]  # Green shades
        )
        st.plotly_chart(pie_fig, use_container_width=True)


def route_monitoring_page():
    # Input for the city to monitor the weather
    city = st.text_input("Enter Route City", "Chennai")
    api_key = "c7ac17f62814db2f8731b1e3d1d6b22d"  # Replace with your OpenWeatherMap API key

    if st.button("Get Weather Data"):
        try:
            # Fetch data from the API using the utility function
            weather_data = get_weather_data(city, api_key)
            
            # Check if the response is valid
            if weather_data and weather_data.get("cod") == 200:
                # Extract weather data
                weather_description = weather_data['weather'][0]['description'].lower()
                temperature = weather_data['main']['temp']
                wind_speed = weather_data['wind']['speed']
                humidity = weather_data['main']['humidity']
                cloudiness = weather_data['clouds']['all']

                # Display weather information using white text and inline HTML styling
                st.markdown(f"<p style='color:white;'><strong>City:</strong> {city}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:white;'><strong>Weather:</strong> {weather_description.capitalize()}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:white;'><strong>Temperature:</strong> {temperature}°C</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:white;'><strong>Wind Speed:</strong> {wind_speed} m/s</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:white;'><strong>Humidity:</strong> {humidity}%</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:white;'><strong>Cloudiness:</strong> {cloudiness}%</p>", unsafe_allow_html=True)

                # Determine recommended speed range based on weather conditions
                if "rain" in weather_description:
                    recommended_speed = "500-700 km/h"
                    speed_range = [500, 700]
                    st.warning("Rainy conditions detected. Reduce speed.")
                elif "storm" in weather_description or wind_speed >= 15:
                    recommended_speed = "400-600 km/h"
                    speed_range = [400, 600]
                    st.warning("Stormy or windy conditions detected. Further reduce speed.")
                elif cloudiness > 80:
                    recommended_speed = "600-800 km/h"
                    speed_range = [600, 800]
                    st.warning("Heavy cloudiness detected. Operate at moderate speed.")
                elif temperature < 0:
                    recommended_speed = "400-600 km/h"
                    speed_range = [400, 600]
                    st.warning("Freezing temperatures detected. Operate at reduced speed.")
                else:
                    recommended_speed = "900-1200 km/h"
                    speed_range = [900, 1200]
                    st.success("Weather conditions are optimal for high-speed travel.")

                # Display the recommended speed range
                st.write(f"**Recommended Speed Range:** {recommended_speed}")

                # Speed gauge visualization
                import plotly.graph_objects as go
                gauge_fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=(speed_range[0] + speed_range[1]) / 2,  # Average speed in the range
                    gauge={
                        "axis": {"range": [0, 1200]},
                        "steps": [
                            {"range": [0, 400], "color": "lightgray"},
                            {"range": [400, 700], "color": "yellow"},
                            {"range": [700, 900], "color": "lightgreen"},
                            {"range": [900, 1200], "color": "green"},
                        ],
                        "bar": {"color": "darkblue"}
                    },
                    title={"text": "Recommended Speed (km/h)"}
                ))
                st.plotly_chart(gauge_fig, use_container_width=True)
            else:
                st.error("Failed to fetch weather data. Please check the city name or API key.")
        except Exception as e:
            st.error(f"An error occurred: {e}")


def energy_optimization_page():
    st.markdown("<h1>Energy Optimization</h1>", unsafe_allow_html=True)

    if st.button("Get Energy-Saving Tip"):
        tips_url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(tips_url)

        if response.status_code == 200:
            posts = response.json()
            selected_post = random.choice(posts)
            st.info(selected_post["title"])
            st.write(selected_post["body"])
        else:
            st.error("Failed to fetch data.")


def pod_health_insights_page(pod_data):
    st.markdown("<h1>Pod Health Insights</h1>", unsafe_allow_html=True)

    pod1 = st.selectbox("Select Pod 1", pod_data["Pod Name"])
    pod2 = st.selectbox("Select Pod 2", pod_data["Pod Name"])

    if pod1 != pod2:
        pod1_data = pod_data[pod_data["Pod Name"] == pod1].iloc[0]
        pod2_data = pod_data[pod_data["Pod Name"] == pod2].iloc[0]

        # Prepare comparison data
        comparison_data = pd.DataFrame({
            "Parameter": ["Current Speed (km/h)", "Battery (%)", "Status"],
            pod1: [pod1_data["Current Speed (km/h)"], pod1_data["Battery (%)"], pod1_data["Status"]],
            pod2: [pod2_data["Current Speed (km/h)"], pod2_data["Battery (%)"], pod2_data["Status"]],
        })

        # Display comparison
        st.table(comparison_data)

        # Create comparison graph
        fig = px.bar(
            comparison_data.melt(id_vars=["Parameter"], var_name="Pod", value_name="Value"),
            x="Parameter", y="Value", color="Pod", barmode="group", title="Pod Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Select two different pods for comparison.")


import streamlit as st
import pandas as pd
import requests
import json
import folium
from streamlit_folium import folium_static
import random

# Set page configuration as the very first Streamlit command
st.set_page_config(page_title="Avishkar Hyperloop Control Center", layout="wide")

# Load the JSON data
with open('db.json') as f:
    pod_data = json.load(f)

# Convert JSON data to DataFrame
pods_df = pd.DataFrame(pod_data['pods'])

#load css
# def load_css(file_name):
#     st.markdown(f'<link rel="stylesheet" href="{file_name}">', unsafe_allow_html=True)
def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Page 1: Main Page
def main_page():
    st.title(" Avishkar Hyperloop Control Center")
    st.header("Pod Tracker")

    # Search filter
    search_term = st.text_input("Search pods by name:")
    filtered_pods = pods_df[pods_df['name'].str.contains(search_term, case=False)]

    # Status filter
    status_filter = st.multiselect(
        "Filter by Status",
        options=pods_df['status'].unique(),
        default=pods_df['status'].unique()
    )
    filtered_pods = filtered_pods[filtered_pods['status'].isin(status_filter)]

    # Sorting
    sort_by = st.selectbox(
        "Sort By",
        ['name', 'speed', 'battery', 'status']
    )
    filtered_pods = filtered_pods.sort_values(by=sort_by)

    # Display pods in a grid
    cols = st.columns(3)
    for idx, pod in filtered_pods.iterrows():
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="pod-card">
                <h3>{pod['name']}</h3>
                <p>Status: <span class="metric-value">{pod['status']}</span></p>
                <p>Speed: <span class="metric-value">{pod['speed']} km/h</span></p>
                <p>Battery: <span class="metric-value">{pod['battery']}%</span></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f" View Details for {pod['name']}"):
                st.session_state.selected_pod = pod['id']
                st.session_state.page = 'details'
                st.rerun()

# Page 2: Pod Details
def pod_details_page():
    st.title("🚀 Avishkar Hyperloop Control Center (2035)")
    st.header("Pod Details")

    selected_pod = pods_df[pods_df['id'] == st.session_state.selected_pod].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="pod-card">
            <h3>{selected_pod['name']}</h3>
            <p>Status: <span class="metric-value">{selected_pod['status']}</span></p>
            <p>Speed: <span class="metric-value">{selected_pod['speed']} km/h</span></p>
            <p>Battery: <span class="metric-value">{selected_pod['battery']}%</span></p>
            <p>Location: <span class="metric-value">Lat {selected_pod['lat']}, Lon {selected_pod['lon']}</span></p>
        </div>
        """, unsafe_allow_html=True)

        # Weather information
        st.subheader("Weather Information")
        weather = fetch_weather_data(selected_pod['lat'], selected_pod['lon'])
        if weather:
            st.markdown(f"""
            <div class="weather-card">
                <p>Temperature: <span class="metric-value">{weather['Temperature']:.1f}°C</span></p>
                <p>Wind Speed: <span class="metric-value">{weather['Wind Speed']:.1f} km/h</span></p>
                <p>Conditions: <span class="metric-value">{weather['Conditions']}</span></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("Weather information not available")

        # Route tips
        st.subheader("Route Tips")
        st.write("- Always check pod status before departure")
        st.write("- Monitor weather conditions for optimal travel")
        st.write("- Ensure battery levels are sufficient for the journey")

    with col2:
        st.subheader("Pod Location and Route")
        map = create_map(selected_pod)
        folium_static(map)

    if st.button("Back to Pod List"):
        st.session_state.page = 'main'
        st.rerun()

def fetch_weather_data(lat, lon):
    api_key = '027bbf8aeb974f3e9dd210621252301'
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}&aqi=no'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = {
            'Temperature': data['current']['temp_c'],
            'Wind Speed': data['current']['wind_kph'],
            'Conditions': data['current']['condition']['text'].capitalize()
        }
        return weather
    else:
        return None

def create_map(pod):
    # Create a map centered on the pod's location
    m = folium.Map(location=[pod['lat'], pod['lon']], zoom_start=6)

    # Add pod marker
    folium.Marker(
        [pod['lat'], pod['lon']],
        popup=pod['name'],
        icon=folium.Icon(color='red', icon='rocket', prefix='fa')
    ).add_to(m)

    # Generate two random stations
    stations = generate_random_stations(pod['lat'], pod['lon'])

    # Add station markers
    for idx, station in enumerate(stations):
        folium.Marker(
            [station['lat'], station['lon']],
            popup=f"Station {idx+1}",
            icon=folium.Icon(color='blue', icon='train', prefix='fa')
        ).add_to(m)

    # Draw track
    track_coordinates = [
        (stations[0]['lat'], stations[0]['lon']),
        (pod['lat'], pod['lon']),
        (stations[1]['lat'], stations[1]['lon'])
    ]
    folium.PolyLine(track_coordinates, color="purple", weight=2, opacity=0.8).add_to(m)

    return m
# def create_map(pod):
#     # Create a DataFrame with pod and station locations
#     stations = generate_random_stations(pod['lat'], pod['lon'])
#     locations = [{'lat': pod['lat'], 'lon': pod['lon'], 'name': pod['name']}]
#     for idx, station in enumerate(stations):
#         locations.append({'lat': station['lat'], 'lon': station['lon'], 'name': f"Station {idx+1}"})
    
#     map_df = pd.DataFrame(locations)
    
#     # Use st.map to display the map
#     st.map(map_df)

def generate_random_stations(pod_lat, pod_lon):
    stations = []
    for _ in range(2):
        lat_offset = random.uniform(-2, 2)
        lon_offset = random.uniform(-2, 2)
        stations.append({
            'lat': pod_lat + lat_offset,
            'lon': pod_lon + lon_offset
        })
    return stations

# Page 3: Pod Comparison
def pod_comparison_page():
    st.title("🚀 Avishkar Hyperloop Control Center (2035)")
    st.header("Pod Comparison")

    col1, col2 = st.columns(2)

    with col1:
        pod1 = st.selectbox("Select first pod", options=pods_df['name'], key="pod1")
    with col2:
        pod2 = st.selectbox("Select second pod", options=pods_df['name'], key="pod2")

    if pod1 and pod2:
        pod1_data = pods_df[pods_df['name'] == pod1].iloc[0]
        pod2_data = pods_df[pods_df['name'] == pod2].iloc[0]

        st.markdown(f"""
        <div class="comparison-card">
            <table>
                <tr>
                    <th>Metric</th>
                    <th>{pod1}</th>
                    <th>{pod2}</th>
                </tr>
                <tr>
                    <td>Status</td>
                    <td class="metric-value">{pod1_data['status']}</td>
                    <td class="metric-value">{pod2_data['status']}</td>
                </tr>
                <tr>
                    <td>Speed</td>
                    <td class="metric-value">{pod1_data['speed']} km/h</td>
                    <td class="metric-value">{pod2_data['speed']} km/h</td>
                </tr>
                <tr>
                    <td>Battery</td>
                    <td class="metric-value">{pod1_data['battery']}%</td>
                    <td class="metric-value">{pod2_data['battery']}%</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

# Sidebar navigation
def sidebar_navigation():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Pod Details", "Pod Comparison"])
    
    if page == "Home":
        st.session_state.page = 'main'
    elif page == "Pod Details":
        if 'selected_pod' not in st.session_state:
            st.sidebar.warning("Please select a pod from the main page first.")
        else:
            st.session_state.page = 'details'
    elif page == "Pod Comparison":
        st.session_state.page = 'comparison'

# Main app logic
def main():
   # st.set_page_config(page_title="Avishkar Hyperloop Control Center", page_icon="🚀", layout="wide")
    load_css("style2.css")

    if 'page' not in st.session_state:
        st.session_state.page = 'main'

    sidebar_navigation()

    if st.session_state.page == 'main':
        main_page()
    elif st.session_state.page == 'details':
        pod_details_page()
    elif st.session_state.page == 'comparison':
        pod_comparison_page()

if __name__ == "__main__":
    main()

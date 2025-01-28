import streamlit as st
from streamlit_option_menu import option_menu
from dash import display_control_dashboard
from styles import load_css
from utils1 import get_pod_data, get_weather_data
from d3 import pod_tracker_page, route_monitoring_page, energy_optimization_page, pod_health_insights_page
import requests  # Added import for requests
import random

# Configure Streamlit theme
st.set_page_config(page_title="Avishkar Hyperloop Dashboard", layout="wide")

# Load custom CSS
st.markdown(load_css("styles1.py"), unsafe_allow_html=True)

# Display Control Dashboard once
if "control_dashboard_displayed" not in st.session_state:
    st.session_state.control_dashboard_displayed = False

if not st.session_state.control_dashboard_displayed:
    display_control_dashboard()
    st.session_state.control_dashboard_displayed = True

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Dashboard",
        options=["Pod Tracker", "Route Monitoring", "Energy Optimization", "Pod Health Insights"],
        icons=["list", "cloud", "lightbulb", "bar-chart"],
        menu_icon="menu-button",
        default_index=0,
        styles={
            "container": {"background-color": "black"},
            "nav-link": {
                "font-size": "16px",
                "color": "white",  # White for menu text
                "--hover-color": "#333333",  # Dark hover effect
            },
            "nav-link-selected": {"background-color": "#005500", "color": "white"},  # Highlight green
        },
    )

# Static Pod Data
pod_data = get_pod_data()

# Function to render headings in uppercase without bold
def render_heading(text):
    return f"<h1 style='color: #00FF00; text-transform: uppercase; font-weight: normal;'>{text}</h1>"

# Render the selected page
if selected == "Pod Tracker":
    st.markdown(render_heading("Pod Tracker"), unsafe_allow_html=True)
    pod_tracker_page(pod_data)
    
    # Apply white color only to the relevant headings within Pod Tracker page
    st.markdown("""
        <style>
            /* Apply white color to specific Pod Tracker headings */
            .pod-list-heading, .pod-location-heading, .pod-status-heading {
                color: white !important;
                font-size: 20px;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

elif selected == "Route Monitoring":
    st.markdown(render_heading("Route Monitoring"), unsafe_allow_html=True)
    route_monitoring_page()

elif selected == "Energy Optimization":
    st.markdown(render_heading("Energy Optimization"), unsafe_allow_html=True)

    if st.button("Get Energy-Saving Tip"):
        tips_url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(tips_url)

        if response.status_code == 200:
            posts = response.json()
            selected_post = random.choice(posts)
            st.markdown(
                f"<p style='color: white;'><b>{selected_post['title']}</b></p>", unsafe_allow_html=True
            )
            st.markdown(
                f"<p style='color: white;'>{selected_post['body']}</p>", unsafe_allow_html=True
            )
        else:
            st.error("Failed to fetch data.")

elif selected == "Pod Health Insights":
    pod_health_insights_page(pod_data)


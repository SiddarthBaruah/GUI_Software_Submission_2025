import streamlit as st
import requests
import pandas as pd
import random

# Sample pod data
pods = [
    {"name": "Avishkar-1", "speed": 800, "battery(%)": 90, "status": "Operational"},
    {"name": "Avishkar-2", "speed": 750, "battery(%)": 80, "status": "Maintenance"},
    {"name": "Avishkar-3", "speed": 0, "battery(%)": 100, "status": "Docked"},
    {"name": "Avishkar-4", "speed": 700, "battery(%)": 60, "status": "Operational"},
]

# API keys and endpoints
WEATHER_API_KEY = "4e266a963fafd84e7ab7dafb067c1dcb"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
ENERGY_TIPS_URL = "https://jsonplaceholder.typicode.com/posts"

# Streamlit App
st.set_page_config(page_title="Hyperloop Control Dashboard", layout="wide")

# Custom CSS for styling
st.markdown(


#      """
#     <style>
#     /* Main body styles */
# body {
#   background-color: green; /* Optional: Set background color for the main body */
#   color: black;
# }

# /* Sidebar container */
# .css-1d391kg {
#   background-color: black !important;
#   color: lime !important;
# }

# /* Text input field in the sidebar */
# .css-1d391kg .stTextInput input {
#   background-color: black !important;
#   color: lime !important;
#   border: 2px solid lime !important;
# }

# /* Sidebar elements */
# .css-1d391kg [data-baseweb="select"], .css-1d391kg button {
#   color: lime !important;
#   background-color: black !important;
#   border: 1px solid lime !important;
# }

# /* Hover effect for dropdowns and buttons */
# .css-1d391kg [data-baseweb="select"]:hover, .css-1d391kg button:hover {
#   color: black !important;
#   background-color: white !important;
# }

# /* Sidebar headers and text */
# .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg p {
#   color: lime !important;
# }
#      </style>
#      """,

 """
    <style>

    /* Change text color to black */
    .main {
        color: black !important;
    }

    /* If you want to adjust header text color too */
    .streamlit-expanderHeader, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }

    .st-bd {
        background-color: black !important;
        color: lime !important;
    }

    .st-bd * {
        color: lime !important; 
    }

    .st-bd input, 
    .st-bd select, 
    .st-bd button, 
    .st-bd label { 
        background-color: black !important; 
        color: lime !important;
        border: 1px solid lime !important; 
    }

    .st-bd input:hover, 
    .st-bd select:hover, 
    .st-bd button:hover, 
    .st-bd label:hover {
        background-color: white !important;
        color: black !important;
    }

    /* Target the main content area (adjust class name if needed) */
    # .st-c0 { 
    #     color: black !important; 
    # }

    /* Style multiselect dropdown options */
    .st-bd [data-baseweb="select"] .st-du-option { 
        background-color: black !important;
        color: lime !important;
    }
    .stDataFrame {
        color: black !important;
        border: 3px solid black !important;
    }
    .stDataFrame th {
        color: black !important;
        border: 1px solid black !important;
    }
    .stDataFrame td {
        color: black !important;
        border: 1px solid black !important;
    }

    table {
        #color: black !important;
        #background-color:black;
        border: 3px solid black !important;
    }
     table th {
        color: black !important;
        border: 1px solid black !important;
        #background-color: black;
    }
     table td {
     border: 1px solid black !important;
        color: black !important;   
    }

    .sidebar .sidebar-content h1 {
        #color: #1DF310;
        #background-color: #1DF310;
        #: 1px solid #1DF310 !important;
        }
        .big-font {
    font-size: 30px !important;
}
   
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚄 Hyperloop Control Dashboard")
st.sidebar.markdown('<p class="big-font">Control Center</p>', unsafe_allow_html=True)
# st.sidebar.markdown(
#     "<h1 style='color: #1DF310;'>Control Center</h1>", 
#     unsafe_allow_html=True
# )

# Pod Tracker
st.header("Pod Tracker")
status_filter = st.sidebar.multiselect(
    "Filter by Status", options=["Operational", "Maintenance", "Docked"]
)
sort_option = st.sidebar.radio("Sort By", options=["Speed", "Battery(%)"])
filtered_pods = [pod for pod in pods if pod["status"] in status_filter or not status_filter]
sorted_pods = sorted(filtered_pods, key=lambda x: x[sort_option.lower()], reverse=True)

pod_df = pd.DataFrame(sorted_pods)
df_html = pod_df.to_html(classes="dataframe", escape=False)
st.markdown(df_html, unsafe_allow_html=True)
#st.dataframe(pod_df)

# Route Monitoring
st.header("Route Monitoring")
route_city = st.sidebar.text_input("Enter Route City", "Los Angeles")
if st.sidebar.button("Get Weather"):
    params = {"q": route_city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        st.write(f"### Weather in {route_city}")
        st.write(f"**Temperature:** {weather_data['main']['temp']}°C")
        st.write(f"**Condition:** {weather_data['weather'][0]['description']}")
        if "rain" in weather_data["weather"][0]["description"].lower():
            st.write("🚧 Suggested Speed Limit: 700 km/h (Rainy)")
        else:
            st.write("🚀 Suggested Speed Limit: 1000 km/h (Clear Skies)")
    else:
        st.error("Failed to fetch weather data. Check the city name or API key.")

# Energy Optimization
st.header("Energy Optimization")
if st.sidebar.button("Get Energy Tip"):
    tips_response = requests.get(ENERGY_TIPS_URL)
    if tips_response.status_code == 200:
        tips = tips_response.json()
        random_tip = random.choice(tips)
        st.info(f"💡 Energy Tip: {random_tip['title']}")
    else:
        st.error("Failed to fetch energy tips. Try again later.")

# Pod Health Insights
st.header("Pod Health Insights")
pod1 = st.selectbox("Select First Pod", options=[pod["name"] for pod in pods])
pod2 = st.selectbox("Select Second Pod", options=[pod["name"] for pod in pods if pod["name"] != pod1])

if pod1 and pod2:
    pod1_data = next(pod for pod in pods if pod["name"] == pod1)
    pod2_data = next(pod for pod in pods if pod["name"] == pod2)
    comparison_df = pd.DataFrame([pod1_data, pod2_data])
    st.table(comparison_df)

# Footer
st.sidebar.write("---")
st.sidebar.write("Designed by Avishkar Hyperloop Team 🌟")

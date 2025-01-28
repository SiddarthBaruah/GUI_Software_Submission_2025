# GUI_Software_Submission_2025

```
# Avishkar Hyperloop Dashboard

## Overview
The **Avishkar Hyperloop Dashboard** is a comprehensive Streamlit application for managing and analyzing Hyperloop operations. The dashboard provides real-time insights and functionalities for:
1. **Pod Tracker**: Track Hyperloop pods, visualize their location and battery levels, and manage operational statuses.
2. **Route Monitoring**: Analyze weather data for routes to determine optimal travel conditions.
3. **Energy Optimization**: Generate energy-saving recommendations for Hyperloop operations.
4. **Pod Health Insights**: Compare critical parameters (speed, battery, status) between pods.

---

## Project Structure and Flow Chart

### File Overview
1. **d2.py**: The main application script managing the dashboard's navigation and rendering.
2. **d3.py**: Implements the detailed logic for Pod Tracker, Route Monitoring, and Pod Health Insights.
3. **utils1.py**: Provides utility functions such as fetching pod data and weather data.
4. **styles1.py**: Handles custom CSS styling for the dashboard. Along with Styles.css file
5. **display_control_dashboard**: A function used to display a control dashboard, imported from dash.py

### Flow Chart
```plaintext
d2.py (Main Dashboard)
│
├── utils1.py
│   ├── get_pod_data(): Provides static data for Hyperloop pods.
│   ├── get_weather_data(city, api_key): Fetches weather data from OpenWeatherMap API.
│
├── d3.py (Contains dashboard pages)
│   ├── pod_tracker_page(pod_data): Displays pod list, battery levels, and map visualization.
│   ├── route_monitoring_page(): Fetches weather data and provides speed recommendations.
│   ├── energy_optimization_page(): Generates random energy-saving tips.
│   ├── pod_health_insights_page(pod_data): Compares key parameters between pods.
│
├── styles1.py: Custom CSS for styling the dashboard.
└── display_control_dashboard (Imported): Displays control features on the dashboard.

**Packages to Install**
To execute this project, install the following Python packages:

pip install streamlit
pip install streamlit-option-menu
pip install plotly
pip install pandas
pip install folium
pip install streamlit-folium
pip install requests

**Functions and File Explanations**
d2.py (Main Application) 
- Purpose: Manages the Streamlit app's layout, navigation, and integration with submodules.
- Key Components:
    st.set_page_config: Configures the Streamlit app’s page title and layout (wide mode).
    Custom CSS: Loads styling from styles1.py for consistent dashboard design.
    Navigation: Implements a sidebar menu using streamlit-option-menu, allowing users to switch between pages.

- Page Render Logic:
Based on user selection (Pod Tracker, Route Monitoring, etc.), the corresponding function from d3.py is invoked to render the page.

d3.py (Page Logic)
- Key Functions:
    pod_tracker_page(pod_data): Displays pod information in a table.
                                Visualizes battery levels using a bar chart (Plotly).
                                Renders pod location using Folium.
                                Shows the status distribution of pods as a pie chart.

    route_monitoring_page():Accepts a city name and fetches weather data from OpenWeatherMap API.
                            Provides recommended speed ranges based on weather conditions like rain, wind, or freezing temperatures.
                            Visualizes speed recommendations using a Plotly gauge chart.
    
    energy_optimization_page():Fetches random energy-saving tips from a placeholder API.
                               Displays the fetched tips dynamically.

    pod_health_insights_page(pod_data): Compares two selected pods based on speed, battery percentage, and operational status.
                                        Displays the comparison as a table and bar chart.

utils1.py (Utility Functions)
     get_pod_data():
         Returns static data for Hyperloop pods, including name, speed, battery percentage, and status.
     get_weather_data(city, api_key):
         Fetches weather data from OpenWeatherMap API using the provided city and api_key.
         Returns weather details like temperature, wind speed, humidity, and conditions.

styles1.py (Custom CSS)
Contains CSS rules for styling dashboard elements like headings, links, and backgrounds.

**Execution**
   
   streamlit run d2.py

Access the Dashboard: Open your browser and navigate to:
   
   http://localhost:8501

```
## docs:

### https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request

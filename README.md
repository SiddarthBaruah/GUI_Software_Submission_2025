Avishkar Hyperloop Control Dashboard

Overview
The Avishkar Hyperloop Control Dashboard is a comprehensive web application built using Streamlit to monitor and manage a hyperloop transportation system. This dashboard provides real-time tracking of hyperloop pods, route monitoring with weather updates, pod health comparisons, live tracking visualization, and an AI-powered chatbot assistant.

Features
1. Pod Tracker
Real-time updates of pod status, position, speed, and battery levels
Filtering and sorting capabilities for easy monitoring
Dynamic simulation of pod movements and status changes
2. Route Monitoring
Live weather updates for selected cities along routes
Speed recommendations based on current weather conditions
Utilizes the python_weather library for real-time weather data
3. Pod Health Comparison
Visual comparison of selected pods' speed and battery levels
Interactive bar charts for easy analysis
4. Live Tracking
Interactive map showing real-time positions of all pods
Route visualization with color-coded pod markers
Automatic updates every second
5. JARVIS Chatbot
AI-powered assistant for hyperloop-related queries
Utilizes the Groq API for natural language processing
Maintains conversation history for context-aware responses


Installation 
Clone the repository.
Install required dependencies :
pip install -r requirements.txt
Set up API keys:
Obtain a Groq API key and replace the placeholder in the initialize_groq_client() function.
Usage
Run the Streamlit app:
streamlit run main.py

Navigate through the tabs to access different features of the dashboard.
Configuration
Modify the routes list in the code to add or change hyperloop routes.
Adjust the simulate_pods() function to alter pod behavior simulation.
Customize the styling by modifying the CSS in the st.markdown() calls.
Dependencies
streamlit
pandas
plotly
folium
streamlit-folium
groq
requests

Contributing
Contributions to improve the Avishkar Hyperloop Control Dashboard are welcome. Please follow these steps:
Fork the repository
Create a new branch (git checkout -b feature-branch)
Make your changes and commit (git commit -am 'Add new feature')
Push to the branch (git push origin feature-branch)
Create a new Pull Request


Acknowledgments
Streamlit for the web app framework
Groq for the AI chatbot capabilities
weatherapi.com for real-time weather data
All contributors and maintainers of the used libraries

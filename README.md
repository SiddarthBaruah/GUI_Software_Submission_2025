#Avishkar Hyperloop Control Center

This project is a Streamlit-based web application for monitoring and controlling Avishkar Hyperloop pods. It provides real-time tracking, status updates, and performance metrics for the hyperloop system.

##Files in this project:
1. Streamlit.py - Main Python script containing the Streamlit application code
2. style2.css - Custom CSS file for styling the web interface
3. db.json - JSON file containing pod data (make sure to create this file if not present)

##To run the application:
1. Ensure you have Python installed on your system
2. Install the required dependencies by running:
   pip install streamlit pandas requests folium streamlit-folium
3. Run the application using the command:
   streamlit run Streamlit.py

##Features:
- Pod tracking with search and filter capabilities
- Interactive map display of pod locations
- Weather information for pod locations
- Pod comparison functionality
- Responsive design with custom CSS styling


import streamlit as st
import pandas as pd
import requests
import random
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Avishkar Hyperloop Control Center",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap');

.stApp {
    background-color: rgba(0, 0, 0, 0.95);
}

.main {
    background-color: rgba(0, 0, 0, 0.95);
}

.stMarkdown, .stTitle, .stHeader {
    font-family: 'Orbitron', sans-serif !important;
    color: #00ff00 !important;
}

div[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    color: #00ff00 !important;
}

div.stButton > button {
    font-family: 'Orbitron', sans-serif !important;
    background-color: rgba(0, 68, 0, 0.8);
    color: #00ff00;
    border: 1px solid #00ff00;
}

div[data-testid="stSelectbox"] {
    font-family: 'Orbitron', sans-serif !important;
    color: #00ff00;
}

div.stDataFrame {
    font-family: 'Orbitron', sans-serif !important;
    background-color: rgba(0, 68, 0, 0.3);
    border: 1px solid #00ff00;
}

div[data-testid="stMetricLabel"] {
    font-family: 'Orbitron', sans-serif !important;
    color: #00ff00;
}

.reportview-container {
    background: rgba(0, 0, 0, 0.95);
}

.sidebar .sidebar-content {
    background: rgba(0, 0, 0, 0.95);
}

h1 {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center !important;
    width: 100% !important;
    color: #00ff00 !important;
    padding: 1rem;
    border-bottom: 2px solid #00ff00;
    margin-bottom: 2rem;
}

div[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0.95);
}

.stWarning {
    background-color: rgba(0, 68, 0, 0.3);
    border: 1px solid #00ff00;
    color: #00ff00;
}

.stInfo {
    background-color: rgba(0, 68, 0, 0.3);
    border: 1px solid #00ff00;
    color: #00ff00;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("Avishkar Hyperloop Control Center")

# Initialize session state
if 'pods' not in st.session_state:
    st.session_state.pods = pd.DataFrame({
        'Pod Name': ['Avishkar-1', 'Avishkar-2', 'Avishkar-3'],
        'Speed (km/h)': [random.uniform(600, 1000) for _ in range(3)],
        'Battery (%)': [random.uniform(60, 100) for _ in range(3)],
        'Status': random.choices(['Operational', 'Maintenance', 'Docked'], k=3)
    })

def update_pod_data():
    for i in range(len(st.session_state.pods)):
        if st.session_state.pods.loc[i, 'Status'] == 'Operational':
            st.session_state.pods.loc[i, 'Speed (km/h)'] = min(1000, st.session_state.pods.loc[i, 'Speed (km/h)'] + random.uniform(-50, 50))
            st.session_state.pods.loc[i, 'Battery (%)'] = max(0, min(100, st.session_state.pods.loc[i, 'Battery (%)'] - random.uniform(0, 1)))

def pod_tracker():
    st.header("Pod Tracker")
    
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ['All'] + list(st.session_state.pods['Status'].unique()))
    with col2:
        sort_by = st.selectbox("Sort by", ['Speed (km/h)', 'Battery (%)'])
    
    filtered_pods = st.session_state.pods
    if status_filter != 'All':
        filtered_pods = filtered_pods[filtered_pods['Status'] == status_filter]
    filtered_pods = filtered_pods.sort_values(by=sort_by, ascending=False)
    
    st.dataframe(
        filtered_pods,
        column_config={
            "Speed (km/h)": st.column_config.NumberColumn(format="%.2f"),
            "Battery (%)": st.column_config.ProgressColumn(min_value=0, max_value=100)
        },
        hide_index=True
    )

def route_monitor():
    st.header("Route Weather Monitor")
    weather = {
        'condition': random.choice(['Clear', 'Rain', 'Cloudy']),
        'temperature': random.uniform(20, 35),
        'humidity': random.uniform(40, 90)
    }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Weather", weather['condition'])
    with col2:
        st.metric("Temperature", f"{weather['temperature']:.1f}°C")
    with col3:
        st.metric("Humidity", f"{weather['humidity']:.1f}%")
    
    speed_limit = 1000 if weather['condition'] == 'Clear' else 700
    st.warning(f"Recommended Speed Limit: {speed_limit} km/h")

def energy_section():
    st.header("Energy Optimization")
    tips = [
        "Optimize pod aerodynamics to reduce energy consumption",
        "Schedule maintenance during off-peak hours",
        "Use regenerative braking to recover energy",
        "Monitor battery temperature for optimal performance"
    ]
    st.info(random.choice(tips))

def pod_comparison():
    st.header("Pod Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        pod1 = st.selectbox("Select First Pod", st.session_state.pods['Pod Name'], key='pod1')
    with col2:
        pod2 = st.selectbox("Select Second Pod", st.session_state.pods['Pod Name'], key='pod2')
    
    if pod1 and pod2:
        data1 = st.session_state.pods[st.session_state.pods['Pod Name'] == pod1].iloc[0]
        data2 = st.session_state.pods[st.session_state.pods['Pod Name'] == pod2].iloc[0]
        
        fig = go.Figure()
        parameters = ['Speed (km/h)', 'Battery (%)']
        
        fig.add_trace(go.Bar(
            name=pod1,
            x=parameters,
            y=[data1['Speed (km/h)'], data1['Battery (%)']],
            marker_color='#00ff00'
        ))
        
        fig.add_trace(go.Bar(
            name=pod2,
            x=parameters,
            y=[data2['Speed (km/h)'], data2['Battery (%)']],
            marker_color='#004400'
        ))
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#00ff00',
            title_text="Pod Performance Comparison",
            title_font_color='#00ff00'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    update_pod_data()
    
    pod_tracker()
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        route_monitor()
    with col2:
        energy_section()
    
    st.divider()
    pod_comparison()

if __name__ == "__main__":
    main()

1.	

import numpy as np
import pandas as pd
import random
import streamlit as st
class new_pod:
    def __init__(self, name):
        self.location = random.choices([(13.0827, 80.2707),(35.6895, 139.6917),(30.0444, 31.2357),(55.7558, 37.6173),(40.7128, -74.0060),(40.4319, 116.5704),(27.1751, 78.0421)])
        self.name = name
        self.speed = float(np.random.randint(300,1200))
        self.pod_status = random.choice(["Docked","Maintenance","Operational"])
        self.battery_level = float(np.random.randint(0,100))
        self.maintenance = random.choice(["None","Major","Minor"])
        
    def new_row(self,d):
        if f'speed{i+1}' not in st.session_state:
            st.session_state['speed'+str(i+1)] = self.speed
        if f'pod_status{i+1}' not in st.session_state:
            st.session_state['pod_status'+str(i+1)] = self.pod_status
        if f'battery_level{i+1}' not in st.session_state:
            st.session_state['battery_level'+str(i+1)] = self.battery_level
        if f"location{i+1}" not in st.session_state:
            st.session_state[f'location{i+1}'] = self.location
        if f"maintenance{i+1}" not in st.session_state:
            st.session_state['maintenance'+str(i+1)] = self.maintenance


        new_row = {
            'name':self.name,
            'speed':int(st.session_state[f'speed{i+1}']),
            'pod status':st.session_state[f'pod_status{i+1}'],
            'battery level':int(st.session_state[f'battery_level{i+1}']),
            'location':st.session_state[f"location{i+1}"],
            'maintenance': st.session_state[f"maintenance{i+1}"]
        }

        d.loc[len(d)] = new_row
        return d
    def creation(d,x):
        global i
        for i in range(x):
            something= new_pod(f"A_{i+1}")
            d = something.new_row(d)
        return d
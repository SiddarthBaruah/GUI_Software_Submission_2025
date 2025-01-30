import streamlit as st
from services.individual_page import individual_page
class sidebar:
	def __init__(self):
		pass
	def creation(data,x):
		page = st.sidebar.selectbox(f"**Go to:** ",["Home"]+[f"A_{i+1}" for i in range(x)])
		for i in range(x):
			if page == f"A_{i+1}":
				page = individual_page.page(data,i+1)
		if page == "Home":
		    st.markdown(f"<span style='color:#FFC196; font-size: 30px'>**POD Overview** </span>",unsafe_allow_html = True,)
		    sort_by = st.sidebar.selectbox("Sort By: ",["Name","Speed","Battery level"])
		    filter_by = st.sidebar.selectbox("Filter by: ",["None","Docked","Maintenance","Operational"])
		    filter_by_maintenance = st.sidebar.selectbox("Filter by: (Maintenance)",["don't filter","None","Major","Minor"])
		    if sort_by == "Name":
		    	data = data.sort_values(by="name")
		    if sort_by == "Speed":
		    	data = data.sort_values(by="speed")
		    if sort_by == "Battery level":
		        data = data.sort_values(by="battery level")
		    if filter_by != "None":
		        data = data.loc[data["pod status"] == filter_by]
		    if filter_by_maintenance != "don't filter":
		    	data = data.loc[data["maintenance"] == filter_by_maintenance]
		    st.write("speeds are in km/h and battery levels are in '%' and location is in terms of latitude and longitude ")
		    st.table(data)
		
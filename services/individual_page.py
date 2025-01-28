import streamlit as st
import pandas as pd
import random
import time
import os
from services.new_pod_creation import new_pod
from services.weather_api import weather_api
from services.custom_json import json
from PIL import Image
class individual_page:
	def __init__(self):
		pass
	def page(d,x):
		st.markdown(f"<span style='color:#FFC196; font-size: 30px'>**Avishkar_{str(x)}** </span>",unsafe_allow_html = True,)
		col1, col2 = st.columns(2)
		with col1:
			latitude = st.session_state[f'location{x}'][0][0]
			st.write(f'**Latitude**: {latitude:.2f}')
			longitude = st.session_state[f'location{x}'][0][1]
			st.write(f'**Longitude**: {longitude:.2f}')
			data = pd.DataFrame({
				'latitude':[latitude],
				'longitude':[longitude]
			})
			data2 = weather_api.get_weather_details(x)
			st.write(f"**Weather Description:** {st.session_state[f'weather_description{x}']}")
			st.write(f"**Temperature:** {st.session_state[f'temperature{x}']}"+str("°C"))
			st.write(f"**Pod Status**: {st.session_state[f'pod_status{x}']}")
			st.map(data)
		with col2:
			st.write(f"**Current speed:** {st.session_state[f'speed{x}']}"+str(" km/h"))
			st.write(f"**Battery Level:** {st.session_state[f'battery_level{x}']:.2f}"+str(" %"))
			if st.button("Real time data"):
				placeholder = st.empty()
				while st.session_state[f"battery_level{x}"]>0:
					st.session_state[f"battery_level{x}"] -= 0.2
					time.sleep(8)
					st.session_state[f"speed{x}"] -= 2
					time.sleep(8)
					st.session_state[f"speed{x}"] += 1
					time.sleep(8)
			st.write(f"**Due to the *excellent battery* that the avishkar team has placed in these pods the battery percentage only lowers for every 30 mins 😏**")
			if int(st.session_state[f'battery_level{x}']) <= 20:
				st.error(f"**Please park the pod to the nearest docking station and charge the battery. Thank you.**")
			st.write(f"**Maintenance:** {st.session_state[f'maintenance{x}']}")
			st.write(f"**Suggested Speed:** {int(st.session_state[f'speed{x}'])+5}"+str(" km/h"))
			if f"{st.session_state[f"weather_description{x}"]}" == "Rainy":
				st.write(f"**Suggest Speed:** Due to severe climatic condition outside ({st.session_state[f"pod_status{x}"]}) we recommend you go at a speed of 700 km/h")
			elif float(f"{st.session_state[f"temperature{x}"]}") <= 1.7:
				st.write(f"**Suggested Speed:** Dues to very low temperature of about {st.session_state[f'temperature{x}']} we recommend you lower you speed to about 600 km/h")
			st.write(f"**POD Overview:**")

			image1 = Image.open('services/images/1.png')
			image2 = Image.open('image2.png')
			image3 = Image.open('image3.png')
			image4 = Image.open('image4.png')
			image5 = Image.open('image5.png')
			image6 = Image.open('image6.png')
			image7 = Image.open('image7.png')
			image8 = Image.open('image8.png')
			image9 = Image.open('image9.png')
			image10 = Image.open('image10.png')
			image11 = Image.open('image11.png')
			image12 = Image.open('image12.png')
			image13 = Image.open('image13.png')
			image14 = Image.open('image14.png')
			image15 = Image.open('image15.png')
			image16 = Image.open('image16.png')

			if f"{st.session_state[f"maintenance{x}"]}" == 'Major':
				image_major = random.choices([image12,image13,image14], k=1)
				if image_major not in st.session_state:
					st.session_state[image_major] = image_major
				st.image(image_major)
				st.markdown(f"**The white squares show the brakes which have not been damaged and the <span style='color: red;'>red</span> ones show the brakes which have been damaged.**", unsafe_allow_html = True)
				st.error(f"**please contact the engineer immediatley** __if you don't want to die__ lol and **stop to the nearest docking station** ")
			elif f"{st.session_state[f"maintenance{x}"]}" == 'Minor':
				image_minor = random.choices([image1,image2,image3,image4,image5,image6,image7,image8,image9,image10], k=1)
				if image_minor not in st.session_state:
					st.session_state[image_minor] = image_minor
				st.image(image_minor)
				st.markdown(f"**The white squares show the brakes which have not been damaged and the <span style='color: red;'>red</span> ones show the brakes which have been damaged.**", unsafe_allow_html = True)
				st.error(f"**please stop to the nearest docking station if you're going for a long ride. Thank you**")
			else:
				st.image(image15)
				st.markdown(f"**The white squares show the brakes which have not been damaged and the <span style='color: red;'>red</span> ones show the brakes which have been damaged.**", unsafe_allow_html = True)
		st.markdown(f"<span style='color:#6667AB; font-size:20px'> Fun Facts About The Hyperloop</span>",unsafe_allow_html = True)
		st.write(json.show_random_api(x))

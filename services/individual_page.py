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
			image2 = Image.open('services/images/2.png')
			image3 = Image.open('services/images/3.png')
			image4 = Image.open('services/images/4.png')
			image5 = Image.open('services/images/5.png')
			image6 = Image.open('services/images/6.png')
			image7 = Image.open('services/images/7.png')
			image8 = Image.open('services/images/8.png')
			image9 = Image.open('services/images/9.png')
			image10 = Image.open('services/images/10.png')
			image11 = Image.open('services/images/11.png')
			image12 = Image.open('services/images/12.png')
			image13 = Image.open('services/images/13.png')
			image14 = Image.open('services/images/14.png')
			image15 = Image.open('services/images/15.png')
			image16 = Image.open('services/images/16.png')

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
		choice = random.choice(["The Hyperloop concept was first proposed by Elon Musk in 2013 as a high-speed transportation system using pods in low-pressure tubes. It aims to reduce travel time between cities to a fraction of the current duration.","Hyperloop pods are designed to travel at speeds of up to 760 mph (1,220 km/h), faster than commercial jetliners. This speed is achieved by using magnetic levitation and reduced air resistance in vacuum tubes.","The system could potentially reduce travel time between Los Angeles and San Francisco to just 35 minutes, compared to the current 6-hour drive. This would revolutionize long-distance travel.","Hyperloop technology uses linear motors to propel the pods, eliminating the need for traditional wheels or engines. The lack of friction allows for more energy-efficient travel.","Elon Musk's original vision for Hyperloop was for it to be a private, open-source project that anyone could contribute to. Several companies, including Virgin Hyperloop and Elon Musk's The Boring Company, are now working on it.","The Hyperloop is expected to have a minimal environmental impact due to its reliance on renewable energy sources. It could even be powered by solar panels installed along the tubes.","While it sounds futuristic, Hyperloop technology is already in development, with test tracks and prototype pods being built and tested in various locations. However, it still faces regulatory and engineering challenges.","The first full-scale test of a Hyperloop pod took place in 2017 in Nevada. The pod reached a speed of 192 mph during the test but still has a long way to go before reaching its maximum potential.","The construction of Hyperloop networks could eventually involve building extensive infrastructure of underground vacuum tubes, which could require vast amounts of resources. However, the potential benefits in speed and efficiency could outweigh the initial investment.","Hyperloop could significantly reduce the need for short-haul flights, contributing to a decrease in carbon emissions and the overall environmental impact of travel. It could be a game-changer for sustainable transportation."])
		st.write("Did You Know?")
		st.write(choice)
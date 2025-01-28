from geopy.geocoders import Nominatim
import streamlit as st
import pydeck as pdk
import time
import requests
import os

def app():
    st.title("Route Monitoring")

    def get_city_from_coordinates(lat, lon):
        # Initialize the geocoder
        geolocator = Nominatim(user_agent="city_locator")

        # Get the location from coordinates
        location = geolocator.reverse((lat, lon), language='en', exactly_one=True)

        # Check if location is found
        if location:
            # Extract city from address
            address = location.raw.get('address', {})
            city = address.get('city', '')
            if not city:
                city = address.get('town', '')
            if not city:
                city = address.get('village', '')
            return city
        else:
            return None

    # Function to render the map with moving route and current position
    def render_map(route, current_position):
        # Line layer for the route
        line_layer = pdk.Layer(
            "LineLayer",
            data=[{"start": route[0], "end": route[1]}],
            get_source_position="start",
            get_target_position="end",
            get_color=[0, 0, 255],  # Blue line
            get_width=5,
        )

        # Scatter layer for the moving cursor (red marker)
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{"position": current_position}],
            get_position="position",
            get_color=[255, 0, 0],  # Red marker
            get_radius=100000,  # Larger marker for visibility
        )

        # View state for the map
        view_state = pdk.ViewState(
            latitude=current_position[1],
            longitude=current_position[0],
            zoom=2,  # Zoom out to see both locations
            pitch=0,
        )

        # Return the Pydeck deck with both layers
        return pdk.Deck(layers=[line_layer, scatter_layer], initial_view_state=view_state)

    # Function to define a pod
    def pods(coords1, coords2, number):
        st.header(f"Pod - Avishkar {number}")
        route = [coords1, coords2]
        current_position = coords1
        map_output = st.empty()
        map_output.pydeck_chart(render_map(route, current_position))
        return map_output

    # Initialize pods
    map_output1 = pods([80.2337, 12.9915], [-74.0060, 40.7128], number=1)
    st.session_state.speed1=1000
    speed1 = st.empty()
    speed1.text(f"Current Speed = {st.session_state.speed1} km/hr")
    placeholder1 = st.empty()
    placeholder1.text("Status - Operational")
    battery1P= st.empty()
    if "battery1" not in st.session_state:
        st.session_state.battery1 = 100
    battery1P.text(f"Battery Status = {st.session_state.battery1}")
    time1 = st.empty()
    time1.text("Current Time left = 16 mins")

    api_key = "581563553001748e3d82d5ecdd5f6da8"
    city = get_city_from_coordinates(72.9133, 19.1334)
    baseurl = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(baseurl)
    data = response.json()

    if data['cod'] == "200":
        forecast = data['list']
        weather_description = forecast[0]
        description = weather_description['weather'][0]['description']
        weather1 = st.empty()
        weather1.text(description)
        if "rain" in description:
            speed1.text("Current speed reduced to 700 km/hr due to rain")
        elif "cloud" in description:
            speed1.text("Current speed reduced to 900 km/h due to cloud")
        else:
            speed1.text("Current speed = 1000km/hr")

    iitm_coords = [80.2337, 12.9915]
    destination_coords1= [-74.0060, 40.7128]
    destination_coords2=[72.9133, 19.1334]
    destination_coords3=[12.5674, 41.8719]

    map_output2 = pods([72.9133, 19.1334], [80.2337, 12.9915], number=2)
    st.session_state.speed2 = 1000
    speed2= st.empty()
    speed2.text(f"Current Speed = {st.session_state.speed2} km/hr")
    placeholder2 = st.empty()
    placeholder2.text("Status - Operational")
    time2 = st.empty()
    time2.text("Current Time left = 16 mins")
    battery2P = st.empty()
    if "battery2" not in st.session_state:
        st.session_state.battery2 = 100
    battery2P.text(f"Battery Status = {st.session_state.battery2}")
    weather2 = st.empty()
    weather2.text(description)

    map_output3 = pods([80.2337, 12.9915], [12.5674, 41.8719], number=3)
    st.session_state.speed3 = 1000
    speed3 = st.empty()
    speed3.text(f"Current Speed = {st.session_state.speed3} km/hr")
    placeholder3 = st.empty()
    placeholder3.text("Status - Operational")
    battery3P = st.empty()
    if "battery3" not in st.session_state:
        st.session_state.battery3 = 100
    battery3P.text(f"Battery Status = {st.session_state.battery3}")
    time3 = st.empty()
    time3.text("Current Time left = 16 mins")
    weather3 = st.empty()
    weather3.text(description)

    if "progress1" not in st.session_state:
        st.session_state.progress1 = 0
    if "progress2" not in st.session_state:
        st.session_state.progress2 = 0
    if "progress3" not in st.session_state:
        st.session_state.progress3 = 0

    while True:
        route1 = [iitm_coords, destination_coords1]
        route2= [destination_coords2, iitm_coords]
        route3 = [iitm_coords, destination_coords3]
        if(st.session_state.progress1>=0):
            current_position = [
                iitm_coords[0] + (destination_coords1[0] - iitm_coords[0]) * (st.session_state.progress1 / 1000),
                iitm_coords[1] + (destination_coords1[1] - iitm_coords[1]) * (st.session_state.progress1 / 1000),
            ]
            tt = 1000 / 60 - st.session_state.progress1 / 60
            t = f"{tt:.2f}"
            time1.text(f"Current time left = {t} minutes")
            map_output1.pydeck_chart(render_map(route1, current_position))
        else:
            st.session_state.battery1 += 6

        if st.session_state.progress1 % 100 == 0:
            api_key = "581563553001748e3d82d5ecdd5f6da8"
            city = get_city_from_coordinates(current_position[1], current_position[0])
            baseurl = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            response = requests.get(baseurl)
            data = response.json()

            if data['cod'] == "200":
                forecast = data['list']
                weather_description = forecast[0]
                description = weather_description['weather'][0]['description']
                #st.text(description)
                weather1.text(description)
                if "rain" in description:
                    st.session_state.speed1=700
                    speed1.text(f"Current speed reduced to {st.session_state.speed1} km/hr due to rain")
                elif "cloud" in description:
                    st.session_state.speed1=900
                    speed1.text(f"Current speed reduced to {st.session_state.speed1} km/hr due to clouds")
                else:
                    st.session_state.speed1=1000
                    speed1.text(f"Current Speed = {st.session_state.speed1} km/hr")
            st.session_state.battery1-=5

        if(st.session_state.progress2>=0):
            current_position = [
                destination_coords2[0] + (iitm_coords[0] - destination_coords2[0]) * (st.session_state.progress2 / 1000),
                destination_coords2[1] + (iitm_coords[1] - destination_coords2[1]) * (st.session_state.progress2/1000),
            ]
            tt = 1000 / 60 - st.session_state.progress2 / 60
            t = f"{tt:.2f}"
            time2.text(f"Current time left = {t} minutes")
            map_output2.pydeck_chart(render_map(route2, current_position))
        else:
            st.session_state.battery2 += 6

        if st.session_state.progress2 % 100 == 0:
            api_key = "581563553001748e3d82d5ecdd5f6da8"
            city = get_city_from_coordinates(current_position[1], current_position[0])
            baseurl = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            response = requests.get(baseurl)
            data = response.json()

            if data['cod'] == "200":
                forecast = data['list']
                weather_description = forecast[0]
                description = weather_description['weather'][0]['description']
                weather2.text(description)
                if "rain" in description:
                    st.session_state.speed2 = 700
                    speed2.text(f"Current speed reduced to {st.session_state.speed2} km/hr due to rain")
                elif "cloud" in description:
                    st.session_state.speed2 = 900
                    speed2.text(f"Current speed reduced to {st.session_state.speed2} km/hr due to clouds")
                else:
                    speed2.text(f"Current Speed = {st.session_state.speed2} km/hr")
            st.session_state.battery2 -= 5

        if(st.session_state.progress3>=0):
            current_position = [
                iitm_coords[0] + (destination_coords3[0] - iitm_coords[0]) * (st.session_state.progress3 / 1000),
                iitm_coords[1] + (destination_coords3[1] - iitm_coords[1]) * (st.session_state.progress3 / 1000),
            ]
            tt = 1000 / 60 - st.session_state.progress3 / 60
            t = f"{tt:.2f}"
            time3.text(f"Current time left = {t} minutes")
            map_output3.pydeck_chart(render_map(route3, current_position))
        else:
            st.session_state.battery3 += 6

        if st.session_state.progress3 % 100 == 0:
            api_key = "581563553001748e3d82d5ecdd5f6da8"
            city = get_city_from_coordinates(current_position[1], current_position[0])
            baseurl = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            response = requests.get(baseurl)
            data = response.json()

            if data['cod'] == "200":
                forecast = data['list']
                weather_description = forecast[0]
                description = weather_description['weather'][0]['description']
                weather3.text(description)
                if "rain" in description:
                    st.session_state.speed3 = 700
                    speed3.text(f"Current speed reduced to {st.session_state.speed3} km/hr due to rain")
                elif "cloud" in description:
                    st.session_state.speed3 = 900
                    speed3.text(f"Current speed reduced to {st.session_state.speed3} km/hr due to clouds")
                else:
                    st.session_state.speed1 = 1000
                    speed3.text(f"Current Speed = {st.session_state.speed3} km/hr")
            st.session_state.battery3 -= 5

        time.sleep(1)  # Adjust speed of movement

        if (st.session_state.progress1 == 1000):
            speed1.text("Recharging Battery")
            placeholder1.text("Status = Reached the destination")
            st.session_state.progress1= (-10)

        if (st.session_state.progress2 == 1000):
            speed2.text("Recharging Battery")
            placeholder2.text("Status = Reached the destination")
            st.session_state.progress2= (-20)

        if (st.session_state.progress3 == 1000):
            speed3.text("Recharging Battery")
            placeholder3.text("Status = Reached the destination")
            st.session_state.progress3 = (-40)

        st.session_state.progress1+=2
        st.session_state.progress2+=1
        st.session_state.progress3+=4
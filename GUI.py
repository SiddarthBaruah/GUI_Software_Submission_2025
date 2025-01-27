import streamlit as st
import pandas as pd
import requests
import random
import pydeck as pdk

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Pod Details", "Weather","Fun Facts","Live Pod Positions"])

with tab1:
    if "pods" not in st.session_state:

        st.session_state.pods = [
            {"Pod Name": "Avishkar-1", "Speed (km/h)": 800,"wear": 0, "Battery (%)": 75, "Status": "Operational"},
            {"Pod Name": "Avishkar-2", "Speed (km/h)": 650,"wear": 5, "Battery (%)": 60, "Status": "Docked"},
            {"Pod Name": "Avishkar-3", "Speed (km/h)": 950,"wear": 75, "Battery (%)": 15, "Status": "Under Maintenance"},
            {"Pod Name": "Avishkar-4", "Speed (km/h)": 700,"wear": 10, "Battery (%)": 85, "Status": "Operational"},
            {"Pod Name": "Avishkar-5", "Speed (km/h)": 850,"wear": 85, "Battery (%)": 10, "Status": "Under Maintenance"}
        ]

    df = pd.DataFrame(st.session_state.pods)

    st.title("Pod Tracker")

    # Allow user to filter by status
    status_filter = st.multiselect("Filter by Status:", options=df["Status"].unique())

    # Allow user to select sorting criteria
    sort_option = st.selectbox("Sort by:", options=["Speed (km/h)", "Battery (%)"])

    # Apply filters
    if status_filter:
        df = df[df["Status"].isin(status_filter)]

    # Sort the DataFrame
    df = df.sort_values(by=sort_option, ascending=False)

    # Display the filtered and sorted data in a table with new indexes
    st.dataframe(df.reset_index(drop = True), use_container_width=True)
    st.divider()


    # Function to simulate wear and tear
    def simulate_wear_and_tear():
        for pod in st.session_state.pods:
            if pod["Status"] == 'Operational':
                pod["wear"] += random.randint(1, 5)     # Random wear and tear increase
                pod["Battery (%)"] -= random.randint(1, 3)  # Random battery drain

                if pod["wear"] > 70 or pod["Battery (%)"] < 20:
                    pod["Status"] = "Maintenance Due"
                else:
                    pod["Status"] = 'Operational'

    st.title("Pod Maintenance Predictor")

    if st.button("Simulate Wear and Tear"):
        simulate_wear_and_tear()
        st.success("Wear and tear simulated and updated!")

    # Display pod statuses
    st.subheader("Pod Status")
    for pod in st.session_state.pods:
        status_message = f"**{pod['Pod Name']}** - Battery: {pod['Battery (%)']}%, Wear: {pod['wear']}%"
        if pod["Status"] == "Maintenance Due":
            st.error(status_message + " (⚠️ Maintenance Required)")

        elif pod["Status"] == 'Operational' or pod["Status"] == 'Docked':
            st.success(status_message + " (✅ No Maintenance Required )")
        elif pod["Status"] == 'Under Maintenance':
            st.warning(status_message + " (🛠️ Under Maintenance)")
    st.divider()

    # Select two pods for comparison
    st.title("Compare Pods")
    show1 = False
    pod1 = st.selectbox("Select First Pod For Comparison", df["Pod Name"])
    pod2 = st.selectbox("Select Second Pod For Comparison", df["Pod Name"])
    if st.button("Compare "):
        show1 = True

    if (pod1 and pod2) and (pod1 != pod2) and (show1 == True):
        pod1_data = df[df["Pod Name"] == pod1].iloc[0]
        pod2_data = df[df["Pod Name"] == pod2].iloc[0]
        comparison = pd.DataFrame({"Parameter": ["Speed (km/h)", "Battery (%)", "Wear (%)"],pod1: [pod1_data["Speed (km/h)"], pod1_data["Battery (%)"], pod1_data["wear"]],pod2: [pod2_data["Speed (km/h)"], pod2_data["Battery (%)"], pod2_data["wear"]]})
        st.write("### Pod Comparison")
        st.table(comparison)

        if st.button("Hide Comparison"):
            show1 = False

    st.divider()

    @st.cache_data(ttl=3600)  # Cache the data to make it faster
    def tip():
        url = "https://jsonplaceholder.typicode.com/comments"
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.json()
        else:
            return []



    if st.button("Get a random energy-saving tip"):

        tip_data = tip()  # Fetch cached data
        if tip_data:
            random_tip = random.choice(tip_data)["body"]
            st.info(random_tip)
            if st.button("Hide tip"):
                st.empty()
        else:
            st.write("No energy-saving tip at the moment.")
            if st.button("Hide tip"):
                st.empty()


# Content for Tab 2
with tab2:
    st.title("Weather Details")

    # OpenWeatherMap API details
    city = st.text_input("Enter Route Location", "Chennai")
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=080cbf332af850d7635fa4653ed5c354&units=metric"

    if st.button("Get Weather Data"):
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
            st.write("Weather:", weather['weather'][0]['description'].capitalize())
            st.write("Temperature:", weather['main']['temp'],"°C" )
            if "rain" in weather["weather"][0]["description"].lower():
                st.warning("Rainy: Reduce speed to 700 km/h.")
            else:
                st.success("Conditions are clear. Speed limit: 1000 km/h.")
        elif response.status_code == 404:
            st.error("Failed to fetch weather data for your current location ")
        else:
            st.error("Enter a valid city")

with tab3:
    manufacturer = st.text_input("Enter a plane manufacturer","boeing")
    manufacturer.lower()
    API_key = '/bqGTFbxNah2Z7j9joAHeQ==fVvbAz0newlr4mtP'
    url  = 'https://api.api-ninjas.com/v1/aircraft?manufacturer={}&model='.format(manufacturer)
    params = {"limit": 10}
    response = requests.get(url, headers={'X-Api-Key': API_key}, params=params)
    try:
        if response.status_code == 200:
            data = response.json()
            number = random.randint(0,9)
            model = data[number]['model']
            max_speed = data[number]['max_speed_knots']
            max_speed = float(max_speed)*1.852001
            max_speed = max_speed//1
            st.write("## Did you know that the",manufacturer.capitalize(),model,"has a max speed of ",max_speed," km/hr")
            if st.button("Generate again"):
                st.empty()
        elif manufacturer == '':
            st.write()
        else:
            st.write("Unable to Fetch Plane Data at the moment")
    except IndexError:
        st.write("Sorry that manufacturer doesn't exist in our database")





with tab4:

    def get_mock_pod_positions():
        return pd.DataFrame({
            "name": ["Avishkar-1", "Avishkar-2", "Avishkar-3"],
            "latitude": [13.0674 + random.uniform(-0.01, 0.01) for a in range(3)],
            "longitude": [80.2376 + random.uniform(-0.01, 0.01) for a in range(3)],
        })


    # Streamlit UI
    st.title("Live Map of Pod Positions")

    # Generate and display the map
    pod_positions = get_mock_pod_positions()

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",
        initial_view_state=pdk.ViewState(
            latitude=13.0827,
            longitude=80.2707,
            zoom=11.5,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=pod_positions,
                get_position="[longitude, latitude]",
                get_color="[200, 30, 0, 160]",
                get_radius=100,
            )
        ],
    ))

    # Optionally refresh pod positions
    if st.button("Refresh Pod Positions"):
        st.rerun()

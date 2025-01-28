import streamlit as st
import random
import requests

# Mock data for pods with added wear and tear feature
pods = [
    {"name": "Avishkar-1", "speed": 850, "battery": 92, "status": "Operational", "description": "High-speed pod ready for testing.", "wear_and_tear": random.randint(50, 100)},
    {"name": "Avishkar-2", "speed": 620, "battery": 80, "status": "Maintenance", "description": "Currently undergoing routine checks.", "wear_and_tear": random.randint(50, 100)},
    {"name": "Avishkar-3", "speed": 0, "battery": 100, "status": "Docked", "description": "Fully charged and awaiting deployment.", "wear_and_tear": random.randint(50, 100)},
    {"name": "Avishkar-4", "speed": 750, "battery": 85, "status": "Operational", "description": "Ready for long-distance operational trials.", "wear_and_tear": random.randint(50, 100)},
]

# Function to fetch weather data
def fetch_weather(city):
    API_KEY = "50c91cc573b9ac2401d12320cbcf27f7"  # Replace with your actual OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Hardcoded energy-saving tips in English
energy_tips = [
    "Turn off lights when you leave a room to save energy.",
    "Use energy-efficient LED bulbs instead of incandescent ones.",
    "Unplug appliances when not in use to avoid phantom energy usage.",
    "Keep windows and doors closed when using air conditioning to maintain the temperature.",
    "Consider using a programmable thermostat to automatically adjust your heating and cooling.",
    "Switch to energy-efficient appliances to reduce energy consumption in the long run.",
    "Wash clothes in cold water to save energy and extend the life of your clothing.",
    "Opt for natural light whenever possible to reduce electricity usage."
]

# Function to display a random energy-saving tip
def fetch_energy_tip():
    return random.choice(energy_tips)

# Hyperloop-related facts (hardcoded list)
hyperloop_facts = [
    "The Hyperloop is a new form of transportation that aims to carry passengers at speeds of over 700 miles per hour.",
    "The idea of the Hyperloop was first proposed by Elon Musk in 2013.",
    "Hyperloop technology involves vacuum tubes and magnetic levitation to reduce friction, allowing for faster travel.",
    "The Hyperloop has the potential to revolutionize long-distance travel, significantly reducing time between cities.",
    "The first real-world Hyperloop test track was built in Nevada, USA by Virgin Hyperloop.",
    "Hyperloop could reduce carbon emissions by providing a more energy-efficient mode of transportation compared to planes and cars."
]

# Function to fetch random facts
def fetch_random_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("text", "No fact available.")
    else:
        return "Failed to fetch fact."

# Streamlit app
st.title("Avishkar Hyperloop Dashboard")
st.subheader("Pioneering the Future of Transportation")

# 1. Pod Management
st.header("Pod Management")

# Filters for pods
status_filter = st.selectbox("Filter pods by status", ["All", "Operational", "Maintenance", "Docked"])
sort_by = st.selectbox("Sort pods by", ["Name", "Speed", "Battery"])

# Filter and sort the pods
filtered_pods = pods if status_filter == "All" else [pod for pod in pods if pod["status"] == status_filter]
if sort_by == "Speed":
    filtered_pods.sort(key=lambda x: x["speed"], reverse=True)
elif sort_by == "Battery":
    filtered_pods.sort(key=lambda x: x["battery"], reverse=True)
else:
    filtered_pods.sort(key=lambda x: x["name"])

# Display pods in a 2x2 grid
columns = st.columns(2)
for idx, pod in enumerate(filtered_pods):
    with columns[idx % 2]:  # Alternate between the two columns
        st.subheader(pod["name"])
        st.write(f"**Speed:** {pod['speed']} km/h")
        st.write(f"**Battery:** {pod['battery']}%")
        st.write(f"**Status:** {pod['status']}")
        st.write(f"**Description:** {pod['description']}")

        # Display wear and tear
        wear_and_tear = pod['wear_and_tear']
        if wear_and_tear > 65:
            st.markdown(f"**Wear and Tear:** <span style='color:red'>{wear_and_tear}% (Requires Maintenance)</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Wear and Tear:** <span style='color:green'>{wear_and_tear}% (No Immediate Maintenance Required)</span>", unsafe_allow_html=True)

        st.write("---")

# 2. Route Monitoring
st.header("Route Monitoring")

city = st.text_input("Enter city for route monitoring", "Mumbai")
if st.button("Fetch Weather Data"):
    weather = fetch_weather(city)
    if weather:
        condition = weather["weather"][0]["description"]
        temp = weather["main"]["temp"]
        st.write(f"**Weather in {city}:** {condition.capitalize()}")
        st.write(f"**Temperature:** {temp}°C")

        if "rain" in condition.lower():
            st.write("**Suggested Speed Limit:** 700 km/h (Rainy Conditions)")
        elif "storm" in condition.lower() or "thunder" in condition.lower():
            st.write("**Suggested Speed Limit:** 500 km/h (Stormy Conditions)")
        else:
            st.write("**Suggested Speed Limit:** 1000 km/h (Optimal Conditions)")
    else:
        st.write("Could not fetch weather data. Please check the city name or API key.")


# Function to fetch energy-saving tips (ensured in English)
def fetch_energy_tips():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json()
        english_tips = [post['title'] for post in posts]  # Extract titles (English)
        random_tip = random.choice(english_tips)  # Select a random English tip
        return random_tip
    else:
        return "Unable to fetch energy-saving tips at the moment."

# Function to fetch real energy-saving tips
def fetch_energy_tips():
    # A list of meaningful energy-saving tips
    tips = [
        "Implementing regenerative braking systems in Hyperloop pods can recapture energy, boosting efficiency.",
        "Advanced lightweight materials, like carbon fiber, enhance Hyperloop energy efficiency.",
        "Utilizing solar panels on Hyperloop infrastructure can generate clean energy, reducing operational costs."
    ]
    return random.choice(tips)  # Return a random meaningful tip

# Energy-Saving Tips Section
st.header("Energy Optimization Tips")
tip = fetch_energy_tips()
st.subheader("Random Energy-Saving Tip:")
st.write(f"**Tip:** {tip}")


# 4. Pod Health Insights
st.header("Pod Health Insights")

pod1 = st.selectbox("Select Pod 1 for comparison", ["None"] + [pod["name"] for pod in pods])
pod2 = st.selectbox("Select Pod 2 for comparison", ["None"] + [pod["name"] for pod in pods])

if pod1 != "None" and pod2 != "None" and pod1 != pod2:
    pod1_data = next(pod for pod in pods if pod["name"] == pod1)
    pod2_data = next(pod for pod in pods if pod["name"] == pod2)

    st.write(f"### Comparing {pod1_data['name']} and {pod2_data['name']}")
    st.write(f"**Speed:** {pod1_data['speed']} km/h vs {pod2_data['speed']} km/h")
    st.write(f"**Battery:** {pod1_data['battery']}% vs {pod2_data['battery']}%")
    st.write(f"**Status:** {pod1_data['status']} vs {pod2_data['status']}")
    st.write(f"**Wear and Tear:** {pod1_data['wear_and_tear']}% vs {pod2_data['wear_and_tear']}%")
else:
    st.write("Please select two different pods for comparison.")

#import streamlit as st
import random
import requests

# Hyperloop-related facts (hardcoded list)
hyperloop_facts = [
    "The Hyperloop is a new form of transportation that aims to carry passengers at speeds of over 700 miles per hour.",
    "The idea of the Hyperloop was first proposed by Elon Musk in 2013.",
    "Hyperloop technology involves vacuum tubes and magnetic levitation to reduce friction, allowing for faster travel.",
    "The Hyperloop has the potential to revolutionize long-distance travel, significantly reducing time between cities.",
    "The first real-world Hyperloop test track was built in Nevada, USA by Virgin Hyperloop.",
    "Hyperloop could reduce carbon emissions by providing a more energy-efficient mode of transportation compared to planes and cars."
]

# Function to fetch a random fact from the Useless Facts API
def fetch_random_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("text", "No fact available.")
    else:
        return "Failed to fetch a random fact."

# Function to fetch a random Hyperloop fact
def fetch_hyperloop_fact():
    return random.choice(hyperloop_facts)

# Streamlit App
st.header("Hyperloop Fun Facts")
st.subheader("Discover something new about Hyperloop and beyond!")

if st.button("Fetch a Fun Fact"):
    # Randomly choose between Useless API fact or Hyperloop fact
    if random.choice([True, False]):
        fact = fetch_random_fact()
        st.write(f"**Did You Know?** {fact}")
    else:
        fact = fetch_hyperloop_fact()
        st.write(f"**Did You Know?** {fact}")

# Function to fetch a limited number of feedback comments in English

# Function to fetch pod feedback (realistic examples)
def fetch_pod_feedback():
    # A list of meaningful feedback for the Hyperloop pods
    feedback = [
        "The pod's speed was exceptional, but it could use more comfortable seating.",
        "Battery life is great, but the pod needs more frequent maintenance checks.",
        "The ride was smooth and quiet—excellent for long journeys.",
        "Pod Avishkar-3 had a minor delay due to wear and tear issues.",
        "I appreciate the eco-friendly nature of the Hyperloop system.",
    ]
    return random.sample(feedback, 2)  # Return 2 random pieces of feedback

# Pod Feedback Section
st.header("Pod Feedback")
st.subheader("Recent Feedback:")
feedbacks = fetch_pod_feedback()
for feedback in feedbacks:
    st.write(f"- {feedback}")



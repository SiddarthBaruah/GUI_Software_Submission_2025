#importing required modules
import streamlit as st
import pandas as pd
import numpy as np
import requests as rq
import random
st.set_page_config(page_title="Avishkar Hyperloop Dashboard", page_icon="🚀")

#Comparing of the Pods
def compare():
    items=['Avishkar1','Avishkar2','Avishkar3','Avishkar4']
    selected=[]
    for item in items:
        if st.checkbox(item):
            selected.append(item)
    if len(selected)>=2:
        batdata={"Pods":selected,"Battery health":df[df['Name'].isin(selected)]['Battery']}
        batdf=pd.DataFrame(batdata)
        batdf.set_index('Pods',inplace=True)
        st.bar_chart(batdf)
        spdata={"Pods":selected,"Average speed":df[df['Name'].isin(selected)]['Speed']}
        spdf=pd.DataFrame(spdata)
        spdf.set_index('Pods',inplace=True)
        st.bar_chart(spdf)
    else:
        st.write("Please select atleast 2 pods to compare")
        
#loction of the pods
def locate(locdf):
    st.map(locdf)
    
#declaring API Keys
wmapupikey='b92903c22af34a3e94154807252101'
wmapupi=r"https://api.weatherapi.com/v1/current.json"
jsonupi=r"https://jsonplaceholder.typicode.com/posts"
image_url=r"https://st3.depositphotos.com/3227089/19322/i/450/depositphotos_193225790-stock-photo-hyperloop-transportation-concept.jpg"
facts_list=[]

#json api
def jsonapi():
    response=rq.get(jsonupi)
    if response.status_code==200:
        posts=response.json()
        random_post=random.choice(posts)
        st.error(f"**A rondom fact on energy optimization**  \n**Title:** {random_post['title']}  \n**Body:** {random_post['body']}")
    else:
        st.info("Nothing recieved")

#weather api
def weather(name):
    jsonapi()
    index=int(name[-1])-1
    lat=location['latitude'][index]
    lon=location['longitude'][index]
    cur_speed=data['Speed'][index]
    bat_level=data['Battery'][index]
    stat=data['Status'][index]
    locnew={"latitude":[lat],"longitude":[lon]}
    locate(locnew)
    parameter={"key":wmapupikey,"q":f"{lat},{lon}"}
    response=rq.get(wmapupi,params=parameter)
    if response.status_code==200:
        dataf=response.json()
        desc=dataf["current"]["condition"]["text"].lower()
        st.write(f"Weather condition: {desc.capitalize()}")
        if "rain" in desc or "shower" in desc or "drizzle" in desc:
            sug_speed=750
        elif "storm" in desc or "blizzard" in desc or "hurricane" in desc or "tornado" in desc:
            sug_speed=0
        elif "gale" in desc or "breeze" in desc or "wind" in desc:
            sug_speed=900
        else:
            sug_speed=1000
        st.write(f"Battery: {bat_level}")
        st.write(f"Status: {stat}")
        if sug_speed==0:
            st.write("EMERGENCY STOP REQUIRED!!!")
        elif cur_speed<=sug_speed:
            st.write(f"Suggested speed for the pod is {sug_speed}.")
            st.write(f"Pods current speed is {cur_speed}.")
        else:
            st.write("Speed of pod needs to be optimized")
            st.write(f"Suggested speed for the pod is {sug_speed}.")
            st.write(f"Pods current speed is {cur_speed}.")
    else:
        st.write("Incorrect coordinates of the location")
    

def fetch_hyperloop_facts():
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": "Hyperloop"
    }
    response = rq.get(url, params=params)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page_id, page_data in pages.items():
        return page_data.get("extract", "No content available")

# Function to extract fun facts from text
def extract_fun_facts(content):
    fun_fact_keywords = ["first", "fastest", "unique", "record", "speed", "concept", "innovative", "proposed", "potential"]
    sentences = content.split(". ")
    fun_facts = [sentence.strip() for sentence in sentences if any(keyword in sentence.lower() for keyword in fun_fact_keywords)]
    return fun_facts

#streamlit main page
facts = fetch_hyperloop_facts()
if facts:
    facts_list = extract_fun_facts(facts)
else:
    st.write("Unable to fetch facts at the moment. Please try again later.")
    
st.sidebar.title("MENU")
option=st.sidebar.selectbox("Pages:",['Home🏠','Locate📍','Compare🆚','Avishkar1','Avishkar2','Avishkar3','Avishkar4','Did You Know?'])
data={"Name":['Avishkar1','Avishkar2','Avishkar3','Avishkar4'],"Speed":[1000,700,850,900],"Battery":[70,90,100,80],"Status":['Docked💤','Maintenance🛠️','Operational🛜','Operational🛜']}
df=pd.DataFrame(data)
filter_on=st.sidebar.selectbox("Filter:",['None','Operational🛜','Maintenance🛠️','Docked💤'])
sort_on=st.sidebar.selectbox("Sort:",['Name','Speed','Battery'])
location={"latitude":[28.7041,19.0760,22.5744,13.0843],"longitude": [77.1025,72.8777,88.3629,80.2705],"city":['Avishkar1','Avishkar2','Avishkar3','Avishkar4']}
locdf=pd.DataFrame(location)
if option=='Home🏠':
    st.markdown("<h1 style='color: red;'>Welcome to Avishkar hyperloop dashboard</h1>", unsafe_allow_html=True)
    if filter_on != 'None':
        df=df.loc[df['Status']==filter_on]
    df=df.sort_values(by=sort_on)
    st.dataframe(df)
    st.image(image_url)
elif option=='Locate📍':
    st.markdown("<h1 style='color: red;'>Locating Pods</h1>", unsafe_allow_html=True)
    locate(locdf)
elif option=='Compare🆚':
    st.markdown("<h1 style='color: red;'>Comparing Pods</h1>", unsafe_allow_html=True)
    compare()
elif option=="Did You Know?":
    st.markdown("<h1 style='color: red;'>5 Random Facts</h1>", unsafe_allow_html=True)
    for i in range(5):
        st.write(f"{i+1}. {random.choice(facts_list)}.")
else:
    st.markdown(f"<h1 style='color: red;'>{option}</h1>", unsafe_allow_html=True)
    weather(option)
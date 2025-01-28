# GUI_Software_Submission_2025
```
Create a fork
Push your code in that repo
Finally create a pull request
```
## docs:

### https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request

# Avishkar Control Dashboard

## Overview
Avishkar Control Dashboard is a web application built with Streamlit that has components such as pod tracker, route monitoring, energy optimisation tips and pod maintainance needs.

---

## Features
1. **Pod Tracker**
    - What it does: Displayes the current speed (in km/h), battery percentage and the status. It also allows to filter the pods based on status. 
    - The thought process for this was pretty straightforward. 
        - Generated mock pod data and used streamlit data editor to display it in the form of a table (so that sorting based on Battery Percentage and Current Speed can be taken care of by streamlit itself and I need not implement it separately).
        - Used streamlit documentation to figure out how to implement multiselect and hence filter based on status.

2. **Route Monitoring**
    - What it does: Allows us to select a location and provide weather conditions and safe speed limits based on the current weather conditions.
    - Thought process and approach:
        - Fetch the weather through the WeatherAPI you had provided. It took me a couple of tries before I figured out how APIs in general and how this API in particular works.
        - I visited the WeatherAPI website to find out the unique weather conditions to map then to speeds. Then I asked ChatGPT to generate a dictionary consisting of unique weather conditions as key and the safe speed limits as value. I just retrieved the value of the key for the speed limit. 

3. **Energy Optimisation**
   - What it does: Provides tips for optimizing energy usage.
   - Thought process and approach:
     - Fetch some random sentences from the JSONPlace holder API. Again took me a few tries to figure out how this API worked.

Once again I went through the streamlit documentation (and used a little bit of ChatGPT) to figure out if there was any way to put (2) and (3) side by side.

4. **Pod Insights**
   - What it does: Comparison tools to compare different pods.
   - Thought process and approach:
     - I asked ChatGPT to generate a code for this and that's how I discovered plotly. I ended up not using the code and referred to plotly's documentation. I initially thought a scatter plot would be good enough and I happened to stumble upon the bar graph in plotly's documentation and thought that was a valuable addition as well. 

5. **Hyperloop fun facts**
    - What it does: Displayes random fun facts about hyperloop systems.
    - Thought process and approach:
        - At this point, I was sort of familiar with how to fetch API's (thanks to question 2 and 3) so all I had to do was find an API. While I couldn't find an API for transport fun fact, and definitely not one for hyperloop alone, I found one that displays random questions about transportation.

6. **Wear Level of Pods**
    - What it does: Tracks the wear level of pods and alerts if wear exceeds 70%.
    - Thought process and approach:
        - Again pretty straightforward approach, just generate random data for the wear level and put them in streamlit data editor, so sorting will take care of itself. Run the wear levels through a loop and display warnings if any of them exceeds 70%.
        - The variable maintain_pods was introduced when I ran the code once but there were no warnings given. I realised after looking at the table that all the pods had wear level below 70% and hence I thought it was important to introduce this (and the column was also looking empty without warnings). 

7. **Pod Insights**
    - What it does: Displays the geographic locations of pods on a world map.
    - Thought process and approach:
        - I asked ChatGPT to generate a code for this part as well, and that's how I found out the scatter_geo function in plotly.

## Installation

### Prerequisites
- Python 3.7 or higher
- Install the required python packages:
    ```bash
    pip install streamlit pandas numpy requests plotly
    ```
---

## How to run
1. Clone the repository:
    ```bash
    git clone https://github.com/LayaLaks/GUI-Module-Avishkar
    cd /workspaces/GUI-Module-Avishkar
    ```

2. Run the streamlit app:
    ```bash
    streamlit run hyperloop.py
    ```

3. A notification would appear to "Open in Browser". Click on that or use the url provided.

---

## API Information

### Weather API
- **Base URL:** `http://api.weatherapi.com/v1/current.json`
- **Key:** Replace the `api_key` variable in the code with your WeatherAPI key.

### Energy Optimization Tips API
- **Base URL:** `https://jsonplaceholder.typicode.com/posts`

### Fun Facts API
- **Base URL:** `https://opentdb.com/api.php?amount=10&category=28`

---
## File Structure
```
.
|-- hyperloop.py # Main streamlit application file
|-- hyperloop_chatgpt_improvements.py # ran my final application through chatgpt and asked to give improvements- can be ignored.
|-- README.md # contains details of thought process and how to run
```

---



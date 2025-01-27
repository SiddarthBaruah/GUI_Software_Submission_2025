# GUI_Software_Submission_2025

## General:

For the General Questionnaire and the responses to the questions, go to the 'TAH GUI app_ED24B051_General and Technical Questionnaire Response.pdf' file.

For Q1, go to 'Q1_final' folder.

For Q2, go to the 'Question 2' section of the pdf; For the bonus part-4, go to 'Q2_part-4_paho-mqtt' folder.

## Approach and Thought process, for Q1:

I have kept in mind the need for a lightweight, yet informative dashboard tool while creating the Streamlit user interface for Question-1. As exemplified in the 'Q1_old' folder, I initially used a sidebar with radio buttons attached for the concept of a lightweight application, then switched to the current use of Navigation panels and modular page codes (increased editing and debugging ease) in the 'pages' directory, as exemplified in the 'Q1_final' folder, which I consider to be my final submission.

To begin with, in 'Dashboard.py', I set the layout to wide to reconcile any table expansions and full view when the navigation panel collapsed; The latter is expanded at the beginning to let the user be aware of its existence and access. The title for the space and some generic instructions follow. An info widget is added at the end to give credit to Streamlit.

Moving on to 'pages/1_Pod_Tracker.py' (the page naming convention is such as to facilitate the Navigation panel to name these pages accordingly, and the pages are arranged in the directory to allow for the same) I create a pandas DataFrame to store the 'pods_data' over classes because DataFrames are easier to visualise as tables and sort/filter with selectbox controls when integrating with Streamlit. Although classes would have been more clean, I also felt there would be an impact on lightweightedness. In case the DataFrame needs to be amended with more pods a function can easily be crafted for the same.

The ```update_live_data``` function gives realistic updation to the ```pods_data```, ensuring Operational pods are updated differently than those that are under Maintenance or are Docked.

The data is updated 20 times with 2 second gaps in between to firstly, simulate real world data communication delays, and secondly, to ensure the live data functionality works as required.

The ```st.empty``` placeholders provide static containers for tables and alerts/widgets to be updated in. If these are not present, previous tables/alerts/widgets are not overwritten and are rather copied. The selectboxes provide for easy integration with pandas DataFrames (boolean selection and ```.sort_values()``` method) for filtering and sorting features. Alerts are only displayed for Operational pods in their respective contexts, while Maintenance Predictor also simulates wear and tear by constant decrement of the measurement variable ```Maintenance Status``` under ```pods_data```.

Then, we come to the API integration parts, which include 'pages/2_Route Monitoring', 'pages/3_Energy_Optimization' and '5_Fun_Facts'. Corresponding to the function required, I have used the requests module to access the URL of the service and if there is a successful response (code ```200```), the required data is extracted from the json and displayed in an intuitive manner. Route Monitoring also has conditionals to display recommended speeds based on certain conditions, names, rain and mist, as these tend to affect the route traversal the most. I have structured this in the most lightweight manner possible to allocate more time for the actual web fetching.

'pages/4_Pod_Health' also uses a similar structure and flow as 'pages/1_Pod_Tracker'. The necessary ```health_metrics``` can be included to be displayed as a table in the list of the same name, located at the start of the file. Selectboxes and ```st.empty()``` placeholders also work as before. The only change is that a comparision table is shown based on the selected options, regarding the health metrics selected for 2 different pods. A warning is displayed is the same pod is selected twice. Updation (20x with 2 second delays) is also done in a similar manner as above.

## Approach and Thought process, for Q2, part 4:

Both the 'publisher.py' and 'subscriber.py' have constants defined at the beginning to facilitate change when necessary. The former then has a function to generate synthetic data (again using the ```pods_data``` format as earlier) and then the normal paho-mqtt syntax for sending data follows to facilitate sourcing on a regular basis via the ```while True``` loop; while the latter first defines a wrapper to print the message once received and then proceeds to have syntax of paho-mqtt to receive messages on a regular basis, inciting a listener to have undistrupted coverage (```loop_forever()```)

## Instructions to run the Q1 application:

1) Install streamlit via pip.
2) Navigating to inside the 'Q1_final' folder, run this command in your terminal: ```streamlit run Dashboard.py```
3) The app will open in your default browser.

## Instructions to run the Q2, part 4 scripts:

1) Install paho-mqtt via pip, and the Mosquitto broker from the internet.
2) Navigating to inside the 'Q2_part-4_paho-mqtt' folder, run this in one terminal: ```python publisher.py``` and this in another: ```python subscriber.py```
3) The first sends messages on a regular interval to the other, where it is displayed.
4) Close each of the clients using KeyboardInterrupt via pressing Ctrl+C in each terminal.


## Final thoughts:

I feel that I have done my level best in the application, and am happy with the progress I made, in learning, exploring and implementing. I would therefore like feedback on where I can improve whatsoever the status of the application. Thank You for the opportunity!

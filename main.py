import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="AVISHKAR")

load_dotenv()

import Route_Monitoring, Energy_tips, Health_of_pods, Filter_pods

# Google Analytics Integration
st.markdown(
    """
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src=f"https://www.googletagmanager.com/gtag/js?id={os.getenv('analytics_tag')}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', os.getenv('analytics_tag'));
        </script>
    """, unsafe_allow_html=True)

print(os.getenv('analytics_tag'))  # Logging the analytics tag for verification


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """ Add a new app to the list of apps """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        """ Run the selected app """
        # Sidebar to select the app
        with st.sidebar:
            app = option_menu(
                menu_title='Pondering',
                options=['Route_Monitoring','Filter_pods', 'Energy_tips', 'Health_of_pods' ],
                icons=['house-fill', 'person-circle', 'trophy-fill', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Run the corresponding app function based on the selection
        if app == "Route_Monitoring":
            Route_Monitoring.app()
        elif app == "Energy_tips":
            Energy_tips.app()
        elif app == "Health_of_pods":
            Health_of_pods.app()
        elif app == "Filter_pods":
            Filter_pods.app()


# Instantiate the MultiApp class and run the selected app
app = MultiApp()
app.run()

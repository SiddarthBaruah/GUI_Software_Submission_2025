import streamlit as st

# Configure the app's layout
st.set_page_config(page_title="Avishkar Control", layout="wide",
                   initial_sidebar_state="expanded")

# Main title for the dashboard
st.title("Avishkar Control")

st.write(
    """
    Welcome to the Hyperloop Control Dashboard. \n
    Use the navigation bar on the right to access different sections of the application.

    Pages include:
    - Pod Tracker: Monitor the status of the pods in real-time.
    - Route Monitoring: Track the weather, get related notifications and progress of the pods.
    - Energy Optimization: Get notifications to optimize energy consumption of the pods.
    - Pod Health: Monitor the health of the pods via comparing health metrics.
    - Did You Know?: Fun facts about Hyperloop for keeping up your enthu.\n\n

    Continue tracking the Avishkar Hyperloop Pods!
    """
)

st.info("Built with Streamlit by Avishkar Hyperloop")

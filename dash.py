# dashboard.py

import streamlit as st
import time

# Display control dashboard with animations
def display_control_dashboard():
    # Create a placeholder to hold content (for dynamic updates)
    placeholder = st.empty()

    # Display the initial content for "CONTROL DASHBOARD"
    with placeholder.container():
        st.markdown('<div class="container"><div class="title">CONTROL DASHBOARD</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Track your pod</div></div>', unsafe_allow_html=True)

    # Wait for 2 seconds before starting fade-out animation
    time.sleep(2)

    # Fade out the text
    with placeholder.container():
        st.markdown('<div class="container"><div class="title fadeOut">CONTROL DASHBOARD</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle fadeOut">Track your pod</div></div>', unsafe_allow_html=True)

    # Wait for the fade-out to complete (2 seconds)
    time.sleep(2)

    # Transition to a plain black screen after the fade-out
    st.markdown(
        """
        <style>
        body {
            background-color: black;
            color: white;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Clear the text and display the black screen
    st.empty()


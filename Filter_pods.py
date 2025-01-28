import streamlit as st
import pandas as pd
import random

def app():
    # Sample data (you can replace it with your own data)
    data = {
        "Name": ["Pod 1", "Pod 2", "Pod 3"],
        "Speed": [st.session_state.speed1, st.session_state.speed2 ,st.session_state.speed3],
        "Battery": [st.session_state.battery1, st.session_state.battery2, st.session_state.battery3],
    }

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Streamlit UI
    st.title("Filter Data by Attributes")

    # Choose the attribute to sort by
    sort_column = st.selectbox("Select Attribute to Sort By", options=df.columns)

    # Choose the sorting order (ascending or descending)
    sort_order = st.radio("Select Sorting Order", options=["Ascending", "Descending"])

    # Sort the data based on user input
    if sort_order == "Ascending":
        sorted_df = df.sort_values(by=sort_column, ascending=True)
    else:
        sorted_df = df.sort_values(by=sort_column, ascending=False)

    # Display the sorted data
    st.subheader(f"Data Sorted by {sort_column} ({sort_order})")
    st.write(sorted_df)

    # List of facts
    facts = [
        "Hyperloop pods can travel at speeds of up to 760 mph, making them faster than airplanes!",
        "The concept of the Hyperloop was first proposed by Elon Musk in 2013.",
        "Hyperloop systems aim to be more energy-efficient than traditional transportation.",
        "Hyperloop pods use magnetic levitation to eliminate friction, enabling ultra-high speeds."
    ]

    # Select a random fact
    random_fact = random.choice(facts)

    # Add custom CSS for a full-length floating box
    st.markdown(
        f"""
            <style>
            .full-length-box {{
                position: fixed;
                bottom: 0;
                left: 20;
                width:50%;
                background-color: #064e3b; /* Dark green */
                color: white;
                padding: 15px 20px;
                text-align: center;
                font-size: 18px;
                border-top: 4px solid #10b981; /* Light green border at the top */
                box-shadow: 0px -4px 6px rgba(0, 0, 0, 0.1);
                z-index: 1000;
            }}
            </style>
            <div class="full-length-box">
                <strong>Did You Know?</strong> {random_fact}
            </div>
            """,
        unsafe_allow_html=True
    )

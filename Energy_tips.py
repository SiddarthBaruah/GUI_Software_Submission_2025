import requests
import streamlit as st
import random

def app():
    def fetch_random_tips():
        # URL for JSONPlaceholder posts
        api_url = "https://jsonplaceholder.typicode.com/posts"

        try:
            # Fetch posts
            response = requests.get(api_url)
            response.raise_for_status()  # Raise exception if API call fails
            posts = response.json()  # Parse JSON response

            # Randomly select 5 tips from the list of posts
            random_tips = random.sample(posts, 5)

            # Display each tip
            st.title("💡 Energy-Saving Tips for the Engineering Team 💡\n")
            for idx, tip in enumerate(random_tips, start=1):
                st.subheader(f"Tip #{idx}: {tip['title']}")
                st.text(f"Detail: {tip['body']}\n")

        except requests.exceptions.RequestException as e:
            st.text(f"Error fetching tips: {e}")

    # Run the function
    fetch_random_tips()

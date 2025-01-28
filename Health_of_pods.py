import streamlit as st
import random

def app():
    st.title("Health of Pods")

    # Pod 1
    st.subheader("Pod - Avishkar 1")
    st.text(f"Battery = {st.session_state.battery1}%")
    t = random.randint(0, 6)
    if t == 0 or st.session_state.battery1==0:
        st.markdown("⚠️ **Warning:** This is an alert!")
        st.text("Maintenance should be done as soon as possible.")
    else:
        st.text(f"Maintenance should be done within the next {t} days")

    # Pod 2
    st.subheader("Pod - Avishkar 2")
    st.text(f"Battery = {st.session_state.battery2}%")
    t = random.randint(0, 6)
    if t == 0 or st.session_state.battery2==0:
        st.markdown("⚠️ **Warning:** This is an alert!")
        st.text("Maintenance should be done as soon as possible.")
    else:
        st.text(f"Maintenance should be done within the next {t} days")

    # Pod 3
    st.subheader("Pod - Avishkar 3")
    st.text(f"Battery = {st.session_state.battery3}%")
    t = random.randint(0, 6)
    if t == 0 or st.session_state.battery3==0:
        st.markdown("⚠️ **Warning:** This is an alert!")
        st.text("Maintenance should be done as soon as possible.")
    else:
        st.text(f"Maintenance should be done within the next {t} days")

import streamlit as st

st.set_page_config(page_title="Info", page_icon="📜")

st.title("📜 Info")

hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.markdown("## Navigation")
st.sidebar.page_link("main.py", label="🔥 Home")
st.sidebar.page_link("pages/map.py", label="🗺️ Map")
st.sidebar.page_link("pages/data.py", label="📊 Data")
st.sidebar.page_link("pages/info.py", label="📜 Info")
st.sidebar.page_link("pages/chatbot.py", label="💬 Chatbot")
st.sidebar.page_link("pages/about.py", label="🔍 About Us")

st.write("""Lately, wildfires have been prevalent throughout the world, the most recent incident being in Los Angeles, California. The L.A. wildfires began earlier this year on January 7th and nearly took firefighters the entire month of January to contain and stop the spread of the fire. Due to the wildfires, thousands of people lost their homes and at least 29 people died trying to protect their homes and loved ones. In addition to the thousands of people being displaced, L.A. experienced a tremendous economic loss, costing over $200 billion, and is considered one of the most costly fires in U.S. history. Wildfires are extremely difficult to control, giving residents and visitors little to no time to evacuate quickly; the short notice caused chaos and difficulty for residents to leave safely as well. Aside from tangible issues that wildfires cause, they can also lead to long-term problems. Wildfires can pose an extreme health threat, especially for individuals who already experience preexisting respiratory issues. Excessive smoke inhalation can be dangerous leading to lung irritation, asthma attacks, and in severe cases, chronic lung diseases.

Although completely preventing wildfires is close to impossible, we tackled the issue by creating a website that allows users to track wildfires and view up-to-date data on past and current wildfires. Through StreamLit, we designed a website that provides current statuses on wildfires and an AI chatbot that users can interact with for further assistance. Our mission is to help people to plan attentively and evacuate safely during wildfires.
""")
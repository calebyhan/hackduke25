import streamlit as st

st.set_page_config(page_title="About Us", page_icon="🔍", layout="wide")

st.title("About Us 🔍")

hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.markdown("## Navigation")
st.sidebar.page_link("main.py", label="Home 🔥")
st.sidebar.page_link("pages/map.py", label="Map 🗺")
st.sidebar.page_link("pages/data.py", label="Data 📊")
st.sidebar.page_link("pages/chatbot.py", label="Chatbot 💬")
st.sidebar.page_link("pages/about.py", label="About Us 🔍")

st.markdown("""<div style="font-size: 20px;">
    As inspiration, we wanted to create a project that raise awareness about the recent LA fires. The project is a Streamlit web application that provides information about wildfires, including a map of recent wildfires, data on wildfires, and a chatbot that answers questions about wildfire prevention.
    Although completely preventing wildfires is close to impossible, we tackled the issue by creating a website that allows users to track wildfires and view up-to-date data on past and current wildfires. Through Streamlit, we designed a website that provides current statuses on wildfires and an AI chatbot that users can interact with for further assistance.
    We integrated an API from <a href="https://firms.modaps.eosdis.nasa.gov/">NASA's Fire Information for Resource Management System (FIRMS)</a> to display real-time wildfire data on a map. The chatbot uses OpenAI's GPT-3 to generate responses to user queries.</div>""", unsafe_allow_html=True)
st.markdown("")
st.markdown("""<div style="font-size: 20px;">
This project was created for HackDuke 2025. The team members are:
<ul>
    <li> Caleb Han</li>
    <li> Mason Mines</li>
    <li>Yewon Song</li>
</ul>
""", unsafe_allow_html=True)
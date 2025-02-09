import streamlit as st

st.set_page_config(page_title="About Us", page_icon="🔍")

st.title("🔍 About Us")

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

st.markdown("""
    This project was created for HackDuke 2025. The team members are:
    * Caleb Han
    * Mason Mines
    * Yewon Song
    
    As inspiration, we wanted to create a project that raise awareness about the recent LA fires. The project is a Streamlit web application that provides information about wildfires, including a map of recent wildfires, data on wildfires, and a chatbot that answers questions about wildfire prevention.
    We integrated an API from [NASA's Fire Information for Resource Management System (FIRMS)](https://firms.modaps.eosdis.nasa.gov/) to display real-time wildfire data on a map. The chatbot uses OpenAI's GPT-3 to generate responses to user queries.
""")
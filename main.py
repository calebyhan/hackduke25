import streamlit as st

st.set_page_config(page_title="Wildfires", page_icon="🔥")

st.title("🔥 Wildfires 🔥")
st.write("Lately, wildfires have been prevalent globally, the most recent incident being the L.A. fires. "
         "Due to the wildfires, thousands of people lost their homes and became displaced. Wildfires also pose an extreme "
         "health threat, especially for individuals who already experience preexisting respiratory issues. "
         "The L.A. fire is considered one of the most costly fires in U.S. history, being over $200 billion in losses.")

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

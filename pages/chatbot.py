import streamlit as st
import numpy as np

st.set_page_config(page_title="Chatbot", page_icon="💬")

st.title("💬 Chatbox")
st.write("Report bugs and track issues.")

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

with st.chat_message("FireBot", avatar="💬"):
    st.write("I am a fire bot. heheh :D")
    st.line_chart(np.random.randn(30,3))

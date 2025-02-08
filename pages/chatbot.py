import streamlit as st
import numpy as np
import random
import time
from openai import OpenAI

st.set_page_config(page_title="Chatbot", page_icon="💬")

st.title("🐻🔥Smokey Bot")

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

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.08)

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Chat with Smokey the Flameproof Bear"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

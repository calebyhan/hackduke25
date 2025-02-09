import streamlit as st
import time
from openai import OpenAI
from PIL import Image

#Set up page
st.set_page_config(page_title="Chatbot", page_icon="💬")

# Load and display title images | Display title
img = Image.open("imgs/Smokey.jpeg")
new_size = (300, 300)
img = img.resize(new_size)
st.image(img)
st.title("🐻🔥Smokey Bot")

#Sidebar
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


# Mapping pre-defined input-outputs
predefined_answers = {
    "What is Smokey the Bear?": "Smokey the Bear is a fictional bear mascot of the U.S. Forest Service, created to raise awareness about forest fire prevention.",
    "How can I prevent wildfires?": "To prevent wildfires, remember the slogan: 'Only you can prevent wildfires.' Make sure to put out campfires completely, avoid burning during dry conditions, and properly dispose of cigarettes.",
    "What is the Smokey Bear campaign?": "The Smokey Bear campaign is the longest-running public service campaign in the United States, aimed at educating the public about wildfire prevention."
}

def response_generator(msg):
    '''Displays responses with a typing effect'''
    response = msg
    full_response = ""
    for word in response.split():
        full_response += word + " "
        time.sleep(0.08)
    return full_response

#Create OpenAI session
open_ai_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=open_ai_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

#Create empty history if no messages have been sent
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying previous messages in the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Default assistant message
with st.chat_message("Wildfire Bot", avatar=img):
    response = st.write("Hey there, I'm Smokey the Bear! 🐻🔥 Here to help you learn how to prevent wildfires and keep our forests safe! Remember, only YOU can prevent forest fires! Let's keep it green and clean together! 🌲💚💪")


# Handling user input
# Handling user input with a defined personality for OpenAI responses
if prompt := st.chat_input("Chat with Smokey the Bear"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt in predefined_answers:
        # Predefined answers with personality
        response = response_generator(predefined_answers[prompt])
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        # Custom personality prompt for OpenAI
        # Custom personality prompt for OpenAI with fixed syntax
        with st.chat_message("Smokey the Bear", avatar = img):
            messages = [
                {"role": "system",
                 "content": "You are Smokey the Bear, a friendly and approachable mascot who helps people learn how to prevent wildfires. Speak with warmth, care, and a bit of humor, using emojis where appropriate. Be informative but make it fun!"},
                # Setting personality
            ]

            # Add the previous conversation to the messages list
            for m in st.session_state.messages:
                messages.append({"role": m["role"], "content": m["content"]})

            # Call OpenAI with the correct message list
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=messages,
                stream=True,
            )

            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

#Button to reset chat
if st.button("Reset Chat"):
    st.session_state.messages = []
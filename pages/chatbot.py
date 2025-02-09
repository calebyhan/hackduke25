import streamlit as st
import time
from openai import OpenAI
from PIL import Image
import pydeck as pdk
import numpy as np
import altair as alt
from utils import get_firms_data, countries

# Set up page
st.set_page_config(page_title="Chatbot", page_icon="💬")

# Sidebar
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

img = Image.open("imgs/Smokey.jpeg").resize((300, 300))
# Load and display title images | Display title
img = Image.open("imgs/Smokey.jpeg").resize((300, 300))
st.image(img)
st.title("🔥🐻 Smokey Bot 🐻🔥")

with st.chat_message("assistant", avatar=img):
    st.write(
        "Hello! I'm Smokey the Bear Bot, here to answer your questions about wildfire prevention and the Smokey Bear campaign. Ask me anything!"
    )

# Predefined responses
predefined_answers = {
    "Generate Map": "Smokey the Bear is a fictional bear mascot of the U.S. Forest Service, created to raise awareness about forest fire prevention.",
    "Generate Data": "To prevent wildfires, remember the slogan: 'Only you can prevent wildfires.' Make sure to put out campfires completely, avoid burning during dry conditions, and properly dispose of cigarettes.",
    "What is the Smokey Bear campaign?": "The Smokey Bear campaign is the longest-running public service campaign in the United States, aimed at educating the public about wildfire prevention."
}

# First selectbox
option = st.selectbox(
    "What would you like to learn about?",
    ("", *predefined_answers.keys()),
    index=0,
    key="main_selectbox"
)

@st.cache_resource
def generate_map(df):
    @st.cache_data
    def get_color_from_brightness(brightness):
        normalized = min(max(brightness, 220), 400)
        scale = int(255 * (normalized - 220) / 110)
        return [255, 255 - scale, 0]

    if "bright_ti5" in df.columns:
        df["color"] = df["bright_ti5"].apply(get_color_from_brightness)

    return pdk.Deck(
        map_style=None,
        initial_view_state={"latitude": 0, "longitude": 0, "zoom": 1, "pitch": 30},
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_radius=10000,
                get_color="color",
                opacity=0.8,
            )
        ],
    )

@st.cache_data
def generate_plot(df, option):
    if option == "Fire Trends Over Time":
        fires_per_day = df.groupby("acq_date").size().reset_index(name="count")
        return fires_per_day.set_index("acq_date")

    elif option == "Fire Frequency vs. Intensity":
        return df

    elif option == "Fire Intensity Histogram":
        hist_data = df["bright_ti5"].value_counts().reset_index()
        hist_data.columns = ["Intensity", "Count"]
        return hist_data

    elif option == "Fire Activity by Day":
        fires_per_day = df.groupby("acq_date").size().reset_index(name="count")
        return fires_per_day.set_index("acq_date")

# Generate response function
def response_generator(msg):
    '''Displays responses with a typing effect.'''
    full_response = ""
    for word in msg.split():
        full_response += word + " "
        time.sleep(0.08)
    return full_response

# OpenAI setup

open_ai_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=open_ai_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=img if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Handle predefined selection
if option in predefined_answers and option not in ["Generate Map", "Generate Data"]:
    prompt = option
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = response_generator(predefined_answers[prompt])
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar=img):
        st.markdown(response)
elif option == "Generate Map":
    country = st.text_input("Enter Country Name")
    if country:
        df = get_firms_data(country, 10)
        with st.chat_message("assistant", avatar=img):
            st.write(
                f"Let's take a look at the fires in {country} over the last 10 days."
            )
        st.pydeck_chart(generate_map(df))

elif option == "Generate Data":
    country = st.text_input("Enter Country Name")
    vis = st.sidebar.radio("Choose a Chart", [
        "Fire Trends Over Time",
        "Fire Frequency vs. Intensity",
        "Fire Intensity Histogram",
        "Fire Activity by Day",
    ])
    if country:
        df = get_firms_data(country, 10)
        plot_data = generate_plot(df, vis)
        with st.chat_message("assistant", avatar=img):
            st.write(
                f"Let's learn about the fires in {country} over the last 10 days."
            )
        st.write(plot_data)
        if option == "Fire Trends Over Time":
            st.subheader("Fire Detections Over Time")
            st.line_chart(plot_data)

        elif option == "Fire Frequency vs. Intensity":
            st.subheader("Fire Frequency vs. Intensity")
            st.scatter_chart(plot_data, x="frp", y="bright_ti4", size="frp", color="bright_ti4")
        #fire
        elif option == "Fire Intensity Histogram":
            chart = alt.Chart(plot_data).mark_bar().encode(
                x="Intensity:Q",
                y="Count:Q"
            ).properties(
                height=300
            )
            st.altair_chart(chart, use_container_width=True)

        elif option == "Fire Activity by Day":
            st.subheader("Fire Activity by Day")
            st.bar_chart(plot_data)

        st.markdown(
            """
            **Note:** FIRMS data is provided by [NASA's Fire Information for Resource Management System (FIRMS)](https://firms.modaps.eosdis.nasa.gov/).
            """
        )

# Chat input
prompt = st.chat_input("Chat with Smokey the Bear")

if prompt:
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and st.session_state.messages[-1]["content"] == prompt:
        st.warning("You already asked this question!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if prompt in predefined_answers:
            response = response_generator(predefined_answers[prompt])
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant", avatar=img):
                st.markdown(response)
        else:
            with st.chat_message("assistant", avatar=img):
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

# Reset chat button
if st.button("Reset Chat"):
    st.session_state.messages = []

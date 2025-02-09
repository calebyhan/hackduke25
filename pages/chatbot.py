import streamlit as st
import time
from openai import OpenAI
from PIL import Image
import pydeck as pdk
import numpy as np
import altair as alt
from utils import get_firms_data, countries

# Set up page
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

# Sidebar
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

img = Image.open("imgs/Smokey.jpeg").resize((300, 300))
st.title("Smokey Bot 🐻🔥")

with st.chat_message("assistant", avatar=img):
    st.markdown(
        '<div style="font-size: 20px;">Hello! I\'m Smokey the Bear Bot 🐻‍🔥, here to teach you about wildfires and how they impact our environment 🌍. I can help you understand wildfire prevention, the effects of wildfires on ecosystems, and even generate maps and visualizations to show fire risk areas 📊. Ask me anything, and let\'s keep our forests safe together! 🔥🌲</div>'
    , unsafe_allow_html=True)

# Predefined responses
predefined_answers = {
    "Generate Wildfire Map": "Hey there! Smokey here. I can help you generate a map of recent wildfire activity 🌍. Just let me know which country you'd like to focus on, and I'll get the details to you faster than a bear can run from a campfire 🔥🐻.",
    "Generate Wildfire Data": "Time to dive into some fire-related data! 🔥 What do you want to explore today? We can look at trends, fire risk areas, and other important info to keep our forests safe 🌲.",
    "Tell me about the recent LA wildfires": "The recent wildfires in Los Angeles were some of the most devastating in recent memory 🔥. In early January 2025, the Palisades and Eaton Fires burned thousands of acres, destroying over 10,000 homes 🏠 and tragically taking at least 29 lives 😞. Strong winds and dry conditions made the fires spread quickly. It's a tough reminder of how important it is to be prepared and prevent wildfires before they start. Let's all do our part to keep our communities safe! 🐻🔥",
    "What caused the recent LA wildfires?": "The cause of the recent LA wildfires is still being investigated 🔎. Experts are looking into possible ignition sources, including human activity and environmental conditions. Dry vegetation and strong winds made it easier for the fires to spread rapidly 🌬️🔥. The goal is to learn from these events and take steps to reduce future risks. Stay aware and stay safe! 🐻🌲",
    "How have the LA wildfires affected the community?": "The LA wildfires have had a major impact on the community 😔. Thousands of homes were destroyed 🏚️, and many families lost their possessions. The fires also impacted cultural landmarks, including vintage cars 🚗🔥. It’s a heartbreaking reminder of how wildfires can change lives in an instant. But through it all, the community has shown incredible strength and resilience 💪. Let’s keep supporting each other and work toward a safer future! 🐻🌳",
    "What is being done to prevent future wildfires in LA?": "In response to the LA wildfires, authorities are stepping up efforts to prevent future disasters 🌲🔥. This includes clearing dry vegetation, improving firebreaks, and using technology like drones and satellites for early detection 🚁🌍. Wildfire safety education is also a top priority—remember, ‘Only you can prevent wildfires!’ 🐻💡 Let’s all do our part to keep the forests safe and reduce the risk of future fires.",
    "What is the environmental impact of wildfires?": "Wildfires can really take a toll on the environment. They destroy habitats 🦉, harm wildlife 🦅, and release carbon dioxide 🏭 into the air, adding to climate change. That's why Smokey says: ‘Only you can prevent wildfires!’ 🐻🔥",
    "What are firebreaks?": "Firebreaks are cleared areas where vegetation is removed to stop wildfires from spreading 🌿➡️❌🔥. They act like a firewall, just without the computer screen! It’s a smart way to protect the forest from a big blaze.",
    "What is a controlled burn?": "A controlled burn is like a well-planned campfire 🔥—done safely, it helps clear away extra vegetation and reduce the risk of larger, uncontrolled wildfires. It's kind of like cleaning up your campsite so it’s safer for everyone! 🏕️",
    "How do wildfires affect air quality?": "Wildfires can really mess with the air quality 🌫️. The smoke contains harmful particles that can cause breathing problems 😷, especially for kids 👶, the elderly 👵, and folks with asthma 💨. So, when Smokey says, ‘Stay safe,’ he means it! 🐻",
    "What laws govern wildfire prevention?": "There are several important laws designed to prevent wildfires ⚖️. These include clearing dry vegetation, regulating open burning during fire season, and encouraging fire safety. Remember: ‘Preventing fires is everyone’s job!’ 🐻🔥",
    "What is the role of satellite data in wildfire management?": "Satellite data is like having a bird’s-eye view of wildfires 🌍. It helps track fire spread, assess damage, and guide firefighting strategies. With satellites, we can stay ahead of the flames! 🚀🔥",
    "How does wildfire smoke impact health?": "That smoky haze? Not just bad for your eyes 👀—it can harm your lungs too 💨. Wildfire smoke can make it tough to breathe, so it’s best to stay indoors or wear a mask when it’s smoky outside 😷. Stay safe, and keep that air clean! 🐻🌬️",
    "What is the role of technology in wildfire detection?": "Technology is a big part of wildfire detection 📡. Drones, sensors, and satellites help us spot fires early, so we can respond quickly and prevent them from spreading. It’s a high-tech way to keep our forests safe 🌲🔥.",
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

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=img if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Handle predefined selection
if option in predefined_answers and option not in ["Generate Wildfire Map", "Generate Wildfire Data"]:
    prompt = option
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = response_generator(predefined_answers[prompt])
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar=img):
        st.markdown(response)

# Map Functionality
elif option == "Generate Wildfire Map":
    country = st.selectbox("Select a country", list(countries.values()))
    if country:
        df = get_firms_data(country, 10)
        with st.chat_message("assistant", avatar=img):
            st.write(f"Let's take a look at the fires in {country} over the last 10 days.")
        st.pydeck_chart(generate_map(df))

# Data Functionality
elif option == "Generate Wildfire Data":
    country = st.selectbox("Select a country", list(countries.values()))
    vis = st.selectbox(
        "What would you like to learn about?",
        ("",
        "Fire Trends Over Time",
        "Fire Frequency vs. Intensity",
        "Fire Intensity Histogram",
        "Fire Activity by Day",),
        index=0,
        key="vis-selectbox"
    )
    with st.chat_message("assistant", avatar=img):
        st.write(
            response_generator(f"Let's learn about the fires in {country} over the last 10 days.")
        )
    if country:
        df = get_firms_data(country, 10)
        plot_data = generate_plot(df, vis)

        if vis == "Fire Trends Over Time":
            st.subheader("Fire Detections Over Time")
            st.line_chart(plot_data)

        elif vis == "Fire Frequency vs. Intensity":
            st.subheader("Fire Frequency vs. Intensity")
            st.scatter_chart(plot_data, x="frp", y="bright_ti4", size="frp", color="bright_ti4")

        elif vis == "Fire Intensity Histogram":
            chart = alt.Chart(plot_data).mark_bar().encode(
                x="Intensity:Q",
                y="Count:Q"
            ).properties(
                height=300
            )
            st.altair_chart(chart, use_container_width=True)

        elif vis == "Fire Activity by Day":
            st.subheader("Fire Activity by Day")
            st.bar_chart(plot_data)

        on = st.toggle("Display DataFrame")

        if on:
            st.dataframe(df)

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

        # OpenAI setup with Smokey's personality instructions and emojis
        if prompt and prompt not in predefined_answers:

            # Adjust OpenAI request to reflect Smokey's style with emojis
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system",
                     "content": "You are Smokey the Bear. Speak in a friendly, educational, and slightly casual manner, always promoting wildfire safety with a lot of fun emojis. Use phrases like 'Only you can prevent wildfires' and provide helpful, positive guidance. 🐻🔥🌲"},
                    {"role": "user", "content": prompt},
                    *[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                ],
                stream=True,
            )

            # Generate and display the response with emojis
            with st.chat_message("assistant", avatar=img):
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})


# Reset chat button
if st.button("Reset Chat"):
    # Clear the session state for messages
    st.session_state.messages = []


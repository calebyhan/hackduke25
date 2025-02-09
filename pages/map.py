import streamlit as st
import pydeck as pdk
import numpy as np
import pandas as pd
from PIL import Image

from utils import get_firms_data, countries

st.set_page_config(page_title="Map", page_icon="️🗺")

st.title("🗺 Map")

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

country = st.selectbox("Select a country", list(countries.values()))

if st.checkbox("Select whole world"):
    country = "the world"

day_range = st.slider("Select a day range", 1, 10, 1)

df = get_firms_data(country, day_range)
latitude = 35.9132
longitude = -79.0558

if df.empty:
    st.warning("No data available for the selected country and day range.")
else:
    if day_range == 1:
        st.subheader(f"FIRMS data for {country}, for the last day.")
    else:
        st.subheader(f"FIRMS data for {country}, for the last {str(day_range)} days.")

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
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=pd.DataFrame({"latitude": [latitude], "longitude": [longitude]}),
                    get_position=["longitude", "latitude"],
                    get_radius=20000,  # Larger radius for visibility
                    get_color=[0, 0, 255],  # Blue color
                    opacity=1.0,
                ),
            ],
        )

    st.pydeck_chart(generate_map(df))

    def generate_gradient():
        width, height = 256, 10
        gradient = np.zeros((height, width, 3), dtype=np.uint8)

        for i in range(width):
            r = 255
            g = int(255 - (i * 255 / (width - 1)))  # Decreasing green from 255 to 0
            b = 0
            gradient[:, i] = [r, g, b]  # Assign color

        return Image.fromarray(gradient)

    st.write("Brightness Temperature (TI5) Scale")
    gradient_img = generate_gradient()
    st.image(gradient_img, caption="Low (290K) → High (400K)", use_container_width=True)

    on = st.toggle("Display DataFrame")

    if on:
        st.dataframe(df)

    st.markdown(
        """
        Each colored dot indicates an active fire. The color of the dot represents the brightness temperature (TI5) of the fire.

        **Note:** FIRMS data is provided by [NASA's Fire Information for Resource Management System (FIRMS)](https://firms.modaps.eosdis.nasa.gov/).
        """
    )

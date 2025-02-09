import streamlit as st
import requests
import io
import pandas as pd
import pydeck as pdk
import geocoder
from utils import FIRMS_KEY, url

st.set_page_config(page_title="Wildfires", page_icon="🔥")

st.title("🔥 Wildfires 🔥")

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

location = geocoder.ip('me').latlng
print(location)
latitude = location[0]
longitude = location[1]

@st.cache_data
def get_location_data():
    response = requests.get(f"{url}/area/csv/{FIRMS_KEY}/VIIRS_SNPP_NRT/world/1")

    if response.status_code == 200:
        csv_data = response.text
        print(csv_data)
        df = pd.read_csv(io.StringIO(csv_data))
        return df
    else:
        st.error("Failed to fetch data. Check API key or try again later.")
        return pd.DataFrame()

df = get_location_data()

# filter data
df = df[(df["latitude"] >= latitude - 5) & (df["latitude"] <= latitude + 5)]
df = df[(df["longitude"] >= longitude - 5) & (df["longitude"] <= longitude + 5)]

if df.empty:
    st.warning("No data available for the selected country and day range.")
else:
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
            initial_view_state={"latitude": latitude, "longitude": longitude, "zoom": 5, "pitch": 30},
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

    st.pydeck_chart(generate_map(df))
import streamlit as st
import requests
import io
import pandas as pd
import pydeck as pdk
import geocoder
from PIL import Image
from utils import FIRMS_KEY, url

st.set_page_config(page_title="Wildfires", page_icon="🔥", layout="wide")

st.title("Wildfires 🔥")

st.markdown("""
<style>
.twenty {
    font-size:20px !important;
}
.twentyfive {
    font-size:25px !important;
}

</style>
""", unsafe_allow_html=True)

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

st.markdown('<div class="twenty" style="margin-bottom: 20px;">Wildfires have been prevalent throughout the world, the most recent incident being in Los Angeles, California. The L.A. wildfires began earlier this year on January 7th and nearly took firefighters the entire month of January to contain and stop the spread of the fire. Due to the wildfires, thousands of people lost their homes and <b>at least 29 people died</b> trying to protect their homes and loved ones. In addition to the thousands of people being displaced, L.A. experienced a tremendous economic loss, costing over <b>$200 billion</b>, and is considered one of the most costly fires in U.S. history.</div>', unsafe_allow_html=True)

location = geocoder.ip('me').latlng
latitude = 34.0549
longitude = -118.2426

@st.cache_data
def get_location_data():
    response = requests.get(f"{url}/area/csv/{FIRMS_KEY}/VIIRS_SNPP_NRT/world/1")

    if response.status_code == 200:
        csv_data = response.text
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
            initial_view_state={"latitude": latitude, "longitude": longitude, "zoom": 7.5, "pitch": 30},
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=["longitude", "latitude"],
                    get_radius=5000,
                    get_color="color",
                    opacity=0.8,
                )
            ],
        )

    st.pydeck_chart(generate_map(df))

    st.divider()

    col1, col2 = st.columns([0.4, 0.6], vertical_alignment="center")

    with col1:
        st.markdown('<div class="twenty" style="text-align: center; margin-bottom: 40px;">Wildfires are extremely difficult to control, giving residents and visitors little to no time to evacuate quickly; the short notice caused chaos and difficulty for residents to leave safely as well.</div>', unsafe_allow_html=True)

    with col2:
        img = Image.open("imgs/structures.png").resize((787, 287))
        st.image(img)

    st.divider()

    with col2:
        st.markdown('<div class="twenty">Aside from tangible issues that wildfires cause, they can also lead to long-term problems. Wildfires can pose an extreme health threat, especially for individuals who already experience preexisting respiratory issues. Excessive smoke inhalation can be dangerous leading to lung irritation, asthma attacks, and in severe cases, chronic lung diseases.</div>', unsafe_allow_html=True)

    with col1:
        img = Image.open("imgs/health_dangers.jpg").resize((1200, 630))
        st.image(img)

    st.markdown('<div style="text-align: center; font-size: 35px;"><b>Our mission is to help people to plan attentively and evacuate safely during wildfires.</b></div>', unsafe_allow_html=True)

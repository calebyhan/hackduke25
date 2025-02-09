import streamlit as st
import altair as alt

from utils import get_firms_data, countries

st.set_page_config(page_title="Data", page_icon="📊")

st.title("📊 Data")

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

if df.empty:
    st.warning("No data available for the selected country and day range.")
else:
    st.sidebar.title("Select Visualization")
    option = st.sidebar.radio("Choose a Chart", [
        "Fire Trends Over Time",
        "Fire Frequency vs. Intensity",
        "Fire Intensity Histogram",
        "Fire Activity by Day",
    ])

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

    plot_data = generate_plot(df, option)

    if option == "Fire Trends Over Time":
        st.subheader("Fire Detections Over Time")
        st.line_chart(plot_data)

    elif option == "Fire Frequency vs. Intensity":
        st.subheader("Fire Frequency vs. Intensity")
        st.scatter_chart(plot_data, x="frp", y="bright_ti4", size="frp", color="bright_ti4")

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

    on = st.toggle("Display DataFrame")

    if on:
        st.dataframe(df)

    st.markdown(
        """
        **Note:** FIRMS data is provided by [NASA's Fire Information for Resource Management System (FIRMS)](https://firms.modaps.eosdis.nasa.gov/).
        """
    )
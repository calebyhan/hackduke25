import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("🏠 Home Page")
st.write("Welcome to the Streamlit App! Use the sidebar to navigate.")

hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.markdown("## Navigation")
st.sidebar.page_link("main.py", label="🏠 Home")
st.sidebar.page_link("pages/page2.py", label="📊 Dashboard")
st.sidebar.page_link("pages/page3.py", label="🐛 Bug Reports")
st.sidebar.page_link("pages/page4.py", label="🔍 Search")
st.sidebar.page_link("pages/test.py", label="📜 History")
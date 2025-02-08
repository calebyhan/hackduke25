import streamlit as st

st.set_page_config(page_title="Bug Reports", page_icon="🐛")

st.title("🐛 Bug Reports")
st.write("Report bugs and track issues.")

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
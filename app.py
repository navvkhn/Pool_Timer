import streamlit as st

st.set_page_config(
    page_title="Pool Timer",
    page_icon="🎱",
    layout="centered"
)

# ✅ Correct Streamlit page redirect
st.switch_page("pages/1_Admin.py")

import streamlit as st

st.set_page_config(
    page_title="Pool Timer",
    page_icon="🎱",
    layout="centered"
)

# ✅ Streamlit-native redirect
st.switch_page("pages/admin.py")

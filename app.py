import streamlit as st

st.set_page_config(
    page_title="Pool Timer",
    page_icon="🎱",
    layout="centered"
)

# 🚀 Auto redirect to Admin page
st.markdown(
    """
    <meta http-equiv="refresh" content="0; url=/admin">
    """,
    unsafe_allow_html=True
)

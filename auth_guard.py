import streamlit as st

def require_auth():
    if "user" not in st.session_state or not st.session_state.user:
        st.switch_page("pages/login.py")

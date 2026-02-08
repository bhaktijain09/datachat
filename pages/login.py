import streamlit as st
import ui
from auth import authenticate_user
from db import init_db

st.set_page_config(page_title="Login", layout="centered")
ui.inject_css(hide_sidebar=True)
init_db()

st.markdown('<div class="auth-wrapper"><div class="auth-card">', unsafe_allow_html=True)

st.markdown("""
<div class="auth-title">Welcome back</div>
<div class="auth-subtitle">Sign in to continue</div>
""", unsafe_allow_html=True)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):
    if authenticate_user(username, password):
        st.session_state.user = username
        st.switch_page("app.py")
    else:
        st.error("Invalid username or password")

if st.button("Create account", use_container_width=True):
    st.switch_page("pages/signup.py")

st.markdown("</div></div>", unsafe_allow_html=True)

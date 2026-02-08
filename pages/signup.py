import streamlit as st
import ui
from auth import create_user
from db import init_db

st.set_page_config(page_title="Signup", layout="centered")
ui.inject_css(hide_sidebar=True)
init_db()

st.markdown('<div class="auth-wrapper"><div class="auth-card">', unsafe_allow_html=True)

st.markdown("""
<div class="auth-title">Create account</div>
<div class="auth-subtitle">Start querying your data</div>
""", unsafe_allow_html=True)

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign up", use_container_width=True):
    if create_user(username, email, password):
        st.session_state.user = username
        st.switch_page("app.py")
    else:
        st.error("Username or email already exists")

if st.button("Back to login", use_container_width=True):
    st.switch_page("pages/login.py")

st.markdown("</div></div>", unsafe_allow_html=True)

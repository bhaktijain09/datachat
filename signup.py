import streamlit as st
import ui

ui.inject_css()

if "users" not in st.session_state:
    st.session_state.users = {}

def signup(username, password, email):
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = {
        "password": password,
        "email": email
    }
    return True

st.markdown('<div class="auth-wrapper"><div class="auth-card">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="auth-title">Create account</div>
    <div class="auth-subtitle">Start querying your data</div>
    """,
    unsafe_allow_html=True
)

u = st.text_input("Username")
e = st.text_input("Email")
p = st.text_input("Password", type="password")

if st.button("Sign up", use_container_width=True):
    if signup(u, p, e):
        st.session_state.user = u
        st.switch_page("app.py")
    else:
        st.error("Username already exists")

if st.button("Back to login", use_container_width=True):
    st.switch_page("login.py")

st.markdown('</div></div>', unsafe_allow_html=True)

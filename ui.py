import streamlit as st

def inject_css(hide_sidebar=False):
    sidebar_css = ""
    if hide_sidebar:
        sidebar_css = """
        section[data-testid="stSidebar"] {
            display: none;
        }
        """

    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: #ffffff;
            color: #1f2937;
        }}

        h1, h2, h3, p, label {{
            color: #1f2937;
        }}

        input {{
            background-color: #f9fafb;
            color: #111827;
            border-radius: 6px;
            border: 1px solid #d1d5db;
        }}


        .auth-title {{
            font-size: 1.8rem;
            font-weight: 700;
        }}

        .auth-subtitle {{
            color: #6b7280;
            margin-bottom: 1.5rem;
        }}

        .auth-card button {{
            background: #111827 !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }}

        {sidebar_css}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str):
    st.markdown(
        f"""
        <div style="margin-bottom: 1.5rem;">
            <h1 style="font-weight: 800;">{title}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

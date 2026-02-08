
import streamlit as st
import ui
from auth_guard import require_auth
from pdf_store import ingest_pdf

st.set_page_config(page_title="PDF Upload", layout="centered")
ui.inject_css()
require_auth()

ui.page_header("Upload PDF for Querying")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    file_path = f"uploaded_pdfs/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    ingest_pdf(file_path)
    st.success("✅ PDF ingested successfully and ready for querying")

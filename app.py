
#  ENV + IMPORTS

from dotenv import load_dotenv
load_dotenv()

import os
import re
import streamlit as st
import pandas as pd
import mysql.connector
import google.generativeai as genai

import ui
from auth_guard import require_auth
from pdf_query import query_pdf   # PDF QUERY PIPELINE


# PAGE CONFIG

st.set_page_config(
    page_title="Query Retrieval System",
    page_icon="uploaded_icons/db_icon.png",
    layout="wide",
)


# GLOBAL UI

ui.inject_css()
require_auth()
ui.page_header("Query Retrieval System")


# GEMINI CONFIG

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# SESSION INIT

if "sql_cache" not in st.session_state:
    st.session_state.sql_cache = {}
if "query_mode" not in st.session_state:
    st.session_state.query_mode = None


# DATABASE HELPERS

def run_query(query: str):
    try:
        conn = mysql.connector.connect(
            user=st.session_state.DB_USER,
            password=st.session_state.DB_PASS,
            host=st.session_state.DB_HOST,
            port=st.session_state.DB_PORT,
            database=st.session_state.DB_NAME,
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None


def generate_schema():
    try:
        conn = mysql.connector.connect(
            user=st.session_state.DB_USER,
            password=st.session_state.DB_PASS,
            host=st.session_state.DB_HOST,
            port=st.session_state.DB_PORT,
            database=st.session_state.DB_NAME,
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        schema = []
        for (table,) in tables:
            cursor.execute(f"DESCRIBE `{table}`;")
            cols = cursor.fetchall()
            schema.append(f"{table}({', '.join(c[0] for c in cols)})")

        cursor.close()
        conn.close()
        return "\n".join(schema)
    except Exception:
        return ""


# SQL SAFETY

FORBIDDEN_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|create|replace|grant|revoke|"
    r"commit|rollback|call|exec|execute|prepare|deallocate|merge|upsert|"
    r"load|outfile|dumpfile|set|use)\b",
    re.IGNORECASE,
)

def is_safe_select_sql(sql: str) -> bool:
    sql = sql.strip().replace("\n", " ")
    return (
        sql.lower().startswith("select")
        and ";" not in sql[:-1]
        and not FORBIDDEN_SQL.search(sql)
    )


# GEMINI SQL GENERATION

BASE_PROMPT = """
You are a senior MySQL database expert.

Rules:
- Use ONLY table and column names from the schema
- Do NOT invent names
- Return ONE valid SELECT query only
- No explanations
"""

def get_gemini_response(question: str):
    if question in st.session_state.sql_cache:
        return st.session_state.sql_cache[question]

    schema = generate_schema()
    if not schema:
        return "ERROR: Schema not available"

    model = genai.GenerativeModel("models/gemini-flash-latest")
    response = model.generate_content(
        f"{BASE_PROMPT}\nSCHEMA:\n{schema}\nQUESTION:\n{question}"
    )

    sql = response.text.strip()
    st.session_state.sql_cache[question] = sql
    return sql



# SIDEBAR


st.sidebar.success(f"Welcome {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("pages/login.py")



# DATABASE CONNECTION (SQL ONLY)

if "DB_USER" not in st.session_state:
    st.sidebar.subheader(" Database Connection")

    with st.sidebar.form("db_form"):
        db_user = st.text_input("DB User", "root")
        db_pass = st.text_input("DB Password", type="password")
        db_host = st.text_input("DB Host", "localhost")
        db_port = st.text_input("DB Port", "3306")
        db_name = st.text_input("DB Name")

        if st.form_submit_button("Connect"):
            try:
                mysql.connector.connect(
                    user=db_user,
                    password=db_pass,
                    host=db_host,
                    port=db_port,
                    database=db_name,
                ).close()

                st.session_state.DB_USER = db_user
                st.session_state.DB_PASS = db_pass
                st.session_state.DB_HOST = db_host
                st.session_state.DB_PORT = db_port
                st.session_state.DB_NAME = db_name
                st.rerun()
            except Exception:
                st.sidebar.error(" Connection failed")



# MAIN APPLICATION


col1, col2 = st.columns(2)



# Radio button for query mode selection
query_mode = st.radio(
    "Select Query Mode:",
    options=["Database (SQL)", "Documents (PDF)"],
    index=0 if st.session_state.get("query_mode") is None else (
        0 if st.session_state.get("query_mode") == "sql" else 1
    ),
    horizontal=True
)

# Update session state based on selection
if query_mode == "Database (SQL)":
    st.session_state.query_mode = "sql"
else:
    st.session_state.query_mode = "pdf"

# Show caption based on mode
if st.session_state.query_mode == "pdf":
    st.caption("Answers are generated strictly from ingested PDFs.")
elif st.session_state.query_mode == "sql":
    st.caption("Answers are generated using your database schema.")



st.subheader(" Ask a Question in English")
question = st.text_input("Enter your question")

# Run query button
if st.button("Run Query"):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    mode = st.session_state.get("query_mode")
    if mode == "sql":
        if "DB_USER" not in st.session_state:
            st.error("Please connect to a database first.")
            st.stop()

        sql = get_gemini_response(question)
        if sql.startswith("ERROR"):
            st.error(sql)
            st.stop()

        if not is_safe_select_sql(sql):
            st.error(" Unsafe SQL detected")
            st.code(sql, language="sql")
            st.stop()

        st.code(sql, language="sql")
        rows = run_query(sql)
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.info("No results found")

    elif mode == "pdf":
        answer = query_pdf(question)
        st.subheader(" Answer from documents")
        st.write(answer)

    else:
        st.warning("Please select a mode: Database (SQL) or Documents (PDF)")

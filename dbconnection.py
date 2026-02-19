import os
import pymysql
from dotenv import load_dotenv

load_dotenv()  # Load .env

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Fail early if any required env variable is missing
if not all([DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Database environment variables are missing!")

DB_PORT = int(DB_PORT)  # MySQL expects integer

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def run_query(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
    finally:
        conn.close()

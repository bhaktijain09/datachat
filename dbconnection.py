
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# 🔑 MySQL connection details from .env
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = int(os.getenv("DB_PORT", ""))
DB_NAME = os.getenv("DB_NAME", "")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def run_query(query):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        conn.commit()
        return result
    finally:
        conn.close()

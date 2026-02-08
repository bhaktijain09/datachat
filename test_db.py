from dbconnection import run_query

try:
    result = run_query("SHOW TABLES;")
    print("Connection successful!")
    print(result)
except Exception as e:
    print("Connection failed:", e)

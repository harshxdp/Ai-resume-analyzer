# --- database.py ---
import sqlite3

# 1. Connect to the database
conn = sqlite3.connect('cv_data.db', check_same_thread=False)
cur = conn.cursor()

# 2. Function to create tables (Run this when the app starts)
def create_tables():
    cur.execute("""CREATE TABLE IF NOT EXISTS user_data(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        sec_token varchar(20), 
        Name varchar(500), Email_ID varchar(500), Phone varchar(20),
        Actual_name varchar(500), Actual_email varchar(500),
        resume_score varchar(8), Timestamp varchar(50), Page_no varchar(5),
        Predicted_Field text, User_level text, Actual_skills text, 
        Recommended_skills text, Recommended_courses text, pdf_name varchar(50)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS user_feedback(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        feed_name varchar(50), feed_email varchar(50),
        feed_score varchar(5), comments varchar(100), Timestamp varchar(50)
    )""")
    conn.commit()

# 3. Function to insert resume data
def insert_data(values):
    cur.execute("""INSERT INTO user_data VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", values)
    conn.commit()

# 4. Function to insert feedback
def insert_feedback(values):
    cur.execute("""INSERT INTO user_feedback VALUES (NULL,?,?,?,?,?)""", values)
    conn.commit()

# 5. Function to fetch data for the Admin panel
def fetch_all_data():
    import pandas as pd
    df = pd.read_sql("SELECT * FROM user_data", conn)
    return df
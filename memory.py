import sqlite3
from datetime import datetime

DB_NAME = "fitness_tracker.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # 1. Added the 5 new medical columns to the table creation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, age INTEGER, sex TEXT,
                weight REAL, height REAL, purpose TEXT, 
                bloodPressure TEXT, pulse INTEGER,
                hasDiabetes BOOLEAN, hasThyroid BOOLEAN,
                otherConditions TEXT, created_at TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, generated_plan TEXT, created_at TEXT,
                FOREIGN KEY(user_id) REFERENCES user_profiles(id)
            )
        """)
        conn.commit()

# 2. Updated the function signature to catch all the new medical data
def store_user_and_plan(name, age, sex, weight, height, purpose, bloodPressure, pulse, hasDiabetes, hasThyroid, otherConditions, plan):
    with get_connection() as conn:
        cursor = conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        
        # 3. Updated the INSERT command to save all 11 fields to the database
        cursor.execute("""
            INSERT INTO user_profiles (
                name, age, sex, weight, height, purpose, 
                bloodPressure, pulse, hasDiabetes, hasThyroid, otherConditions, 
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, sex, weight, height, purpose, bloodPressure, pulse, hasDiabetes, hasThyroid, otherConditions, timestamp))
        
        user_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO health_plans (user_id, generated_plan, created_at)
            VALUES (?, ?, ?)
        """, (user_id, plan, timestamp))
        conn.commit()
import sqlite3
from datetime import datetime

DB_NAME = "fitness_tracker.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
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

def store_user_and_plan(name, age, sex, weight, height, purpose, bloodPressure, pulse, hasDiabetes, hasThyroid, otherConditions, plan):
    with get_connection() as conn:
        cursor = conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        
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

# --- NEW: Check if a plan was already made today ---
def get_todays_plan(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        today_str = datetime.utcnow().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT h.generated_plan 
            FROM health_plans h
            JOIN user_profiles u ON h.user_id = u.id
            WHERE u.name = ? AND h.created_at LIKE ?
            ORDER BY h.created_at DESC LIMIT 1
        """, (name, f"{today_str}%"))
        result = cursor.fetchone()
        return result[0] if result else None

# --- NEW: Get the last 7 days to feed to the AI ---
def get_weekly_history(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.created_at, h.generated_plan 
            FROM health_plans h
            JOIN user_profiles u ON h.user_id = u.id
            WHERE u.name = ?
            ORDER BY h.created_at DESC LIMIT 7
        """, (name,))
        rows = cursor.fetchall()
        
        history = ""
        for row in rows:
            # We just send a summary of the past plans so we don't overwhelm the AI
            history += f"Date: {row[0][:10]} | Past Plan Details: {row[1][:300]}...\n"
        return history
import sqlite3
from datetime import datetime

DB_NAME = "forecasts.db"

def setup_database():
    """Architectural Foundation: Creates the database and table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # We define a strict SQL schema that matches our Pydantic AI output
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,
            confidence_score INTEGER,
            reasoning TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🗄️ Database checked/initialized.")

def save_forecast(category, score, reasoning):
    """The Load Phase: Inserts a new AI forecast into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get the exact time the forecast was made
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Using parameterized queries (?) to prevent SQL Injection attacks
    cursor.execute('''
        INSERT INTO ai_forecasts (timestamp, category, confidence_score, reasoning)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, category, score, reasoning))
    
    conn.commit()
    conn.close()
    print(f"💾 Forecast permanently saved to {DB_NAME} at {timestamp}")
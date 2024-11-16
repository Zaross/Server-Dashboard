import os
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

database_path = "./databases/dashboard.db"

def init_db():
    db_exists = os.path.exists(database_path)
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    if not db_exists:
        c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        username = "admin@admin.com"
        password = pwd_context.hash("admin")
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       (username, password, "admin"))
    else:
        print("Database is existing.")

    conn.commit()
    conn.close()

init_db()

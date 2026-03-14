import sqlite3
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DB_PATH = "admin_logs.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technical_debt (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                issues_identified TEXT,
                migration_plan TEXT,
                raw_response TEXT
            )
        ''')
        conn.commit()
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def log_technical_debt(ai_response):
    try:
        issues_match = re.search(r'\*\*Critical Issues:\*\*\s*(.*?)(?=\n\*\*|$)', ai_response, re.DOTALL)
        migration_match = re.search(r'\*\*(?:Migration Action|Step-by-Step Migration) Plan:\*\*\s*(.*?)(?=\n\*\*|$)', ai_response, re.DOTALL)

        issues = issues_match.group(1).strip() if issues_match else ""
        migration = migration_match.group(1).strip() if migration_match else ""

        if issues or migration:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO technical_debt (timestamp, issues_identified, migration_plan, raw_response)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), issues, migration, ai_response))
            conn.commit()
            conn.close()
    except Exception as e:
        logger.error(f"Error logging technical debt: {e}")

def clear_technical_debt():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM technical_debt')
        conn.commit()
    except Exception as e:
        logger.error(f"Error clearing technical debt: {e}")
    finally:
        if conn:
            conn.close()

init_db()

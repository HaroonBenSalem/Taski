import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

def get_connection():
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        # Production (Render) — use the full connection string
        return psycopg2.connect(database_url)
    else:
        # Local development — use individual variables from .env
        return psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", 5432),
            dbname=os.environ.get("DB_NAME", "taskmanager"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", ""),
        )


def execute(query, params=None, fetchall=False, fetchone=False):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query, params)
                if fetchall:
                    return cur.fetchall()
                if fetchone:
                    return cur.fetchone()
                return None
    finally:
        conn.close()
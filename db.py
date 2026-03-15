import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", 5432),
        dbname=os.environ.get("DB_NAME", "taskmanager"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", ""),
    )


def execute(query, params=None, fetchall=False, fetchone=False):
    """
    Helper to run any query without repeating connection boilerplate.
    Returns rows as dicts (RealDictRow).
    """
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

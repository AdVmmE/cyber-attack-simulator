import sqlite3
import os

class DBManager:
    def __init__(self, db_path="simulation.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize the database with schema."""
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        
        if not os.path.exists(schema_path):
            print(f"Error: Schema file not found at {schema_path}")
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            with open(schema_path, "r") as f:
                schema_script = f.read()
            cursor.executescript(schema_script)
            conn.commit()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Database initialization failed: {e}")
        finally:
            conn.close()

    def execute_query(self, query, params=(), fetch_one=False, fetch_all=False):
        """Helper to execute queries safely (or unsafely depending on usage)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        result = None
        try:
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            conn.commit()
        except Exception as e:
            result = e # Return error to caller for display
        finally:
            conn.close()
        return result
        
    def execute_unsafe_query(self, query):
        """
        Executes a query directly without parameters. DO NOT USE IN REAL APPS.
        This is for simulating SQL Injection vulnerabilities only.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        result = None
        try:
            # VULNERABILITY: Directly executing string query
            cursor.executescript(query) # supports multiple statements for stacking attacks? 
            # Actually executescript returns standard cursor, but for SELECT we usually use execute.
            # But for injection we might want execute.
            # Let's use execute for the login simulation.
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
        except Exception as e:
            result = str(e)
        finally:
            conn.close()
        return result

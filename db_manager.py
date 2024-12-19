import os
import psycopg2
from dotenv import load_dotenv
from pass_data import PassData
load_dotenv()

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("FSTR_DB_HOST"),
            port=os.getenv("FSTR_DB_PORT"),
            user=os.getenv("FSTR_DB_LOGIN"),
            password=os.getenv("FSTR_DB_PASS"),
            database="fstr_db"
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def add_pass(self, name, description):
        query = "INSERT INTO passes (name, description) VALUES (%s, %s) RETURNING id;"
        self.cursor.execute(query, (name, description))
        pass_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return pass_id

def get_pass_by_id(self, pass_id: int):
    query = "SELECT * FROM passes WHERE id = %s;"
    self.cursor.execute(query, (pass_id,))
    return self.cursor.fetchone()


def update_pass(self, pass_id: int, pass_data: PassData):
    query = """
    UPDATE passes
    SET name = %s, description = %s
    WHERE id = %s AND status = 'new';
    """
    try:
        self.cursor.execute(query, (pass_data.name, pass_data.description, pass_id))
        self.connection.commit()
        return True
    except Exception as e:
        self.connection.rollback()
        print(f"Error updating pass: {e}")
        return False


def get_passes_by_email(self, email: str):
    query = "SELECT * FROM passes WHERE user_email = %s;"
    self.cursor.execute(query, (email,))
    return self.cursor.fetchall()

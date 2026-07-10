import os
import sqlite3

DATABASE = os.path.join(os.path.dirname(__file__), "fiado.db")

def get_connection():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    return sqlite3.connect(DATABASE)

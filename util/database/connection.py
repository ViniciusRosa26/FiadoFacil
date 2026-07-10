import sqlite3

DATABASE = "database/fiado.db"

def get_connection():
    return sqlite3.connect(DATABASE)
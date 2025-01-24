import json
from openai import OpenAI
import os
import sqlite3
from time import time


# Get current directory and setup file path generation
fdir = os.path.dirname(__file__)
def get_path(fname):
    return os.path.join(fdir, fname)

sqlite_db_path = get_path("cbb_db.sqlite")
setup_data_path = get_path("setup_data.sql")
setup_tables_path = get_path("setup_tables.sql")


# Erase db if already exists
if os.path.exists(sqlite_db_path):
    os.remove(sqlite_db_path)
    
# Start connection, create cursor, generate table, and insert data
sqlite_connection = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_connection.cursor()
with (
        open(setup_tables_path) as setup_tables,
        open(setup_data_path) as setup_data
    ):
    
    setup_tables_script = setup_tables.read()
    setup_data_script = setup_data.read()
    
sqlite_cursor.executescript(setup_tables_script)
sqlite_cursor.executescript(setup_data_script)


def run_query(query):
    return sqlite_cursor.execute(query).fetchall()

def fetch_database():
    tables = ['Commissioner', 'Conference', 'Team', 'Player']
    
    for table in tables:
        print(f"{table} Data:")
        data = run_query(f'SELECT * FROM {table}')
        for row in data:
            print('  ', row)
        print()
        
    
        
fetch_database()
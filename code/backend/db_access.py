import sqlite3
from typing import Optional
from traffic_entry import TrafficEntry
import configparser
import os
import jsonpickle

config = configparser.ConfigParser()
path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config.read(os.path.join(path, 'config.ini'))
database_name = config['database']['NAME']
table_name = config['database']['TABLE_NAME']
conn: sqlite3.Connection = sqlite3.connect(database_name, check_same_thread=False)
cursor: sqlite3.Cursor = conn.cursor()

def create_table():
    print(f"Creating the table {table_name} (if not exists yet).")
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crossingId INTEGER,
            time1 FLOAT,
            time2 FLOAT,
            speed FLOAT,
            countdown FLOAT
        )
    ''')
    conn.commit()

def insert_entry(crossing_id: int, time1: float):
    print(f"Inserting entry for crossing {crossing_id}.")
    cursor.execute(f'''
        INSERT INTO {table_name} (crossingId, time1)
        VALUES (?, ?)
    ''', (crossing_id, time1))
    conn.commit()

def get_entry(crossing_id: int) -> Optional[TrafficEntry]:
    """
    Fetches the most relevant traffic entry for the specified crossing ID.
    """
    
    print(f"Fetching entry for crossing {crossing_id}.")
    cursor.execute(f'''
        SELECT * FROM {table_name}
        WHERE crossingId = ?
        ORDER BY time1 DESC
        LIMIT 1
    ''', (crossing_id,))
    entry = TrafficEntry()
    db_entry = cursor.fetchone()
    entry.id = int(db_entry[0])
    entry.crossingId = int(db_entry[1])
    entry.time1 = db_entry[2]
    entry.time2 = db_entry[3]
    entry.speed = db_entry[4]
    entry.countdown = db_entry[5]
    return entry

def get_all_entries():
    print("Fetching all entries..")
    cursor.execute(f'''
        SELECT * FROM {table_name}
        ORDER BY time1 DESC
    ''')
    entry_array = []
    db_entries = cursor.fetchall()
    for db_entry in db_entries:
        entry = TrafficEntry()
        entry.id = int(db_entry[0])
        entry.crossingId = int(db_entry[1])
        entry.time1 = db_entry[2]
        entry.time2 = db_entry[3]
        entry.speed = db_entry[4]
        entry.countdown = db_entry[5]
        entry_array.append(entry)
    return entry_array

def save_entry(entry: TrafficEntry):
    print(f"Saving entry for crossing {entry.crossingId}.")
    cursor.execute(f'''
        UPDATE {table_name}
        SET time1 =?, time2 =?, speed =?, countdown=?
        WHERE id =?
    ''', (entry.time1, entry.time2, entry.speed, entry.countdown, entry.id))
    conn.commit()

def close_connection():
    print("Closing the sqlite-connection.")
    conn.close()
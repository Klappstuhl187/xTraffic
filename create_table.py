import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('livetraffic.db')
cursor = conn.cursor()

# SQL-Befehl zum Erstellen der Tabelle
cursor.execute('''
    CREATE TABLE IF NOT EXISTS live (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crossingId INTEGER,
        time1 TIMESTAMP,
        time2 TIMESTAMP,
        time3 TIMESTAMP,
        speed1 FLOAT,
        speed2 FLOAT
    )
''')

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("Die Tabelle 'live' wurde erfolgreich erstellt.")

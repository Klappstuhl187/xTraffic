import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('livetraffic.db')
cursor = conn.cursor()

# SQL-Befehl zum Löschen der Tabelle
cursor.execute("DROP TABLE IF EXISTS live")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("Die Tabelle 'live' wurde erfolgreich gelöscht.")

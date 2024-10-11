import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('livetraffic.db')
cursor = conn.cursor()

# SQL-Befehl zum Abrufen aller Daten aus der Tabelle 'live'
cursor.execute('SELECT * FROM live')
rows = cursor.fetchall()

# Spaltenüberschriften
headers = [i[0] for i in cursor.description]

# Tabelle anzeigen
print(f"{' | '.join(headers)}")  # Spaltenüberschriften ausgeben
print('-' * 50)

# Alle Zeilen der Tabelle ausgeben
for row in rows:
    print(' | '.join(str(cell) for cell in row))

# Verbindung schließen
conn.close()

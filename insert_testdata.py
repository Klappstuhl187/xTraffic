import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('livetraffic.db')
cursor = conn.cursor()

# Testwerte in die Tabelle 'live' einfügen
cursor.execute("INSERT INTO live (CrossingId, time1, time2, time3, speed) VALUES (?, ?, ?, ?, ?)", (1, 100, 110, 120, 80))
cursor.execute("INSERT INTO live (CrossingId, time1, time2, time3, speed) VALUES (?, ?, ?, ?, ?)", (1, 110, 120, 130, 80))
cursor.execute("INSERT INTO live (CrossingId, time1, time2, time3, speed) VALUES (?, ?, ?, ?, ?)", (1, 120, 130, 140, 80))

# Änderungen speichern
conn.commit()

# Überprüfen, ob die Daten eingefügt wurden
print ('CrossingId | Time1 | Time2 | Time3 | Speed')
cursor.execute("SELECT * FROM live")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Verbindung schließen
conn.close()

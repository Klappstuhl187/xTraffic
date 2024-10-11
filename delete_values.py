import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('livetraffic.db')
cursor = conn.cursor()

try:
    # 1. Alle Einträge in der Tabelle 'live' löschen
    cursor.execute('''
    DELETE FROM live;
    ''')
    print("Alle Einträge in der Tabelle 'live' wurden gelöscht.")

    # Änderungen speichern
    conn.commit()

except sqlite3.Error as e:
    print(f"Ein Fehler ist aufgetreten: {e}")

finally:
    # Verbindung schließen
    conn.close()

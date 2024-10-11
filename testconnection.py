import serial
import sqlite3
from datetime import datetime

# Serielle Verbindung zum Arduino (Passe den Port ggf. an, z.B. /dev/ttyUSB0)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('livetraffic.db')
cursor = conn.cursor()

# Funktion zum Einfügen der Daten in die Datenbank
def insert_data():
    crossingId = 1
    time1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Aktuelle Uhrzeit im passenden Format
    time2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO live (crossing_id, time1, time2, time3) VALUES (?, ?, ?, ?)",
                   (crossing_id, time1, time2, time3))
    conn.commit()  # Speichere die Änderung
    print("Daten erfolgreich eingefügt:", (crossing_id, time1, time2, time3))

# Hauptschleife zum Lesen der seriellen Daten
while True:
    if ser.in_waiting > 0:
        # Daten vom Arduino lesen
        data = ser.readline().decode('utf-8').rstrip()

        if data == "BUTTON_PRESSED":
            print("Button gedrückt, Daten werden in die Datenbank eingetragen...")
            insert_data()

# Verbindung schließen, wenn das Programm beendet wird (optional)
# conn.close()

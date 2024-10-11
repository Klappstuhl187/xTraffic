import serial
import time

# Serielle Verbindung zum Arduino herstellen
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Passe ggf. die Schnittstelle an
time.sleep(2)  # Warte, bis die Verbindung stabil ist

print("Verbindung zum Arduino hergestellt. Warte auf LED-Status...")

# Funktion zur Protokollierung von Nachrichten
def log_message(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{current_time}] {message}")

# Endlos-Schleife, um Nachrichten vom Arduino zu empfangen
while True:
    if arduino.in_waiting > 0:
        # Lese die Nachricht vom Arduino
        message = arduino.readline().decode('utf-8').strip()
        # Protokolliere die Nachricht mit Zeitstempel
        log_message(message)
    time.sleep(0.1)  # Kleine Pause, um die CPU-Last zu verringern

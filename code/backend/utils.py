import time
import threading

def keepalive_task():
    while True:
        time.sleep(1)

def create_keepalive_thread():
    keepalive_thread = threading.Thread(target=keepalive_task)
    keepalive_thread.start()
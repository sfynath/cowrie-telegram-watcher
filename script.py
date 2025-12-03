#!/usr/bin/env python3
import json
import time
import requests

TOKEN = "7521602808:AAG-ODC0f3DaALUAB9fK6eL_Sr6Bp_CjmWM"
CHAT_ID = -4925100000
LOGFILE = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_telegram(text):
    try:
        r = requests.post(URL, data={"chat_id": CHAT_ID, "text": text})
        print("Telegram status:", r.status_code)
    except Exception as e:
        print("Error kirim Telegram:", e)

def follow(file):
    file.seek(0, 2)  # lompat ke akhir file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def main():
    with open(LOGFILE, "r") as f:
        for line in follow(f):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            # hanya kirim untuk login sukses
            if event.get("eventid") == "cowrie.login.success":
                src = event.get("src_ip", "-")
                user = event.get("username", "-")
                pwd  = event.get("password", "-")
                msg = (
                    "🔥 Cowrie Honeypot Login Success\n"
                    f"IP     : {src}\n"
                    f"User   : {user}\n"
                    f"Passwd : {pwd}"
                )
                send_telegram(msg)

if __name__ == "__main__":
    main()

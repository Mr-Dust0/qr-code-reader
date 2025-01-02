from datetime import datetime
import platform
import os
import json
import requests

URL = "https://192.168.5.102"

def logPdfOpen(file: str):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    hostname = platform.node()
    data = {
        "TimeStamp": current_time,
        "HostName": hostname,
        "FileName":file 
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(URL + "/log", data=json.dumps(data), headers=headers, verify=False)
        print(response.status_code)
        print(response.text)
    except Exception as e:
        print(URL)
        print(e)
        print("Cant reach centernal server")
        os.system('dunstify "Cant reach centeral server"')

def logPdfClose():
    hostname = platform.node()
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    data = {
        "HostName": hostname,
        "TimeStampClosed":current_time 
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.put(URL + "/fileclosed", data=json.dumps(data), headers=headers, verify=False)
        print(response.status_code)
        print(response.text)
    except Exception as e:
        print(URL)
        print(e)
        print("Cant reach centernal server")
        os.system('dunstify "Cant reach centeral server"')


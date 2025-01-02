from datetime import datetime
import platform
import os
import json
import requests
from config import URL


def logPdfOpen(file: str):
    hostname = platform.node()
    data = {
        "HostName": hostname,
        "FileName":file 
    }
    headers = {"Content-Type": "application/json"}
    try:
        # Send json to the log server to log what file has been opened and by what hostname
        # Dont send the time because the time can be off on the pi
        response = requests.post(URL + "/log", data=json.dumps(data), headers=headers, verify=False)
        print(response.text)
    except Exception as e:
        print("Cant reach centernal server")
        os.system('dunstify "Cant reach centeral server"')

def logPdfClose():
    hostname = platform.node()
    data = {
        "HostName": hostname,
    }
    headers = {"Content-Type": "application/json"}
    try:
        # Send hostname to centeral log server and that will mark the most recent opened file by the hostname as closed.
        response = requests.put(URL + "/fileclosed", data=json.dumps(data), headers=headers, verify=False)
        print(response.text)
    except Exception as e:
        print(URL)
        print(e)
        print("Cant reach centernal server")
        os.system('dunstify "Cant reach centeral server"')


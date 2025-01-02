import os
import time
import subprocess
from evdev import InputDevice, categorize, ecodes
import subprocess
from config import key_map
import handle_userinput 



output = []
def get_device_path(notifed):
    command = "sudo lshw | grep barcode -i -A 3 | tail -n1 | cut -d ':' -f 2"
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=100)
    device_path = result.stdout
    if device_path == "":
        if not notifed:
            os.system('dunstify "Scanner disconnected"')
            print("alerted")
            notifed  = True
        time.sleep(5)
        return notifed, ""
    os.system('dunstify "Connected to the scanner"')
    notifed = False
    return  notifed , device_path.strip()

def listen_to_scanner():
    try:
        # Open the device
        device_path = ""
        notifed = False
        while device_path == "":
            notifed, device_path = get_device_path(notifed)
        scanner = InputDevice(device_path)
        print(f"Listening for input from: {scanner.name}")
        # Store previously pressed keys to avoid duplicates
        pressed_keys = set()
        capatize = False
        # Loop to capture events
        for event in scanner.read_loop():
            if event.type == ecodes.EV_KEY:  # Key press/release events
                key_event = categorize(event)
                # Only process key press (not key release)
                if key_event.keystate == key_event.key_down:
                    if key_event.keycode not in pressed_keys:
                        char = key_map[key_event.keycode]
                        if char == "err":
                            print("Werid keyboard thing")
                            continue
                        if char == "cap":
                            capatize = True
                            continue
                        if char == '\n':
                            #print(''.join(output)[8:])
                            file_url = handle_userinput.format_qr_code(output)
                            handle_userinput.kill_xpdf()
                            output.clear()
                            handle_userinput.handle_file_url(file_url)
                        else:
                            if capatize:
                                print(f"{char.upper()} is capataized")
                                output.append(char.upper())
                                capatize = False
                            else:
                                output.append(char)
                        pressed_keys.add(key_event.keycode)  # Mark key as pressed
                elif key_event.keystate == key_event.key_up:
                    # Mark key as released
                    if key_event.keycode in pressed_keys:
                        pressed_keys.remove(key_event.keycode)
                        # This stops duplicate keys from being read from input because the key can only be read once when the key is down because the key is addeed to an set and when the key is realsed the character is removed from the set.
    except OSError as e:
        if e.errno == 19 or e.errno == 2:
            listen_to_scanner()  # Call the function to handle the error when the scanner disconnects this makes it try to connect to the device again and will display the notification saying that the scanner is disconnected.
        else:
            print(f"An error occurred: {e}")


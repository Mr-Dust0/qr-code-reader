import os
import time
import subprocess
from evdev import InputDevice, categorize, ecodes
import subprocess
from config import key_map
import handle_userinput 



output = []
def get_device_path(notifed):
    # Command to see if the scanner is connected and get the device path
    command = "sudo lshw | grep barcode -i -A 3 | tail -n1 | cut -d ':' -f 2"
    # Using run to make sure the progarms waits until the command runs before carrying on.
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    device_path = result.stdout
    # Check if the device is connected
    if device_path == "":
        # Check to see if the user has already been notified
        if not notifed:
            os.system('dunstify "Scanner disconnected"')
            notifed  = True
        return notifed, ""
    os.system('dunstify "Connected to the scanner"')
    # Reset notifed boolean so the user is notified next time the scanner disconnects
    notifed = False
    return  notifed , device_path.strip()

def listen_to_scanner():
    try:
        device_path = ""
        notifed = False
        # Call get_device_path while the device is not conencted
        while device_path == "":
            notifed, device_path = get_device_path(notifed)
            time.sleep(5)
        scanner = InputDevice(device_path)
        print(f"Listening for input from: {scanner.name}")
        # Store previously pressed keys to avoid duplicates
        pressed_keys = set()
        capatize = False
        # Loop to capture events
        for event in scanner.read_loop():
            if event.type == ecodes.EV_KEY:  
                key_event = categorize(event)
                # Only process key press (not key release)
                if key_event.keystate == key_event.key_down:
                    # Make sure the keycode has not already be read
                    if key_event.keycode not in pressed_keys:
                        # map the keycode to an corresponding character
                        char = key_map[key_event.keycode]
                        # When the device is turned on and scans nothing
                        if char == "err":
                            print("Werid keyboard thing")
                            continue
                        # When the char pressed is shift capatize = True makes the next characters capatilized
                        if char == "cap":
                            capatize = True
                            continue
                        # End of QR code file path so process the date
                        if char == '\n':
                            # Extract file path
                            file_url = handle_userinput.format_qr_code(output)
                            # kill the previously opened document or drawing and log the closing
                            handle_userinput.kill_xpdf()
                            output.clear()
                            # Open pdf and log the opening
                            handle_userinput.handle_file_url(file_url)
                        else:
                            # When shift is pressed character before
                            if capatize:
                                output.append(char.upper())
                                capatize = False
                            else:
                                output.append(char)
                        pressed_keys.add(key_event.keycode)  
                elif key_event.keystate == key_event.key_up:
                    if key_event.keycode in pressed_keys:
                        # Remove key from set as key is now pressed up
                        pressed_keys.remove(key_event.keycode)
    except OSError as e:
        if e.errno == 19 or e.errno == 2:
    # Call the function to handle the error when the scanner disconnects and the file is no longer present to try and conenct to it again
            listen_to_scanner()  
        else:
            print(f"An error occurred: {e}")


import os
import time
from evdev import InputDevice, categorize, ecodes, list_devices
from config import key_map
import handle_userinput 
import inotify.adapters



output = []
def get_device_path():
    # Get all the devices currently connected to the machine looking in /dev/input
    for dev in list_devices():
        # Check to see if the barcode is already connected
        if "barcode" in InputDevice(dev).name:
            os.system("dunstify 'Scanner Connected'")
            # Return the path of the barcode scanner normally like /dev/input/event13
            return dev
    # Alerted user device is not connected
    os.system("dunstify 'Scanner not connected'")
    notifier = inotify.adapters.Inotify()
    # Watch the /dev/input path for events like an new file being created there
    notifier.add_watch('/dev/input/')
    # Go through one event after another when they are generated
    for event in notifier.event_gen():
        if event is not None:
            # If the event is an file creation see if event is in the file name of the created file because all input devices start with event
            if 'IN_CREATE' in event[1]:
                if "event" in event[3]:
                    # Sleep for one second beacuse accessing the file when its first created causes errors
                    time.sleep(1)
                    dev = InputDevice(event[2] + event[3])
                    # See if the newly connected device is the barcode scanner
                    if "barcode" in dev.name:
                        os.system("dunstify 'Scanner Connected'")
                        return event[2] + event[3]


def listen_to_scanner():
    try:
        # Call get_device_path while the device is not conencted
        device_path = get_device_path()
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


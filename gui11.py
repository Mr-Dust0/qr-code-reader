import os
import time
import subprocess
from pathlib import Path
from tkinter import Tk, Canvas
from PIL import Image, ImageTk  # Import Pillow for image handling
from evdev import InputDevice, categorize, ecodes
import subprocess
import threading
import logger
from gui import create_gui


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"
URL = "https://192.168.5.102"
output = []
key_map = {
    "KEY_A": 'a', "KEY_B": 'b', "KEY_C": 'c', "KEY_D": 'd',
    "KEY_E": 'e', "KEY_F": 'f', "KEY_G": 'g', "KEY_H": 'h',
    "KEY_I": 'i', "KEY_J": 'j', "KEY_K": 'k', "KEY_L": 'l',
    "KEY_M": 'm', "KEY_N": 'n', "KEY_O": 'o', "KEY_P": 'p',
    "KEY_Q": 'q', "KEY_R": 'r', "KEY_S": 's', "KEY_T": 't',
    "KEY_U": 'u', "KEY_V": 'v', "KEY_W": 'w', "KEY_X": 'x',
    "KEY_Y": 'y', "KEY_Z": 'z',
    "KEY_1": '1', "KEY_2": '2', "KEY_3": '3', "KEY_4": '4',
    "KEY_5": '5', "KEY_6": '6', "KEY_7": '7', "KEY_8": '8',
    "KEY_9": '9', "KEY_0": '0',
    "KEY_BACKSLASH": '\\',  # Handle backslash
    "KEY_SLASH": '/',      # Handle slash
    "KEY_DOT": '.',        # Handle dot
    "KEY_SPACE": ' ',      # Handle space (if you want to allow space between words)
    "KEY_ENTER": '\n',     # Handle enter
    "KEY_MINUS": '-',
    "KEY_KEYBOARD": "err",
        "KEY_LEFTSHIFT":"cap"}


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def open_pdf(file_url: str):
    try:
        # Get the number of pages in the PDF
        num_of_pages = subprocess.check_output(
            ["pdfinfo", file_url],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        home = os.path.expandvars("$HOME")
        # Extract number of pages
        pages = [line for line in num_of_pages.splitlines() if "Pages" in line]
        num_of_pages = pages[0].split(":")[1].strip() if pages else "0"
        print(f"Number of pages: {num_of_pages}")
        if num_of_pages == "1":
            subprocess.Popen(['xpdf', file_url, '-fullscreen', '-q'])
            time.sleep(2)  # Give it time to load
        else:
            os.system('dunstify "This file is going to take longer because it has more than one page."')
            subprocess.Popen(['pdfcrop', file_url, f"{home}/outputdoc.pdf"]).wait()
            subprocess.Popen(['xpdf', f'{home}/outputdoc.pdf', '-cont', '-geom', screen_geometry])
            time.sleep(3)
        print(file_url)
        logger.logPdfOpen(file_url)
    except subprocess.CalledProcessError as e:
        print(f"Error opening PDF: {e.output.decode()}")
        os.system(f'dunstify "Error: {e.output.decode()}"')


def handle_file_url(file_url):
    if file_url:
        os.system(f'dunstify "Loading file: {file_url}"')
        if file_url.endswith(".pdf"):
            open_pdf(file_url)
        elif file_url.endswith(".docx"):
            os.system(f'dunstify "Loading DOCX file: {file_url}"')
            subprocess.Popen(['abiword', file_url, '--geometry', screen_geometry ])
            time.sleep(5) # loading abiword takes longer than loading xpdf
        else:
            print("Unsupported file type.")
            os.system(f'dunstify "Unsported file type {file_url}"')


def kill_xpdf(file_url):
    try:
         result = subprocess.run(            ["pgrep", "-f",'xpdf'],            stdout=subprocess.PIPE,            stderr=subprocess.PIPE,            text=True        )        # If pgrep found a process, it will have output        return result.returncode == 0
         if result.returncode == 0:
             subprocess.Popen(['pkill', '-f', 'xpdf'])
             time.sleep(0.5)  # Wait to ensure it terminates
             logger.logPdfClose()
             
    except Exception as e:
        print(f"Error killing xpdf: {e}")


def format_qr_code(user_input):
    user_input_text = ''.join(user_input)
    print(user_input_text)
    print(user_input)
    try:
        index_of_forward_slash = user_input_text.index('/')
        file_url = ''.join(user_input[index_of_forward_slash:])
        return file_url
    except ValueError:
        os.system(f'dunstify "QR code error: Invalid ata: {user_input_text[7:]}"')
        return ''


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
                            file_url = format_qr_code(output)
                            kill_xpdf(file_url)
                            output.clear()
                            handle_file_url(file_url)
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


def main():
    global screen_geometry
    screen_geometry = subprocess.check_output(
            "xdpyinfo | awk '/dimensions/{print $2}'", shell=True
        ).decode('utf-8').strip()
    #logger.logPdfOpen("/Testing New Layout")
    #logger.logPdfClose()
    scanner_thread = threading.Thread(target=listen_to_scanner, daemon=True)
    scanner_thread.start()
    
    create_gui(screen_geometry)
main()

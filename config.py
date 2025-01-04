import subprocess
from pathlib import Path
from os import environ

# Needed to display the pdf document full screen and adapt to different mointors
screen_geometry = subprocess.check_output(
            "xdpyinfo | awk '/dimensions/{print $2}'", shell=True
        ).decode('utf-8').strip()
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"
IMAGE_PATH = ASSETS_PATH / Path("image_1.jpg")  
URL = environ.get('URL')
output = []
# Keymap is needed to map the input from the evdev InputDevice to actuall characters that can be used
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



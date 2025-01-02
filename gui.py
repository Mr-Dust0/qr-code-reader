from pathlib import Path
from tkinter import Tk, Canvas
from PIL import Image, ImageTk  # Import Pillow for image handling
from config import screen_geometry
from config import ASSETS_PATH


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def create_gui():
    window = Tk()
    window.title("QR Code Reader")
    window.geometry(screen_geometry)
    window.configure(bg="#FFFFFF")
    width, height = map(int, screen_geometry.split('x'))
        # Create a canvas for UI design
    canvas = Canvas(window, bg="#FFFFFF", height=height, width=width, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
        # Calculate relative positions
    rect_width = int(width * 0.55)  # 40% of screen width
    rect_height = int(height * 0.13)  # 10% of screen height
    rect_x1 = (width - rect_width) / 2
    rect_y1 = (height - rect_height) / 2 + int(height * 0.21)  # 10% of screen height from top
    rect_x2 = rect_x1 + rect_width
    rect_y2 = rect_y1 + rect_height
    canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="#D9D9D9", outline="")
    rect_center_x = (rect_x1 + rect_x2) / 2
    rect_center_y = (rect_y1 + rect_y2) / 2
    canvas.create_text(rect_center_x, rect_center_y, anchor="n",
                           text="Please Scan the QR Code.",
                           fill="#000000",
                           font=("Inter ExtraBold", int(height * 0.05)))  # Font size relative to screen height
        # Add image in the center between the text and the rectangle using Pillow
    image_path = relative_to_assets("image_1.jpg")  # Path to your .jpeg image
    try:
        img = Image.open(image_path)  # Open the image using Pillow
        img = img.resize((int(width * 0.2), int(height * 0.2)))  # Resize image to 20% of screen width/height
        img_tk = ImageTk.PhotoImage(img)  # Convert image for Tkinter
        image_id = canvas.create_image(rect_center_x, rect_center_y + rect_height + int(height * 0.05), image=img_tk)  # Position image below the text
        canvas.image = img_tk  # Keep a reference to the image to avoid garbage collectionexcept
    except Exception as e:
        print(f"Error loading image: {e}")

        # Add instructions text to the canvas
    last = int(height * 0.1)  # Starting position 10% of the height
    title = "Instructions for how to use"
    instruction_text_1 = "1) Turn on QR code reader by pressing the trigger button and wait until the blue lights go solid, indicating the device is connected."
    instruction_text_2 = "2) Please scan the QR code and wait a bit. The PDF should be displayed on the screen. If not, retry or unplug and replug the device as there may be an issue with the internet."
    instruction_text_3 = "3) If the pdf being read is a word document transferred, please give it some time to load as the pdf has to be edited first so that it can be displayed on one page."
    instruction_text_4 = "4) After the pdf has been loaded, please wait 5 seconds before reading again"
    canvas.create_text(
            int(width * 0.05), last,  # Position at the center
            text=title, font=("Arial", int(height * 0.05), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    last += int(height * 0.1)
    canvas.create_text(
            int(width * 0.05), last,  # Position at the center
            text=instruction_text_1, font=("Arial", int(height * 0.03), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    last += int(height * 0.1)
    canvas.create_text(int(width * 0.05), last,  # Slightly below the first instruction
            text=instruction_text_2, font=("Arial", int(height * 0.03), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    last += int(height * 0.15)
    canvas.create_text(
            int(width * 0.05), last,  # Position at the center
            text=instruction_text_3, font=("Arial", int(height * 0.03), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    last += int(height * 0.1)
    canvas.create_text(
            int(width * 0.05), last,  # Position at the center
            text=instruction_text_4, font=("Arial", int(height * 0.03), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    window.mainloop()



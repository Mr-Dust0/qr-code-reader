from tkinter import Tk, Canvas
from PIL import Image, ImageTk  
from config import IMAGE_PATH, screen_geometry




def create_gui():
    """Creates the tkinter window for the application"""
    window = Tk()
    window.title("QR Code Reader")
    # Allows the application to adapt to the mointor the application is being displayed on.
    window.geometry(screen_geometry)
    window.configure(bg="#FFFFFF")
    width, height = map(int, screen_geometry.split('x'))
    canvas = Canvas(window, bg="#FFFFFF", height=height, width=width, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    # Calcuates realtive postions for the text and images to go in the UI so can adapt to mointor resoloution
    rect_width = int(width * 0.55)  
    rect_height = int(height * 0.13)  
    rect_x1 = (width - rect_width) / 2
    rect_y1 = (height - rect_height) / 2 + int(height * 0.21)  
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
    try:
        img = Image.open(IMAGE_PATH)  
        # Resize image to 20% of screen width/height
        img = img.resize((int(width * 0.2), int(height * 0.2)))  
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(rect_center_x, rect_center_y + rect_height + int(height * 0.05), image=img_tk) 
        # Keep a reference to the image to avoid the image being collected by the garabage collector
        canvas.image = img_tk  
    except Exception as e:
        print(f"Error loading image: {e}")

    # Add instructions text to the gui to give users instructions on how to use the application
    # Starting position 10% of the height and adding 10% each time to keep the text on different lines and relative to the resoloution of the mointor.
    last = int(height * 0.1)  
    title = "Instructions for how to use"
    instruction_text_1 = "1) Turn on QR code reader by pressing the trigger button and wait until the blue lights go solid, indicating the device is connected."
    instruction_text_2 = "2) Please scan the QR code and wait a bit. The PDF should be displayed on the screen. If not, retry or unplug and replug the device as there may be an issue with the internet."
    instruction_text_3 = "3) If the pdf being read is a word document transferred, please give it some time to load as the pdf has to be edited first so that it can be displayed on one page."
    instruction_text_4 = "4) After the pdf has been loaded, please wait 5 seconds before reading again"
    canvas.create_text(
            int(width * 0.05), last,  
            text=title, font=("Arial", int(height * 0.05), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    last += int(height * 0.1)
    canvas.create_text(
            int(width * 0.05), last,  
            text=instruction_text_1, font=("Arial", int(height * 0.03), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    last += int(height * 0.1)
    canvas.create_text(int(width * 0.05), last,  # Slightly below the first instruction
            text=instruction_text_2, font=("Arial", int(height * 0.03), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    last += int(height * 0.15)
    canvas.create_text(
            int(width * 0.05), last,  
            text=instruction_text_3, font=("Arial", int(height * 0.03), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    last += int(height * 0.1)
    canvas.create_text(
            int(width * 0.05), last,  
            text=instruction_text_4, font=("Arial", int(height * 0.03), "bold"), fill="black", width=width - int(width * 0.1), anchor="nw")
    window.mainloop()



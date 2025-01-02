import logger
import subprocess
import os
import time
from config import screen_geometry

def format_qr_code(user_input):
    # Convert the list to an string
    user_input_text = ''.join(user_input)
    try:
        # The qr code reads #0026 with random numbers so want to get the start of file path
        index_of_forward_slash = user_input_text.index('/')
        file_url = (user_input_text[index_of_forward_slash:])
        return file_url
    except ValueError:
        os.system(f'dunstify "QR code error: Invalid Data: {user_input_text} (ignore the # and the numbers)"')
        return ''

def open_pdf(file_url: str):
    try:
        home = os.path.expandvars("$HOME")
        # Get the number of pages in the PDF
        num_of_pages = subprocess.check_output(["pdfinfo", file_url],stderr=subprocess.STDOUT).decode('utf-8')
        # Extract number of pages from the output
        pages = [line for line in num_of_pages.splitlines() if "Pages" in line]
        num_of_pages = pages[0].split(":")[1].strip() if pages else "0"
        print(f"Number of pages: {num_of_pages}")
        # If the pdf is just an drawing so can just be opened
        if num_of_pages == "1":
            subprocess.Popen(['xpdf', file_url, '-fullscreen', '-q'])
            # Give it time to load can't use run because that will hang the progarm until user shuts the document
            time.sleep(2)  
        # More than one page
        else:
            os.system('dunstify "This file is going to take longer because it has more than one page."')
            # Cropt the pdf to get rid of margins so the whole pdf can be displayed on the mointor without scrolling because the end user will only have an scanner as input and have no keyboard and mouse
            subprocess.Popen(['pdfcrop', file_url, f"{home}/outputdoc.pdf"]).wait()
            subprocess.Popen(['xpdf', f'{home}/outputdoc.pdf', '-cont', '-geom', screen_geometry])
            time.sleep(3)
        # Log the pdf being opened to the centernal server
        logger.logPdfOpen(file_url)
    except subprocess.CalledProcessError as e:
        print(f"Error opening PDF: {e.output.decode()}")
        os.system(f'dunstify "Error: {e.output.decode()}"')


def handle_file_url(file_url):
    if file_url:
        os.system(f'dunstify "Loading file: {file_url}"')
        # Check to see what document type loading
        if file_url.endswith(".pdf"):
            open_pdf(file_url)
        elif file_url.endswith(".docx"):
            os.system(f'dunstify "Loading DOCX file: {file_url}"')
            subprocess.Popen(['abiword', file_url, '--geometry', screen_geometry ])
            time.sleep(5) # loading abiword takes longer than loading xpdf
        else:
            print("Unsupported file type.")
            os.system(f'dunstify "Unsported file type {file_url}"')

def kill_xpdf():
    try:
        # If pgrep found a process, it will have returncode equal zero so know an document is already open so have to kill that procoess.
         result = subprocess.run(["pgrep", "-f",'xpdf'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)        
         if result.returncode == 0:
             subprocess.Popen(['pkill', '-f', 'xpdf'])
             #time.sleep(0.5)
            # Log the closing of the file
             logger.logPdfClose()
    except Exception as e:
        print(f"Error killing xpdf: {e}")

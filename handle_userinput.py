import logger
import subprocess
import os
import time
from config import screen_geometry

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

def kill_xpdf():
    try:
         result = subprocess.run(            ["pgrep", "-f",'xpdf'],            stdout=subprocess.PIPE,            stderr=subprocess.PIPE,            text=True        )        # If pgrep found a process, it will have output        return result.returncode == 0
         if result.returncode == 0:
             subprocess.Popen(['pkill', '-f', 'xpdf'])
             time.sleep(0.5)  # Wait to ensure it terminates
             logger.logPdfClose()
             
    except Exception as e:
        print(f"Error killing xpdf: {e}")

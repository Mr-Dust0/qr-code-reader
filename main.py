import threading
from gui import create_gui
from handle_scanner import listen_to_scanner
from os import  environ
def main():
    # Starts an thread in background that handles getting input from the scanner
    scanner_thread = threading.Thread(target=listen_to_scanner, daemon=True)
    scanner_thread.start()
    create_gui()
    #if environ.get("URL"):
        #create_gui()
    #else:
        #print("Make sure URL env is set to log server")
        #exit(10)

if __name__ == "__main__":
    main()

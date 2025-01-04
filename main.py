import threading
from gui import create_gui
from handle_scanner import listen_to_scanner

def main():
    # Starts an thread in background that handles getting input from the scanner
    scanner_thread = threading.Thread(target=listen_to_scanner, daemon=True)
    scanner_thread.start()
    create_gui()

if __name__ == "__main__":
    main()

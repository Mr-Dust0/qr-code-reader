import threading
from gui import create_gui
from handle_scanner import listen_to_scanner


def main():
    scanner_thread = threading.Thread(target=listen_to_scanner, daemon=True)
    scanner_thread.start()
    create_gui()
main()

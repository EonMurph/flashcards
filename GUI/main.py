from sys import exit
from app_window import FlashcardsWindow
from PySide6.QtWidgets import QApplication

def main():
    flashcardsApp = QApplication([])
    flashcardsWindow = FlashcardsWindow()
    flashcardsWindow.show()
    exit(flashcardsApp.exec())

if __name__ == "__main__":
    main()
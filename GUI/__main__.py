from sys import exit
from app_controller import Flashcards
from app_model import FlashcardsModel
from app_window import FlashcardsWindow
from PySide6.QtWidgets import QApplication

def main():
    flashcardsApp = QApplication([])
    flashcardsWindow = FlashcardsWindow(decks=["1", "2"], note_types=["1", "2"])
    flashcardsWindow.show()
    Flashcards(view=flashcardsWindow, model=FlashcardsModel())
    exit(flashcardsApp.exec())

if __name__ == "__main__":
    main()
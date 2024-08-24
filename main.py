from sys import exit
from GUI import FlashcardsWindow, FlashcardsModel, Flashcards
from PySide6.QtWidgets import QApplication

def createApp():
    flashcardsApp = QApplication([])
    flashcardsWindow = FlashcardsWindow(decks=["1", "2"], note_types=["1", "2"])
    flashcardsWindow.show()
    Flashcards(view=flashcardsWindow, model=FlashcardsModel(), data="test")
    flashcardsApp.exec()

def main():
    createApp()

if __name__ == "__main__":
    main()

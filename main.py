from sys import exit
from GUI import FlashcardsWindow, FlashcardsModel, Flashcards
from PySide6.QtWidgets import QApplication
from genanki import Note, Model, Deck
from data import decks


def createApp() -> None:
    flashcardsApp = QApplication([])
    flashcardsModel = FlashcardsModel(decks=decks)
    flashcardsWindow = FlashcardsWindow(
        decks=flashcardsModel.decks,
        initialNote=flashcardsModel.currentFlashcard,
    )
    flashcardsWindow.show()
    Flashcards(view=flashcardsWindow, model=flashcardsModel)
    flashcardsApp.exec()


def main() -> None:
    createApp()


if __name__ == "__main__":
    main()

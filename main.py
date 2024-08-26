from sys import exit
from GUI import FlashcardsWindow, FlashcardsModel, Flashcards
from PySide6.QtWidgets import QApplication
from genanki import Note, Model, Deck
from data import decks, FlashcardsData


def createApp() -> None:
    flashcardsApp = QApplication([])
    flashcardsData = FlashcardsData(decks=decks)
    flashcardsWindow = FlashcardsWindow(
        decks=["1", "2"],
        note_types=["1", "2"],
        initialNote=flashcardsData.currentFlashcard,
    )
    flashcardsWindow.show()
    Flashcards(view=flashcardsWindow, model=FlashcardsModel(), data=flashcardsData)
    flashcardsApp.exec()


def main() -> None:
    createApp()


if __name__ == "__main__":
    main()

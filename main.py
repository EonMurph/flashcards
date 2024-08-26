from sys import exit
from GUI import FlashcardsWindow, FlashcardsModel, Flashcards
from PySide6.QtWidgets import QApplication
from genanki import Note, Model, Deck
from data import decks, FlashcardsData

my_note = Note(
    model=Model(
        model_id=1607392319,
        name="Simple Model",
        fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Test"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            }
        ],
        css="",
        model_type=0,
    ),
    fields=["Capital of Argentina", "Buenos Aires", "test"],
    sort_field="Capital of Argentina",
    guid="HSnG{z%dU<",
)


def createApp():
    flashcardsApp = QApplication([])
    flashcardsWindow = FlashcardsWindow(
        decks=["1", "2"], note_types=["1", "2"], initialNote=my_note
    )
    flashcardsWindow.show()
    Flashcards(
        view=flashcardsWindow, model=FlashcardsModel(), data=FlashcardsData(decks=decks)
    )
    flashcardsApp.exec()


def main():
    createApp()


if __name__ == "__main__":
    main()

from GUI.app_model import FlashcardsModel
from GUI.app_window import FlashcardsWindow


class Flashcards:
    """Controller class for the Flashcards app."""

    def __init__(self, view: FlashcardsWindow, model: FlashcardsModel):
        self.view = view
        self.model = model
        self._connectSignalsAndSlots()

    def _connectSignalsAndSlots(self):
        self.view.noteCreator.clicked.connect(
            lambda: self.model.FlashcardOperations.createFlashcard()
        )
        self.view.noteDeleter.clicked.connect(
            lambda: self.model.FlashcardOperations.deleteFlashcard()
        )

        for editor in self.view.flashcardEditors:
            editor.textEditor.textChanged.connect(
                lambda e=editor: self.model.TextOperations.renderPreview(
                    text=e.textEditor.toPlainText(),
                    preview=e.flashcardPreview,
                )
            )

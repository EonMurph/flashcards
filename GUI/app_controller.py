from GUI.app_model import FlashcardsModel
from GUI.app_window import FlashcardsWindow
from GUI.flashcard_editor import FlashcardEditor
from data import FlashcardsData
from functools import partial


class Flashcards:
    """Controller class for the Flashcards app."""

    def __init__(
        self, view: FlashcardsWindow, model: FlashcardsModel, data: FlashcardsData
    ):
        self.view = view
        self.model = model
        self.data = data
        self._connectSignalsAndSlots()

    def _connectSignalsAndSlots(self):
        self.view.noteCreator.clicked.connect(
            lambda: self.model.FlashcardOperations.createFlashcard()
        )
        self.view.noteDeleter.clicked.connect(
            lambda: self.model.FlashcardOperations.deleteFlashcard()
        )

        def getFields(editors: list[FlashcardEditor]) -> dict[str, str]:
            editorsText: list[str] = [
                editor.textEditor.toPlainText() for editor in editors
            ]
            fields = {
                field[0]: field[1]
                for field in zip(
                    [
                        field["name"]
                        for field in self.data.currentFlashcard.model.fields
                    ],
                    editorsText,
                )
            }

            return fields

        for editor in self.view.editors:
            editor.textEditor.textChanged.connect(
                lambda e=editor: self.model.TextOperations.renderPreview(
                    fields=getFields(editors=self.view.editors),
                    previews=self.view.flashcardPreviews,
                    template=self.data.currentFlashcard.model.templates[0],
                )
            )

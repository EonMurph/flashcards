from GUI.app_model import FlashcardsModel
from GUI.app_window import FlashcardsWindow
from GUI.flashcard_editor import FlashcardEditor
from data import FlashcardsData
from functools import partial


class Flashcards:
    """Controller class for the Flashcards app."""

    def __init__(self, view: FlashcardsWindow, model: FlashcardsModel) -> None:
        self.view = view
        self.model = model

        self._previewRender = partial(
            self.model.textOperations.renderPreview,
            previews=self.view.flashcardPreviews,
        )

        self._onLoad()
        self._connectSignalsAndSlots()

    def _generateFieldsArg(self, editors: list[FlashcardEditor]) -> dict[str, str]:
        editorsText: list[str] = [editor.textEditor.toPlainText() for editor in editors]
        fields = {
            field[0]: field[1]
            for field in zip(
                [field["name"] for field in self.model.currentFlashcard.model.fields],
                editorsText,
            )
        }

        return fields

    def _setTemplateNamesItems(self) -> None:
        self.view.noteTemplateSelector.addItems(self.model.templateNames)

    def _setModelNamesItems(self) -> None:
        self.view.noteModelSelector.addItems(self.model.modelNames)

    def _onLoad(self) -> None:
        """Method to be called upon loading the window. This method will call some starter functions in `self.model` so that the loaded window will display properly."""
        self._previewRender(
            fields=self._generateFieldsArg(editors=self.view.editors),
            template=self.model.currentFlashcard.model.templates[0],
        )
        self._setTemplateNamesItems()
        self._setModelNamesItems()

    def _connectSignalsAndSlots(self) -> None:
        self.view.noteCreator.clicked.connect(
            lambda: self.model.flashcardOperations.createFlashcard()
        )
        self.view.noteDeleter.clicked.connect(
            lambda: self.model.flashcardOperations.deleteFlashcard()
        )

        for editor in self.view.editors:
            editor.textEditor.textChanged.connect(
                lambda: self._previewRender(
                    fields=self._generateFieldsArg(editors=self.view.editors),
                    template=self.model.currentTemplate,
                )
            )

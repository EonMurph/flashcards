from GUI.app_model import FlashcardsModel
from GUI.app_window import FlashcardsWindow
from GUI.flashcard_editor import FlashcardEditor
from functools import partial


class Flashcards:
    """Controller class for the Flashcards app."""

    def __init__(self, view: FlashcardsWindow, model: FlashcardsModel) -> None:
        self.view = view
        self.model = model

        self._renderPreview = partial(
            self.model.textOperations.renderPreview,
            previews=self.view.flashcardPreviews,
            model=self.model,
        )

        self._onLoad()
        self._connectSignalsAndSlots()

    def _generateFieldsArg(self, editors: list[FlashcardEditor]) -> dict[str, str]:
        """
        This method is to be called only within call to the self._renderPreview attribute.
        This method is for generating the fields argument used in the model.renderPreview method.
        """
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
        """
        This method is to be called when the model for a flashcard has been changed.
        Method for setting the template QComboBox selectors items.
        """
        self.view.noteTemplateSelector.clear()
        self.view.noteTemplateSelector.addItems(self.model.templateNames)

    def _setModelNamesItems(self) -> None:
        """
        This method is to be called once on initialisation of the controller class.
        This method is for setting the model QComboBox selectors items.
        """
        self.view.noteModelSelector.clear()
        self.view.noteModelSelector.addItems(self.model.modelNames)

    def _refreshFlashcard(self) -> None:
        """
        This method is to be called when changing flashcard data.
        This method refreshes the flashcard related UI.
        """
        self.view.refreshFlashcardEditor(self.model.currentFlashcard)

    def _changeDeck(self, index: int) -> None:
        """
        This method is to be called when changing the deck.
        This method sets the new deck data, and then refreshes any flashcard and deck related UI.
        """
        self.model.setDeckData(deck=self.view.deckSelector.itemText(index).lower())
        self._refreshFlashcard()
        self._onLoad()

    def _changeTemplate(self, index: int) -> None:
        """
        This method is to be connected to the indexChanged signal of the templates QComboBox.
        This method is for changing the current template of a flashcardPreview.
        """
        self.model.setCurrentTemplate(templateName=self.model.templateNames[index])
        self._renderPreview(fields=self._generateFieldsArg(editors=self.view.editors))

    def _changeModel(self, index: int) -> None:
        """
        This method is to be connected to the indexChanged signal of the model QComboBox.
        This method is for changing the current model of a flashcard.
        """
        self.model.setCurrentModel(modelName=self.model.modelNames[index])
        self._refreshFlashcard()
        self._setTemplateNamesItems()
        self._previewRender(fields=self._generateFieldsArg(editors=self.view.editors))

    def _onLoad(self) -> None:
        """
        This method is to only be called upon initialisation of the controller class.
        This method will call some starter functions in `self.model` so that the loaded window will display properly.
        """
        self._refreshFlashcard()
        self._setModelNamesItems()

    def _connectSignalsAndSlots(self) -> None:
        """
        This method is to only be called upon initialisation of the controller class.
        This method connected any signals to their correct slot.
        """
        self.view.noteCreator.clicked.connect(
            lambda: self.model.flashcardOperations.createFlashcard()
        )
        self.view.noteDeleter.clicked.connect(
            lambda: self.model.flashcardOperations.deleteFlashcard()
        )

        for editor in self.view.editors:
            editor.textEditor.textChanged.connect(
                lambda: self._renderPreview(
                    fields=self._generateFieldsArg(editors=self.view.editors)
                )
            )

        self.view.noteTemplateSelector.currentIndexChanged.connect(
            lambda i: self._changeTemplate(index=i)
        )
        self.view.noteModelSelector.currentIndexChanged.connect(
            lambda i: self._changeModel(index=i)
        )
        self.view.deckSelector.currentIndexChanged.connect(
            lambda i: self._changeDeck(i)
        )

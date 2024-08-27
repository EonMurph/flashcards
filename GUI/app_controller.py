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
        self.view.flashcardTemplateSelector.clear()
        self.view.flashcardTemplateSelector.addItems(self.model.templateNames)

    def _setModelNamesItems(self) -> None:
        """
        This method is to be called once on initialisation of the controller class.
        This method is for setting the model QComboBox selectors items.
        """
        self.view.flashcardModelSelector.clear()
        self.view.flashcardModelSelector.addItems(self.model.modelNames)

    def _setFlashcardNumDisplayText(self) -> None:
        """
        This method is to be called on initialisation of the controller class, or when refreshing the flashcard, whether by creation, deletion or deck changing.
        This method is for setting the text for the QLabel displaying the number of flashcards in the deck and the changes status of the deck.
        """
        self.view.flashcardNumDisplay.setText(
            f"Flashcards in deck: {self.model.numFlashcards}({'+-'[self.model.flashcardChangesStatus < 0] + str(abs(self.model.flashcardChangesStatus))})"
        )

    def _setCurrentFlashcardIndexText(self) -> None:
        """
        This method is to be called on initialisation of the controller class, or when either the index of the current flashcard changed or the number of flashcards in the deck changed.
        This method is for setting the text for the QLabel displaying the current flashcard's index out of the total number of flashcards in the deck.
        """
        self.view.currentFlashcardIndex.setText(
            f"{self.model.currentFlashcardIndex + 1}/{self.model.numFlashcards}"
        )

    def _changeFlashcard(self, indexDifference: int) -> None:
        """
        This method is to be called when changing which flashcard is being viewed.
        This method is for calling the model.changeFlashcard method and then refreshing the flashcard related UI.
        """
        self.model.flashcardOperations.changeFlashcard(
            model=self.model, indexDifference=indexDifference
        )
        self._refreshFlashcard()

    def _refreshFlashcard(self) -> None:
        """
        This method is to be called when changing flashcard data.
        This method refreshes the flashcard related UI.
        """
        self.view.refreshFlashcardEditor(self.model.currentFlashcard)
        self._setTemplateNamesItems()
        self._setCurrentFlashcardIndexText()
        self._renderPreview(fields=self._generateFieldsArg(editors=self.view.editors))

    def _changeDeck(self, index: int) -> None:
        """
        This method is to be called when changing the deck.
        This method sets the new deck data, and then refreshes any flashcard and deck related UI.
        """
        self.model.setDeckData(deck=self.view.deckSelector.itemText(index).lower())
        self._refreshFlashcard()

    def _changeFlashcard(self, indexDifference: int) -> None:
        """
        This method is to be called when changing which flashcard is being viewed.
        This method is for calling the model.changeFlashcard method and then refreshing the flashcard related UI.
        """
        self.model.flashcardOperations.changeFlashcard(indexDifference=indexDifference)
        self._changeModel(index=self.model.modelNames.index(self.model.currentFlashcard.model.name))
        self.view.flashcardModelSelector.setCurrentIndex(self.view.flashcardModelSelector.findText(self.model.currentFlashcard.model.name))
        self._refreshFlashcard()

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
        self.model.setCurrentModel(modelArg=self.model.modelNames[index])
        self._refreshFlashcard()

    def _onLoad(self) -> None:
        """
        This method is to only be called upon initialisation of the controller class.
        This method will call some starter functions in `self.model` so that the loaded window will display properly.
        """
        self._refreshFlashcard()
        self._setModelNamesItems()
        self._setFlashcardNumDisplayText()
        self._setCurrentFlashcardIndexText()

    def _connectSignalsAndSlots(self) -> None:
        """
        This method is to only be called upon initialisation of the controller class.
        This method connected any signals to their correct slot.
        """
        self.view.flashcardCreator.clicked.connect(
            lambda: self.model.flashcardOperations.createFlashcard()
        )
        self.view.flashcardDeleter.clicked.connect(
            lambda: self.model.flashcardOperations.deleteFlashcard()
        )

        for editor in self.view.editors:
            editor.textEditor.textChanged.connect(
                lambda: self._renderPreview(
                    fields=self._generateFieldsArg(editors=self.view.editors)
                )
            )

        self.view.flashcardTemplateSelector.currentIndexChanged.connect(
            lambda i: self._changeTemplate(index=i)
        )
        self.view.flashcardModelSelector.currentIndexChanged.connect(
            lambda i: self._changeModel(index=i)
        )
        self.view.deckSelector.currentIndexChanged.connect(
            lambda i: self._changeDeck(i)
        )

        self.view.previousFlashcardButton.clicked.connect(
            lambda: self._changeFlashcard(indexDifference=-1)
        )
        self.view.nextFlashcardButton.clicked.connect(
            lambda: self._changeFlashcard(indexDifference=1)
        )

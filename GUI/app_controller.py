from .app_model import FlashcardsModel
from .app_window import FlashcardsWindow
from .flashcard_editor import FlashcardEditor
from custom_note import CustomNote


class Flashcards:
    """Controller class for the Flashcards app."""

    def __init__(self, view: FlashcardsWindow, model: FlashcardsModel) -> None:
        self.view = view
        self.model = model
        self.refreshOperations = RefreshOperations(self)

        self._onLoad()
        self._connectSignalsAndSlots()

    def _generateFields(self, editors: dict) -> dict[str, str]:
        """
        This method is to be called only within a call to the self._renderPreview attribute.
        This method is for generating the fields argument used in the model.renderPreview method.
        """
        editorsText: list[str] = [
            editors[fieldName].textEditor.toPlainText() for fieldName in editors
        ]
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
        self.view.flashcardModelSelector.addItems(self.model.flashcardModelNames)

    def _setFlashcardNumDisplayText(self) -> None:
        """
        This method is to be called on initialisation of the controller class, or when the UI component's refresh method gets called.
        This method is for setting the text for the QLabel displaying the number of flashcards in the deck and the changes status of the deck.
        """
        self.view.flashcardNumDisplay.setText(
            f"Flashcards in deck: {self.model.numFlashcards}({'+-'[self.model.flashcardChangesStatus < 0] + str(abs(self.model.flashcardChangesStatus))})"
        )

    def _setCurrentFlashcardIndexDisplayText(self) -> None:
        """
        This method is to be called on initialisation of the controller class, or when the UI component's refresh method get's called.
        This method is for setting the text for the QLabel displaying the current flashcard's index out of the total number of flashcards in the deck.
        """
        self.view.currentFlashcardIndexDisplay.setText(
            f"{self.model.currentFlashcardIndex + 1}/{self.model.numFlashcards}"
        )

    def _refreshFlashcard(self) -> None:
        """
        This method is to be called when changing flashcard data.
        This method refreshes the flashcard related UI.
        """
        self.view.refreshFlashcardEditor(self.model.currentFlashcard)
        self._setTemplateNamesItems()
        self._setCurrentFlashcardIndexDisplayText()
        self.view.flashcardModelSelector.setCurrentIndex(
            self.view.flashcardModelSelector.findText(
                self.model.currentFlashcard.model.name
            )
        )
        self._renderPreview(fields=self._generateFields(editors=self.view.editors))

    def _refreshFlashcardEditor(self, note: CustomNote) -> None:
        """
        This method is to be called when refreshing the flashcard field editors.
        This methods rebuilds and then reconnects the new flashcard editors to their signals.
        """
        self.view.refreshFlashcardEditor(note=note)
        self._connectTextEditors()

    def _onManipulatingDeck(self) -> None:
        self._setFlashcardNumDisplayText()
        self._refreshFlashcard()

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
        self._changeModel(
            index=self.model.flashcardModelNames.index(
                self.model.currentFlashcard.model.name
            )
        )
        self.view.flashcardModelSelector.setCurrentIndex(
            self.view.flashcardModelSelector.findText(
                self.model.currentFlashcard.model.name
            )
        )
        self._refreshFlashcard()

    def _changeTemplate(self, index: int) -> None:
        """
        This method is to be connected to the indexChanged signal of the templates QComboBox.
        This method is for changing the current template of a flashcardPreview.
        """
        self.model.setCurrentTemplate(templateName=self.model.templateNames[index])
        self._renderPreview(fields=self._generateFields(editors=self.view.editors))

    def _changeModel(self, index: int) -> None:
        """
        This method is to be connected to the indexChanged signal of the model QComboBox.
        This method is for changing the current model of a flashcard.
        """
        self.model.setCurrentFlashcardModel(
            modelArg=self.model.flashcardModelNames[index]
        )
        self._refreshFlashcard()

    def _createFlashcard(self) -> None:
        self.model.flashcardOperations.createFlashcard()
        self._onManipulatingDeck()

    def _deleteFlashcard(self, flashcard: CustomNote) -> None:
        self.model.flashcardOperations.deleteFlashcard(flashcard=flashcard)
        self._onManipulatingDeck()

    def _setRefreshMethods(self) -> None:
        self.view.flashcardModelSelector.refresh = (
            lambda: self.refreshOperations._flashcardModelSelectorRefresh()
        )
        self.view.flashcardTemplateSelector.refresh = (
            lambda: self.refreshOperations._flashcardTemplateSelectorRefresh()
        )
        for fieldName in self.view.editors:
            self.view.editors[fieldName].refresh = (
                lambda: self.refreshOperations._flashcardEditorRefresh()
            )
        for preview in self.view.flashcardPreviews:
            preview.refresh = lambda: self.refreshOperations._flashcardPreviewRefresh()
        self.view.flashcardNumDisplay.refresh = (
            lambda: self.refreshOperations._flashcardNumDisplayTextRefresh()
        )
        self.view.currentFlashcardIndexDisplay.refresh = (
            lambda: self.refreshOperations._currentFlashcardIndexDisplayTextRefresh()
        )

    def _onLoad(self) -> None:
        """
        This method is to only be called upon initialisation of the controller class.
        This method will call some starter functions in `self.model` so that the loaded window will display properly.
        """
        self._setModelNamesItems()
        self._setFlashcardNumDisplayText()
        self._setCurrentFlashcardIndexDisplayText()
        self._refreshFlashcard()
        self._setRefreshMethods()

    def _connectTextEditors(self) -> None:
        """
        This method is to be called whenever the field text editors are (re)built.
        This method connects all the field text editors to the _saveFields method.
        """
        for fieldName in self.view.editors:
            self.view.editors[fieldName].textEditor.textChanged.connect(
                lambda: self._saveFields()
            )

    def _connectSignalsAndSlots(self) -> None:
        """
        This method is to only be called upon initialisation of the controller class.
        This method connected any signals to their correct slot.
        """
        self.view.flashcardCreator.clicked.connect(lambda: self._createFlashcard())
        self.view.flashcardDeleter.clicked.connect(
            lambda: self._deleteFlashcard(self.model.currentFlashcard)
        )

        self._connectTextEditors()

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


class RefreshOperations:
    def __init__(self, controller: Flashcards) -> None:
        self.controller = controller

    def _flashcardModelSelectorRefresh(self) -> None:
        """
        This method is to be called when the current flashcard is changed, whether by creation, deletion, deck change, or flashcard navigation.
        This method refreshes the flashcard model selector QComboBox to display the correct current flashcard model and related data.
        """
        flashcardModel = self.controller.view.flashcardModelSelector.currentData()
        self.controller.model.setCurrentFlashcardModel(
            self.controller.model.flashcardModels[flashcardModel]
        )

    def _flashcardTemplateSelectorRefresh(self) -> None:
        """
        This method is to be called when the current model is changed and when the current flashcard is changed, whether by creation, deletion, deck change, or flashcard navigation.
        This method refreshes the flashcard template selector QComboBox to display the correct flashcard template and related data.
        """
        flashcardTemplate = self.controller.view.flashcardTemplateSelector.currentData()
        self.controller.model.setCurrentTemplate(
            templateName=self.controller.model.templates[flashcardTemplate]
        )

    def _flashcardEditorRefresh(self) -> None:
        """
        This method is to be called when the current model is changed and when the current flashcard is changed, whether by creation, deletion, deck change, or flashcard navigation.
        This method rebuilds and then reconnects the new flashcard editors to their signals.
        """
        self.controller.view.refreshFlashcardEditor(
            self.controller.model.currentFlashcard
        )
        self.controller._connectTextEditors()

    def _flashcardPreviewRefresh(self) -> None:
        """
        This method is to be called on flashcard, field data, template, model, or deck change.
        This method refreshes the flashcard previews.
        """
        self.controller._renderPreview(
            fields=self.controller._generateFields(self.controller.view.editors)
        )

    def _flashcardNumDisplayTextRefresh(self) -> None:
        """
        This method is to be called when changing the number of flashcards, whether by creation, deletion or deck changing.
        This method calls a method that sets the text for a QLabel widget.
        """
        self.controller._setFlashcardNumDisplayText()

    def _currentFlashcardIndexDisplayTextRefresh(self) -> None:
        """
        This method is to be called when the current flashcard index changes, whether by creation, deletion, navigation or deck change.
        This methods calls a method that sets the text for a QLabel widget.
        """
        self.controller._setCurrentFlashcardIndexDisplayText()

from genanki import Deck, Note, Model
from GUI.flashcard_preview import FlashcardPreview


class FlashcardsModel:
    """Model class for the functionality of the Flashcards app."""

    def __init__(self, decks: dict[str, Deck], models: dict[str, Model]) -> None:
        self.textOperations = TextOperations(self)
        self.flashcardOperations = FlashcardOperations(self)
        self.decks = decks
        self.models = models
        self.modelNames: list[str] = [model for model in self.models]
        self.setDeckData()

    def setDeckData(self, deck: str = "cs2208", flashcardIndex: int = 0) -> None:
        """
        This method is to be called on a deck change.
        This method sets all the deck related data and calls methods for setting flashcard data.
        """
        self.currentDeck: Deck = self.decks[deck]
        self.numFlashcards: int = len(self.currentDeck.notes)
        self.setFlashcardData(flashcardIndex)
        self.flashcardChangesStatus: int = 0
        self.templateNames = [template["name"] for template in self.templates]

    def setFlashcardData(self, flashcardIndex: int = 0) -> None:
        """
        This method is to be called on either a deck change or a flashcard change.
        This method sets all flashcard related data and called methods for setting the current model.
        """
        if self.numFlashcards <= flashcardIndex:
            flashcardIndex = 0
        self.currentFlashcard: Note = self.currentDeck.notes[flashcardIndex]
        self.currentFlashcardIndex: int = flashcardIndex
        self.setCurrentModel(self.currentFlashcard.model)

    def setTemplatesData(self) -> None:
        """
        This method is to be called on a model change.
        This method sets all the template related data.
        """
        self.templates: list[dict[str, str]] = self.currentFlashcard.model.templates
        self.currentTemplate: dict[str, str] = self.templates[0]
        self.templateNames = [template["name"] for template in self.templates]

    def setCurrentTemplate(self, templateName: str) -> None:
        """
        This method is to be connected to the template QComboBox's indexChanged signal.
        This method sets the current template for the renderPreview method.
        """
        for template in self.templates:
            if template["name"] == templateName:
                self.currentTemplate = template
                return None

    def setCurrentModel(self, modelArg: str | Model) -> None:
        """
        This method is to be called up a change a flashcard or to be connected to the model QComboBox's indexChanged signal.
        """
        for model in self.models:
            if modelArg in [model, self.models[model]]:
                self.currentFlashcard.model = self.models[model]
                self.setTemplatesData()
                return None


class TextOperations:
    """Class containing methods for manipulating text in the flashcards."""

    def __init__(self, model: FlashcardsModel) -> None:
        self.model = model

    def renderPreview(
        self,
        fields: dict[str, str],
        previews: list[FlashcardPreview],
    ) -> None:
        template = self.model.currentTemplate
        frontFormat = template["qfmt"].format()
        backFormat = template["afmt"].format().replace("{FrontSide}", frontFormat)
        formats = [frontFormat, backFormat]
        for i in range(2):
            previews[i].flashcardPreview.setHtml(formats[i].format(**fields))


class FlashcardOperations:
    """Class containing methods for manipulating the flashcards themselves."""

    def __init__(self, model: FlashcardsModel) -> None:
        self.model = model

    def createFlashcard(self) -> None:
        defaultModel = self.model.models["Default Model"]
        self.model.currentDeck.add_note(Note(model=defaultModel, fields=[]))
        self.model.numFlashcards += 1
        self.model.flashcardChangesStatus += 1
        self.model.setFlashcardData(self.model.numFlashcards - 1)

    def deleteFlashcard(self, flashcard: Note) -> None:
        self.model.currentDeck.notes.remove(flashcard)
        self.model.numFlashcards -= 1
        self.model.flashcardChangesStatus -= 1
        self.model.setFlashcardData(self.model.currentFlashcardIndex)

    def changeFlashcard(self, indexDifference: int) -> None:
        n = self.model.numFlashcards
        currentIndex = self.model.currentFlashcardIndex
        newIndex = (currentIndex + n + indexDifference) % n
        self.model.setFlashcardData(flashcardIndex=newIndex)

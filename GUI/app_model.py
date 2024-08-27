from genanki import Deck, Note, Model
from GUI.flashcard_preview import FlashcardPreview


class FlashcardsModel:
    """Model class for the functionality of the Flashcards app."""

    def __init__(self, decks: dict[str, Deck], models: dict[str, Model]) -> None:
        self.textOperations = TextOperations(self)
        self.flashcardOperations = FlashcardOperations(self)
        self.decks = decks
        self.models = models
        self.setDeckData()

    def setDeckData(self, deck: str = "cs2208") -> None:
        self.currentDeck: Deck = self.decks[deck]
        self.numFlashcards: int = len(self.currentDeck.notes)
        self.setFlashcardData()
        self.flashcardChangesStatus: int = 0
        self.modelNames: list[str] = [model for model in self.models]
        self.templateNames = [template["name"] for template in self.templates]

    def setFlashcardData(self, noteIndex: int = 0) -> None:
        self.currentFlashcard: Note = self.currentDeck.notes[noteIndex]
        self.currentFlashcardIndex: int = noteIndex
        self.setTemplatesData()

    def setTemplatesData(self) -> None:
        self.templates: list[dict[str, str]] = self.currentFlashcard.model.templates
        self.currentTemplate: dict[str, str] = self.templates[0]
        self.templateNames = [template["name"] for template in self.templates]

    def setCurrentTemplate(self, templateName: str) -> None:
        for template in self.templates:
            if template["name"] == templateName:
                self.currentTemplate = template
                return None

    def setCurrentModel(self, modelName: str) -> None:
        for model in self.models:
            if model == modelName:
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

    @staticmethod
    def createFlashcard() -> None:
        pass

    @staticmethod
    def deleteFlashcard() -> None:
        pass

    def changeFlashcard(self, indexDifference: int) -> None:
        n = self.model.numFlashcards
        currentIndex = self.model.currentFlashcardIndex
        newIndex = (currentIndex + n + indexDifference) % n
        self.model.setFlashcardData(noteIndex=newIndex)

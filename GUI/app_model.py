from turtle import mode
from genanki import Deck, Note, Model
from GUI.flashcard_preview import FlashcardPreview


class FlashcardsModel:
    """Model class for the functionality of the Flashcards app."""

    def __init__(self, decks: dict[str, Deck], models: dict[str, Model]) -> None:
        self.textOperations = TextOperations()
        self.flashcardOperations = FlashcardOperations()
        self.decks = decks
        self.models = models
        self.getDeckData()

    def getDeckData(self, deck: str = "cs2208") -> None:
        self.currentDeck: Deck = self.decks[deck]
        self.getFlashcardData()
        self.modelNames: list[str] = [model for model in self.models]
        self.templates = self.getTemplates()
        self.templateNames = [template["name"] for template in self.templates]

    def getFlashcardData(self, noteIndex: int = 0) -> None:
        self.currentFlashcard: Note = self.currentDeck.notes[noteIndex]
        self.currentModel: Model = self.currentFlashcard.model
        self.currentTemplate: dict[str, str] = self.currentModel.templates[0]

    def getTemplates(self) -> list[dict[str, str]]:
        return [template for template in self.currentModel.templates]

    def setCurrentTemplate(self, templateName: str) -> None:
        for template in self.templates:
            if template["name"] == templateName:
                self.currentTemplate = template
                return None

    def setCurrentModel(self, modelName: str) -> None:
        for model in self.models:
            if model == modelName:
                self.currentModel = self.models[model]
                self.templates = self.getTemplates()
                self.templateNames = [template["name"] for template in self.templates]
                return None


class TextOperations:
    """Class containing methods for manipulating text in the flashcards."""

    @staticmethod
    def renderPreview(
        model: FlashcardsModel,
        fields: dict[str, str],
        previews: list[FlashcardPreview],
    ) -> None:
        template = model.currentTemplate
        frontFormat = template["qfmt"].format()
        backFormat = template["afmt"].format().replace("{FrontSide}", frontFormat)
        formats = [frontFormat, backFormat]
        for i in range(2):
            previews[i].flashcardPreview.setHtml(formats[i].format(**fields))


class FlashcardOperations:
    """Class containing methods for manipulating the flashcards themselves."""

    @staticmethod
    def createFlashcard() -> None:
        pass

    @staticmethod
    def deleteFlashcard() -> None:
        pass

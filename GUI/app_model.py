from PySide6.QtWidgets import QTextEdit


class FlashcardsModel:
    """Model class for the functionality of the Flashcards app."""

    class TextOperations:
        @staticmethod
        def renderPreview(text: str, preview: QTextEdit):
            preview.setHtml(text)

    class FlashcardOperations:
        @staticmethod
        def createFlashcard():
            pass

        @staticmethod
        def deleteFlashcard():
            pass

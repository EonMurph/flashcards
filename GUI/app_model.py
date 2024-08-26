from GUI.flashcard_preview import FlashcardPreview


class FlashcardsModel:
    """Model class for the functionality of the Flashcards app."""

    class TextOperations:
        @staticmethod
        def renderPreview(
            fields: dict[str, str],
            previews: list[FlashcardPreview],
            template: dict[str, str],
        ) -> None:
            frontFormat = template["qfmt"].format()
            backFormat = template["afmt"].format().replace("{FrontSide}", frontFormat)
            previews[0].flashcardPreview.setHtml(frontFormat.format(**fields))
            previews[1].flashcardPreview.setHtml(backFormat.format(**fields))

    class FlashcardOperations:
        @staticmethod
        def createFlashcard() -> None:
            pass

        @staticmethod
        def deleteFlashcard() -> None:
            pass

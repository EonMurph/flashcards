from genanki import Note, Deck
from GUI.flashcard_editor import FlashcardEditor
from GUI.flashcard_preview import FlashcardPreview
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QGridLayout,
)


class FlashcardsWindow(QMainWindow):
    """Window or view class for the Flashcards app."""

    def __init__(self, decks: dict[str, Deck], initialNote: Note) -> None:
        super().__init__()
        self.setWindowTitle("Flashcards")
        self.setGeometry(50, 100, 800, 800)
        self.setStyleSheet("QTextEdit { font-size: 13pt; }")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay(decks, initialNote)

    def _createDisplay(self, decks: dict[str, Deck], initialNote: Note) -> None:
        self._createFlashcardToolbar(decks)
        self._createFlashcardEditor(initialNote)
        self._createFlashcardPreview()
        self._createFlashcardNavToolbar()

    def _createFlashcardToolbar(self, decks: dict[str, Deck]) -> None:
        layout = QHBoxLayout()
        self.deckSelector = QComboBox()
        self.deckSelector.addItems([deck.upper() for deck in decks])
        self.noteModelSelector = QComboBox()
        self.noteTemplateSelector = QComboBox()
        self.noteCreator = QPushButton()
        self.noteCreator.setText("&Create")
        self.noteDeleter = QPushButton()
        self.noteDeleter.setText("&Delete")
        layout.addWidget(self.deckSelector)
        layout.addWidget(self.noteModelSelector)
        layout.addWidget(self.noteTemplateSelector)
        layout.addWidget(self.noteCreator)
        layout.addWidget(self.noteDeleter)
        self.generalLayout.addLayout(layout)

    def refreshFlashcardEditor(self, note: Note) -> None:
        while self.flashcardLayout.count():
            child = self.flashcardLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._createFlashcardEditor(note, refresh=True)

    def _createFlashcardEditor(self, note: Note, refresh: bool = False) -> None:
        if not refresh:
            self.flashcardLayout = QGridLayout()

        maxColumns = 2
        numFields = len(note.model.fields)
        self.editors: list[FlashcardEditor] = []
        for i in range(numFields):
            row = i // maxColumns
            col = i % maxColumns
            fieldNames = note.model.fields
            fieldNames = [fieldName["name"] for fieldName in fieldNames]
            fieldData: str = note.fields[i]
            editor = FlashcardEditor(row, fieldNames[i], fieldData)
            self.editors.append(editor)
            self.flashcardLayout.addWidget(self.editors[i], row, col)

        if not refresh:
            self.generalLayout.addLayout(self.flashcardLayout)

    def _createFlashcardPreview(self) -> None:
        layout = QHBoxLayout()
        frontFlashcard = FlashcardPreview("Front")
        backFlashcard = FlashcardPreview("Back")
        self.flashcardPreviews = [frontFlashcard, backFlashcard]
        for preview in self.flashcardPreviews:
            layout.addWidget(preview)

        self.generalLayout.addLayout(layout)

    def _createFlashcardNavToolbar(self) -> None:
        pass

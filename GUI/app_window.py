from genanki import Deck
from data import CustomNote
from .flashcard_editor import FlashcardEditor
from .flashcard_preview import FlashcardPreview
from .custom_widgets import RefreshableQComboBox, RefreshableQLabel
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QGridLayout,
    QFrame,
)


class FlashcardsWindow(QMainWindow):
    """Window or view class for the Flashcards app."""

    def __init__(self, decks: dict[str, Deck], initialNote: CustomNote) -> None:
        super().__init__()
        self.setWindowTitle("Flashcards")
        self.setGeometry(50, 100, 800, 800)
        self.setStyleSheet("QTextEdit { font-size: 13pt; }")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay(decks, initialNote)

    def _createDisplay(self, decks: dict[str, Deck], initialNote: CustomNote) -> None:
        class QHLine(QFrame):
            def __init__(self) -> None:
                super(QHLine, self).__init__()
                self.setFrameShape(QFrame.HLine)  # type: ignore

        self._createFlashcardToolbar(decks)
        self.generalLayout.addWidget(QHLine())
        self._createFlashcardEditor(initialNote)
        self.generalLayout.addWidget(QHLine())
        self._createFlashcardPreview()
        self.generalLayout.addWidget(QHLine())
        self._createFlashcardNavToolbar()

    def _createFlashcardToolbar(self, decks: dict[str, Deck]) -> None:
        layout = QHBoxLayout()
        self.deckSelector = QComboBox()
        self.deckSelector.addItems([deck.upper() for deck in decks])
        self.flashcardModelSelector = RefreshableQComboBox()
        self.flashcardTemplateSelector = RefreshableQComboBox()
        self.flashcardCreator = QPushButton()
        self.flashcardCreator.setText("&Create")
        self.flashcardDeleter = QPushButton()
        self.flashcardDeleter.setText("&Delete")
        layout.addWidget(self.deckSelector)
        layout.addWidget(self.flashcardModelSelector)
        layout.addWidget(self.flashcardTemplateSelector)
        layout.addWidget(self.flashcardCreator)
        layout.addWidget(self.flashcardDeleter)
        self.generalLayout.addLayout(layout)

    def refreshFlashcardEditor(self, note: CustomNote) -> None:
        while self.flashcardLayout.count():
            child = self.flashcardLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._createFlashcardEditor(note, refresh=True)

    def _createFlashcardEditor(self, note: CustomNote, refresh: bool = False) -> None:
        if not refresh:
            self.flashcardLayout = QGridLayout()

        maxColumns = 2
        numFields = len(note.model.fields)
        self.editors: dict[str, FlashcardEditor] = {}
        fieldNames: list[str] = [fieldName["name"] for fieldName in note.model.fields]
        for i in range(numFields):
            row = i // maxColumns
            col = i % maxColumns
            try:
                fieldData: str = note.fields[i]
            except IndexError:
                fieldData = ""
            editor = FlashcardEditor(row, fieldNames[i], fieldData)
            self.editors[fieldNames[i]] = editor
            self.flashcardLayout.addWidget(self.editors[fieldNames[i]], row, col)

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
        flashcardNavBar = QHBoxLayout()
        self.flashcardNumDisplay = RefreshableQLabel()
        self.previousFlashcardButton = QPushButton()
        self.previousFlashcardButton.setText("Previous")
        self.currentFlashcardIndexDisplay = RefreshableQLabel()
        self.currentFlashcardIndexDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentFlashcardIndexDisplay.setMaximumWidth(40)
        self.nextFlashcardButton = QPushButton()
        self.nextFlashcardButton.setText("Next")

        flashcardNavBar.addWidget(self.flashcardNumDisplay)
        flashcardNavBar.addWidget(self.previousFlashcardButton)
        flashcardNavBar.addWidget(self.currentFlashcardIndexDisplay)
        flashcardNavBar.addWidget(self.nextFlashcardButton)
        self.generalLayout.addLayout(flashcardNavBar)

from genanki import Deck
from custom_note import CustomNote
from .flashcard_editor import FlashcardEditor
from .flashcard_preview import FlashcardPreview
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QGridLayout,
    QLabel,
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

    @staticmethod
    def _withRefresh(widget_cls):
        """This method is for adding refresh capabilities to QWidgets."""

        class RefreshableWidget(widget_cls):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self.dirty = False

            def makeDirty(self) -> None:
                self.dirty = True

            def refresh(self) -> None:
                print("Refresh not yet implemented")

        return RefreshableWidget

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
        self.flashcardModelSelector = self._withRefresh(QComboBox)()
        self.flashcardTemplateSelector = self._withRefresh(QComboBox)()
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
        self.editors = {}
        fieldNames: list[str] = [fieldName["name"] for fieldName in note.model.fields]
        for i in range(numFields):
            row = i // maxColumns
            col = i % maxColumns
            try:
                fieldData: str = note.fieldData[i]
            except IndexError:
                fieldData = ""
            editor = self._withRefresh(FlashcardEditor)(row, fieldNames[i], fieldData)
            self.editors[fieldNames[i]] = editor
            self.flashcardLayout.addWidget(self.editors[fieldNames[i]], row, col)

        if not refresh:
            self.generalLayout.addLayout(self.flashcardLayout)

    def _createFlashcardPreview(self) -> None:
        layout = QHBoxLayout()
        frontFlashcard = self._withRefresh(FlashcardPreview)("Front")
        backFlashcard = self._withRefresh(FlashcardPreview)("Back")
        self.flashcardPreviews = [frontFlashcard, backFlashcard]
        for preview in self.flashcardPreviews:
            layout.addWidget(preview)

        self.generalLayout.addLayout(layout)

    def _createFlashcardNavToolbar(self) -> None:
        flashcardNavBar = QHBoxLayout()
        self.flashcardNumDisplay = self._withRefresh(QLabel)()
        self.previousFlashcardButton = QPushButton()
        self.previousFlashcardButton.setText("Previous")
        self.currentFlashcardIndexDisplay = self._withRefresh(QLabel)()
        self.currentFlashcardIndexDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentFlashcardIndexDisplay.setMaximumWidth(40)
        self.nextFlashcardButton = QPushButton()
        self.nextFlashcardButton.setText("Next")

        flashcardNavBar.addWidget(self.flashcardNumDisplay)
        flashcardNavBar.addWidget(self.previousFlashcardButton)
        flashcardNavBar.addWidget(self.currentFlashcardIndexDisplay)
        flashcardNavBar.addWidget(self.nextFlashcardButton)
        self.generalLayout.addLayout(flashcardNavBar)

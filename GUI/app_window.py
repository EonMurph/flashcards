from genanki import Note
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
    QToolBar,
    QToolButton,
)


class FlashcardsWindow(QMainWindow):
    """Window or view class for the Flashcards app."""

    def __init__(self, decks: list[str], note_types: list[str], initialNote: Note):
        super().__init__()
        self.setWindowTitle("Flashcards")
        self.setGeometry(50, 100, 800, 800)
        self.setStyleSheet("QTextEdit { font-size: 13pt; }")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay(decks, note_types, initialNote)

    def _createDisplay(self, decks, note_types, initialNote):
        self._createFlashcardToolbar(decks, note_types)
        self.createFlashcardEditor(initialNote)
        self._createFlashcardPreview()
        self._createFlashcardNavToolbar()

    def _createFlashcardToolbar(self, decks, note_types):
        layout = QHBoxLayout()
        self.deckSelector = QComboBox()
        self.deckSelector.addItems(decks)
        self.noteTypeSelector = QComboBox()
        self.noteTypeSelector.addItems(note_types)
        self.noteCreator = QPushButton()
        self.noteCreator.setText("&Create")
        self.noteDeleter = QPushButton()
        self.noteDeleter.setText("&Delete")
        layout.addWidget(self.deckSelector)
        layout.addWidget(self.noteTypeSelector)
        layout.addWidget(self.noteCreator)
        layout.addWidget(self.noteDeleter)
        self.generalLayout.addLayout(layout)

    def createFlashcardEditor(self, note: Note):
        self.flashcardLayout = QGridLayout()
        maxColumns = 2
        numFields = len(note.model.fields)
        fields = []
        for i in range(numFields):
            row = i // maxColumns
            col = i % maxColumns
            fieldNames = note.model.fields
            fieldNames = [fieldName["name"] for fieldName in fieldNames]
            fieldData: str = note.fields[i]
            fields.append(fieldData)
            self.flashcardLayout.addWidget(
                FlashcardEditor(row, fieldNames[i], fieldData), row, col
            )
        self.generalLayout.addLayout(self.flashcardLayout)

        #! layout.addWidget(self._createTextToolbar())

    def _createFlashcardPreview(self):
        layout = QHBoxLayout()
        frontFlashcard = FlashcardPreview("Front")
        backFlashcard = FlashcardPreview("Back")
        self.flashcardPreviews = [frontFlashcard, backFlashcard]
        for preview in self.flashcardPreviews:
            layout.addWidget(preview)

        self.generalLayout.addLayout(layout)

    #! def _createTextToolbar(self):
    #!     textToolbar = QToolBar()
    #!     # self.headingButton = QToolButton(textToolbar)
    #!     # self.normalTextButton = QToolButton(textToolbar)
    #!     self.boldButton = QToolButton(textToolbar)
    #!     self.italicButton = QToolButton(textToolbar)
    #!     self.underlineButton = QToolButton(textToolbar)

    #!     toolbarButtons = [
    #!         # self.headingButton,
    #!         # self.normalTextButton,
    #!         self.boldButton,
    #!         self.italicButton,
    #!         self.underlineButton,
    #!     ]
    #!     for button in toolbarButtons:
    #!         textToolbar.addWidget(button)

    #!     return textToolbar

    def _createFlashcardNavToolbar(self):
        pass

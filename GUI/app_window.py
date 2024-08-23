from flashcard_editor import FlashcardEditor
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QToolBar,
    QToolButton,
    QTextEdit
)


class FlashcardsWindow(QMainWindow):
    """Window or view class for the Flashcards app."""

    def __init__(self, decks: list[str], note_types: list[str]):
        super().__init__()
        self.setWindowTitle("Flashcards")
        self.setGeometry(50, 100, 800, 800)
        self.setStyleSheet("QTextEdit { font-size: 13pt; }")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay(decks, note_types)

    def _createDisplay(self, decks, note_types):
        self._createFlashcardToolbar(decks, note_types)
        self._createFlashcardEditor()
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

    def _createFlashcardEditor(self):
        layout = QVBoxLayout()
        #! layout.addWidget(self._createTextToolbar())
        frontFlashcard = FlashcardEditor("Front")
        backFlashcard = FlashcardEditor("Back")
        self.flashcardEditors = [frontFlashcard, backFlashcard]
        for editor in self.flashcardEditors:
            layout.addWidget(editor)

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

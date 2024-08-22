from xml.etree import cElementTree
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QTextEdit,
    QLabel,
    QToolBar,
    QToolButton,
)


class FlashcardsWindow(QMainWindow):
    def __init__(self, decks: list[str], note_types: list[str]):
        super().__init__()
        self.setWindowTitle("Flashcards")
        self.setGeometry(50, 100, 800, 800)
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
        self.noteDeleter = QPushButton()
        layout.addWidget(self.deckSelector)
        layout.addWidget(self.noteTypeSelector)
        layout.addWidget(self.noteCreator)
        layout.addWidget(self.noteDeleter)
        self.generalLayout.addLayout(layout)

    def _createFlashcardEditor(self):
        pass

    def _createTextToolbar(self):
        pass

    def _createFlashcardNavToolbar(self):
        pass

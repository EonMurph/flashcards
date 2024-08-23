from PySide6.QtWidgets import QTextEdit, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt


class FlashcardEditor(QWidget):
    """Custom widget for flashcard editor UI component, containing flashcard text editor and preview."""

    def __init__(self, view: str):
        super().__init__()
        self.generalLayout = QHBoxLayout()
        self.setLayout(self.generalLayout)

        self._createTextEditor()
        self._createFlashcardPreview(view)

    def _createTextEditor(self):
        self.textEditor = QTextEdit()
        self.textEditor.setFontPointSize(15)
        self.generalLayout.addWidget(self.textEditor)
    
    def _createFlashcardPreview(self, view: str):
        previewLayout = QVBoxLayout()
        self.generalLayout.addLayout(previewLayout)
        
        previewLabel = QLabel()
        previewLabel.setText(view)
        font = previewLabel.font()
        font.setPointSize(15)
        previewLabel.setFont(font)
        previewLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        flashcardPreview = QTextEdit()
        flashcardPreview.setFontPointSize(self.textEditor.fontPointSize())
        flashcardPreview.setReadOnly(True)

        components = [previewLabel, self.flashcardPreview]
        for component in components[::[-1, 1][view == "Front"]]:
            previewLayout.addWidget(component)
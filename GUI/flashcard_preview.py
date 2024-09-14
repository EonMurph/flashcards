from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt
from .custom_widgets import WidgetWithRefresh


class FlashcardPreview(QWidget, WidgetWithRefresh):
    """Custom widget for the flashcard preview UI component."""

    def __init__(self, view: str):
        super().__init__()
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)

        self._createFlashcardPreview(view)

    def _createFlashcardPreview(self, view: str):
        previewLayout = QVBoxLayout()
        self.generalLayout.addLayout(previewLayout)

        previewLabel = QLabel()
        previewLabel.setText(view)
        previewLabel.setStyleSheet("font-size: 15pt; margin: 0px 10px")
        previewLabel.setAlignment(Qt.AlignmentFlag.AlignLeft if view == "Front" else Qt.AlignmentFlag.AlignRight)
        self.flashcardPreview = QTextEdit()
        self.flashcardPreview.setReadOnly(True)

        previews = [previewLabel, self.flashcardPreview]
        for preview in previews:
            previewLayout.addWidget(preview)

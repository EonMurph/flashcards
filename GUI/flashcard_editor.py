from PySide6.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QLabel


class FlashcardEditor(QWidget):
    """Custom widget for the flashcard editor UI component."""

    def __init__(self, row, fieldName: str, fieldData: str = ""):
        super().__init__()
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)

        self._createTextEditor(row=row, fieldName=fieldName, fieldData=fieldData)

    def _createTextEditor(self, row, fieldName, fieldData):
        textLabel = QLabel()
        textLabel.setText(fieldName)
        textLabel.setStyleSheet("font-size: 12pt;")
        self.textEditor = QTextEdit()
        self.textEditor.setText(fieldData)
        components = [textLabel, self.textEditor]
        for component in components[:: [-1, 1][row == 0]]:
            self.generalLayout.addWidget(component)

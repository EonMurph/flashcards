from typing import Any, Callable
from PySide6.QtWidgets import QComboBox, QLabel


class WidgetWithRefresh:
    """
    This class is to be inherited by my custom QWidget class to allow for refresh functionality.
    """

    def __init__(self) -> None:
        self._dirty = False
        self.refreshMethod: Callable | None = None

    def makeDirty(self) -> None:
        """
        Marks widget as needing a refresh.
        """
        self._dirty = True

    def _makeClean(self) -> None:
        """
        Marks widget as having been refreshed.
        """
        self._dirty = False

    def needsRefresh(self) -> bool:
        return self._dirty

    def refreshWidget(self) -> None:
        if self.refreshMethod is None:
            print("Refresh method has not been implemented.")
        else:
            self.refreshMethod()
            self._makeClean()


class RefreshableQComboBox(QComboBox, WidgetWithRefresh):
    def __init__(self) -> None:
        super().__init__()


class RefreshableQLabel(QLabel, WidgetWithRefresh):
    def __init__(self) -> None:
        super().__init__()

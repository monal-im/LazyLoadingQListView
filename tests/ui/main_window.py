
from PyQt5 import QtWidgets, uic

from ui.utils import BaseModel, LazyItemModel
                
import logging
logger = logging.getLogger(__name__)

LOAD_CONTEXT = 150

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load ui
        uic.loadUi("tests/ui/main_window.ui", self)
        self.uiWidget_listView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        # create ui items
        items = []
        for index in range(20000):
            items.append(f"item {index}")

        # configure models
        self.baseModel = BaseModel(items, self.uiWidget_listView)
        self.lazyItemModel = LazyItemModel(self.baseModel)
        self.uiWidget_listView.setModel(self.lazyItemModel)
        self.lazyItemModel.setVisible(0, LOAD_CONTEXT)
        self.lazyItemModel.setVisible(500, 1550)
        self._setCurrentRow(1100)

    def _setCurrentRow(self, row):
        index = self.lazyItemModel.createIndex(row, 0)
        logger.info(f"Setting row {row} to index {index.row()}")
        #self.uiWidget_listView.scrollTo(index, hint=QtWidgets.QAbstractItemView.PositionAtCenter)
        with self.lazyItemModel.triggerScrollChanges():
            start = self.lazyItemModel.mapFromSource(self.lazyItemModel.createIndex(max(0, row-LOAD_CONTEXT), 0)).row()
            end = self.lazyItemModel.mapFromSource(self.lazyItemModel.createIndex(min(row+LOAD_CONTEXT, self.lazyItemModel.rowCount(None)), 0)).row()
            self.lazyItemModel.setVisible(start, end)

            self.uiWidget_listView.setCurrentIndex(self.lazyItemModel.mapFromSource(index))
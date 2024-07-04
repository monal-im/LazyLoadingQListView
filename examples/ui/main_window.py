
from PyQt5 import QtWidgets, uic

from ui.utils import BaseModel, LazyItemModel
                
import logging
logger = logging.getLogger(__name__)

LOAD_CONTEXT = 150

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load ui
        uic.loadUi("examples/ui/main_window.ui", self)
        self.uiWidget_listView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        # create ui items
        items = []
        for index in range(20000):
            items.append(f"item {index}")

        # configure models
        self.baseModel = BaseModel(items, self.uiWidget_listView)
        self.lazyItemModel = LazyItemModel(self.baseModel, self.uiWidget_listView)
        self.uiWidget_listView.setModel(self.lazyItemModel)
        
        self.lazyItemModel.setCurrentRow(1100)
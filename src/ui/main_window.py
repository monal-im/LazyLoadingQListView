
from PyQt5 import QtWidgets, uic

from ui.utils.base_model import BaseModel
                
import logging
logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load ui
        uic.loadUi("src/ui/main_window.ui", self)

        # create ui items
        items = []
        for index in range(5000):
            items.append(f"item {index}")

        # configure models
        self.baseModel = BaseModel(items, self.uiWidget_listView)
        #self.lazyItemModel = LazyItemModel(self.baseModel)
        #self.uiWidget_listView.setModel(self.lazyItemModel)
        self.uiWidget_listView.setModel(self.baseModel)
        #self.lazyItemModel.setVisible(0, 100)

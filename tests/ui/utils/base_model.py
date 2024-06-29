from PyQt5 import QtCore
import functools

import logging
logger = logging.getLogger(__name__)

LRU_MAXSIZE = 1024*1024

class BaseModel(QtCore.QAbstractListModel):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.items = items

    def headerData(self, *args):
        return None
    
    @functools.lru_cache(maxsize=LRU_MAXSIZE, typed=True)
    def data(self, index, role):
        if index.isValid() or (0 <= index.row() < len(self.items)):
            if role == QtCore.Qt.DisplayRole:
                entry = self.items[index.row()]
                return entry
            #elif role == QtCore.Qt.FontRole:
            #    return 
            #elif role == QtCore.Qt.BackgroundRole:
            #    return 
            #elif role == QtCore.Qt.ForegroundRole:
            #    return 
        else:
            logger.info(f"data called with invalid index: {index.row()}")
        return None

    def rowCount(self, index):
        return len(self.items)

    def columnCount(self, index):
        return 1
    
    def listView(self):
        return self.parent

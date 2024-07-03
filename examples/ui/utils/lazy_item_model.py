from PyQt5 import QtCore, QtWidgets
import functools

from .proxy_data import ProxyData

import logging
logger = logging.getLogger(__name__)

LAZY_DISTANCE = 400
LAZY_LOADING = 100
LOAD_CONTEXT = 150

class LazyItemModel(QtCore.QAbstractProxyModel):
    class ChangeTriggeredFlag:
        def __init__(self, model):
            self.model = model
        def __enter__(self):
            self.model.triggeredProgramatically = True
        def __exit__(self, type, value, traceback):
            self.model.triggeredProgramatically = False

    def __init__(self, sourceModel, parent=None):
        super().__init__(parent)
        self.setSourceModel(sourceModel)
        self.proxyData = ProxyData(self)

        self.triggeredProgramatically = False
        self.listView().verticalScrollBar().valueChanged.connect(self.scrollbarMovedHandler)
        self.sourceModel().layoutAboutToBeChanged.connect(self.layoutAboutToBeChangedHandler)
        self.sourceModel().layoutChanged.connect(self.layoutChangedHandler)

        # proxy signals, too
        signals = [
            "columnsAboutToBeInserted", "columnsAboutToBeMoved", "columnsAboutToBeRemoved",
            "columnsInserted", "columnsMoved", "columnsRemoved", "dataChanged", "headerDataChanged",
            "layoutAboutToBeChanged", "layoutChanged", "modelAboutToBeReset", "modelReset",
            "rowsAboutToBeInserted", "rowsAboutToBeMoved", "rowsAboutToBeRemoved", "rowsInserted",
            "rowsMoved", "rowsRemoved",
        ]
        def emitter(signal, *args):
            logger.debug(f"Proxying signal '{signal}' from parent model with args: {args}")
            getattr(self, signal).emit(*args)
        
        for signal in signals:
            getattr(sourceModel, signal).connect(functools.partial(emitter, signal))

    def layoutAboutToBeChangedHandler(self, *args):
        # the topIndex is needed to restore our scroll position after triggering a lazy loading by scrolling up
        self.topIndex     = self.mapToSource(self.listView().indexAt(self.listView().viewport().contentsRect().topLeft()))
        
        # save current selected index, to be restored later on
        # use sourceModel indexes because they stay stable even when we insert rows in this model
        self.currentIndexBefore = self.mapToSource(self.listView().currentIndex())

    def layoutChangedHandler(self, *args):
        # timer function to be called once the loading completed
        def correctIt():
            # select item that was selected *before* we inserted stuff
            if self.currentIndexBefore.isValid():
                toProxyIndex = self.mapFromSource(self.currentIndexBefore)
                logger.debug(f"Resetting selected index to correct one: {self.currentIndexBefore.row() = }, {toProxyIndex.row() = }")
                self.listView().setCurrentIndex(toProxyIndex)
            
            # scroll to item that was at viewport top *before* we inserted stuff
            self.listView().scrollTo(self.mapFromSource(self.topIndex), hint=QtWidgets.QAbstractItemView.PositionAtTop)
            
            self.triggeredProgramatically = False
        
        # use a timer to add this event to the back of our event queue because it won't visibly select the item otherwise
        # this timer has to trigger the correct scrollTo() after setting the current index, to not jump to that index when
        # using the mouse to scroll
        # (even without a timer it still selects the correct item, just not visibly)
        # (calling QtWidgets.QApplication.processEvents() before calling setCurrentIndex() won't help)
        self.correctingTimer = QtCore.QTimer()
        self.correctingTimer.setSingleShot(True)
        self.correctingTimer.timeout.connect(correctIt)
        self.correctingTimer.start(0)
    
    def setVisible(self, start, end):
        logger.debug(f"Setting visibility of rows in interval: {start = }, {end = }")
        self.beginInsertRows(self.createIndex(start, 1), start, end);
        self.proxyData.setVisible(start, end)
        self.endInsertRows();

    def scrollbarMovedHandler(self, *args):
        # if triggeredProgramatically is True the scrollbar wasn't moved by the user and shouldn't load any more rows
        if self.triggeredProgramatically != False:
            return
        
        topIndex     = self.mapToSource(self.listView().indexAt(self.listView().viewport().contentsRect().topLeft()))
        bottomIndex  = self.mapToSource(self.listView().indexAt(self.listView().viewport().contentsRect().bottomLeft()))

        previousIndex = self.proxyData.getPreviousIndexWithState(topIndex, False)
        if previousIndex != None and topIndex.row() - previousIndex <= LAZY_DISTANCE:
            # don't use the context manager because we have to set it to false in the timer
            self.triggeredProgramatically = True
            
            self.layoutAboutToBeChangedHandler()
            # this is the actual loading and will move all indexes to other positions
            self.setVisible(max(previousIndex - LAZY_LOADING, 0), topIndex.row())
            self.layoutChangedHandler()
            
            # we don't need to check if we have to lazy load rows below us, if we already had to load rows above us --> just return
            return
        
        nextIndex = self.proxyData.getNextIndexWithState(bottomIndex, False)
        if nextIndex != None and nextIndex - bottomIndex.row() <= LAZY_DISTANCE:
            with self.triggerScrollChanges():
                self.setVisible(bottomIndex.row(), min(nextIndex + LAZY_LOADING, self.sourceModel().rowCount(None)))
    
    def triggerScrollChanges(self):
        return self.ChangeTriggeredFlag(self)

    @functools.lru_cache(typed=True)
    def parent(self, index):
        # this method logs errors if not implemented, so simply return an invalid index to make qt happy
        return QtCore.QModelIndex()
    
    @functools.lru_cache(typed=True)
    def index(self, row, column, parent=None):
        # this method logs errors if not implemented and is needed for qt to show content
        return self.createIndex(row, column, parent)
    
    def mapFromSource(self, sourceIndex):
        # from real index to proxy index
        return self.createIndex(self.proxyData.getNextVisibleProxyRow(sourceIndex.row()), 0)

    def mapToSource(self, proxyIndex):
        # from proxy index to real index
        if not proxyIndex.isValid():
            return QtCore.QModelIndex()
        nextVisibleRow = self.proxyData.getNextVisibleRow(proxyIndex.row())
        try:
            return self.sourceModel().createIndex(nextVisibleRow, 0)
        except:
            logger.exception(f"Exception with data: {nextVisibleRow = } {proxyIndex.row() = }")
            raise

    def rowCount(self, index):
        return self.proxyData.getRowCount()

    @functools.lru_cache(typed=True)
    def columnCount(self, index):
        return self.sourceModel().columnCount(index)
    
    @functools.lru_cache(typed=True)
    def listView(self):
        return self.sourceModel().listView()

    def setCurrentRow(self, row):
        index = self.createIndex(row, 0)
        logger.info(f"Setting row {row} to index {index.row()}")
        with self.triggerScrollChanges():
            self.setVisible(max(row-LOAD_CONTEXT, 0), min(row+LOAD_CONTEXT, self.sourceModel().rowCount(None)))

            self.listView().setCurrentIndex(self.mapFromSource(index))
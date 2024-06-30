# LazyLoadingQListView
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![Blog](https://img.shields.io/badge/blog-pyqt-green.svg)](https:https://doc.qt.io/) ![License](https://img.shields.io/badge/License-MIT-%23efefef?style=flat&color=%234287f5&link=https%3A%2F%2Fgithub.com%2Fmonal-im%2FLazyLoadingQListView%2Fblob%2Fmaster%2FLICENSE)

A proxy data model allowing to add Lazy Loading capabilities to any QListView and its Model

## Installation
There are two ways to use the LazyItemModel.
1. Install via pip
    ```
    pip install LazyLoadingQListView
    ```
    By installing the LazyItemModel with pip, easy usage is guaranteed.
    ```python
    from LazyLoadingQListView import LazyItemModel
    ```


2. Downloading from Github
    [LazyLoadingQListView](https://github.com/monal-im/LazyLoadingQListView) 
    By installing the code from github, it is possible to make additional changes, according to your needs.


## Useage
The *LazyItemModel* is nothing more than a proxy model, that changes dynamicly due to scrolling or by setting a range of items visbile by hand ([setVisible(start, end)](#setVisible)). The *LazyItemModel* can eather be installed via pip or by copying the code provided in this reposetory, if you want to make additional changes. To use the *LazyItemModel* you also need to create a *baseModel* and a *QListView*. The Models must be stacked as shown below:

<img src="https://github.com/monal-im/LazyLoadingQListView/assets/76741977/6ea8ef46-1651-44f6-b312-dd787e43bd2c" alt="Structure" width="400"/>

```python
# configure models
self.listView = QtWidgets.QListView()
self.baseModel = BaseModel(items, self.listView)
self.lazyItemModel = LazyItemModel(self.baseModel)
self.listView.setModel(self.lazyItemModel)

self.lazyItemModel.setVisible(0, 150)
```
As visible in the implementation above not only the *QListView* is passed to the *baseModel* but the items that should be displayed aswell. Because of that the *baseModel* should be modified that you can pass the items directly to the init. We recommend to derive from the [*QtCore.QAbstractListModel*](https://doc.qt.io/qtforpython-5/PySide2/QtCore/QAbstractListModel.html).

The elements are automatically made visible when scrolling but if you jump to a position not visible yet, you have to set the items visible with [setVisible(start, end)](#setVisible).

## Functions
[__init__(sourceModel, parent=None)](#init)\
[__layoutAboutToBeChangedHandler__()](#layoutAboutToBeChangedHandler)\
[__layoutChangedHandler__()](#layoutChangedHandler)\
[__setVisible__(start, end)](#setVisible)\
[__scrollbarMovedHandler__()](#scrollbarMovedHandler)\
[__triggerScrollChanges__()](#triggerScrollChanges)\
[__parent__(index)](#parent)\
[__mapFromSource__(sourceIndex)](#mapFromSource)\
[__mapToSource__(proxyIndex)](#mapToSource)\
[__rowCount__(index)](#rowCount)\
[__columnCount__(index)](#columnCount)\
[__listView__()](#listView)

##
#### init
arguments: (sourceModel, parent=None)\
This function initializes the *LazyItemModel* and takes a *sourceModel* which can be the *baseModel* or an additional *proxyModel*. The parent is None by default and is just used to initialize the model.

##
#### layoutAboutToBeChangedHandler
This function can be called before changing the layout. It saves the current position that can be set again with __layoutChangedHandler()__.This function is automatically called when the *sourceModel* emits __layoutAboutToBeChanged__.

##
#### layoutChangedHandler
This function can be called after the current position is set with __layoutAboutToBeChangedHandler()__ and the layout has changed. This function is automatically called when the *sourceModel* emits __layoutChanged__.

##
#### setVisible
arguments: (start = int, end = int)\
This function sets a range of items visible.

##
#### scrollbarMovedHandler
This function can be used, if you want to manually want to make sure everything is loaded properly. It is automatically called when the value of the vertical scrollbar changed.

##
#### triggerScrollChanges
This function is used to prevent loading of new lines when it is not used by a user. E.g. loading more rows.

##
#### parent
arguments: (index)\
Returns the parent. The index given to the function isn't used but is required by Qt.

##
#### mapFromSource
arguments: (sourceIndex)\
This function converts the realIndex to the proxyIndex. The realIndex is the index returned by the *baseModel* and can differ to the indexes provided by the *listView*.

##
#### mapToSource
arguments: (proxyIndex)\
This function converts the proxyIndex to the realIndex. The proxyIndex is the index returned by the *listView*, it can differ from the realIndex, because of parts that aren't loaded yet.

##
#### rowCount
arguments: (index)\
This function returns the rowCount. The index given to the function isn't used but is required by Qt.

##
#### columnCount
arguments: (index)\
This function returns the columnCount. The index given to the function isn't used but is required by Qt.

##
#### listView
This function returns the *listView*.

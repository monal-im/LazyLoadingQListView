# LazyLoadingQListView
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![Blog](https://img.shields.io/badge/blog-pyqt-green.svg)](https:https://doc.qt.io/) ![License](https://img.shields.io/badge/License-MIT-%23efefef?style=flat&color=%234287f5&link=https%3A%2F%2Fgithub.com%2Fmonal-im%2FLazyLoadingQListView%2Fblob%2Fmaster%2FLICENSE)

A proxy data model allowing to add Lazy Loading capabilities to any QListView and its Model

## Installation
There are two ways to use the *LazyItemModel*.
1. Install via pip
    ```
    pip install LazyLoadingQListView
    ```
    Installing the *LazyItemModel* with pip ensures easy use.
    ```python
    from LazyLoadingQListView import LazyItemModel
    ```

2. Download from Github
    [LazyLoadingQListView](https://github.com/monal-im/LazyLoadingQListView) 
    By installing the code from Github it is possible to make further changes as needed.


## Usage
If you are processing large amounts of data that you want to display in a [*QListView*](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QListView.html), or if you are adding large amounts of items to the [*QListView*](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QListView.html) in a short period of time, you may experience long wait times. But this is not a problem of Python, specifically the problem is the time it takes Pyqt to create an uiItem. To solve this problem, we created the *LazyItemModel*. It creates the uiItems on demand through the UI, implements smooth scrolling in both directions and allows jumps with a simple implementation.

1. Import the library
    ```python
    from LazyLoadingQListView import LazyItemModel
    ```

2. Implementation\
    Typically when implementing the [*QListView*](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QListView.html) you simply create a baseModel and pass it to the [*QListView*](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QListView.html). Basically you do the same thing here but add the *LazyItemModel* in between as shown below:

    <img src="https://github.com/monal-im/LazyLoadingQListView/assets/76741977/6ea8ef46-1651-44f6-b312-dd787e43bd2c" alt="Structure" width="400"/>

    ```python
    # configure models
    self.listView = QtWidgets.QListView()
    self.baseModel = BaseModel()
    self.lazyItemModel = LazyItemModel(self.baseModel, self.listView, 150)
    self.listView.setModel(self.lazyItemModel)
    ```

    The *baseModel* can be any model of your choice as long as the [*QListView*](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QListView.html) is able to use it. It can even be a different proxy model.

    When initializing the *LazyItemModel*, you have the option of passing a number as a third option to make the first items visible directly. If nothing is passed, the first 150 items are set to Visible. You can also pass __None__ and nothing will be set as visible.

    A complete example (including a simple base model) can be found in the examples folder.
    Another good example is the [*DebugTools*](https://github.com/monal-im/DebugTools) from Monal, where the *LazyItemModel* is already used.

    ##

    Jumping to rows is easy by simply using the existing setCurrentRow function. The function requires the index you want to switch to. It automatically sets the lines visible and switches to the given line.

    ```python
        self.lazyItemModel.setCurrentRow(x)
    ```

## Functions
These are the functions provided by the *LazyItemModel*

[__init__(sourceModel, parent=None)](#init)\
[__setVisible__(start, end)](#setVisible)\
[__setCurrentRow__(row)](#setCurrentRow)


[__mapFromSource__(sourceIndex)](#mapFromSource)\
[__mapToSource__(proxyIndex)](#mapToSource)\
[__rowCount__(index)](#rowCount)\
[__columnCount__(index)](#columnCount)

##
#### init
arguments: (sourceModel, parent=None)\
This function initializes the *LazyItemModel* and takes a *sourceModel*, which can be the *baseModel* or an additional *proxyModel*. The parent defaults to None and is only used to initialize the model.

##
#### setVisible
arguments: (start = int, end = int)\
This function makes a range of items visible.

##
#### setCurrentRow
This function needs the line (int) you want to go to

##
#### mapFromSource
arguments: (sourceIndex)\
This function converts the realIndex to the proxyIndex. The realIndex is the index returned by the *baseModel* and may be different from the indexes provided by the *listView*.

##
#### mapToSource
arguments: (proxyIndex)\
This function converts the proxyIndex to the realIndex. The proxyIndex is the index returned by *listView*. It may differ from the realIndex due to parts not yet loaded.

##
#### rowCount
arguments: (index)\
This function returns the rowCount. The index passed to the function is not used, but is required by Qt.

##
#### columnCount
arguments: (index)\
This function returns the ColumnCount. The index passed to the function is not used, but is required by Qt.


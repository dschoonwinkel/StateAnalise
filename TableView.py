# This Python file uses the following encoding: utf-8
from PySide2 import QtCore
from PySide2.QtCore import QFile, QAbstractTableModel, Qt
from PySide2 import QtWidgets
from PySide2.QtWidgets import QTableView, QHeaderView, QComboBox, QPushButton, QLineEdit
from PySide2.QtUiTools import QUiLoader
import os
import pandas as pd
import re
import Categories


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class TableView(QtWidgets.QWidget):
    def __init__(self, strAbsFilename):
        super().__init__()
        self.load_ui()
        self.tableView = self.findChild(QTableView, "tableView")
        self.ComboBoxCategory = self.findChild(QComboBox, "CategoryComboBox")
        self.ComboBoxCategory.insertItems(0, Categories.categories)
        self.ComboBoxCategory.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.buttonAddToCategories = self.findChild(QPushButton, "buttonAddToCategories")
        self.buttonAddToCategories.clicked.connect(self.AddToCategories)
        self.EntryLineEdit = self.findChild(QLineEdit, "EntryLineEdit")

        strDirectory, strFile = os.path.split(strAbsFilename)
        strDirectory = os.path.join(strDirectory, "uncategorized")
        strFileToProcess = re.sub(".csv", "_uncategorized.csv", strFile)
        strFileToProcess = os.path.join(strDirectory, strFileToProcess)
        data = pd.read_csv(strFileToProcess, index_col=[0])

        self.model = TableModel(data)
        self.tableView.setModel(self.model)
        self.tableView.resize(800, 400)
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def onCurrentIndexChanged(self, ix):
        print("currentIndex:", ix)
        print("Item: ", self.ComboBoxCategory.currentText())

    def AddToCategories(self):
        strCurrentItem = self.ComboBoxCategory.currentText()
        Categories.write_categories("categories1_backup.txt", Categories.categories, Categories.match_strings_dict)
        Categories.match_strings_dict[strCurrentItem].append(self.EntryLineEdit.text())
        print("New match string: ", Categories.match_strings_dict[strCurrentItem])
        Categories.write_categories("categories1.txt", Categories.categories, Categories.match_strings_dict)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "TableView.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

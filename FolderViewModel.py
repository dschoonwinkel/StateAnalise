# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QFileDialog, QPushButton, QListView
from PySide2.QtCore import QStringListModel
import glob
import os
import datetime
from sort_by_vendor import SortByVendor
from compare_budget import CompareBudgetWithActuals
from plot_monthly import PlotStackedBarFilename
from TableView import TableView
import re

class FolderViewModel:
    def __init__(self, parent, strFolderButtonName, strFileListViewName,
                 strSortVendorButton="", strShowUncategorizedButton="", strCompareBudgetButton="", strPlotMonthliesButton=""):
        self.parent = parent
        self.buttonOpenFolder = parent.findChild(QPushButton, strFolderButtonName)
        self.buttonOpenFolder.clicked.connect(self.FolderButtonClicked)

        self.ListViewFileList = parent.findChild(QListView, strFileListViewName)
        self.StringModelFilesList = QStringListModel([])
        self.ListViewFileList.setModel(self.StringModelFilesList)
        self.ListViewFileList.clicked.connect(self.FileSelected)

        if strSortVendorButton != "":
            self.buttonSortVendor = parent.findChild(QPushButton, strSortVendorButton)
            self.buttonSortVendor.clicked.connect(self.SortByVendorClicked)

        if strShowUncategorizedButton != "":
            self.buttonShowUncategorized = parent.findChild(QPushButton, strShowUncategorizedButton)
            self.buttonShowUncategorized.clicked.connect(self.ShowUncategorizedClicked)

        if strCompareBudgetButton != "":
            self.buttonCompareBudget = parent.findChild(QPushButton, strCompareBudgetButton)
            self.buttonCompareBudget.clicked.connect(self.CompareBudgetClicked)

        if strPlotMonthliesButton != "":
            self.buttonPlotMonthlies = parent.findChild(QPushButton, strPlotMonthliesButton)
            self.buttonPlotMonthlies.clicked.connect(self.PlotMonthliesClicked)

    def FolderButtonClicked(self):

        self.strFoldername = str(QFileDialog.getExistingDirectory(self.parent, "Select Directory", "C:/Users/danie/Development/StateAnalise/State"))
#        self.strFoldername = str(QFileDialog.getExistingDirectory(self.parent, "Select Directory", "."))
        self.vstrFileNames = [os.path.basename(x) for x in glob.glob(os.path.join(self.strFoldername, "*.csv"))]
        self.vtsMonthYear = list()
        for strFilename in self.vstrFileNames:
            match = re.search("\w{3}\d{4}", strFilename)
            if match is not None:
                self.vtsMonthYear.append(datetime.datetime.strptime(match[0], "%b%Y"))
                print(self.vtsMonthYear[-1])
            elif re.search("combined.csv", strFilename) is not None:
                self.vtsMonthYear.append(datetime.datetime(1970,1,1))

        self.vstrFileNames = [x for _,x in sorted(zip(self.vtsMonthYear,self.vstrFileNames))]

        self.StringModelFilesList.setStringList(self.vstrFileNames)

    def FileSelected(self, item):
        item = self.StringModelFilesList.itemData(item)[0]
        print("Item selected: ", item)
        self.strFullFilename = os.path.join(self.strFoldername, item)
        print(self.strFullFilename)

    def SortByVendorClicked(self):
        strFilenameToProcess = self.strFullFilename
        print("Sort By Vendor file: ", strFilenameToProcess)
        SortByVendor(strFilenameToProcess, True)

    def ShowUncategorizedClicked(self):
        strFilenameToProcess = self.strFullFilename
        print("Show uncategorized file: ", strFilenameToProcess)
        self.TableView = TableView(strFilenameToProcess)
        self.TableView.show()

    def CompareBudgetClicked(self):
        print("Compare button clicked", self.strFullFilename)
        CompareBudgetWithActuals(self.strFullFilename)

    def PlotMonthliesClicked(self):
        print("Plot Monthly in directory: ", self.strFoldername)
        PlotStackedBarFilename(self.strFoldername)

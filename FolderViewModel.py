# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QFileDialog, QPushButton, QListView
from PySide2.QtCore import QStringListModel
import glob
import os
import Debiet.convert_pdf2csv_DSTjek_pandas

class FolderViewModel:
    def __init__(self, parent, strFolderButtonName, strConvertToCSVButtonName,
                 strFileListViewName, strConvertToCSVScriptName, strConvertAllButtonName):
        self.parent = parent
        self.buttonOpenFolder = parent.findChild(QPushButton, strFolderButtonName)
        self.buttonOpenFolder.clicked.connect(self.FolderButtonClicked)

        self.ListViewFileList = parent.findChild(QListView, strFileListViewName)
        self.StringModelFilesList = QStringListModel([])
        self.ListViewFileList.setModel(self.StringModelFilesList)
        self.ListViewFileList.clicked.connect(self.FileSelected)

        self.buttonConvertToCSV = parent.findChild(QPushButton, strConvertToCSVButtonName)
        self.buttonConvertToCSV.clicked.connect(self.ConvertClicked)
        self.strConvertToCSVScriptName = strConvertToCSVScriptName

        self.buttonConvertAll = parent.findChild(QPushButton, strConvertAllButtonName)
        self.buttonConvertAll.clicked.connect(self.ConvertAllClicked)

    def FolderButtonClicked(self):
        self.strFoldername = str(QFileDialog.getExistingDirectory(self.parent, "Select Directory", "C:\\Users\\danie\\Development\\StateAnalise\\State"))
        self.vstrFileNames = [os.path.basename(x) for x in glob.glob(os.path.join(self.strFoldername, "*.pdf"))]
        self.StringModelFilesList.setStringList(self.vstrFileNames)

    def FileSelected(self, item):
        item = self.StringModelFilesList.itemData(item)[0]
        print("Item selected: ", item)
        self.strFullFilename = os.path.join(self.strFoldername, item)
        print(self.strFullFilename)

    def ConvertClicked(self):
        result=getattr(Debiet.convert_pdf2csv_DSTjek_pandas, "ConvertDebietToCSV")(self.strFullFilename)

    def ConvertAllClicked(self):
        files = glob.glob(os.path.join(self.strFoldername, "*.pdf"))
#        print("Files to convert:", files)
        for file in files:
            print("Processing: ", file)




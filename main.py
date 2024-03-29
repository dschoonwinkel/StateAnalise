# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from FolderViewModel import FolderViewModel
import matplotlib


class StateMainWindow(QWidget):
    def __init__(self):
        super(StateMainWindow, self).__init__()
        self.load_ui()
        self.setWindowTitle("State Analise " + self.GetVersionNumber())
        self.DebietFolderVM = FolderViewModel(self,
                                              "buttonDebietOpenFolder",
                                              "ListViewDebietFiles",
                                              "buttonDebietSortVendor",
                                              "buttonDebietShowUncategorized")
        self.KredietFolderVM = FolderViewModel(self,
                                            "buttonKredietOpenFolder",
                                            "ListViewKredietFiles",
                                            "buttonKredietSortVendor",
                                            "buttonKredietShowUncategorized")
        self.IreneFolderVM = FolderViewModel(self,
                                            "buttonIreneOpenFolder",
                                            "listViewIrene",
                                            "buttonIreneSortVendor",
                                            "buttonIreneShowUncategorized")
        self.AlleFolderVM = FolderViewModel(self,
                                            "buttonAlleTranOpenFolder",
                                            "ListViewAlleTranFiles",
                                            "buttonAlleSortVendor",
                                            "buttonAlleShowUncategorized",
                                            "buttonAlleCompareBudget",
                                            "buttonAllePlotMonthlies")

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def GetVersionNumber(self):
        f = open("version.txt", 'r')
        return f.read()

if __name__ == "__main__":
    matplotlib.use('Qt5Agg')
    matplotlib.pyplot.rcParams["figure.figsize"] = (12,6)
    app = QApplication([])
    widget = StateMainWindow()
    widget.show()
    sys.exit(app.exec_())

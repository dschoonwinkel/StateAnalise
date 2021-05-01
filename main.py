# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from FolderViewModel import FolderViewModel


class StateMainWindow(QWidget):
    def __init__(self):
        super(StateMainWindow, self).__init__()
        self.load_ui()
        self.DebietFolderVM = FolderViewModel(self,
                                              "buttonDebietOpenFolder",
                                              "ListViewDebietFiles",
                                              "buttonDebietSortVendor")
        self.KredietFolderVM = FolderViewModel(self,
                                            "buttonKredietOpenFolder",
                                            "ListViewKredietFiles",
                                            "buttonKredietSortVendor")
        self.IreneFolderVM = FolderViewModel(self,
                                            "buttonIreneOpenFolder",
                                            "listViewIrene",
                                            "buttonIreneSortVendor")
        self.AlleFolderVM = FolderViewModel(self,
                                            "buttonAlleTranOpenFolder",
                                            "ListViewAlleTranFiles",
                                            "buttonAlleSortVendor")

        self.buttonCompareBudget = self.findChild(QPushButton, "buttonCompareBudget")
        self.buttonCompareBudget.clicked.connect(self.CompareBudgetClicked)

        self.buttonBurnDown = self.findChild(QPushButton, "buttonBurnDown")
        self.buttonBurnDown.clicked.connect(self.BurnDownClicked)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def CompareBudgetClicked(self):
        print("Compare button clicked")

    def BurnDownClicked(self):
        print("Burn Down button clicked")

if __name__ == "__main__":
    app = QApplication([])
    widget = StateMainWindow()
    widget.show()
    sys.exit(app.exec_())

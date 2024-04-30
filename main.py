import sys
import os

from PySide6.QtCore import QThread, Qt, Slot
from PySide6.QtWidgets import QFileDialog, QApplication, QWidget
from UI.ui_form import Ui_Widget

import numpy as np

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_file_path = ""
        #Initialise the UI
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        #Find the stage settling results file
        self.ui.pushButtonFindInputFile.clicked.connect(self.openResultTXTFile)
    
    def openResultTXTFile(self):
        #Record the txt file location
        tupleFName = QFileDialog.getOpenFileName(self, "Select the settling results txt file", os.getcwd(), "All files (txt files (*.txt))")
        local_txt_file_path = tupleFName[0]
        #Report back
        self.ui.lineEditInputFileLocation.clear()
        self.ui.lineEditInputFileLocation.setText(local_txt_file_path)
        self.input_file_path = local_txt_file_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())
import sys
import os

from PySide6.QtCore import QThread, Qt, Slot
from PySide6.QtWidgets import QFileDialog, QApplication, QWidget
from UI.ui_form import Ui_Widget
from Processing.Processing import clsProcessing

import numpy as np

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_file_path = ""
        self.thresholdTimeMS = 0.0
        #Initialise the UI
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        #Find the stage settling results file
        self.ui.pushButtonFindInputFile.clicked.connect(self.openResultTXTFile)
        #Start processing
        self.ui.pushButtonShowResults.clicked.connect(self.startProcessing)
        #Start analysing
        self.ui.pushButtonStartAnalysing.clicked.connect(self.analyser)
    
    def openResultTXTFile(self):
        #Record the txt file location
        tupleFName = QFileDialog.getOpenFileName(self, "Select the settling results txt file", os.getcwd(), "All files (txt files (*.txt))")
        local_txt_file_path = tupleFName[0]
        #Report back
        self.ui.lineEditInputFileLocation.clear()
        self.ui.lineEditInputFileLocation.setText(local_txt_file_path)
        self.input_file_path = local_txt_file_path
    
    def startProcessing(self):
        #Start processing
        #Create a new object
        self.newProcessing = clsProcessing(self.input_file_path)

        #Create a QThread object
        self.thread = QThread()
        #Move the process to the thread
        self.newProcessing.moveToThread(self.thread)
        #Connect signals and slots
        self.thread.started.connect(self.newProcessing.producerInputFileToIndividualList)
        #Start the thread
        self.thread.start()
        self.newProcessing.finished.connect(self.thread.quit)
        self.newProcessing.finished.connect(self.newProcessing.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        #Update the plot
        self.newProcessing.signalUpdatePlotNormalSmallX.connect(self.qtSlot_UpdatePlot)

        #Set up the UI during the processing
        self.ui.pushButtonShowResults.setEnabled(False)
        self.ui.pushButtonShowResults.setText("Under processing!")
        self.thread.finished.connect(
            lambda: self.ui.pushButtonShowResults.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.ui.pushButtonShowResults.setText("Show results!")
        )

    def analyser(self):
        #Get the threshold time ms
        self.thresholdTimeMS = float(self.ui.lineEditTimeForAnalysing.text())*1000
        #Start analysing
        #Create a new object
        self.newProcessingForAnalyser = clsProcessing(self.input_file_path, self.thresholdTimeMS)
        #Create a QThread object
        self.threadForAnalyser = QThread()
        #Move the process to the thread
        self.newProcessingForAnalyser.moveToThread(self.threadForAnalyser)
        #Connect signals and slots
        self.threadForAnalyser.started.connect(self.newProcessingForAnalyser.producerAnalysingResult)

        self.newProcessingForAnalyser.finished.connect(self.threadForAnalyser.quit)
        self.newProcessingForAnalyser.finished.connect(self.newProcessingForAnalyser.deleteLater)
        self.threadForAnalyser.finished.connect(self.threadForAnalyser.deleteLater)

        self.threadForAnalyser.finished.connect(
            lambda: self.ui.pushButtonStartAnalysing.setEnabled(True)
        )
        self.threadForAnalyser.finished.connect(
            lambda: self.ui.pushButtonStartAnalysing.setText("Start analysing!")
        )

        #Update the analysis result
        self.newProcessingForAnalyser.signalUpdateAnalysisResultNormalSmallX.connect(self.qtSlot_UpdateAnalysisResult)
        #Start the thread
        self.threadForAnalyser.start()
        #Set UI during analysis
        self.ui.pushButtonStartAnalysing.setEnabled(False)
        self.ui.pushButtonStartAnalysing.setText("Analysing!")

        
    
    @Slot()
    def qtSlot_UpdatePlot(self):
        self.ui.gvSmallNormalX.clear()
        self.ui.gvSmallNormalX.setTitle(
            "X small"
        )
        self.ui.gvSmallNormalX.plot(self.newProcessing.npArrayNormalSmallXFinalPositionX, 
                                    self.newProcessing.npArrayNormalSmallXSettingTimems, 
                                    pen=None, 
                                    symbol='o')
        
    @Slot()
    def qtSlot_UpdateAnalysisResult(self):
        #Get the number of movements
        intTotalNumbersOfMovements = len(self.newProcessingForAnalyser.listNormallSmallXLongSettling)
        #Clear the previous messages
        self.ui.textEditNormalX.clear()
        #Udate
        self.ui.textEditNormalX.insertPlainText("There are {} movements.\n".format(intTotalNumbersOfMovements))
        for i in range(intTotalNumbersOfMovements):
            self.ui.textEditNormalX.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditNormalX.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listNormallSmallXLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listNormallSmallXLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listNormallSmallXLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listNormallSmallXLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listNormallSmallXLongSettling[i][4]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())
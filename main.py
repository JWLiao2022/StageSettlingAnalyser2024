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

        #Initialise the plot
        self.plotInitialiser()
    
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
        self.newProcessing.signalUpdatePlot.connect(self.qtSlot_UpdatePlot)

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
        self.newProcessingForAnalyser.signalUpdateAnalysisResult.connect(self.qtSlot_UpdateAnalysisResult)
        #Start the thread
        self.threadForAnalyser.start()
        #Set UI during analysis
        self.ui.pushButtonStartAnalysing.setEnabled(False)
        self.ui.pushButtonStartAnalysing.setText("Analysing!")

        
    
    @Slot()
    def qtSlot_UpdatePlot(self):
        #Normal Small X
        #Set up the plot
        self.ui.gvSmallNormalX.clear()
        
        self.ui.gvSmallNormalX.plot(self.newProcessing.npArrayNormalSmallXFinalPositionX, 
                                    self.newProcessing.npArrayNormalSmallXSettingTimems, 
                                    pen=None, 
                                    symbol='o')
        #Normal Big X
        self.ui.gvBigNormalX.clear()
        self.ui.gvBigNormalX.setTitle(
            "X Big"
        )
        self.ui.gvBigNormalX.plot(self.newProcessing.npArrayNormalBigXFinalPositionX, 
                                    self.newProcessing.npArrayNormalBigXSettingTimems, 
                                    pen=None, 
                                    symbol='o')
        #Normal Small Y
        self.ui.gvSmallNormalY.clear()
        self.ui.gvSmallNormalY.setTitle(
            "Y small"
        )
        self.ui.gvSmallNormalY.plot(self.newProcessing.npArrayNormalSmallYFinalPositionY, 
                                    self.newProcessing.npArrayNormalSmallYSettingTimems, 
                                    pen=None, 
                                    symbol='o')
        #Normal Big Y
        self.ui.gvBigNormalY.clear()
        self.ui.gvBigNormalY.setTitle(
            "Y Big"
        )
        self.ui.gvBigNormalY.plot(self.newProcessing.npArrayNormalBigYFinalPositionY, 
                                    self.newProcessing.npArrayNormalBigYSettingTimems, 
                                    pen=None, 
                                    symbol='o')
        
    @Slot()
    def qtSlot_UpdateAnalysisResult(self):
        #Get the number of movements
        intTotalNumbersOfMovementsNormalSmallX = len(self.newProcessingForAnalyser.listNormalSmallXLongSettling)
        intTotalNumbersOfMovementsNormalBigX = len(self.newProcessingForAnalyser.listNormalBigXLongSettling)
        intTotalNumbersOfMovementsNormalSmallY = len(self.newProcessingForAnalyser.listNormalSmallYLongSettling)
        intTotalNumbersOfMovementsNormalBigY = len(self.newProcessingForAnalyser.listNormalBigYLongSettling)
        #Clear the previous messages
        self.ui.textEditNormalSmallX.clear()
        self.ui.textEditNormalBigX.clear()
        self.ui.textEditNormalSmallY.clear()
        self.ui.textEditNormalBigY.clear()
        #Udate
        #Normal Small X
        self.ui.textEditNormalSmallX.insertPlainText("There are {} small movements in X.\n".format(intTotalNumbersOfMovementsNormalSmallX))
        for i in range(intTotalNumbersOfMovementsNormalSmallX):
            self.ui.textEditNormalSmallX.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditNormalSmallX.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listNormalSmallXLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listNormalSmallXLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listNormalSmallXLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listNormalSmallXLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listNormalSmallXLongSettling[i][4]))
        #Normal Big X
        self.ui.textEditNormalBigX.insertPlainText("There are {} big movements in X.\n".format(intTotalNumbersOfMovementsNormalBigX))
        for i in range(intTotalNumbersOfMovementsNormalBigX):
            self.ui.textEditNormalBigX.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditNormalBigX.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listNormalBigXLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listNormalBigXLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listNormalBigXLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listNormalBigXLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listNormalBigXLongSettling[i][4]))
        #Normal Small Y
        self.ui.textEditNormalSmallY.insertPlainText("There are {} small movements in Y.\n".format(intTotalNumbersOfMovementsNormalSmallY))
        for i in range(intTotalNumbersOfMovementsNormalSmallY):
            self.ui.textEditNormalSmallY.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditNormalSmallY.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listNormalSmallYLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listNormalSmallYLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listNormalSmallYLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listNormalSmallYLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listNormalSmallYLongSettling[i][4]))
        #Normal Big Y
        self.ui.textEditNormalBigY.insertPlainText("There are {} big movements in Y.\n".format(intTotalNumbersOfMovementsNormalBigY))
        for i in range(intTotalNumbersOfMovementsNormalBigY):
            self.ui.textEditNormalBigY.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditNormalBigY.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listNormalBigYLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listNormalBigYLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listNormalBigYLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listNormalBigYLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listNormalBigYLongSettling[i][4]))
    def plotInitialiser(self):
        #Normal X small
        self.ui.gvSmallNormalX.setTitle(
            "X small"
        )
        self.ui.gvSmallNormalX.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvSmallNormalX.setLabel(axis='bottom', text='Final X position (mm)')
        self.ui.gvSmallNormalX.showAxis('right')
        self.ui.gvSmallNormalX.showAxis('top')
        self.ui.gvSmallNormalX.showGrid(True, True)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())
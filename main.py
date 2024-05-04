import sys
import os

from PySide6.QtCore import QThread, Qt, Slot
from PySide6.QtWidgets import QFileDialog, QApplication, QWidget
from UI.ui_form import Ui_Widget
from Processing.Processing import clsProcessing

import numpy as np
import statistics

import pyqtgraph as pg
import pyqtgraph.exporters

from pathlib import Path

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_file_path = ""
        self.input_folder_path = ""
        self.output_file_path = ""
        self.thresholdTimeMS = 0.0
        #Initialise the UI
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        #Disable the plot, save, and analyse button before user input a file
        self.ui.pushButtonShowResults.setEnabled(False)
        self.ui.pushButtonSavePlots.setEnabled(False)
        self.ui.pushButtonStartAnalysing.setEnabled(False)
        #Find the stage settling results file
        self.ui.pushButtonFindInputFile.clicked.connect(self.openResultTXTFile)
        #Start processing
        self.ui.pushButtonShowResults.clicked.connect(self.startProcessing)
        #Start analysing
        self.ui.pushButtonStartAnalysing.clicked.connect(self.analyser)
        #Save results
        self.ui.pushButtonSavePlots.clicked.connect(self.saveResultPlotFile)

        #Initialise the plot
        self.plotInitialiser()

        #Set the tab 0 to appear first
        self.ui.tabWidget.setCurrentIndex(0)
    
    def openResultTXTFile(self):
        #Record the txt file location
        tupleFName = QFileDialog.getOpenFileName(self, "Select the settling results txt file", os.getcwd(), "All files (txt files (*.txt))")
        local_txt_file_path = tupleFName[0]
        #Report back
        self.ui.lineEditInputFileLocation.clear()
        self.ui.lineEditInputFileLocation.setText(local_txt_file_path)
        self.input_file_path = local_txt_file_path
        self.input_folder_path = os.path.dirname(os.path.abspath(local_txt_file_path))
        #Enable the plot button
        if (self.input_file_path != ""):
            self.ui.pushButtonShowResults.setEnabled(True)
    
    def saveResultPlotFile(self):
        #Record the output file name
        tupleSaveFName = QFileDialog.getSaveFileName(self, "Input the system name", self.input_folder_path, "Image files (*.png)")
        #Report back
        self.output_file_path = tupleSaveFName[0]
        output_folder_path = os.path.dirname(os.path.abspath(self.output_file_path))
        #Get the user input file name
        systemName = Path(self.output_file_path).stem
        #Save images
        #Normal Small X
        #Create the full file path
        fileName = systemName + "-NormalSmallX.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvSmallNormalX.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Normal Big X
        fileName = systemName + "-NormalBigX.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvBigNormalX.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Normal Small Y
        fileName = systemName + "-NormalSmallY.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvSmallNormalY.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Normal Big Y
        fileName = systemName + "-NormalBigY.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvBigNormalY.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Fastest Small X
        #Create the full file path
        fileName = systemName + "-FastestSmallX.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvSmallFastestX.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Fastest Big X
        #Create the full file path
        fileName = systemName + "-FastestBigX.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvBigFastestX.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Fastest Small Y
        #Create the full file path
        fileName = systemName + "-FastestSmallY.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvSmallFastestY.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Fastest Big Y
        #Create the full file path
        fileName = systemName + "-FastestBigY.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvBigFastestY.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Normal Z and X
        #Create the full file path
        fileName = systemName + "-NormalZX.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvNormalZX.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Normal Z and Y
        fileName = systemName + "-NormalZY.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvNormalZY.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Fastest Z and X
        fileName = systemName + "-FastestZX.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvFastestZX.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        #Fastest Z and Y
        fileName = systemName + "-FastestZY.png"
        final_output_file_path = os.path.join(output_folder_path, fileName)
        #Export the plot
        exporter = pyqtgraph.exporters.ImageExporter(self.ui.gvFastestZY.plotItem)
        exporter.parameters()['width'] = 1020
        exporter.export(final_output_file_path)
        
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
        self.thread.finished.connect(
            lambda: self.ui.pushButtonSavePlots.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.ui.pushButtonStartAnalysing.setEnabled(True)
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
        #Set up the plot
        #Normal Small X
        self.ui.gvSmallNormalX.clear()
        intTotalMovements = len(self.newProcessing.listNormalSmallXFinalPositionX)
        floatMeanSettleTime = statistics.fmean(self.newProcessing.listNormalSmallXSettingTimems)
        floatMaxSettleTime = max(self.newProcessing.listNormalSmallXSettingTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listNormalSmallXTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listNormalSmallXTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean settle (ms): %.2f \n" %(floatMeanSettleTime) +
                              "Max settle (ms): %.2f \n" %(floatMaxSettleTime) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvSmallNormalX.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvSmallNormalX.plot(self.newProcessing.listNormalSmallXFinalPositionX, 
                                    self.newProcessing.listNormalSmallXSettingTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Normal Big X
        self.ui.gvBigNormalX.clear()
        intTotalMovements = len(self.newProcessing.listNormalBigXFinalPositionX)
        floatMeanSettleTime = statistics.fmean(self.newProcessing.listNormalBigXSettingTimems)
        floatMaxSettleTime = max(self.newProcessing.listNormalBigXSettingTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listNormalBigXTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listNormalBigXTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean settle (ms): %.2f \n" %(floatMeanSettleTime) +
                              "Max settle (ms): %.2f \n" %(floatMaxSettleTime) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvBigNormalX.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvBigNormalX.plot(self.newProcessing.listNormalBigXFinalPositionX, 
                                    self.newProcessing.listNormalBigXSettingTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Normal Small Y
        self.ui.gvSmallNormalY.clear()
        intTotalMovements = len(self.newProcessing.listNormalSmallYFinalPositionY)
        floatMeanSettleTime = statistics.fmean(self.newProcessing.listNormalSmallYSettingTimems)
        floatMaxSettleTime = max(self.newProcessing.listNormalSmallYSettingTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listNormalSmallYTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listNormalSmallYTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean settle (ms): %.2f \n" %(floatMeanSettleTime) +
                              "Max settle (ms): %.2f \n" %(floatMaxSettleTime) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvSmallNormalY.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvSmallNormalY.plot(self.newProcessing.listNormalSmallYFinalPositionY, 
                                    self.newProcessing.listNormalSmallYSettingTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Normal Big Y
        self.ui.gvBigNormalY.clear()
        intTotalMovements = len(self.newProcessing.listNormalBigYFinalPositionY)
        floatMeanSettleTime = statistics.fmean(self.newProcessing.listNormalBigYSettingTimems)
        floatMaxSettleTime = max(self.newProcessing.listNormalBigYSettingTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listNormalBigYTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listNormalBigYTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean settle (ms): %.2f \n" %(floatMeanSettleTime) +
                              "Max settle (ms): %.2f \n" %(floatMaxSettleTime) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvBigNormalY.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvBigNormalY.plot(self.newProcessing.listNormalBigYFinalPositionY, 
                                    self.newProcessing.listNormalBigYSettingTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Fastest Small X
        self.ui.gvSmallFastestX.clear()
        intTotalMovements = len(self.newProcessing.listFastestSmallXFinalPositionX)
        floatMeanSettleTime = statistics.fmean(self.newProcessing.listFastestSmallXSettingTimems)
        floatMaxSettleTime = max(self.newProcessing.listFastestSmallXSettingTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listFastestSmallXTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listFastestSmallXTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean settle (ms): %.2f \n" %(floatMeanSettleTime) +
                              "Max settle (ms): %.2f \n" %(floatMaxSettleTime) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvSmallFastestX.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvSmallFastestX.plot(self.newProcessing.listFastestSmallXFinalPositionX, 
                                    self.newProcessing.listFastestSmallXSettingTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Fastest Big X
        self.ui.gvBigFastestX.clear()
        intTotalMovements = len(self.newProcessing.listFastestBigXFinalPositionX)
        floatMeanSettleTime = statistics.fmean(self.newProcessing.listFastestBigXSettingTimems)
        floatMaxSettleTime = max(self.newProcessing.listFastestBigXSettingTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listFastestBigXTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listFastestBigXTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean settle (ms): %.2f \n" %(floatMeanSettleTime) +
                              "Max settle (ms): %.2f \n" %(floatMaxSettleTime) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvBigFastestX.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvBigFastestX.plot(self.newProcessing.listFastestBigXFinalPositionX, 
                                    self.newProcessing.listFastestBigXSettingTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Fastest Small Y
        self.ui.gvSmallFastestY.clear()
        intTotalMovements = len(self.newProcessing.listFastestSmallYFinalPositionY)
        floatMeanSettleTime = statistics.fmean(self.newProcessing.listFastestSmallYSettingTimems)
        floatMaxSettleTime = max(self.newProcessing.listFastestSmallYSettingTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listFastestSmallYTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listFastestSmallYTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean settle (ms): %.2f \n" %(floatMeanSettleTime) +
                              "Max settle (ms): %.2f \n" %(floatMaxSettleTime) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvSmallFastestY.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvSmallFastestY.plot(self.newProcessing.listFastestSmallYFinalPositionY, 
                                    self.newProcessing.listFastestSmallYSettingTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Fastest Big Y
        self.ui.gvBigFastestY.clear()
        intTotalMovements = len(self.newProcessing.listFastestBigYFinalPositionY)
        floatMeanSettleTime = statistics.fmean(self.newProcessing.listFastestBigYSettingTimems)
        floatMaxSettleTime = max(self.newProcessing.listFastestBigYSettingTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listFastestBigYTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listFastestBigYTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean settle (ms): %.2f \n" %(floatMeanSettleTime) +
                              "Max settle (ms): %.2f \n" %(floatMaxSettleTime) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvBigFastestY.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvBigFastestY.plot(self.newProcessing.listFastestBigYFinalPositionY, 
                                    self.newProcessing.listFastestBigYSettingTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Normal Z and X
        self.ui.gvNormalZX.clear()
        intTotalMovements = len(self.newProcessing.listNormalZTotalTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listNormalZTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listNormalZTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvNormalZX.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvNormalZX.plot(self.newProcessing.listNormalZFinalPositionX, 
                                    self.newProcessing.listNormalZTotalTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Normal Z and Y
        self.ui.gvNormalZY.clear()
        intTotalMovements = len(self.newProcessing.listNormalZTotalTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listNormalZTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listNormalZTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvNormalZY.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvNormalZY.plot(self.newProcessing.listNormalZFinalPositionY, 
                                    self.newProcessing.listNormalZTotalTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Fastest Z and X
        self.ui.gvFastestZX.clear()
        intTotalMovements = len(self.newProcessing.listFastestZTotalTimems)
        print(intTotalMovements)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listFastestZTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listFastestZTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvFastestZX.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvFastestZX.plot(self.newProcessing.listFastestZFinalPositionX, 
                                    self.newProcessing.listFastestZTotalTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        #Fastest Z and Y
        self.ui.gvFastestZY.clear()
        intTotalMovements = len(self.newProcessing.listFastestZTotalTimems)
        floatMeanMoveTime = statistics.fmean(self.newProcessing.listFastestZTotalTimems)
        floatMaxMoveTime = max(self.newProcessing.listFastestZTotalTimems)
        title = ("Total moves: {} \n".format(intTotalMovements) +
                              "Mean move (ms): %.2f \n" %(floatMeanMoveTime) + 
                              "Max move (ms): %.2f" %(floatMaxMoveTime))
        self.text = pg.TextItem(title, color=(0, 0, 0), fill=(255, 255, 255))
        self.ui.gvFastestZY.addItem(self.text)
        self.text.setPos(25,3580)
        self.ui.gvFastestZY.plot(self.newProcessing.listFastestZFinalPositionY, 
                                    self.newProcessing.listFastestZTotalTimems, 
                                    pen=None, 
                                    symbol='o',
                                    symbolSize=8)
        
    @Slot()
    def qtSlot_UpdateAnalysisResult(self):
        #Get the number of movements
        intTotalNumbersOfMovementsNormalSmallX = len(self.newProcessingForAnalyser.listNormalSmallXLongSettling)
        intTotalNumbersOfMovementsNormalBigX = len(self.newProcessingForAnalyser.listNormalBigXLongSettling)
        intTotalNumbersOfMovementsNormalSmallY = len(self.newProcessingForAnalyser.listNormalSmallYLongSettling)
        intTotalNumbersOfMovementsNormalBigY = len(self.newProcessingForAnalyser.listNormalBigYLongSettling)
        intTotalNumbersOfMovementsFastestSmallX = len(self.newProcessingForAnalyser.listFastestSmallXLongSettling)
        intTotalNumbersOfMovementsFastestBigX = len(self.newProcessingForAnalyser.listFastestBigXLongSettling)
        intTotalNumbersOfMovementsFastestSmallY = len(self.newProcessingForAnalyser.listFastestSmallYLongSettling)
        intTotalNumbersOfMovementsFastestBigY = len(self.newProcessingForAnalyser.listFastestBigYLongSettling)
        intTotalNumbersOfMovementsNormalZ = len(self.newProcessingForAnalyser.listNormalZLongTotal)
        intTotalNumbersOfMovementsFastestZ = len(self.newProcessingForAnalyser.listFastestZLongTotal)
        #Clear the previous messages
        self.ui.textEditNormalSmallX.clear()
        self.ui.textEditNormalBigX.clear()
        self.ui.textEditNormalSmallY.clear()
        self.ui.textEditNormalBigY.clear()
        self.ui.textEditFastestSmallX.clear()
        self.ui.textEditFastestBigX.clear()
        self.ui.textEditFastestSmallY.clear()
        self.ui.textEditFastestBigY.clear()
        self.ui.textEditNormalZ.clear()
        self.ui.textEditFastestZ.clear()
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
        #Fastest Small X
        self.ui.textEditFastestSmallX.insertPlainText("There are {} small movements in X.\n".format(intTotalNumbersOfMovementsFastestSmallX))
        for i in range(intTotalNumbersOfMovementsFastestSmallX):
            self.ui.textEditFastestSmallX.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditFastestSmallX.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listFastestSmallXLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listFastestSmallXLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listFastestSmallXLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listFastestSmallXLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listFastestSmallXLongSettling[i][4]))
        #Fastest Big X
        self.ui.textEditFastestBigX.insertPlainText("There are {} big movements in X.\n".format(intTotalNumbersOfMovementsFastestBigX))
        for i in range(intTotalNumbersOfMovementsFastestBigX):
            self.ui.textEditFastestBigX.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditFastestBigX.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listFastestBigXLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listFastestBigXLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listFastestBigXLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listFastestBigXLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listFastestBigXLongSettling[i][4]))
        #Fastest Small Y
        self.ui.textEditFastestSmallY.insertPlainText("There are {} small movements in Y.\n".format(intTotalNumbersOfMovementsFastestSmallY))
        for i in range(intTotalNumbersOfMovementsFastestSmallY):
            self.ui.textEditFastestSmallY.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditFastestSmallY.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listFastestSmallYLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listFastestSmallYLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listFastestSmallYLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listFastestSmallYLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listFastestSmallYLongSettling[i][4]))
        #Fastest Big Y
        self.ui.textEditFastestBigY.insertPlainText("There are {} big movements in Y.\n".format(intTotalNumbersOfMovementsFastestBigY))
        for i in range(intTotalNumbersOfMovementsFastestBigY):
            self.ui.textEditFastestBigY.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditFastestBigY.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listFastestBigYLongSettling[i][0],
                                                                                                                  self.newProcessingForAnalyser.listFastestBigYLongSettling[i][1],
                                                                                                                  self.newProcessingForAnalyser.listFastestBigYLongSettling[i][2],
                                                                                                                  self.newProcessingForAnalyser.listFastestBigYLongSettling[i][3],
                                                                                                                  self.newProcessingForAnalyser.listFastestBigYLongSettling[i][4]))
        #Normal Z
        self.ui.textEditNormalZ.insertPlainText("There are {}  movements in Z.\n".format(intTotalNumbersOfMovementsNormalZ))
        for i in range(intTotalNumbersOfMovementsNormalZ):
            self.ui.textEditNormalZ.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditNormalZ.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listNormalZLongTotal[i][0],
                                                                                                                  self.newProcessingForAnalyser.listNormalZLongTotal[i][1],
                                                                                                                  self.newProcessingForAnalyser.listNormalZLongTotal[i][2],
                                                                                                                  self.newProcessingForAnalyser.listNormalZLongTotal[i][3],
                                                                                                                  self.newProcessingForAnalyser.listNormalZLongTotal[i][4]))
        #Fastest Z
        self.ui.textEditFastestZ.insertPlainText("There are {}  movements in Z.\n".format(intTotalNumbersOfMovementsFastestZ))
        for i in range(intTotalNumbersOfMovementsFastestZ):
            self.ui.textEditFastestZ.insertPlainText("Movement {}:\n".format(i))
            self.ui.textEditFastestZ.insertPlainText("From \n ({} mm, {} mm) \n to \n({} mm, {} mm) \n it took {} ms.\n\n".format(self.newProcessingForAnalyser.listFastestZLongTotal[i][0],
                                                                                                                  self.newProcessingForAnalyser.listFastestZLongTotal[i][1],
                                                                                                                  self.newProcessingForAnalyser.listFastestZLongTotal[i][2],
                                                                                                                  self.newProcessingForAnalyser.listFastestZLongTotal[i][3],
                                                                                                                  self.newProcessingForAnalyser.listFastestZLongTotal[i][4]))

    def plotInitialiser(self):
        #Normal Small X
        self.ui.gvSmallNormalX.setTitle("Normal Small X movements")
        self.ui.gvSmallNormalX.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvSmallNormalX.setLabel(axis='bottom', text='Final X position (mm)')
        self.ui.gvSmallNormalX.showAxis('right')
        self.ui.gvSmallNormalX.showAxis('top')
        self.ui.gvSmallNormalX.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvSmallNormalX.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvSmallNormalX.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvSmallNormalX.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvSmallNormalX.showGrid(True, True)
        self.ui.gvSmallNormalX.setXRange(-99.5, 99.5)
        self.ui.gvSmallNormalX.setYRange(-2, 3480)
        #Normal Big X
        self.ui.gvBigNormalX.setTitle("Normal Big X movements")
        self.ui.gvBigNormalX.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvBigNormalX.setLabel(axis='bottom', text='Final X position (mm)')
        self.ui.gvBigNormalX.showAxis('right')
        self.ui.gvBigNormalX.showAxis('top')
        self.ui.gvBigNormalX.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvBigNormalX.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvBigNormalX.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvBigNormalX.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvBigNormalX.showGrid(True, True)
        self.ui.gvBigNormalX.setXRange(-99.5, 99.5)
        self.ui.gvBigNormalX.setYRange(-2, 3480)
        #Normal Small Y
        self.ui.gvSmallNormalY.setTitle("Normal Small Y movements")
        self.ui.gvSmallNormalY.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvSmallNormalY.setLabel(axis='bottom', text='Final Y position (mm)')
        self.ui.gvSmallNormalY.showAxis('right')
        self.ui.gvSmallNormalY.showAxis('top')
        self.ui.gvSmallNormalY.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvSmallNormalY.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvSmallNormalY.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvSmallNormalY.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvSmallNormalY.showGrid(True, True)
        self.ui.gvSmallNormalY.setXRange(-99.5, 99.5)
        self.ui.gvSmallNormalY.setYRange(-2, 3480)
        #Normal Big Y
        self.ui.gvBigNormalY.setTitle("Normal Big Y movements")
        self.ui.gvBigNormalY.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvBigNormalY.setLabel(axis='bottom', text='Final Y position (mm)')
        self.ui.gvBigNormalY.showAxis('right')
        self.ui.gvBigNormalY.showAxis('top')
        self.ui.gvBigNormalY.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvBigNormalY.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvBigNormalY.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvBigNormalY.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvBigNormalY.showGrid(True, True)
        self.ui.gvBigNormalY.setXRange(-99.5, 99.5)
        self.ui.gvBigNormalY.setYRange(-2, 3480)
        #Fastest Small X
        self.ui.gvSmallFastestX.setTitle("Fastest Small X movements")
        self.ui.gvSmallFastestX.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvSmallFastestX.setLabel(axis='bottom', text='Final X position (mm)')
        self.ui.gvSmallFastestX.showAxis('right')
        self.ui.gvSmallFastestX.showAxis('top')
        self.ui.gvSmallFastestX.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvSmallFastestX.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvSmallFastestX.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvSmallFastestX.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvSmallFastestX.showGrid(True, True)
        self.ui.gvSmallFastestX.setXRange(-99.5, 99.5)
        self.ui.gvSmallFastestX.setYRange(-2, 3480)
        #Fastest Big X
        self.ui.gvBigFastestX.setTitle("Fastest Big X movements")
        self.ui.gvBigFastestX.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvBigFastestX.setLabel(axis='bottom', text='Final X position (mm)')
        self.ui.gvBigFastestX.showAxis('right')
        self.ui.gvBigFastestX.showAxis('top')
        self.ui.gvBigFastestX.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvBigFastestX.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvBigFastestX.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvBigFastestX.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvBigFastestX.showGrid(True, True)
        self.ui.gvBigFastestX.setXRange(-99.5, 99.5)
        self.ui.gvBigFastestX.setYRange(-2, 3480)
        #Fastest Small Y
        self.ui.gvSmallFastestY.setTitle("Fastest Small Y movements")
        self.ui.gvSmallFastestY.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvSmallFastestY.setLabel(axis='bottom', text='Final Y position (mm)')
        self.ui.gvSmallFastestY.showAxis('right')
        self.ui.gvSmallFastestY.showAxis('top')
        self.ui.gvSmallFastestY.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvSmallFastestY.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvSmallFastestY.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvSmallFastestY.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvSmallFastestY.showGrid(True, True)
        self.ui.gvSmallFastestY.setXRange(-99.5, 99.5)
        self.ui.gvSmallFastestY.setYRange(-2, 3480)
        #Fastest Big Y
        self.ui.gvBigFastestY.setTitle("Fastest Big Y movements")
        self.ui.gvBigFastestY.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvBigFastestY.setLabel(axis='bottom', text='Final Y position (mm)')
        self.ui.gvBigFastestY.showAxis('right')
        self.ui.gvBigFastestY.showAxis('top')
        self.ui.gvBigFastestY.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvBigFastestY.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvBigFastestY.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvBigFastestY.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvBigFastestY.showGrid(True, True)
        self.ui.gvBigFastestY.setXRange(-99.5, 99.5)
        self.ui.gvBigFastestY.setYRange(-2, 3480)
        #Normal Z and X
        self.ui.gvNormalZX.setTitle("Normal Z movements with final X positions")
        self.ui.gvNormalZX.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvNormalZX.setLabel(axis='bottom', text='Final X position (mm)')
        self.ui.gvNormalZX.showAxis('right')
        self.ui.gvNormalZX.showAxis('top')
        self.ui.gvNormalZX.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvNormalZX.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvNormalZX.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvNormalZX.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvNormalZX.showGrid(True, True)
        self.ui.gvNormalZX.setXRange(-99.5, 99.5)
        self.ui.gvNormalZX.setYRange(-2, 3480)
        #Normal Z and Y
        self.ui.gvNormalZY.setTitle("Normal Z movements with final Y positions")
        self.ui.gvNormalZY.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvNormalZY.setLabel(axis='bottom', text='Final Y position (mm)')
        self.ui.gvNormalZY.showAxis('right')
        self.ui.gvNormalZY.showAxis('top')
        self.ui.gvNormalZY.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvNormalZY.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvNormalZY.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvNormalZY.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvNormalZY.showGrid(True, True)
        self.ui.gvNormalZY.setXRange(-99.5, 99.5)
        self.ui.gvNormalZY.setYRange(-2, 3480)
        #Fastest Z and X
        self.ui.gvFastestZX.setTitle("Fastest Z movements with final X positions")
        self.ui.gvFastestZX.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvFastestZX.setLabel(axis='bottom', text='Final X position (mm)')
        self.ui.gvFastestZX.showAxis('right')
        self.ui.gvFastestZX.showAxis('top')
        self.ui.gvFastestZX.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvFastestZX.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvFastestZX.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvFastestZX.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvFastestZX.showGrid(True, True)
        self.ui.gvFastestZX.setXRange(-99.5, 99.5)
        self.ui.gvFastestZX.setYRange(-2, 3480)
        #Fastest Z and Y
        self.ui.gvFastestZY.setTitle("Fastest Z movements with final Y positions")
        self.ui.gvFastestZY.setLabel(axis='left', text='Settling time (ms)')
        self.ui.gvFastestZY.setLabel(axis='bottom', text='Final Y position (mm)')
        self.ui.gvFastestZY.showAxis('right')
        self.ui.gvFastestZY.showAxis('top')
        self.ui.gvFastestZY.getAxis('right').enableAutoSIPrefix(enable=False)
        self.ui.gvFastestZY.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.ui.gvFastestZY.getAxis('top').enableAutoSIPrefix(enable=False)
        self.ui.gvFastestZY.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.ui.gvFastestZY.showGrid(True, True)
        self.ui.gvFastestZY.setXRange(-99.5, 99.5)
        self.ui.gvFastestZY.setYRange(-2, 3480)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())
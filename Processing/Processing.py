import sys
import os

from PySide6.QtCore import QThread, Signal
import numpy as np
import time

class clsProcessing(QThread):
    finished = Signal()
    signalUpdatePlotNormalSmallX = Signal()
    signalUpdateAnalysisResultNormalSmallX = Signal()

    def __init__(self, input_file_path, thresholdTimeMS = 0.0, parent=None):
        super(clsProcessing, self).__init__(parent)
        #Copy the user input information over to the local variables
        self.input_file_path = input_file_path
        #Initialise a list for the results of Normal Small X
        self.listNormalSmallX = []
        self.listNormalSmallXFinalPositionX = []
        self.listNormalSmallXSettingTimems = []
        self.npArrayNormalSmallXFinalPositionX = np.zeros(1, dtype=np.float16)
        self.npArrayNormalSmallXSettingTimems = np.zeros(1, dtype=np.float16)

        self.listNormallSmallXLongSettling = []
        self.listNormalSmallYLongSettling = []

        self.thresholdTimems = thresholdTimeMS

    def producerInputFileToIndividualList(self):
        #Open the input file and sort them into corresponding list
        data = [i.strip('\n').split('\t') for i in open(self.input_file_path)]        
        for line in data:
            if (line[-1] == "1") and (line[-2] == "False") and (line[-3] == "True"):
                self.listNormalSmallX.append(line[:-3])
        
        #For plotting
        for line in self.listNormalSmallX:
            self.listNormalSmallXFinalPositionX.append(line[0])
            self.listNormalSmallXSettingTimems.append(line[-2])
        
        #Have the list back the np array
        self.npArrayNormalSmallXFinalPositionX = np.array(self.listNormalSmallXFinalPositionX, dtype=np.float32)
        self.npArrayNormalSmallXSettingTimems = np.array(self.listNormalSmallXSettingTimems, dtype=np.float32)

        #Set ready for plotting signal
        self.signalUpdatePlotNormalSmallX.emit()

        #Set the finish signal
        self.finished.emit()
    
    def producerAnalysingResult(self):
        #Open the input file and sort them into a list
        data = [i.strip('\n').split('\t') for i in open(self.input_file_path)]
        #Start analysing the data
        for count, line in enumerate(data):
            if count == 1:
                #The first movement is always normal small y move from (0mm, 0mm) position
                #Check the setting time
                if np.float16(line[-5]) >= self.thresholdTimems:
                    self.listNormalSmallYLongSettling.append(['0', '0', line[0], line[1], line[-5]])
            else:
                #Locate the normal small x move
                if (line[-1] == "1") and (line[-2] == "False") and (line[-3] == "True"):
                    #Check the settling time
                    if np.float16(line[-5]) >= self.thresholdTimems:
                        self.listNormallSmallXLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
        
        print(self.listNormallSmallXLongSettling)

        #Set the signal for updating the analysing result
        self.signalUpdateAnalysisResultNormalSmallX.emit()

        #Set the finish signal
        self.finished.emit()


        
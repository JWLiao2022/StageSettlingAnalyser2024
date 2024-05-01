import sys
import os

from PySide6.QtCore import QThread, Signal
import numpy as np
import time

class clsProcessing(QThread):
    finished = Signal()
    signalUpdatePlot = Signal()
    signalUpdateAnalysisResult = Signal()

    def __init__(self, input_file_path, thresholdTimeMS = 0.0, parent=None):
        super(clsProcessing, self).__init__(parent)
        #Copy the user input information over to the local variables
        self.input_file_path = input_file_path
        #Initialise two lists and two np arrays for each movement
        #Normal Small X
        self.listNormalSmallXFinalPositionX = []
        self.listNormalSmallXSettingTimems = []
        self.npArrayNormalSmallXFinalPositionX = np.zeros(1, dtype=np.float16)
        self.npArrayNormalSmallXSettingTimems = np.zeros(1, dtype=np.float16)
        #Normal Big X
        self.listNormalBigXFinalPositionX = []
        self.listNormalBigXSettingTimems = []
        self.npArrayNormalBigXFinalPositionX = np.zeros(1, dtype=np.float16)
        self.npArrayNormalBigXSettingTimems = np.zeros(1, dtype=np.float16)
        #Normal Small Y
        self.listNormalSmallYFinalPositionY = []
        self.listNormalSmallYSettingTimems = []
        self.npArrayNormalSmallYFinalPositionY = np.zeros(1, dtype=np.float16)
        self.npArrayNormalSmallYSettingTimems = np.zeros(1, dtype=np.float16)
        #Normal Big Y
        self.listNormalBigYFinalPositionY = []
        self.listNormalBigYSettingTimems = []
        self.npArrayNormalBigYFinalPositionY = np.zeros(1, dtype=np.float16)
        self.npArrayNormalBigYSettingTimems = np.zeros(1, dtype=np.float16)
        #Fastest Small X
        self.listFastestSmallXFinalPositionX = []
        self.listFastestSmallXSettingTimems = []
        self.npArrayFastestSmallXFinalPositionX = np.zeros(1, dtype=np.float16)
        self.npArrayFastestSmallXSettingTimems = np.zeros(1, dtype=np.float16)
        #Fastest Big X
        self.listFastestBigXFinalPositionX = []
        self.listFastestBigXSettingTimems = []
        self.npArrayFastestBigXFinalPositionX = np.zeros(1, dtype=np.float16)
        self.npArrayFastestBigXSettingTimems = np.zeros(1, dtype=np.float16)
        #Fastest Small Y
        self.listFastestSmallYFinalPositionY = []
        self.listFastestSmallYSettingTimems = []
        self.npArrayFastestSmallYFinalPositionY = np.zeros(1, dtype=np.float16)
        self.npArrayFastestSmallYSettingTimems = np.zeros(1, dtype=np.float16)
        #Fastest Big Y
        self.listFastestBigYFinalPositionY = []
        self.listFastestBigYSettingTimems = []
        self.npArrayFastestBigYFinalPositionY = np.zeros(1, dtype=np.float16)
        self.npArrayFastestBigYSettingTimems = np.zeros(1, dtype=np.float16)
        #Z
        self.listNormalZFinalPositionX = []
        self.listNormalZFinalPositionY = []
        self.listNormalZSettingTimems = []
        self.listFastestZFinalPositionX = []
        self.listFastestZFinalPositionY = []
        self.listFastestZSettingTimems = []
        self.npArrayNormalZFinalPositionX = np.zeros(1, dtype=np.float16)
        self.npArrayNormalZFinalPositionY = np.zeros(1, dtype=np.float16)
        self.npArrayNormalZSettingTimems = np.zeros(1, dtype=np.float16)
        self.npArrayFastestZFinalPositionX = np.zeros(1, dtype=np.float16)
        self.npArrayFastestZFinalPositionY = np.zeros(1, dtype=np.float16)
        self.npArrayFastestZSettingTimems = np.zeros(1, dtype=np.float16)

        #List for the settling time analysis
        #Normal Small X
        self.listNormalSmallXLongSettling = []
        #Normal Big X
        self.listNormalBigXLongSettling = []
        #Normal Small Y
        self.listNormalSmallYLongSettling = []
        #Normal Big Y
        self.listNormalBigYLongSettling = []
        #Fastest Small X
        self.listFastestSmallXLongSettling = []
        #Fastest Big X
        self.listFastestBigXLongSettling = []
        #Fastest Small Y
        self.listFastestSmallYLongSettling = []
        #Fastest Big Y
        self.listFastestBigYLongSettling = []
        #Z
        self.listNormalZLongSettling = []
        self.listFastestZLongSettling = []
        #User input threshold settling time
        self.thresholdTimems = thresholdTimeMS

    def producerInputFileToIndividualList(self):
        #Open the input file and sort them into corresponding list
        data = [i.strip('\n').split('\t') for i in open(self.input_file_path)]        
        for line in data:
            #Normal Small X movements
            if (line[-1] == "1") and (line[-2] == "False") and (line[-3] == "True"):
                self.listNormalSmallXFinalPositionX.append(line[0])
                self.listNormalSmallXSettingTimems.append(line[-5])
            #Normal Big X
            elif (line[-1] == "1") and (line[-2] == "True") and (line[-3] == "True"):
                self.listNormalBigXFinalPositionX.append(line[0])
                self.listNormalBigXSettingTimems.append(line[-5])
            #Normal Small Y
            elif (line[-1] == "1") and (line[-2] == "False") and (line[-3] == "False"):
                self.listNormalSmallYFinalPositionY.append(line[0])
                self.listNormalSmallYSettingTimems.append(line[-5])
            #Normal Big Y
            elif (line[-1] == "1") and (line[-2] == "True") and (line[-3] == "False"):
                self.listNormalBigYFinalPositionY.append(line[0])
                self.listNormalBigYSettingTimems.append(line[-5])
            #Fastest Small X
            if (line[-1] == "0") and (line[-2] == "False") and (line[-3] == "True"):
                self.listFastestSmallXFinalPositionX.append(line[0])
                self.listFastestSmallXSettingTimems.append(line[-5])
            #Fastest Big X
            elif (line[-1] == "0") and (line[-2] == "True") and (line[-3] == "True"):
                self.listFastestBigXFinalPositionX.append(line[0])
                self.listFastestBigXSettingTimems.append(line[-5])
            #Fastest Small Y
            elif (line[-1] == "0") and (line[-2] == "False") and (line[-3] == "False"):
                self.listFastestSmallYFinalPositionY.append(line[0])
                self.listFastestSmallYSettingTimems.append(line[-5])
            #Fastest big Y
            elif (line[-1] == "0") and (line[-2] == "True") and (line[-3] == "False"):
                self.listFastestBigYFinalPositionY.append(line[0])
                self.listFastestBigYSettingTimems.append(line[-5])
        
        #Have the list back the np array
        self.npArrayNormalSmallXFinalPositionX = np.array(self.listNormalSmallXFinalPositionX, dtype=np.float32)
        self.npArrayNormalSmallXSettingTimems = np.array(self.listNormalSmallXSettingTimems, dtype=np.float32)
        self.npArrayNormalBigXFinalPositionX = np.array(self.listNormalBigXFinalPositionX, dtype=np.float32)
        self.npArrayNormalBigXSettingTimems = np.array(self.listNormalBigXSettingTimems, dtype=np.float32)
        self.npArrayNormalSmallYFinalPositionY = np.array(self.listNormalSmallYFinalPositionY, dtype=np.float32)
        self.npArrayNormalSmallYSettingTimems = np.array(self.listNormalSmallYSettingTimems, dtype=np.float32)
        self.npArrayNormalBigYFinalPositionY = np.array(self.listNormalBigYFinalPositionY, dtype=np.float32)
        self.npArrayNormalBigYSettingTimems = np.array(self.listNormalBigYSettingTimems, dtype=np.float32)
        self.npArrayFastestSmallXFinalPositionX = np.array(self.listFastestSmallXFinalPositionX, dtype=np.float32)
        self.npArrayFastestSmallXSettingTimems = np.array(self.listFastestSmallXSettingTimems, dtype=np.float32)
        self.npArrayFastestBigXFinalPositionX = np.array(self.listFastestBigXFinalPositionX, dtype=np.float32)
        self.npArrayFastestBigXSettingTimems = np.array(self.listFastestBigXSettingTimems, dtype=np.float32)
        self.npArrayFastestSmallYFinalPositionY = np.array(self.listFastestSmallYFinalPositionY, dtype=np.float32)
        self.npArrayFastestSmallYSettingTimems = np.array(self.listFastestSmallYSettingTimems, dtype=np.float32)
        self.npArrayFastestBigYFinalPositionY = np.array(self.listFastestBigYFinalPositionY, dtype=np.float32)
        self.npArrayFastestBigYSettingTimems = np.array(self.listFastestBigYSettingTimems, dtype=np.float32)

        #Set ready for plotting signal
        self.signalUpdatePlot.emit()

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
                        self.listNormalSmallXLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
                #Normal Big X
                elif (line[-1] == "1") and (line[-2] == "True") and (line[-3] == "True"):
                    #Check the settling time
                    if np.float16(line[-5]) >= self.thresholdTimems:
                        self.listNormalBigXLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
                #Normal Small Y
                elif (line[-1] == "1") and (line[-2] == "False") and (line[-3] == "False"):
                    #Check the settling time
                    if np.float16(line[-5]) >= self.thresholdTimems:
                        self.listNormalSmallYLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
                #Normal Big Y
                elif (line[-1] == "1") and (line[-2] == "True") and (line[-3] == "False"):
                    #Check the settling time
                    if np.float16(line[-5]) >= self.thresholdTimems:
                        self.listNormalBigYLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
                #Fastest Small X
                #Fastest Big X
                #Fastest Small Y
                #Fastest Big Y

        #Set the signal for updating the analysing result
        self.signalUpdateAnalysisResult.emit()

        #Set the finish signal
        self.finished.emit()


        
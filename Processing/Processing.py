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
        #Initialise parameters
        #Normal Small X
        self.listNormalSmallXFinalPositionX = []
        self.listNormalSmallXSettingTimems = []
        self.listNormalSmallXTotalTimems = []
        self.listNormalSmallXCruisTimems = []
        #Normal Big X
        self.listNormalBigXFinalPositionX = []
        self.listNormalBigXSettingTimems = []
        self.listNormalBigXTotalTimems = []
        self.listNormalBigXCruisTimems = []
        #Normal Small Y
        self.listNormalSmallYFinalPositionY = []
        self.listNormalSmallYSettingTimems = []
        self.listNormalSmallYTotalTimems = []
        self.listNormalSmallYCruisTimems = []
        #Normal Big Y
        self.listNormalBigYFinalPositionY = []
        self.listNormalBigYSettingTimems = []
        self.listNormalBigYTotalTimems = []
        self.listNormalBigYCruisTimems = []
        #Fastest Small X
        self.listFastestSmallXFinalPositionX = []
        self.listFastestSmallXSettingTimems = []
        self.listFastestSmallXTotalTimems = []
        self.listFastestSmallXCruisTimems = []
        #Fastest Big X
        self.listFastestBigXFinalPositionX = []
        self.listFastestBigXSettingTimems = []
        self.listFastestBigXTotalTimems = []
        self.listFastestBigXCruisTimems = []
        #Fastest Small Y
        self.listFastestSmallYFinalPositionY = []
        self.listFastestSmallYSettingTimems = []
        self.listFastestSmallYTotalTimems = []
        self.listFastestSmallYCruisTimems = []
        #Fastest Big Y
        self.listFastestBigYFinalPositionY = []
        self.listFastestBigYSettingTimems = []
        self.listFastestBigYTotalTimems = []
        self.listFastestBigYCruisTimems = []
        #Z
        self.listNormalZFinalPositionX = []
        self.listNormalZFinalPositionY = []
        self.listNormalZTotalTimems = []
        self.listFastestZFinalPositionX = []
        self.listFastestZFinalPositionY = []
        self.listFastestZTotalTimems = []


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
        self.listNormalZLongTotal = []
        self.listFastestZLongTotal = []
        #User input threshold settling time
        self.thresholdTimems = thresholdTimeMS

    def producerInputFileToIndividualList(self):
        #Open the input file and sort them into corresponding list
        data = [i.strip('\n').split('\t') for i in open(self.input_file_path)]        
        for line in data:
            #Normal Small X movements
            if (line[-1] == "1") and (line[-2] == "False") and (line[-3] == "True"):
                self.listNormalSmallXFinalPositionX.append(np.float16(line[0]))
                self.listNormalSmallXSettingTimems.append(np.float16(line[4]))
                self.listNormalSmallXTotalTimems.append(np.float16(line[2]))
                self.listNormalSmallXCruisTimems.append(np.float16(line[3]))
            #Normal Big X
            elif (line[-1] == "1") and (line[-2] == "True") and (line[-3] == "True"):
                self.listNormalBigXFinalPositionX.append(np.float16(line[0]))
                self.listNormalBigXSettingTimems.append(np.float16(line[4]))
                self.listNormalBigXTotalTimems.append(np.float16(line[2]))
                self.listNormalBigXCruisTimems.append(np.float16(line[3]))
            #Normal Small Y
            elif (line[-1] == "1") and (line[-2] == "False") and (line[-3] == "False"):
                self.listNormalSmallYFinalPositionY.append(np.float16(line[1]))
                self.listNormalSmallYSettingTimems.append(np.float16(line[4]))
                self.listNormalSmallYTotalTimems.append(np.float16(line[2]))
                self.listNormalSmallYCruisTimems.append(np.float16(line[3]))
            #Normal Big Y
            elif (line[-1] == "1") and (line[-2] == "True") and (line[-3] == "False"):
                self.listNormalBigYFinalPositionY.append(np.float16(line[1]))
                self.listNormalBigYSettingTimems.append(np.float16(line[4]))
                self.listNormalBigYTotalTimems.append(np.float16(line[2]))
                self.listNormalBigYCruisTimems.append(np.float16(line[3]))
            #Fastest Small X
            if (line[-1] == "0") and (line[-2] == "False") and (line[-3] == "True"):
                self.listFastestSmallXFinalPositionX.append(np.float16(line[0]))
                self.listFastestSmallXSettingTimems.append(np.float16(line[4]))
                self.listFastestSmallXTotalTimems.append(np.float16(line[2]))
                self.listFastestSmallXCruisTimems.append(np.float16(line[3]))
            #Fastest Big X
            elif (line[-1] == "0") and (line[-2] == "True") and (line[-3] == "True"):
                self.listFastestBigXFinalPositionX.append(np.float16(line[0]))
                self.listFastestBigXSettingTimems.append(np.float16(line[4]))
                self.listFastestBigXTotalTimems.append(np.float16(line[2]))
                self.listFastestBigXCruisTimems.append(np.float16(line[3]))
            #Fastest Small Y
            elif (line[-1] == "0") and (line[-2] == "False") and (line[-3] == "False"):
                self.listFastestSmallYFinalPositionY.append(np.float16(line[1]))
                self.listFastestSmallYSettingTimems.append(np.float16(line[4]))
                self.listFastestSmallYTotalTimems.append(np.float16(line[2]))
                self.listFastestSmallYCruisTimems.append(np.float16(line[3]))
            #Fastest big Y
            elif (line[-1] == "0") and (line[-2] == "True") and (line[-3] == "False"):
                self.listFastestBigYFinalPositionY.append(np.float16(line[1]))
                self.listFastestBigYSettingTimems.append(np.float16(line[4]))
                self.listFastestBigYTotalTimems.append(np.float16(line[2]))
                self.listFastestBigYCruisTimems.append(np.float16(line[3]))
            #Normal Z
            if (line[-1] == "1"):
                self.listNormalZFinalPositionX.append(np.float16(line[0]))
                self.listNormalZFinalPositionY.append(np.float16(line[1]))
                self.listNormalZTotalTimems.append(np.float16(line[5]))
            #Fastest Z
            elif (line[-1] == "0"):
                self.listFastestZFinalPositionX.append(np.float16(line[0]))
                self.listFastestZFinalPositionY.append(np.float16(line[1]))
                self.listFastestZTotalTimems.append(np.float16(line[5]))

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
                elif (line[-1] == "0") and (line[-2] == "False") and (line[-3] == "True"):
                    #Check the settling time
                    if np.float16(line[-5]) >= self.thresholdTimems:
                        self.listFastestSmallXLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
                #Fastest Big X
                elif (line[-1] == "0") and (line[-2] == "True") and (line[-3] == "True"):
                    #Check the settling time
                    if np.float16(line[-5]) >= self.thresholdTimems:
                        self.listFastestBigXLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
                #Fastest Small Y
                elif (line[-1] == "0") and (line[-2] == "False") and (line[-3] == "False"):
                    #Check the settling time
                    if np.float16(line[-5]) >= self.thresholdTimems:
                        self.listFastestSmallYLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
                #Fastest Big Y
                elif (line[-1] == "0") and (line[-2] == "True") and (line[-3] == "False"):
                    #Check the settling time
                    if np.float16(line[-5]) >= self.thresholdTimems:
                        self.listFastestBigYLongSettling.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-5]])
            #Check Z
            if count == 1:
                #The first movement is always normal small y move from (0mm, 0mm) position
                #Check the setting time
                if np.float16(line[-4]) >= self.thresholdTimems:
                    self.listNormalZLongTotal.append(['0', '0', line[0], line[1], line[-4]])
            else:
                #Normal Z
                if (line[-1] == "1"):
                    if np.float16(line[-4]) >= self.thresholdTimems:
                        self.listNormalZLongTotal.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-4]])
                #Fastest Z
                elif (line[-1] == "0"):
                    if np.float16(line[-4]) >= self.thresholdTimems:
                        self.listFastestZLongTotal.append([data[count-1][0], data[count-1][1], line[0], line[1], line[-4]])

        #Set the signal for updating the analysing result
        self.signalUpdateAnalysisResult.emit()

        #Set the finish signal
        self.finished.emit()


        
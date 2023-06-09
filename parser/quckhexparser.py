#Eliseo Izazaga

#this application will with the matplot 2 axis charts to plot the batter, charging current, voltage, and SOC (percent)
#this will use the parasite simple chart

#the hostsubplot will be used for the  original backdrop and the par subplot will be the secondary axis,
#both take data in a list format and attributed to a specific label, then the list will be ploted,


#EVERY SINGLE DATA POINT FROM EACH COLUMN WILL NEED TO BE PLOTTED TO THE TIME STAMP WHEN RECORDED


#EXAMPLE,
#TIME LIST [TIME1, TIME2, TIME3, TIME4, TIME5, TIME6, TIME7]
#SOC LIST [1, 1, 2, 2, 3, 4, 5, 5,]

from datetime import datetime
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd
timeOnXAxisFormat = mdates.DateFormatter("%H:%M:%S")

locationInDrive = r"C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\Aquila Stuff\Coulumb Counting\Automated Counting\partialData\VerbosePIR\\"  #folder containing the logs 
specificLog = "hexToFlip"        #log name without file extention (no .txt or .png)
toProcess = locationInDrive + specificLog + ".txt"  #this outputs a parsed log with the name PARTSED



#############################################################################################################################################

logToOpen = toProcess
directoryToSaveNewParsedLog = locationInDrive + " PARSED "+specificLog + ".txt"     #this outputs a parsed log with the name PARTSED


timeStamps          = []
CCunderLoad         = []
VOLTunderLOAD       = []
CCnotUnderLoad      = []
VOLTnotUnderLoad    = []


dataList                = []

toSaveForParsedLog = []
def toInt(inList):
    ret = [eval(i) for i in inList]
    return ret

def sanitizeTimeStamps(timeStampList):#This is to clean up and sanitize the time stamp list and return it
    sanitizedList = timeStampList
    #print(sanitizedList)
    for x in range(len(sanitizedList)):
        manipString = sanitizedList[x]
        manipString = str(manipString)
        tempList = []
        tempList = manipString.split(' ')
        #print(tempList)
        sanitizedList[x] = tempList[1]  #if you are having time stamp issues this the the number to change, 1 or 3
        manipString = sanitizedList[x]

        manipString = str(manipString)
        tempList = []
        tempList = manipString.split('.')
        sanitizedList[x] = tempList[0]

        #sanitizedList[x] = datetime.strptime(sanitizedList[x], "%H:%M:%S") #UNCOMMENT THIS LINE TO TURN TIMESTAMPS INTO DATETIME OBJECTS,
    #print(tempList)
    #print(sanitizedList)
    return sanitizedList #return type is string

def findTotalTimeElapsed(intimeStampList, inBATCurList): #this function uses the battery current data, it looks for when the current went to 0 and matches up the index of the
    #list with the timeStamp list, subtracts the time stamp from when the battery current was 0 and the start of the test to find the total charttime, the time is returned in
    #string format
    i = 200 #index starts at 50 because batCurr can sometimes be 0 at the start of the test

    while i in range(len(inBATCurList)):
        #print(inBATCurList[i])
        i = i + 1
        if inBATCurList[i] == 0:
            #print(inBATCurList[i])

            startTime = intimeStampList[0]
            print(startTime)
            endTime = intimeStampList[i]
            print(endTime)
            startTime = datetime.strptime(startTime, "%H:%M:%S")
            #print(startTime)
            endTime = datetime.strptime(endTime, "%H:%M:%S")
            #print(endTime)
            toReturn = endTime - startTime
            #print(toReturn)
            return toReturn


#with open(directoryToSaveNewParsedLog, 'a') as fp:
#                fp.writelines(str(read_data))
#                fp.write("\n")



with open(logToOpen, encoding="ANSI") as inFile:
    for line in inFile:
        read_data = inFile.readline()
        print(read_data)
        splitInLine = read_data.split(" ")
        #print(splitInLine)
        toSave = str(splitInLine[1]) + str(splitInLine[0])
        #print(toSave)
        with open(directoryToSaveNewParsedLog, 'a') as fp:
                fp.writelines(toSave)
                fp.write("\n")
                fp.close()


       







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

locationInDrive = r"C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\BATTERY\A14\PRO5\INDOOR\Termination current set at 250mA\\"  #folder containing the logs 
specificLog = "BAT1 A9M1257FA01F9 250mA Termination Current"        #log name without file extention (no .txt or .png)
toProcess = locationInDrive + specificLog + ".txt"  #this outputs a parsed log with the name PARTSED
toPlot = locationInDrive + specificLog + ".png"
plotTitle = specificLog    #chart title will be log name, temp, bat type.     

#############################################################################################################################################

logToOpen = toProcess
directoryToSaveNewParsedLog = locationInDrive + " PARSED "+specificLog + ".txt"     #this outputs a parsed log with the name PARTSED
chartTitle = plotTitle
saveAs = toPlot


#saveAs = saveAs + chartTitle + ".png"


xAxisScaler = 1     #for different temperatures require different scalers to properly display data, it is contigent on
                    #the number of data points taken during the test
#roomtemp: = 1
#cold = 3
#hot = tbd

#inLogToParse = open(logToOpen, "r")
#currentLine = inLogToParse.readlines()
#print(currentLine)

timeStamps = []
BAT_CUR = []
TEMP = []
PERC = []
VOLT = []
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
        sanitizedList[x] = tempList[3]  #if you are having time stamp issues this the the number to change, 1 or 3
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


#this does the log parsing
headerFoundFlag = 0 #this is a flag to indicate that the header has been found

with open(logToOpen, encoding="ANSI") as inFile:
    for line in inFile:
        read_data = inFile.readline()
        #print(read_data)
        #if read_data.find('\n') != -1 and headerFoundFlag == 0:
            #testHeader = read_data.split(",")
            #print(testHeader)
            #headerFoundFlag = 1
        if read_data.find('$') != -1:   #looks for the comma delimited part of the log file and splits all data at the comma and saves every data point in a big list.
            #print("dataFound")
            #print(read_data)
            #print(len(read_data))
            dataList = read_data.split(",")
            #print(len(dataList))
            #print(dataList)
            if len(dataList) == 20:
                with open(directoryToSaveNewParsedLog, 'a') as fp:
                    fp.writelines(str(dataList))
                    fp.write("\n")
                timeStamps.append(dataList[0])
                BAT_CUR.append(dataList[7])
                TEMP.append(dataList[5])
                PERC.append(dataList[6])
                VOLT.append(dataList[4])
            #print(timeStamps)
    #print(timeStamps)
    timeStamps = sanitizeTimeStamps(timeStamps)
    BAT_CUR = toInt(BAT_CUR)
    TEMP = toInt(TEMP)
    PERC = toInt(PERC)
    VOLT = toInt(VOLT)


    print(timeStamps)
    print(BAT_CUR)
    print(TEMP)
    print(PERC)
    print(VOLT)


######################################################################################plotting########################################################
plt.figure(figsize=(18,10))
host = host_subplot(111, axes_class=axisartist.Axes)
timeElapsed = findTotalTimeElapsed(timeStamps, BAT_CUR)

timeElapsed = "Total Time: HH:MM:SS " + str(timeElapsed)
#timeElapsed = "Total Time: HH:MM:SS " + "20:44:46"
#timeElapsed = "TEST NOT COMPLETE, JEITTA OVER TEMP"

par1 = host.twinx()


par1.axis["right"].toggle(all=True)

toPlotAgainst = len(PERC)

p1, = host.plot(BAT_CUR,   label="Current")
p1, = host.plot(VOLT,   label="Voltage")
p2, = par1.plot(PERC,  label="SOC")
p2, = par1.plot(TEMP, label="Temperature")
#p3 = host.plot(timeStamps, PERC)


host.set_xlim(0, (len(timeStamps) / xAxisScaler)) # X limit is contigent on the # of data points taken
host.set_ylim(0, 5000)
par1.set_ylim(-25 , 100)



plt.yticks(np.arange(-2000, 5000, 500))
#plt.xticks(np.arange(0, (len(PERC) / xAxisScaler), 1000))
plt.tick_params(axis='x', which='major', labelsize = 3)
plt.xticks( rotation=25 )
plt.title(chartTitle)
plt.grid()

host.set_xlabel(timeElapsed)
host.set_ylabel("Voltage and Current")
par1.set_ylabel("Temperature and SOC")

host.legend()

host.axis["left"].label.set_color('black')
par1.axis["right"].label.set_color('black')

plt.savefig(saveAs)
plt.show()

############################################################Excel Part####################################################################3
#this is the part where it places the parsed log into an excel workbook along with the chart.







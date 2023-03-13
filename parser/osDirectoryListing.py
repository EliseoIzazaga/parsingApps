import os
 


locationInDrive = r"C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\BATTERY\A-4B Battery\ULTRA\directoryTest\\"



print(os.listdir(locationInDrive))

logsInFolder = os.listdir(locationInDrive)
print(logsInFolder)

for i in range(len(logsInFolder)):
    print(logsInFolder[i])
    print(type(logsInFolder[i]))

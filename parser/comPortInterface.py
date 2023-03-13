#Eliseo Izazaga
import time
#this application will chart and plot the battery charging mechanism in the GEN 5 cameras through the
#serial port and matplotlib
import sys
import glob
import serial

def serial_ports():
    """
    Successfully tested on Windows 8.1 x64
    Windows 10 x64
    Mac OS X 10.9.x / 10.10.x / 10.11.x
    Ubuntu 14.04 / 14.10 / 15.04 / 15.10
    with both Python 2 and Python 3


         Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def openSerialPort(COMDEVICENUMBER):
    """This function opens a new port and returns it in the main body of the application"""
    #encodedComPort = str(COMDEVICENUMBER)
    newport = serial.Serial(port=COMDEVICENUMBER, baudrate=115200, parity="N", stopbits=1, bytesize=8, timeout=0.1)
    print("Opened " + newport.portstr)
    return newport

def utilityBatteryFunction(targetCam):
    targetCam.write('\r'.encode('ascii'))
    targetCam.reset_input_buffer()
    targetCam.reset_output_buffer()
    targetCam.write('\r'.encode('ascii'))
    targetCam.reset_input_buffer()
    targetCam.reset_output_buffer()
    targetCam.write('\r'.encode('ascii'))
    targetCam.reset_input_buffer()
    targetCam.reset_output_buffer()
    targetCam.flush()
    print("command sent: " + "pm")
    targetCam.write("pm".encode('utf-8'))
    data = []

    for x in range(13):
        data.append(targetCam.read_until())
    #print(data)
    targetCam.reset_input_buffer()
    targetCam.reset_output_buffer()
    #print(comparison)
    #print(str(data[-1]))
    return data

def getBatteryData(target):
    batteryDataList = []
    batteryDataList = utilityBatteryFunction(target)
    comparison = 'b\'\''
    while str(batteryDataList[-1]) == comparison:
        batteryDataList = utilityBatteryFunction(target)
    print(batteryDataList)
    return batteryDataList

if __name__ == '__main__':
    TESTCAM1 = openSerialPort("COM10")
    getBatteryData(TESTCAM1)
    listofSerPorts = serial_ports()
    print(listofSerPorts)
    #testCommand = 'pm'.encode('utf-8') + '\r'.encode('ascii')
    #TESTCAM1.write(testCommand)
    #print(TESTCAM1.read(100))
    #TESTCAM1.reset_input_buffer()
    #TESTCAM1.reset_output_buffer()

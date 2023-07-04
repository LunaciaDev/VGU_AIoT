import time
import serial.tools.list_ports

try:
    ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
except:
    print("Cannot open port.")
    
def sendCommand(command):
    ser.write(command.encode())

sendCommand("2")
time.sleep(5)
sendCommand("3")
time.sleep(5)
sendCommand("4")
time.sleep(5)
sendCommand("5")
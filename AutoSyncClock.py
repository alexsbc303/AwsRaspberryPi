import serial
import time
from datetime import date, datetime
import re

#Defining the port parameters
port = serial.Serial("/dev/ttyUSB0", baudrate=2400, timeout=1)

#Variables
start = True
#String Command
get_string = [27, 67, 67]
final_enter = [13, 10]
#Timestamp variable
now = datetime.now()

def SyncClock(time_string):
    if time_string != '':
        #Write Command
        print('YYMMDDhhmmss: ', time_string)
        port.write(bytearray(get_string))
        port.write(bytearray(time_string, 'utf-8'))
        port.write(bytearray(final_enter))
#         print(bytearray(get_string))
#         print(bytearray(time_string, 'utf-8'))
#         print(bytearray(final_enter))
    print('--------------------')
    print('Finished immediate sync')
    print('--------------------')
    
def RegularSyncClock(time_string):
    while start == True:
        now = datetime.now()
        time_string = now.strftime("%y%m%d%H%M%S")
        if now.strftime("%H%M") == '2359' or now.strftime("%H%M") == '0600' or now.strftime("%H%M") == '1200' or now.strftime("%H%M") == '1800':
            print('YYMMDDhhmmss: ', time_string)
            #Write Command
            port.write(bytearray(get_string))
            port.write(bytearray(time_string, 'utf-8'))
            port.write(bytearray(final_enter))
#             print(bytearray(get_string))
#             print(bytearray(time_string, 'utf-8'))
#             print(bytearray(final_enter))
            print('--------------------')
            print('Finished regular sync')
            print('--------------------')
            time.sleep(60)
    port.close()
        
#Main Function
print('Sync Clock (From Server Clock to AWS Field Unit Clock)')
#Auto input time
time_string = now.strftime("%y%m%d%H%M%S")
#Start sync clock
SyncClock(time_string)
RegularSyncClock(time_string)

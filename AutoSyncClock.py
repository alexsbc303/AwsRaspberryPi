import serial
import time
from datetime import date, datetime

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
    print('--------------------')
    print('Finished immediate sync')
    print('--------------------')
    
def RegularSyncClock(time_string):
    while start == True:
        now = datetime.now()
        matches = ['2345', '0245', '0545', '0845', '1145', '1445', '1745']
        time_string = now.strftime("%y%m%d%H%M%S")
        if now.strftime("%H%M") in matches:
            print('YYMMDDhhmmss: ', time_string)
            #Write Command
            port.write(bytearray(get_string))
            port.write(bytearray(time_string, 'utf-8'))
            port.write(bytearray(final_enter))
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

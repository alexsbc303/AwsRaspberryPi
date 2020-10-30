import serial
from datetime import date, datetime
import re

#Defining the port parameters
port = serial.Serial("/dev/ttyUSB0", baudrate=2400, timeout=1)

#Variables
#String Command
get_string = [27, 67, 67]
final_enter = [13, 10]
#null variable
selection = ''

def SyncClock(time):
    if time != '':
        #Write Command
        port.write(bytearray(get_string))
        port.write(bytearray(time, 'utf-8'))
        port.write(bytearray(final_enter))
#         print(bytearray(get_string))
#         print(bytearray(time, 'utf-8'))
#         print(bytearray(final_enter))
        print('--------------------')
    port.close()
    print('Finished')
    
def FetchTime(data):
    time = ''
    #Get Time - YYMMDDhhmmss
    match = re.search(r'\d\d\d\d\d\d\d\d\d\d\d\d', data)
    if match:
        time = match.group()
    else:
        print('Cannot find time')
    #Start sync clock
    SyncClock(time)
    
#Main Function
#Choose between using (1) Manual Input / (2) Server Clock
print('Choose between using (1) Manual Input and (2) Server Clock (Type 1 or 2), or default')
choice = input()

if choice == '1':
    #Manual input
    print('Sync Clock (Manual input to AWS Field Unit Clock)')
    #input
    print('Enter current time (YYMMDDhhmmss): ')
    time_string = input()
    print('YYMMDDhhmmss: ', time_string)
    FetchTime(time_string)
elif choice == '2':
    #Server Clock input
    print('Sync Clock (From Server Clock to AWS Field Unit Clock)')
    now = datetime.now()
    time_string = now.strftime("%y%m%d%H%M%S")
    print('YYMMDDhhmmss: ', time_string)
    FetchTime(time_string)
else:
    print('#Default - Sync Clock (From Server Clock to AWS Field Unit Clock)')
    now = datetime.now()
    time_string = now.strftime("%y%m%d%H%M%S")
    print('YYMMDDhhmmss: ', time_string)
    FetchTime(time_string)

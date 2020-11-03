import configparser
import serial
import re
from pathlib import Path
from datetime import datetime

#Defining the port parameters
port = serial.Serial("/dev/ttyUSB0", baudrate=2400, timeout=1)

#Variables
#Fetch device name from config file
config = configparser.ConfigParser()
config.read('/boot/config.txt')
station_name = config.get('aws', 'name')

#String Command
get_DD = [27, 68, 68, 13]
get_BH = [27, 66, 72, 13]
#Timestamp variable
now = datetime.now()
month = now.strftime("%b")
#Pathways
current_path = Path.cwd()
Aws_path = ''
station_path = ''
day_path = ''

def CreateAwsDirectory():
    #Aws
    if not (current_path / 'Aws').exists():
        Aws_path = current_path / 'Aws'
        Aws_path.mkdir()
#         print(f"Aws directory: ", Aws_path)
    else:
        Aws_path = current_path / 'Aws'
#         print(f"Aws directory: ", Aws_path)

def CreateStationDirectory():
    #Station's short name - Assume BCS is used 
    if not (current_path / 'Aws' / station_name).exists():
        station_path = current_path / 'Aws' / station_name
        station_path.mkdir()
#         print(f"Station directory: ", station_path)
    else:
        station_path = current_path / 'Aws' / station_name
#         print(f"Station directory: ", station_path)
        
def CreateMonthDirectory():
    #Month
    if not (current_path / 'Aws' / station_name / month).exists():
        month_path = current_path / 'Aws' / station_name / month
        month_path.mkdir()
#         print(f"Month directory: ", month_path)
    else:
        month_path = current_path / 'Aws' / station_name / month
#         print(f"Month directory: ", month_path)
        
def CreateDayDirectory():
    #Month - Jan to Dec
    now = datetime.now()
    if not (current_path / 'Aws' / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}').exists():
        day_path = current_path / 'Aws' / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}'
        day_path.mkdir()
#         print(f"Directory: ", day_path)
    else:
        day_path = current_path / 'Aws' / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}'
#         print(f"Directory: ", day_path)
                
def ReadData(start):
    count = 0
    while count < 2:
        port.write(bytearray(get_DD))
        read_port_DD = port.readline()
        #Print read code
        print('DD: ', read_port_DD)
        #Fetch necessary information from data
        FetchInfo(str(read_port_DD))
        print('--------------------')            
        count += 1
    port.close()
    print('Finished')
        
def FetchInfo(data):
    station = ''
    timestamp = ''
    info = ''
    reset = ''
    
    #Get 1 BackLog data
    port.write(bytearray(get_BH))
    read_port_BH = port.readline()
    #Print read code
    print('BH: ', read_port_BH)
    #Fetch whole string from BH
    print('--------------------')
    
    #Get Station + YY/MM/DD/HH/MM info
    firstrow_match = re.search(r'(x02)(\w\w\w)(\w\w\w\w\w\w\w\w\w\w)', data)
    if firstrow_match:
        print('Firstrow: ', firstrow_match.group(2), firstrow_match.group(3))
        station = firstrow_match.group(2)
        timestamp = firstrow_match.group(3)
    else:
        print('Firstrow: ')
    #Get other info
    secondrow_match = re.search(r'(A\w+)', data)
    if secondrow_match:
        print('Secondrow: ', secondrow_match.group())
        info = secondrow_match.group()
    else:
        print('Secondrow: ')
    #Get reset message
    resetmsg_match =  re.search(r'(A----B----C----D----E----F----G----H----I----J----K----L----M----N----O----P----Q----R----T----U----V----p----v----16)', data)
    if resetmsg_match:
        print('Reset Message: ', resetmsg_match.group(), 'A')
        reset = resetmsg_match.group() + 'A'
    else:
        print('Reset Message: ')
    
    CreateFile(station, timestamp, info, reset, read_port_BH)
    
def CreateFile(s, t, i, r, bh):
    #Filename - Station + YYMMDDHHMM
    CreateAwsDirectory()
    CreateStationDirectory()
    CreateMonthDirectory()
    CreateDayDirectory()
    now = datetime.now()
    current_path = Path.cwd() / 'Aws' / station_name
    file_path = current_path / f'{station_name}{now.strftime("%y%m%d%H%M")}.txt'
    print(f"Directory: ", file_path)
    with file_path.open('w') as f:
        f.write(f'{s}{t}\n{i}{r}\n{bh}')
        
#Main Function
#Current directory: /home/pi/Desktop/data
print('Station Name: ', station_name)
print('------------------------------')
#Start reading data 
ReadData(True)

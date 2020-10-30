import configparser
import serial
import time
import re
import shutil
import os
from pathlib import Path
from datetime import date, datetime

#Defining the port parameters
port = serial.Serial("/dev/ttyUSB0", baudrate=2400, timeout=1)

#Variables
#Fetch device name from config file
config = configparser.ConfigParser()
config.read('/boot/config.txt')
station_name = config.get('aws', 'name')
print('Station Name: ', station_name)

#String Command
get_string = [27, 68, 68, 13]
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
        print(f"Aws directory: ", Aws_path)
    else:
        Aws_path = current_path / 'Aws'
        print(f"Aws directory: ", Aws_path)

def CreateStationDirectory():
    #Station's short name - Assume BCS is used 
    if not (current_path / 'Aws' / station_name).exists():
        station_path = current_path / 'Aws' / station_name
        station_path.mkdir()
        print(f"Station directory: ", station_path)
    else:
        station_path = current_path / 'Aws' / station_name
        print(f"Station directory: ", station_path)
        
def CreateMonthDirectory():
    #Month
    if not (current_path / 'Aws' / station_name / month).exists():
        month_path = current_path / 'Aws' / station_name / month
        month_path.mkdir()
        print(f"Month directory: ", month_path)
    else:
        month_path = current_path / 'Aws' / station_name / month
        print(f"Month directory: ", month_path)
        
def CreateDayDirectory():
    #Month - Jan to Dec
    now = datetime.now()
    if not (current_path / 'Aws' / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}').exists():
        day_path = current_path / 'Aws' / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}'
        day_path.mkdir()
        print(f"Day directory: ", day_path)
    else:
        day_path = current_path / 'Aws' / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}'
        print(f"Day directory: ", day_path)
                
def ReadData(start):
    while start == True:
        #Write Command
        port.write(bytearray(get_string))
        #Read the port information
        read_port = port.readline()
#       Print code per minute
#       print(read_port)
        #Fetch necessary information from data
        FetchInfo(str(read_port))
        #Housekeeping when 0000
        Housekeeping()
        print('--------------------')
        time.sleep(60)
        
    port.close()
   
def FetchInfo(data):
    station = ''
    timestamp = ''
    info = ''
    reset = ''
    #Get Station + YY/MM/DD/HH/MM info
    firstrow_match = re.search(r'(x02)(\w\w\w)(\w\w\w\w\w\w\w\w\w\w)', data)
    if firstrow_match:
        print('Firstrow: ', firstrow_match.group(2), firstrow_match.group(3))
        station = firstrow_match.group(2)
        timestamp = firstrow_match.group(3)
    else:
        print('Cannot find first row')
    #Get other info
    secondrow_match = re.search(r'(A\w+)', data)
    if secondrow_match:
        print('Secondrow: ', secondrow_match.group())
        info = secondrow_match.group()
    else:
        print('Cannot find second row')
    #Get reset message
    resetmsg_match =  re.search(r'(A----B----C----D----E----F----G----H----I----J----K----L----M----N----O----P----Q----R----T----U----V----p----v----16)', data)
    if resetmsg_match:
        print('Reset Message: ', resetmsg_match.group(), 'A')
        reset = resetmsg_match.group() + 'A'
        print('\n')
    else:
        print('Cannot find reset message')
        print('\n')
        
    CreateFile(station, timestamp, info, reset)
    
def CreateFile(s, t, i, r):
    #Filename - Station + YYMMDDHHMM
    CreateAwsDirectory()
    CreateStationDirectory()
    CreateMonthDirectory()
    CreateDayDirectory()
    now = datetime.now()
    current_path = Path.cwd() / 'Aws' / station_name
    file_path = current_path / f'{station_name}{now.strftime("%y%m%d%H%M")}.txt'
    with file_path.open('w') as f:
        f.write(f'{s}{t}\n{i}{r}')

def Housekeeping():
    now = datetime.now()
    source_path = Path.cwd() / 'Aws' / station_name
    destination_path = source_path / month / f'{station_name}_{now.strftime("%y%m%d")}'
    files = os.listdir(source_path)
    if (now.strftime("%H%M") == '2359'):
        for filename in files:
            if filename.endswith('.txt'):    
                shutil.move(f"{source_path}/{filename}", destination_path)
        print('*****')
        print('Housekeeping successful!')
        print('*****')
        
#Main Function
#Current directory: /home/pi/Desktop/data
print(f"Current directory: {Path.cwd()}")
print('------------------------------')
#Start reading data 
ReadData(True)
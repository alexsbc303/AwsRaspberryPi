import configparser
import serial
import re
import time
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
#Timestamp variable
now = datetime.now()
month = now.strftime("%b")
#Pathways
current_path = Path('/home/pi/DATA/')
#Change Aws_choice to go to different directories
Aws_choice = 'AWS_manual_data'
Aws_path = ''
station_path = ''
day_path = ''

def CreateAwsDirectory():
    #Aws
    if not (current_path / Aws_choice).exists():
        Aws_path = current_path / Aws_choice
        Aws_path.mkdir()
    else:
        Aws_path = current_path / Aws_choice

def CreateStationDirectory():
    #Station's short name - Assume BCS is used 
    if not (current_path / Aws_choice / station_name).exists():
        station_path = current_path / Aws_choice / station_name
        station_path.mkdir()
    else:
        station_path = current_path / Aws_choice / station_name
        
def CreateMonthDirectory():
    #Month
    if not (current_path / Aws_choice / station_name / month).exists():
        month_path = current_path / Aws_choice / station_name / month
        month_path.mkdir()
    else:
        month_path = current_path / Aws_choice / station_name / month
        
def CreateDayDirectory():
    #Month - Jan to Dec
    now = datetime.now()
    if not (current_path / Aws_choice / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}').exists():
        day_path = current_path / Aws_choice / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}'
        day_path.mkdir()
    else:
        day_path = current_path / Aws_choice / station_name / month / f'{station_name}_{now.strftime("%y%m%d")}'
                
def ReadData(start):
    count = 0
    while count < 1:
        #Get existing data
        port.write(get_DD)
        read_port_DD = port.read(300).decode('utf-8')
        #Print read code
        print('DD: ', read_port_DD)       
        count += 1

        CreateFile(read_port_DD)
        
    port.close()
    print('Finished')
    
def CreateFile(data1):
    #Filename - Station + YYMMDDHHMM
    CreateAwsDirectory()
    CreateStationDirectory()
    CreateMonthDirectory()
    CreateDayDirectory()
    now = datetime.now()
    current_path = Path('/home/pi/DATA/') / Aws_choice / station_name
    file_path = current_path / f'{station_name}{now.strftime("%y%m%d%H%M")}.txt'
    print(f"Directory: ", file_path)
    with file_path.open('a+') as f:
        f.write(f'{data1}')
        
#Main Function
#Current directory: /home/pi/Desktop/data
print('Station Name: ', station_name)
print('------------------------------')
#Start reading data 
ReadData(True)

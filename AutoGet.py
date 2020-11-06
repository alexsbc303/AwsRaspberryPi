import configparser
import serial
import time
import re
import shutil
import os
from pathlib import Path
from datetime import date, datetime, timedelta

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
current_path = Path('/home/pi/DATA/')
#Change Aws_choice to go to different directories
Aws_choice = 'AWS'
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
    while start == True:
        now = datetime.now()
        if now.strftime("%S") == '05':
            print('Current Time: ', now.strftime("%y%m%d%H%M%S"))
            #Get existing data
            port.write(get_DD)
            read_port_DD = port.read(300).decode('utf-8')
            #Print read code
            print('DD: ', read_port_DD)
            
            #Get BackLog data
            port.write(get_BH)
            read_port_BH = port.read(300).decode('utf-8')
            #Print read code
            print('BH: ', read_port_BH)
            print('--------------------')
            
            #Create File
            CreateFile(read_port_DD, read_port_BH)
            
            #Housekeeping when 0830
            Housekeeping()
            
            print('--------------------')
#             time.sleep(60)
    port.close()
    
def CreateFile(data1, data2):
    #Filename - Station + YYMMDDHHMM
    CreateAwsDirectory()
    CreateStationDirectory()
    CreateMonthDirectory()
    CreateDayDirectory()
    now = datetime.now()
    current_path = Path.cwd() / Aws_choice / station_name
    file_path = current_path / f'{station_name}{now.strftime("%y%m%d%H%M")}.txt'
    print(f"Directory: ", file_path)
    with file_path.open('a+') as f:
        f.write(f'{data1}{data2}')
        
def Housekeeping():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    source_path = Path('/home/pi/DATA/') / Aws_choice / station_name
    destination_path = source_path / month / f'{station_name}_{yesterday.strftime("%y%m%d")}'
    files = os.listdir(source_path)
    if (now.strftime("%H%M") == '0830'):
        for filename in files:
            if yesterday.strftime("%y%m%d") in filename:
                if filename.endswith('.txt'):
                    shutil.move(f"{source_path}/{filename}", destination_path)
        print('*****')
        print('Housekeeping successful!')
        print('*****')

#Main Function
#Current directory: /home/pi/Desktop/data
print('Station Name: ', station_name)
print('------------------------------')
#Start reading data 
ReadData(True)
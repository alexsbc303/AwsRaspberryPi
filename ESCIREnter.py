import serial

#Defining the port parameters
port = serial.Serial("/dev/ttyUSB0", baudrate=2400, timeout=1)

#Variables
#String Command
get_string = [27, 73, 82, 13]

def Reset_Field_Unit():
    #Write Command
    port.write(bytearray(get_string))
    print(bytearray(get_string))
    print('--------------------')
    port.close()
    print('Finished')
        
#Main Function
print('Reset Field Unit')
Reset_Field_Unit()


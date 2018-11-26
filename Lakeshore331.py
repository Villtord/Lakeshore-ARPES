# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 16:12:00 2018

@author: Preparation PC
"""


def send_command (com_name, command):

    import serial.tools.list_ports
    import io
#    import random
    
    """ Open COM-port and send/read the command"""
    ser = serial.Serial(com_name,                   
                         baudrate=9600,
                         bytesize=serial.SEVENBITS,
                         parity=serial.PARITY_ODD,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=0.1)

    ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),  
                               newline = '\r\n',
                               line_buffering = True)
    
    """Write a command(s) to pressure controller and read the reply """
    try:
        command_full = str(command) + "\r\n"
#        command = "KRDG?B\r\n"
#        command = "RDGST?\r\n"
#        command = "SETP?\r\n"
        ser_io.write(command_full)
        read_str = ser_io.read()
    except:
        pass    
    
    ser.close()
    try:
#        read_str = str(random.randint(1,10)/10000000)
#        read_str += ','+str(random.randint(1,10)/10000000)
        return read_str[:-1]
    except:
        pass
#    
#print(send_command("COM100","*IDN?"))
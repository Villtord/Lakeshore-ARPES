# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 19:40:14 2018

@author: Preparation PC
"""



import socket               # Import socket module
from threading import Timer
import _thread
import time
import datetime as dt
import shutil
from Lakeshore331 import send_command

global host, port, com_port_name
host = '132.187.37.41'
#host = socket.gethostname()
port = 63205
com_port_name = 'COM100'
filename_dynamic = "Lakeshore331-Log-Dynamic.dat"

class RepeatedTimer(object):
    
    def __init__(self, interval, function, *args):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class pressure_server():

    global host, port, com_port_name, filename_dynamic    

    def __init__(self):

        super(self.__class__, self).__init__()
        self.counter = 0
        self.flag = 0
        self.pressure=''
        self.old_filename=""
        print ('new server initialized')
        
        with open(filename_dynamic,"w+") as f:            
            f.write ('Time, Temperature_A, Temperature_B \n')
    
    def on_new_client(self,clientsocket,addr):
        
        while True:
            time.sleep(0.5)     # while loop discriminator - otherwise overload
            msg = clientsocket.recv(1024)
#            print (addr, ' >> ', msg)           
            if not msg: 
                self.counter -= 1
                break            
            if msg == 'so you think you can tell':
                clientsocket.send(self.temp.encode()) 
            else:
                print ("sending command to Lakeshore: ", msg)
                value = send_command(com_port_name,msg)
                clientsocket.send(value.encode())
        
        print (str(self.counter))
        clientsocket.shutdown(socket.SHUT_RDWR)   
        clientsocket.close()

    def start(self):    
                    
        print ('starting pressure measure thread')
    
        
        self.t = RepeatedTimer(1, self.update_pressure_thread)
        
        self.s = socket.socket()         # Create a socket object
        
        print ('Server started!')
        print ('Waiting for clients...')
        
        self.s.bind((host, port))        # Bind to the port
        self.s.listen(5)                 # Now wait for client connection.
#        self.s.settimeout(20)

        while True:
            
            try:
                time.sleep(1)       # while loop discriminator - otherwise overload
                print ('now will try to accept connection')
                print (str(self.counter))
                c, addr = self.s.accept()     # Establish connection with client.
                print ('Got connection from', addr)
                self.counter += 1    
                _thread.start_new_thread(self.on_new_client,(c,addr))
            except:
                pass
            
            if self.counter == 0:        
                self.flag = 1
                break
                print ('breaking while loop')
        
        try:
            self.s.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.s.close()
        self.t.stop()
    
    def update_pressure_thread(self):
        try:
            self.temp = send_command(com_port_name,"KRDG?A")[:-1]+","+send_command(com_port_name, "KRDG?B")[:-1]
            print (self.temp)
        except:
            print ('no pressure received')
            pass
        
        """ here we will log the data to a file """
        filename = "Lakeshore331_Log_"+dt.datetime.now().strftime("%y-%m-%d")+".dat"
        
        """ empty dynamic file if new day """
        if (self.old_filename != filename):
            with open(filename_dynamic,"w+") as f:            
                f.write ('Time, Temperature_A, Temperature_B \n')
        self.old_filename = filename
        
        """ write the value into dynamic file and copy it to log file """
        with open(filename_dynamic,"a+") as f:
            try:
                self.temperature_A = float(self.temp.split(",")[0])
                self.temperature_B = float(self.temp.split(",")[1])
            except:
                self.temperature_A = 0.0
                self.temperature_B = 0.0
                pass
            if (self.temperature_A < 500.0) and (self.temperature_B < 500.0):
                f.write (dt.datetime.now().strftime("%H:%M:%S")+
                         ', '+str(self.temperature_A)+', '+str(self.temperature_B)+'\n')
        shutil.copy2(filename_dynamic, filename) # target filename is /dst/dir/file.ext
 

def new_server():

    print ('no connection - starting a new server')
    server_5 = pressure_server()
    server_5.start()

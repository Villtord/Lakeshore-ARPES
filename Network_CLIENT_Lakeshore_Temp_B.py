# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:53:30 2018

@author: Victor Rogalev
"""

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal,QTimer,QThread
import sys, gc, socket
import select

from UI_simple import Ui_MainWindow

global host, port

host = '132.187.37.41'
#host = socket.gethostname()
port = 63205


class pressure_get_value(QThread):
    
    global host, port
    
    new_value_trigger = pyqtSignal('QString')
    
    def __init__(self, *args, **kwargs):      

        super(self.__class__, self).__init__()        
        print ("get_value initializeed")
        self.connection_flag = False
        print (self.connection_flag)

    def check_connection(self):
        
        if not self.connection_flag:
            print ('establishing connection')
            print ('host is ', host)
            self.mySocket = socket.socket()
            try:
                self.mySocket.connect((host,port))
                self.connection_flag = True
                print ('connection established')
                self.update_pressure()
            except: 
                self.connection_flag = False
                self.mySocket.close()
                print ('no connection')
        else:
            self.update_pressure()
        			
    def update_pressure(self):        
               
        try:
            print (self.mySocket.getsockname())
            message = 'so you think you can tell'
            print ('attepmt to send: ', message)
            self.mySocket.setblocking(0)
            try:
                self.mySocket.send(message.encode())
                print ('message send')
                timeout = 1
                ready = select.select([self.mySocket],[],[],timeout)
                if ready[0]:
                    self.pressure = self.mySocket.recv(1024).decode() 
                    print ('Received from server: ' + self.pressure) 
            except:
                print ('error here')
                self.connection_flag = False
                pass
            self.new_value_trigger.emit(self.pressure)
        except:
            pass
        
    def close (self):
        
        try: 
            self.mySocket.close()
        except:
            pass

        
class ExampleApp(QWidget, Ui_MainWindow):
            
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)
        
        self.networking = pressure_get_value()
        self.start()
      
    def resizeEvent(self, evt):

        font = self.font()
        font.setPixelSize(self.height()*0.7)
        self.label.setFont(font)
        self.label.setGeometry(0, 0, self.width(), self.height())
        gc.collect()

    def start(self):

        start_pressure="100"
        self.label.setText(start_pressure)
        self.label.setStyleSheet("QLabel { background-color : green; color : orange; }")
        
        self.timer_x = QTimer(self)
        self.timer_x.timeout.connect(self.networking.check_connection)        
        self.timer_x.start(1000)

        self.networking.new_value_trigger.connect(self.update_screen)
        
        self.networking.start()

        gc.collect()
        
    def update_screen(self, pressure):
        
        """ Here we process the value received from server and choose channel A split[0] or B split[1] """
        try:
            self.pressure = float(pressure.split(",")[1])
            if (self.pressure < 500):
                self.label.setText(str(self.pressure))
        except:
            pass
        gc.collect()
    
    def __del__ (self):

        try:
            self.networking.mySocket.close()
        except:
            pass
        self.timer_x.stop()
        self.timer_x.deleteLater()
        
    def closeEvent(self,event):

        try:
            self.networking.mySocket.close()
        except:
            pass
        self.timer_x.stop()
        self.timer_x.deleteLater()


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.setWindowTitle("Lakeshore331_Temp_A - client")
    form.resize (380,150)
    form.show()                         # Show the form
    sys.exit(app.exec_())

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

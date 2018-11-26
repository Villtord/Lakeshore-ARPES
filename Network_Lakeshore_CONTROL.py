# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 17:07:57 2018

@author: Victor
"""


from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal,QTimer,QThread
import sys, gc, socket, select

from UI_simple_2 import Ui_MainWindow

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
    
    global host, port
            
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)
        
        self.StyleSheetOn = "QRadioButton::indicator {width: 15px; height: 15px; border-radius: 7px;} QRadioButton::indicator:unchecked { background-color: lime; border: 2px solid gray;}"
        self.StyleSheetOff= "QRadioButton::indicator {width: 15px; height: 15px; border-radius: 7px;} QRadioButton::indicator:unchecked { background-color: black; border: 2px solid gray;}"
        
        
        self.networking = pressure_get_value()
        self.start()
      
    def resizeEvent(self, evt):
        
        font = self.font()
        if float (self.height()/self.width())<=1.5:
            font.setPixelSize(self.height()*0.45)
        self.label.setFont(font)
        self.label.setGeometry(0, 0, self.width(), self.height()*0.7)
        self.lineEdit.setGeometry(0, self.height()*0.75, self.width()*0.4, self.height()*0.3)
        self.pushButton.setGeometry(self.width()*0.5, self.height()*0.75, self.width()*0.5, self.height()*0.3)
        gc.collect()

    def start(self):

        start_pressure="A:273"
        self.label.setText(start_pressure)

        self.pushButton.clicked.connect(self.control_setpoint)
        self.lineEdit.editingFinished.connect(self.renew_setpoint)
        
        self.timer_x = QTimer(self)
        self.timer_x.timeout.connect(self.networking.update_pressure)        
        self.timer_x.start(1000)

        self.networking.new_value_trigger.connect(self.update_screen)
        
        self.networking.start()

        gc.collect()
        
    def control_setpoint(self):
        
        if self.pushButton.text() == "Start T control":
            
            self.pushButton.setText("STOP")
            self.power = 0
            self.radiobutton.setStyleSheet(self.StyleSheetOn)
            
            """ Set a setpoint """  
            try:
                print ("user command: "+"SETP 1,"+str(self.lineEdit.text()))
                self.send_network_command("SETP 1,"+str(self.lineEdit.text()))
            except:
                print ('can not set setpoint')
                pass 

            """ Set a low power mode """
            try:
                self.power = int(self.send_network_command("RANGE 1;RANGE?"))
                print(str(self.power))
            except:
                print ('can not set low power mode')
                pass  
            
            """ Just for safety reasons check if the power is low """                        
            if self.power != 1:    
                print ("power is not correct - switching off")
                self.send_network_command("RANGE 0")
 

                
        else:
            """ Stop heater """
            self.send_network_command("RANGE 0")
            self.pushButton.setText("Start T control")
            self.radiobutton.setStyleSheet(self.StyleSheetOff)
            print ("user command - heater stop")
            
            
    def renew_setpoint(self):
        """ Set a new setpoint """  
        try:
            print ("user command: "+"SETP 1,"+str(self.lineEdit.text()))
            self.send_network_command("SETP 1,"+str(self.lineEdit.text()))
        except:
            print ('can not set setpoint')
            pass 
    
    def send_network_command(self, message):
        
        self.mySocket = socket.socket()
        try:
            self.mySocket.connect((host,port))
            print ('connection established')
            self.update_pressure()
        except: 
            self.mySocket.close()
            print ('no connection')
        
        try:
            print (self.mySocket.getsockname())
            print ('attepmt to send: ', message)
            self.mySocket.setblocking(0)
            try:
                self.mySocket.send(message.encode())
                print ('message send')
                timeout = 1
                ready = select.select([self.mySocket],[],[],timeout)
                if ready[0]:
                    self.value = self.mySocket.recv(1024).decode() 
                    print ('Received from server: ' + self.value) 
            except:
                print ('error here')
                pass
        except:
            pass
        return (self.value)
        
    def update_screen(self, pressure):
        """ Here we process the value received from device """
        try:
            self.pressure = float(pressure)
            if (self.pressure < 500):
                if self.pressure == 0:
                    self.label.setText("A:"+"OVER")
                else:
                    self.label.setText("A:"+str(self.pressure))
        except:
            if pressure == "None":
                self.label.setText("A:"+pressure)
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
    form.resize (350,180)
    form.show()                         # Show the form
    sys.exit(app.exec_())

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function



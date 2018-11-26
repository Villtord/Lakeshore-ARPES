# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\UI_simple.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import gc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
#        MainWindow.resize(250,150)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(15, 15, MainWindow.width()-30, MainWindow.height()-30))
        self.widget.setObjectName("widget")
        self.widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        

        
        """ Label with actual temperature A. should we add B?"""
        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet("QLabel { background-color : darkgreen; color : white; }")
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setLineWidth(1)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        
        """ Lower part of the panel - setpoint and start/stop button """
        self.horizontal_widget = QtWidgets.QWidget(self)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontal_widget)
        self.horizontalLayout.setObjectName("verticalLayout")
        
        StyleSheetOn = "QRadioButton::indicator {width: 15px; height: 15px; border-radius: 7px;} QRadioButton::indicator:unchecked { background-color: lime; border: 2px solid gray;}"
        StyleSheetOff= "QRadioButton::indicator {width: 15px; height: 15px; border-radius: 7px;} QRadioButton::indicator:unchecked { background-color: black; border: 2px solid gray;}"
        
        self.radiobutton = QtWidgets.QRadioButton(self.horizontal_widget)
        self.radiobutton.setStyleSheet(StyleSheetOff)
        self.radiobutton.setObjectName("radiobutton")

        self.lineEdit = QtWidgets.QLineEdit(self.horizontal_widget)
        self.lineEdit.setStyleSheet("QLineEdit{font:bold;font-size: 16px;font-family: Arial;color: rgb(255, 0, 0);background-color: rgb(38,56,76);}")
        self.lineEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.lineEdit.setToolTip("Setpoint in K")
        self.lineEdit.setStatusTip("")
        self.lineEdit.setText("283")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setFrame(False)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        
        self.pushButton = QtWidgets.QPushButton(self.horizontal_widget)
        self.pushButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.pushButton.setText("Start T control")
        self.pushButton.setStyleSheet("QPushButton{font: bold; font-size: 16px;font-family: Arial;color: rgb(255, 255, 255);background-color: rgb(50,56,76);}")
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayout.addWidget(self.radiobutton)                        
        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.addWidget(self.pushButton)
        
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.horizontal_widget)
 
        gc.collect()
    




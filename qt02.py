#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):      
        btn1 = QPushButton("Buton 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Buton 2", self)
        btn2.move(150, 50)
      
        btn1.clicked.connect(self.buttonClicked)            
        btn2.clicked.connect(self.buttonClicked3)
        
        self.statusBar()
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Basit uygulama')
        self.show()
        
        
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' tıklandı')
        
    def buttonClicked2(self):
        sender = self.sender()
        cmd = "echo 'icerik01' >> ornekdosya.txt"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cikti=proc.communicate()
        
    def buttonClicked3(self):
        sender = self.sender()
        cmd = "echo 'icerik - "+sender.text()+"' >> ornekdosya.txt"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cikti=proc.communicate()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

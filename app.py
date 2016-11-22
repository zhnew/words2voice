#!/usr/bin/python3
# -*- coding: utf-8 -*-

#word to voice app

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication,QPushButton,QComboBox,QLabel)
from PyQt5.QtGui import QIcon,QColor
import words2voice
from datasbuilder import *
#import dictvoice

class W2VApp(QMainWindow):
    
    def __init__(self):
        super(W2VApp,self).__init__()
        self._initUI()
        self.wordfile=""

        self.thread=words2voice.W2Vthread(self)
        self.thread.update.connect(self.updateText)

        
    def _initUI(self):      
    
        btn2=QPushButton("words import",self)
        btn2.move(30,40)

        btn2.clicked.connect(self.selectwords)

        self.textShow=QTextEdit(self)
        self.textShow.setReadOnly(True)
        self.textShow.setTextColor(QColor('red'))
        self.textShow.setTextBackgroundColor(QColor('gray'))
        self.textShow.setFixedSize(450,650)
        self.textShow.move(159,40)
        
        label1=QLabel("interval",self)
        label1.move(30,80)
        combo1 = QComboBox(self)
        combo1.addItem("0.5")
        combo1.addItem("0.7")
        combo1.addItem("0.9")
        combo1.addItem("1.1")
        combo1.addItem("1.3")
        combo1.addItem("1.5")
        combo1.setFixedSize(50,30)
        combo1.move(90,80)
        combo1.findText("0.7")
        self.combo1=combo1

        label2=QLabel("timesleep",self)
        label2.move(30,120)
        combo2 = QComboBox(self)
        combo2.addItem("0.5")
        combo2.addItem("0.7")
        combo2.addItem("0.9")
        combo2.addItem("1.1")
        combo2.addItem("1.3")
        combo2.addItem("1.5")
        combo2.addItem("2.0")
        combo2.setFixedSize(50,30)
        combo2.move(90,120)
        combo2.findText("1.3")
        self.combo2=combo2
        
        btn3 = QPushButton("start",self)
        btn3.move(30,160)

        btn4=QPushButton('pause',self)
        btn4.move(30,200)
        self.btn4=btn4

        btn5=QPushButton("stop",self)
        btn5.move(30,240)
        
        btn6=QPushButton("export",self)
        btn6.move(30,350)
        
        btn3.clicked.connect(self.startPlay)
        btn4.clicked.connect(self.pausePlay)
        btn5.clicked.connect(self.stopPlay)
        btn6.clicked.connect(self.exportWords)
        
        self.setGeometry(300, 100, 650, 700)
        self.setWindowTitle('words speaker')
        self.show()
        
    def selectwords(self):

        f=QFileDialog.getOpenFileName(self,'Open file','d:\Users\zhn\Desktop\doc')
        text=self.textShow.toPlainText()
        text+="\n"+"words files is: "+f[0]
        self.textShow.setText(text)
        self.wordfile=f[0]

    def updateText(self,w):
        text='<h2>'+w+'</h2>'+text2html(getWord(w))
        self.textShow.setHtml(text)

    def startPlay(self):
        interval=float(str(self.combo1.currentText()))
        timesleep=float(str(self.combo2.currentText()))
        if  self.thread.isStopped():  
            self.thread.setWordFile(self.wordfile)
            self.thread.setparams(interval,timesleep)
            self.thread.start()

    def pausePlay(self):
        print self.thread.isRunning()
        if self.thread.isRunning():
            if pauseLock.locked():
                self.btn4.setText("pause")
                pauseLock.release()
            else:
                self.btn4.setText("continue")
                interval=float(str(self.combo1.currentText()))
                timesleep=float(str(self.combo2.currentText()))
                self.thread.setparams(interval,timesleep)
                pauseLock.acquire()

    def stopPlay(self):
        self.thread.setStop(True)

    def exportWords(self):
        print "export words"
    
    def closeEvent(self,e):
        if pauseLock.locked():
            pauseLock.release()
        self.thread.setStop(True)
        super(W2VApp,self).closeEvent(e)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = W2VApp()
    sys.exit(app.exec_())

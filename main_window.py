import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import  QScrollArea, QGridLayout, QPushButton, QVBoxLayout, QDialog

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import *
from PyQt5 import uic

from new_dialog import NewDialog
from project_data import ProjectData
from drawing import *
from symbol_button import *
from fontgen import *
from fontread import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/fontgen.ui', self)
        
        self.setLayout(QtWidgets.QVBoxLayout())
        
        self.projectData = ProjectData()
        self.projectData.x = 9
        self.projectData.y = 9
        self.projectData.name = "expfont"
        
        self.gridSizeEdit.setText(str(self.projectData.gridSize))
        self.gridSizeEdit.editingFinished.connect(self.changeGridSize)
        
        vbox = QVBoxLayout() 
        self.generateAsciiButtons(vbox)
        self.scrollWidget.setContentsMargins(0,0,0,0)
        self.scroll.setContentsMargins(0,0,0,0)
        vbox.setContentsMargins(2,2,0,0)
        self.scrollWidget.setFixedHeight((30) * (256))
        self.scrollWidget.setLayout(vbox)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.selectedSymbol = self.asciiSymbols[0]
        self.resetButtonColors()
        
        self.drawingArea:DrawingArea = DrawingArea(self.drawingScrollAreaWidget,  self.projectData.x, self.projectData.y, self.projectData.gridSize)
        #self.drawingScrollAreaWidget//.addWidget(self.drawingArea)
        self.initProgramLoop()
        
        
        self.actionNew.triggered.connect(self.createNewFileDialog)
        self.actionOpen.triggered.connect(self.readProjectDialog)
        self.actionGenerateFiles.triggered.connect(self.generateFiles)
        
        self.currentAsciiLabel = QLabel("ASCII    ")
        self.statusbar.addWidget( QLabel("   "))
        self.statusbar.addWidget(self.currentAsciiLabel)
        
        self.currentSizeLabel = QLabel("SIZE:" + str(self.projectData.x) + "x" + str(self.projectData.y)+ "  ")
        self.statusbar.addWidget( QLabel("   "))
        self.statusbar.addWidget(self.currentSizeLabel)
        
        self.currentPosX = QLabel("X:0 ")
        self.statusbar.addWidget( QLabel("   "))
        self.statusbar.addWidget(self.currentPosX)
        self.currentPosY = QLabel("Y:0 ")
        self.statusbar.addWidget( QLabel("   "))
        self.statusbar.addWidget(self.currentPosY)
        
        
    def generateAsciiButtons(self, vbox):
        self.asciiSymbols = []
        for i in range(0,256):  
            self.asciiSymbols.append(SymbolButton(self.scrollWidget, chr(i) + " (" + str(i) + ")", self.projectData.x, self.projectData.y, None, self.symbolSelectCallback))
            self.asciiSymbols[-1].setFixedSize(100,25)
            self.asciiSymbols[-1].move(5, i * 28)
            
            
    def programLoop(self):
        if self.projectData.restart:
            self.projectData.restart = False
            self.restartProject()

    def restartProject(self):
        self.drawingArea.reinitDrawingArea(self.projectData.x, self.projectData.y, self.projectData.gridSize)
        self.currentSizeLabel.setText("SIZE:" + str(self.projectData.x) + "x" + str(self.projectData.y))
        self.drawingArea.update()
        for s in self.asciiSymbols:
            s.resetBitMap(self.projectData.x, self.projectData.y, None)
        pass
       
    def resetButtonColors(self):  
        for s in self.asciiSymbols:
            s.setStyleSheet("background-color: white")
        
    def symbolSelectCallback(self, symbol):
        self.resetButtonColors()
        symbol.setStyleSheet("background-color: lightblue")
        self.selectedSymbol = symbol
        self.currentAsciiLabel.setText("ASCII: " + symbol.text())
        self.drawingArea.bitMap = symbol.bitMap
        self.drawingArea.update()
        pass
    
            
    def initProgramLoop(self):
        timer = QTimer(self)
        timer.setInterval(100)
        timer.setSingleShot(False)
        timer.timeout.connect(self.programLoop)
        timer.start()
        return timer
            
    @QtCore.pyqtSlot()
    def createNewFileDialog(self):
        newDialog = NewDialog(self, self.projectData)   
        newDialog.exec() 
        
    @QtCore.pyqtSlot()
    def readProjectDialog(self):
        readDialog = ReadDialog(self, self.projectData, self.asciiSymbols)
        readDialog.exec()
    
    @QtCore.pyqtSlot()  
    def generateFiles(self):
        font = GeneratedFont(self.projectData.name, self.projectData.x, self.projectData.y, self.asciiSymbols)

    @QtCore.pyqtSlot() 
    def changeGridSize(self):
        newGridSize = int(self.gridSizeEdit.text())
        if newGridSize > 0 and newGridSize < 100:            
            self.projectData.gridSize = newGridSize
        else:
            self.projectData.gridSize = 20
        self.drawingArea.reinitDrawingArea(self.projectData.x, self.projectData.y, self.projectData.gridSize, self.selectedSymbol.bitMap)
        self.drawingArea.update()

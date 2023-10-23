import os
import re

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTime

from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QTimeEdit
)

from symbol_button import *
from project_data import *

class ReadDialog(QDialog):
    def __init__(self, parent, projectData:ProjectData, asciiSymbols:SymbolButton):
        super().__init__(parent)
        uic.loadUi('ui/dialog_read.ui', self)
        self.projectData = projectData
        self.selectButton.clicked.connect(self.selectFilepath)
        self.openButton.clicked.connect(self.readProject)
        self.projectPath = ""
        self.asciiSymbols = asciiSymbols
        self.lines = []
        self._parent = parent
        
    def readProject(self):
        file = open(self.projectPath, 'r')
        self.lines = file.readlines()
        self.dataLineStart = self.readStartLine()
        self._parent.restartProject()
        self.readDataContent(self.dataLineStart)
        self.close()
        
        
    def readStartLine(self):
        for j, line in enumerate(self.lines):
            if "[] =" in line:
                csplit = line.split('[')[0]
                csplit = csplit.split("uint8_t ")[1]
                for i, c in enumerate(reversed(csplit)):
                    rei = len(csplit) - i
                    if c == "x":
                        y = int(csplit[rei:])
                        self.projectData.y = y
                        name = csplit[:rei - 1]
                        f = filter(str.isalpha, name)
                        name = "".join(f)
                        self.projectData.name = name
                        x = csplit[:rei - 1]
                        f = filter(str.isdigit, x)
                        x = int("".join(f))
                        self.projectData.x = x
                        print("x = ", self.projectData.x)
                        print("y = ", self.projectData.y)
                        print("name = ", name)
                        return j + 1
                        
    def readDataContent(self, startLine):
        x:int = 0
        y:int = 0
        symbolIndex:int = 0
        
        for s in self.asciiSymbols:
            s.resetBitMap(self.projectData.x, self.projectData.y, None)
        
        for line in self.lines[startLine:]:
            lineArray = (line.replace(" ", "").replace("\n", "")).split(",")
            if '' in lineArray:
                lineArray.remove('')
            #if '};' in lineArray:
            #    return
            
            print(lineArray)
            for elem in lineArray:
                if "}" in elem:
                    if symbolIndex >= len(self.asciiSymbols):
                        return
                    self.asciiSymbols[symbolIndex].update()
                    return
                val = int(elem, 0)
                for j in range(7,-1,-1):
                    print(j)
                    if isBitSet(val, j):
                        self.asciiSymbols[symbolIndex].bitMap[y][x] = 1
                    x += 1
                    if x >= self.projectData.x:
                        x = 0
                        y += 1
                    if y >= self.projectData.y:
                        if symbolIndex >= len(self.asciiSymbols):
                            return
                        self.asciiSymbols[symbolIndex].update()
                        symbolIndex += 1
                        y = 0
                        

    def selectFilepath(self):
        projectPath = QFileDialog.getOpenFileName(self, 'Open font source file', os.getcwd())[0]
        print(projectPath)
        self.filepathEdit.setText(projectPath)
        self.projectPath = projectPath
        
        
def isBitSet(x, n):
    return x & 2 ** n != 0 
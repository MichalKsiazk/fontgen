from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
import sys


class DrawingArea(QWidget):
    def __init__(self, parent, x, y, gridSize):
        
        super(DrawingArea, self).__init__(parent)
      
        self.reinitDrawingArea(x, y, gridSize)     
        self.setContentsMargins(0, 0, 0, 0)
        pass

    def reinitDrawingArea(self, x, y, gridSize, bitMap=None):
        self.width = x * gridSize
        self.height = y * gridSize
        self.x = x
        self.y = y
        self.gridSize = gridSize
        if bitMap is None:
            self.bitMap = [[0 for z in range(x)] for c in range(y)]
        else:
            self.bitMap = bitMap
        self.setGeometry(5, 5, self.width, self.height)

    def mousePressEvent(self, event):
        px = int(event.x() / self.gridSize)
        py = int(event.y()  / self.gridSize)
        if event.button() == Qt.LeftButton:
            self.bitMap[py][px] = 1
        if event.button() == Qt.RightButton:
            self.bitMap[py][px] = 0
        self.update()

    def mouseReleaseEvent(self, event):
        pass
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        self.drawOuterBorder()
        self.drawGrid()
        self.drawBitMap()
        
    def drawOuterBorder(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        painter.drawRect(0, 0, self.width, self.height)
    
    def drawGrid(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for x in range(0, self.x):
            painter.drawLine(x * self.gridSize, 0, x * self.gridSize, self.height)
        for y in range(0, self.y):
            painter.drawLine(0, y * self.gridSize, self.width, y * self.gridSize)
            
    def drawBitMap(self):
        painter = QPainter(self)
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        for y in range(self.y):
            for x in range(self.x):
                if self.bitMap[y][x]:
                    x0 = x * self.gridSize
                    y0 = y * self.gridSize
                    painter.drawRect(x0, y0, self.gridSize, self.gridSize)
                    
                
                
        

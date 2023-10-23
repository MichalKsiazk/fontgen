from PyQt5.QtWidgets import  QScrollArea, QGridLayout, QPushButton, QVBoxLayout, QDialog

class SymbolButton(QPushButton):
    def __init__(self, parent, name, x, y, bitMap, onClickCallback):
        super(SymbolButton, self).__init__(parent)
        self.resetBitMap(x, y, bitMap)
        self.setText(name)    
        self.clicked.connect(self.onclick)
        self.onClickCallback = onClickCallback
            
    def resetBitMap(self, x, y, bitMap):
        self.x = x
        self.y = y
        if bitMap is None:
            self.bitMap = [[0 for z in range(x)] for c in range(y)]
        else:
            self.bitMap = bitMap
            
    def onclick(self):
        print(self.text())
        self.onClickCallback(self)

    def isEmpty(self):
        empty:bool = True
        for r in self.bitMap:
            if any(r):
                empty = False
                return False
        return True
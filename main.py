import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from main_window import *


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

window.show()
app.exec_()
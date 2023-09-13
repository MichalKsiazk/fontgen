import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTime

from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QTimeEdit
)

from project_data import ProjectData

class NewDialog(QDialog):
    def __init__(self, parent, projectData:ProjectData):
        super().__init__(parent)
        uic.loadUi('ui/dialog_new.ui', self)
        self.projectData = projectData
        self.startButton.clicked.connect(self.start_new_project)
        
    def start_new_project(self):
        self.projectData.x = self.spinX.value()
        self.projectData.y = self.spinY.value()
        self.projectData.name = self.lineEdit.text()
        self.projectData.restart = True
        self.close()
        

import json
import os
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

#custom classes
from map_manager import MapManager

CURRENT_DIRECTORY = Path(__file__).resolve().parent


class testGlyph(QtWidgets.QWidget):
    def __init__(self, parent=None, color1='red', color2='blue', w=100, h=200):
        super().__init__(parent)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.color1 = color1
        self.color2 = color2
        self.width = w
        self.height = h
        self.scale = 1.0
        self.x = 0
        self.y = 0
        
    def sizeHint(self):
        return QtCore.QSize(self.width, self.height)

    def move(self, x, y, scale):
        self.scale = scale
        w = int(scale * self.width)
        h = int(scale * self.height)
        self.x = x
        self.y = y
        self.setGeometry(QtCore.QRect(x,y,w,h))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QColor(self.color1))
        brush.setStyle(Qt.SolidPattern)
        
        w2 = int(self.scale * self.width/2)
        h2 = int(self.scale * self.height/2)
        rect = QtCore.QRect(0,0,w2,h2)

        
        painter.fillRect(rect, brush)

        brush.setColor(QColor(self.color2))
        rect = QtCore.QRect(w2,h2,w2,h2)

        painter.fillRect(rect,brush)



class holder(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(holder, self).__init__(*args, **kwargs)
        self.setMinimumSize(860,540)
        #layout = QtWidgets.QVBoxLayout()
        self.g1 = testGlyph(self)
        self.g1.move(50,50,2.0)
        #layout.addWidget(self.g1)
        self.g2 = testGlyph(self, 'black','green')
        #self.g2.move(0,50,1.0)
        self.g2.setGeometry(QtCore.QRect(0,50,100,200))
        #layout.addWidget(self.g2)

        #self.setLayout(layout)

        button = QPushButton('PyQt5 button', self)
        button.move(0,0)
        button.clicked.connect(self.moveG1)

    def moveG1(self):
        self.g1.move(self.g1.x+1,self.g1.y+1,1.0)
        

    
import time
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    vol = holder()
    vol.show()
    app.exec_()
    vol.moveG1()

    

    sys.exit()

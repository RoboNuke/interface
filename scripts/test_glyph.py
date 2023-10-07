import sys
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class TestGlyph(QWidget):
    def __init__(self, parent=None, lat=0.0, lng=0.0, color="red"):
        super().__init__(parent)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.setLatLng(lat, lng)

        self.width = 200
        self.height = 100
        self.color = color

    def sizeHint(self):
        return QSize(self.width, self.height)

    def moveScalePixel(self, x, y, scale):
        self.scale = scale
        w = int(scale * self.width/2.0)
        h = int(scale * self.height/2.0)
        self.x = x
        self.y = y
        self.setGeometry(QtCore.QRect(x-w,y-h,2*w,2*h))
        #self.setGeometry(QtCore.QRect(0,0,400,200))
        
    def setLatLng(self, lat, lng, scale=1.0):
        self.lat = lat
        self.lng = lng
        self.scale = scale

    def paintEvent(self, event):
        painter = QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QColor(self.color))
        brush.setStyle(Qt.SolidPattern)
        
        w2 = int(self.scale * self.width)
        h2 = int(self.scale * self.height)
        rect = QtCore.QRect(0,0,w2,h2)

        painter.fillRect(rect, brush)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    g = TestGlyph()
    g.show()
    sys.exit(app.exec_())

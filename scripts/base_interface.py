import json
import os
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel

#custom classes
from map_manager import MapManager, MapTracker
from test_glyph import TestGlyph

CURRENT_DIRECTORY = Path(__file__).resolve().parent

PERM_GRANTED = QtWebEngineWidgets.QWebEnginePage.PermissionGrantedByUser

class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        
        self.setMinimumSize(1920,1080)

        
        self.map_manager = MapManager(self)
        self.map_manager.clicked.connect(self.mapClickedCB)
        self.tracker = MapTracker()
        self.map_manager.mapMoved.connect(self.tracker.updateMapLimits)
        self.map_manager.mapMoved.connect(self.mapMovedCB)
        
        self.view = QtWebEngineWidgets.QWebEngineView()
        channel = QtWebChannel.QWebChannel(self.view)
        channel.registerObject("map_manager", self.map_manager)
        self.view.page().setWebChannel(channel)
        filename = os.fspath(CURRENT_DIRECTORY / "index.html")
        url = QtCore.QUrl.fromLocalFile(filename)
        self.view.load(url)

        self.button = QtWidgets.QPushButton("Place Glyph")
        self.button.setFixedSize(100,50)
        self.button.clicked.connect(self.placeGlyphButtonCB)
        self.placeGlyph = False
        
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.button)
        lay.addWidget(self.view)

        self.view.page().featurePermissionRequested.connect(self.permissionRequested)
        self.glyphs = []

    def placeGlyphButtonCB(self):
        self.placeGlyph = True

    def mapClickedCB(self, lat, lng):
        if self.placeGlyph:
            ng = TestGlyph(self.view, lat, lng, 'red')
            x,y,scale = self.tracker.convertLatLng2Pixels(lat, lng)
            ng.moveScalePixel(x,y,scale)
            ng.show()
            self.glyphs.append(ng)
            self.placeGlyph = False
        
    def permissionRequested(self, frame, feature):
        self.view.page().setFeaturePermission(frame, feature, PERM_GRANTED)

    def mapMovedCB(self, data):
        for gl in self.glyphs:
            x,y,scale = self.tracker.convertLatLng2Pixels(gl.lat, gl.lng)
            gl.moveScalePixel(x,y,scale)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = Interface()
    w.show()

    sys.exit(app.exec_())

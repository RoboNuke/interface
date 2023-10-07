import json
import os
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel

#custom classes
from map_manager import MapManager

CURRENT_DIRECTORY = Path(__file__).resolve().parent

PERM_GRANTED = QtWebEngineWidgets.QWebEnginePage.PermissionGrantedByUser

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._was_clicked = False

        self.setMinimumSize(1920,1080)
        self.button = QtWidgets.QPushButton("Press me")
        self.button.setFixedSize(200,100)
        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.label.setFixedSize(1920,25)

        self.view = QtWebEngineWidgets.QWebEngineView()
        map_manager = MapManager(self)
        channel = QtWebChannel.QWebChannel(self.view)
        channel.registerObject("map_manager", map_manager)
        self.view.page().setWebChannel(channel)
        filename = os.fspath(CURRENT_DIRECTORY / "index.html")
        url = QtCore.QUrl.fromLocalFile(filename)
        self.view.load(url)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.button)
        lay.addWidget(self.label)
        lay.addWidget(self.view)

        map_manager.clicked.connect(self.handle_map_clicked)
        self.view.page().featurePermissionRequested.connect(self.permissionRequested)
        print(type(self.view),type(self.view.page()))
        self.button.clicked.connect(self.handle_button_clicked)

    def handle_map_clicked(self, lat, lng):
        if self._was_clicked:
            self.label.setText(f"latitude: {lat} longitude: {lng}")
        self._was_clicked = False

    def handle_button_clicked(self):
        self._was_clicked = True

    def permissionRequested(self, frame, feature):
        print(type(frame),type(feature))
        self.view.page().setFeaturePermission(frame, feature, PERM_GRANTED)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())

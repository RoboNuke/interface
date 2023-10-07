
from PyQt5 import QtCore

class MapManager(QtCore.QObject):
    clicked = QtCore.pyqtSignal(float, float)

    @QtCore.pyqtSlot(str, str)
    def receive_data(self, message, json_data):
        data = json.loads(json_data)
        if message == "click":
            self.clicked.emit(data["lat"], data["lng"])

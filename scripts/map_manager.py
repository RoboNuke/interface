
from PyQt5 import QtCore
import json
class MapManager(QtCore.QObject):
    clicked = QtCore.pyqtSignal(float, float)
    mapMoved = QtCore.pyqtSignal(object)
    
    @QtCore.pyqtSlot(str, str)
    def receive_data(self, message, json_data):
        data = json.loads(json_data)
        if message == "click":
            self.clicked.emit(data["lat"], data["lng"])
        elif message == "move":
            self.mapMoved.emit(data)
        elif message == "init":
            self.mapMoved.emit(data)
        else:
            print(message,":",data)


class MapTracker():
    def __init__(self):

        # map vars
        self.mapCenter = []
        self.mapCorners = {"N":0.0, "S":0.0, "E":0.0, "W":0.0}
        self.zoomLevel = -1
        self.baseZoom = 15
        
        # container vars
        self.pxCenter = []
        self.pxSize = []
        self.scale = -1
        #print('init')

    def calcScale(self):
        self.scale = float(self.zoomLevel)/float(self.baseZoom)
        self.scale = max((self.scale - 1.0) * 4 + 1.0,0.0)
        #print(self.scale)

        
    def updateMapLimits(self, data):
        cen = data[0]
        corners = data[1]
        pixSize = data[2]
        zoom = data[3]

        
        self.mapCenter = [cen['lat'], cen['lng']]
        self.zoomLevel = zoom
        self.calcScale()
        self.pxSize = [pixSize['x'], pixSize['y']]

        self.mapCorners["S"] = corners['_southWest']['lat']
        self.mapCorners["N"] = corners['_northEast']['lat']
        self.mapCorners["E"] = corners['_northEast']['lng']
        self.mapCorners["W"] = corners['_southWest']['lng']
        #print(self.mapCorners)

    def convertLatLng2Pixels(self, lat, lng):

        # (x - min)/(max-min) * pix
        mcs = self.mapCorners
        u = (lng - mcs['W'])/(mcs['E'] - mcs['W']) * self.pxSize[0]
        v = (lat - mcs['N'])/(mcs['S'] - mcs['N']) * self.pxSize[1]

        return [int(u),int(v), self.scale]

    
        

        




import socketio
import sys

from PyQt5.QtCore import pyqtSignal

from Application.Utils.configReader import *
# from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import *
from threading import Thread



class SioClient(QMainWindow):
    sgOnPosition=pyqtSignal(list)
    sgOnTWSWM =pyqtSignal(list)
    sgOnTWM =pyqtSignal(list)

    def __init__(self):
        super(SioClient, self).__init__()
        self.sio = socketio.Client()
        self.emmiters()
        self.IN=0
        self.UP=0


        # self.connect()

    def startSocket(self,token):
        self.token=token
        Thread(target=self.connect).start()


    def connect(self):
        self.sio.connect('http://192.168.113.60:8000')


    def emmiters(self):
        self.sio.on('connect', self.on_connect)
        # self.sio.on('hello', self.on_data)
        self.sio.on('potwData', self.on_position)
        # self.sio.on('potwData', self.UP_on_position)
        self.sio.on('twm', self.on_TWM)
        self.sio.on('twswmData', self.on_TWSWM)
        self.sio.on('disconnect', self.on_disconnect)


    def on_connect(self):
        self.sio.emit('on_message', self.token)
        # self.sio.emit('on_message','hello')
        # self.sio.emit("message", )

        print('Socket connected successfully!')


    def on_disconnect(self):
        print('Socket disconnected successfully.....!')
        self.connect()

    def on_data(self,data):
        # pass
        print(data)

        # print('Socket disconnected successfully!')

    def on_position(self,data):
        self.IN += 1

        # print(self.IN,'POTW',data)
        self.sgOnPosition.emit(data)

    def UP_on_position(self,data):
        self.UP+=1

        print(self.UP,'POTW',data)
        # self.sgOnPosition.emit(data)

    def on_TWM(self,data):
        print('TWM', data)
        self.sgOnTWM.emit(data)

    def on_TWSWM(self,data):
        print('TWSWM', data)
        self.sgOnTWSWM.emit(data)

    def on_margin(self,data):
        pass
        # print(data)
        # self.sgOnMargin.emit(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sio = SioClient()
    sio.connect()
    sys.exit(app.exec_())






import traceback

import socketio
import sys

from PyQt5.QtCore import pyqtSignal

from Application.Utils.configReader import *
# from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread



class SioClient(QMainWindow):

    sgOnPosition=pyqtSignal(list)
    sgOnTWM =pyqtSignal(list)
    sgOnTWSWM =pyqtSignal(list)


    sgOnCMPosition=pyqtSignal(list)
    sgOnCMTWM =pyqtSignal(list)

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
        try:
            self.sio.connect('http://180.211.116.155:3536')
            # self.sio.wait()

        except:
            print(traceback.print_exc(),'trajfkjdkfd')
            # self.messageBox = QMessageBox()
            # # self.messageBox.setIcon(QMessageBox.Critical)
            # # self.messageBox.setWindowTitle('Error')
            # # self.messageBox.setWindowFlags(Qt.WindowStaysOnTopHint)
            # self.messageBox.setText('Server Error..!! ')
            # self.messageBox.show()


    def emmiters(self):
        self.sio.on('connect', self.on_connect)
        self.sio.on('hello', self.on_data)
        self.sio.on('potwData', self.on_position)
        # self.sio.on('potwData', self.UP_on_position)
        self.sio.on('twmData', self.on_TWM)
        self.sio.on('twswmData', self.on_TWSWM)

        #########CASH#########################
        self.sio.on('cmpotwdata',self.on_CMposition)
        self.sio.on('cmtwmdata',self.on_CMTWM)


        self.sio.on('disconnect', self.on_disconnect)


    def on_connect(self):
        self.sio.emit('on_message', self.token)
        # self.sio.emit('on_message','hello')
        # self.sio.emit("message", )

        print('Socket connected successfully!')


    def on_disconnect(self):
        print('Socket disconnected successfully.....!')
        # self.sio.sleep(0.001)
        self.connect()

    def on_data(self,data):
        # pass
        print(data)

        # print('Socket disconnected successfully!')

    def on_CMposition(self,data):
        # self.IN += 1

        # print('POTW',data)
        self.sgOnCMPosition.emit(data)

    def on_CMTWM(self,data):
        # self.IN += 1

        # print('POTW',data)
        self.sgOnCMTWM.emit(data)

    def on_position(self,data):
        self.IN += 1

        # print('POTW',data)
        self.sgOnPosition.emit(data)



    def on_TWM(self,data):
        # print('TWM', data)
        self.sgOnTWM.emit(data)

    def on_TWSWM(self,data):
        # print('TWSWM', data)
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






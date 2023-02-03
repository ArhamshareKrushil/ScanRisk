import json
import traceback
import pickle
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtNetwork
from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket


class CMNotisReader(QMainWindow):
    sgdatasend = pyqtSignal(object)
    sgcount=pyqtSignal(int)

    def __init__(self):

        super(CMNotisReader, self).__init__()
        self.tcpSocket = QTcpSocket(self)

        # self.makeRequest()
        self.isLoggedIn = False
        self.tcpSocket.waitForConnected(1000)

        self.tcpSocket.connected.connect(self.on_connect)
        # self.tcpSocket.readyRead.connect(self.On_readyRead)
        self.tcpSocket.error.connect(self.displayError)
        self.tcpSocket.disconnected.connect(self.on_disconeect)

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.On_readyRead)
        # self.timer.start()

        self.le = QLineEdit(self)
        self.le.setGeometry(20, 20, 200, 20)

        self.pb = QPushButton(self)
        self.pb.setGeometry(20, 70, 200, 20)
        self.pb.clicked.connect(self.sendD)
        self.c = 0

    def on_connect(self):
        print('connected')
        self.timer.start()

    def on_disconeect(self):
        print('disconnected')
        self.isLoggedIn = False
        self.makeRequest()

    def makeRequest(self):
        HOST = '127.0.0.5'
        PORT = 30698
        self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)

    def sendD(self):
        try:
            user = self.le.text()
            dict = {'Type': 'Auth', 'User': 'Arham'}
            print('dict', dict)
            # jd=json.dumps(dict)
            jd = pickle.dumps(dict)
            # print(msg)
            self.tcpSocket.write(jd)

        except:
            print(traceback.print_exc())

    def sendtrade(self):
        dict = {'Type': 'sendTrade', 'Start': 0}
        # jd = json.dumps(dict)
        jd = pickle.dumps(dict)
        print(dict)
        self.tcpSocket.write(jd)

    def On_readyRead(self):
        try:

            # print('Notis')

            if (self.isLoggedIn == False):

                # d = data.decode()
                data = self.tcpSocket.read(1024)
                data = pickle.loads(data)

                if (len(data) > 1):

                    if (data['Type'] == 'AuthRes'):
                        if (data['status'] == 'Connected'):
                            print('Connected...')
                            self.sendtrade()
                            self.isLoggedIn = True


                        else:
                            print('Retry')

            else:
                data = self.tcpSocket.read(1100)

                data = data.decode('UTF-8')
                # print(data)
                if (data != ''):
                    len1 = len(data)
                    # print(len1)

                    if (len1 == 1100):

                        trade = data[:220]

                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[220:440]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[440:660]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[660:880]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[880:1100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1



                    elif (len1 == 880):

                        trade = data[:220]

                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[220:440]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[440:660]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[660:880]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                    elif (len1 == 660):

                        trade = data[:220]

                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[220:440]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[440:660]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                    elif (len1 == 440):

                        trade = data[:220]

                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                        trade = data[220:440]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1

                    elif (len1 == 220):

                        trade = data[:220]

                        i = trade.split(',')
                        self.sgdatasend.emit(i)

                        self.c += 1




                    else:
                        print('invalid legth')

                    # print(self.c)
                    self.sgcount.emit(self.c)

                # data = self.tcpSocket.read(100)
                # data = data.decode('UTF-8')
                # if(data!=' '):
                #     print(data)
                #
                #     if (len(data) > 1):
                #         self.c += 1
                #





        except:
            print(traceback.print_exc())

    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass
        else:
            print(self, "The following error occurred: %s." % self.tcpSocket.errorString())

    def printdd(self):
        print('data')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    client = CMNotisReader()
    client.sgdatasend.connect(client.printdd)
    client.show()
    sys.exit(app.exec_())



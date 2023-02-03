import json
import traceback
import pickle
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtNetwork
from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket


class DCReader(QMainWindow):
    sgdatasend = pyqtSignal(object)
    sgcount = pyqtSignal(int)
    def __init__(self):



        super(DCReader, self).__init__()
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
        HOST = '127.0.0.8'
        PORT = 9000
        self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)

    def sendD(self):
        try:
            user = self.le.text()
            dict = {'Type': 'Auth', 'User': 'Arham'}
            print('dict',dict)
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

            # print('DCReader')

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

                data=data.decode('UTF-8')
                # print(data)
                if(data!=''):
                    len1 = len(data)
                    # print(len1)
                    if (len1 == 1100):

                        trade = data[:100]

                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[300:400]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[400:500]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[500:600]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[600:700]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[700:800]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[800:900]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[900:1000]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[1000:1100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                    elif (len1 == 1000):

                        trade = data[:100]

                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1


                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[300:400]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[400:500]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[500:600]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[600:700]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[700:800]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[800:900]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[900:1000]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                    elif (len1 == 900):

                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[300:400]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[400:500]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[500:600]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[600:700]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[700:800]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[800:900]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                    elif (len1 == 800):

                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[300:400]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[400:500]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[500:600]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[600:700]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[700:800]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                    elif (len1 == 700):

                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[300:400]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[400:500]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[500:600]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[600:700]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                    elif (len1 == 600):

                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[300:400]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[400:500]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[500:600]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                    elif (len1 == 500):

                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[300:400]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[400:500]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1
                    elif (len1 == 400):
                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[300:400]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                    elif (len1 == 300):
                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[200:300]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1



                    elif (len1 == 200):
                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                        trade = data[100:200]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1

                    elif(len1==100):
                        trade = data[:100]
                        i = trade.split(',')
                        self.sgdatasend.emit(i)
                          
                        self.c += 1


                    else:
                        print('invalid legth')

                    self.sgcount.emit(self.c)
                    # print(self.c)




                    






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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    client = DCReader()
    client.show()
    sys.exit(app.exec_())



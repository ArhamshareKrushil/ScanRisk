from PyQt5.QtNetwork import QUdpSocket,QHostAddress
from PyQt5 import QtCore, QtNetwork
import lzo
import struct
import json
from Application.Utils import  getMasters


class Receiver(QtCore.QObject):

    sgNPF = QtCore.pyqtSignal(dict)
    def __init__(self):

        self.port = 25698
        super(Receiver, self).__init__()
        self._socket = QtNetwork.QUdpSocket(self)
        self._socket.bind(QHostAddress.AnyIPv4, self.port,QUdpSocket.ShareAddress|QUdpSocket.ReuseAddressHint)
        self._socket.readyRead.connect(self.on_readyRead)
        self.listMsgCodeCom = []
        self.listMsgCode = []
        #self.fo_contract,self.eq_contract,self.cd_contract,self.heads = getMasters(False)

    def join_grp(self):
        print("on decoded join")
        self._socket.joinMulticastGroup(QHostAddress('233.1.2.3'))
        print("-------")

    def leave_grp(self):
        self._socket.leaveMulticastGroup(QHostAddress('233.1.2.3'))

    @QtCore.pyqtSlot()
    def on_readyRead(self):
        while self._socket.hasPendingDatagrams():
            packet, host, port = self._socket.readDatagram(
                self._socket.pendingDatagramSize()
            )

            print(json.loads(packet.decode())['ID'])
            pack = json.loads(packet.decode())
            self.sgNPF.emit(pack)
            # if(pack['Token']==82222):
                # print(pack)

if __name__ == "__main__":
    import sys
    from Application.Utils.configReader import get_udp_port
    env = "UAT"
    port_cash, port_fo, port_cd = get_udp_port(env)
    print(port_fo)
    app = QtCore.QCoreApplication(sys.argv)

    # receiver1 = Receiver(35099)
    #
    # thread = QtCore.QThread()
    # thread.start()
    # receiver1.moveToThread(thread)

    receiver2 = Receiver(port_fo)
    thread2 = QtCore.QThread()
    thread2.start()
    receiver2.moveToThread(thread2)

    receiver2.join_grp()


    sys.exit(app.exec_())
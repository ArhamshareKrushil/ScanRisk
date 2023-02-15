import threading
import os
import numpy as np
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QUdpSocket,QHostAddress
from PyQt5 import QtCore, QtNetwork
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
from Application.Services.UDP.Utils import parseFeeds
from Application.Utils.configReader import get_udp_port

from py_vollib.black_scholes.implied_volatility import implied_volatility as iv
from py_vollib.black_scholes.greeks.analytical import delta
from py_vollib.black_scholes.greeks.analytical import gamma
from py_vollib.black_scholes.greeks.analytical import rho
from py_vollib.black_scholes.greeks.analytical import theta
from py_vollib.black_scholes.greeks.analytical import vega
# from py_vollib.helpers.exceptions import PriceIsBelowIntrinsic
from py_lets_be_rational.exceptions import BelowIntrinsicException,AboveMaximumException



import datetime
class Receiver(QtCore.QObject):
    sgData7202 = pyqtSignal(dict)
    sgCMData7202 = pyqtSignal(dict)
    sgData7208 = pyqtSignal( dict)
    sgDataIV_LTP = pyqtSignal( dict)
    sgDataIV_BA = pyqtSignal( dict)
    sgDataGreeks = pyqtSignal( dict)
    def __init__(self, port):
        super(Receiver, self).__init__()

        self.port = port

        self.getSetting()

        self.r=0.001
        self._socket = QtNetwork.QUdpSocket(self)
        self._socket.bind(QHostAddress.AnyIPv4, self.port,QUdpSocket.ShareAddress|QUdpSocket.ReuseAddressHint)
        self._socket.readyRead.connect(self.on_readyRead)
        self._socket.connected.connect(lambda: print('fo recv connected'))


        todate = datetime.datetime.today().strftime('%Y%m%d')
        self.todate = datetime.datetime.strptime(todate,'%Y%m%d')
        self.classWiseList = {}

        self.FinalList = {'NSEFO':[] ,'NSECM':[]}



        # self.fo_contract,self.eq_contract,self.cd_contract,self.heads = getMaster(False)
        # self.sgData7208.connect(self.calculateIv)
        # self.sgData7202.connect(self.calculateIv)
        # self.sgData7202.connect(self.updateValues)
        # self.sgData7208.connect(self.updateValues)

    def join_grp(self):
        print('fo_receiver join',self.port)
        self._socket.joinMulticastGroup(QHostAddress('233.1.2.5'))

    def leave_grp(self):
        self._socket.leaveMulticastGroup(QHostAddress('233.1.2.5'))

    @QtCore.pyqtSlot()
    def on_readyRead(self):
        while self._socket.hasPendingDatagrams():
            packet, host, port = self._socket.readDatagram(
                self._socket.pendingDatagramSize()
            )

            # th = threading.Thread(target=parseFeeds,args=(self,packet,port))
            # th.start()
            # print('packet',packet)
            parseFeeds(self,packet,port)


    # def subscribedList (self,superClass,Exchange,token):
    #     if(superClass in self.classWiseList.keys()):
    #         if (Exchange in self.classWiseList[superClass].keys()):
    #             if (token in self.classWiseList[superClass][Exchange]):
    #                 pass
    #             else:
    #                 self.classWiseList[superClass][Exchange].append(token)
    #                 self.FinalList[Exchange].append(token)
    #         else:
    #             self.classWiseList[superClass][Exchange] = []
    #             self.classWiseList[superClass][Exchange].append(token)
    #
    #             self.FinalList[Exchange] = []
    #             self.FinalList[Exchange].append(token)
    #     else:
    #         self.classWiseList[superClass] = {Exchange:[]}
    #         self.classWiseList[superClass][Exchange].append(token)
    #
    #         self.FinalList[Exchange]=[]
    #         self.FinalList[Exchange].append(token)
    #
    #
    #
    # def UnsubscribedList(self,superClass, Exchange, token):
    #     if(superClass in self.classWiseList.keys()):
    #         if(Exchange in self.classWiseList[superClass].keys()):
    #             if(token in self.classWiseList[superClass][Exchange]):
    #                 self.classWiseList[superClass][Exchange].remove(token)
    #                 self.FinalList[Exchange].remove(token)

    def getSetting(self):
        loc=os.getcwd().split('Application')[0]
        # print(loc)
        path=os.path.join(loc,'Resources','config_json.json')
        # print(path)

        f = open(path)
        data1 = json.load(f)
        self.port_fo = data1["UDP_FO"]
        self.port_cash = data1["UDP_CASH"]




    def subscribedlist(self,classname, Exch, token):
        # print('insubscribedlist test',classname,Exch,token)
        if classname in self.classWiseList:
            if Exch in self.classWiseList[classname]:
                if token in self.classWiseList[classname][Exch]:
                    pass
                else:
                    self.classWiseList[classname][Exch].append(token)
                    self.FinalList[Exch].append(token)
            else:
                self.classWiseList[classname][Exch] = []
                self.classWiseList[classname][Exch].append(token)

                if Exch in self.FinalList:
                    self.FinalList[Exch].append(token)
                else:
                    self.FinalList[Exch] = []
                    self.FinalList[Exch].append(token)
        else:
            self.classWiseList[classname] = {}
            self.classWiseList[classname][Exch] = []
            self.classWiseList[classname][Exch].append(token)

            if Exch in self.FinalList:
                self.FinalList[Exch].append(token)
            else:

                self.FinalList[Exch] = []
                self.FinalList[Exch].append(token)
        # print('FinalList',self.FinalList)

    def Unsubscribedlist(self,classname, Exch, token):
        if classname in self.classWiseList:
            if Exch in self.classWiseList[classname]:
                if token in self.classWiseList[classname][Exch]:
                    self.classWiseList[classname][Exch].remove(token)
                    self.FinalList[Exch].remove(token)




    # def updateValues(self,data):
    #     # print('data1',data)
    #     if(data['Exch'] == 2):
    #         if(data['ID']==7202):
    #             prevData = self.fo_contract[data['Token'] - 35000]
    #             prevVolume = prevData[32]
    #             newVolume = prevVolume + data['FillVolume']
    #             # print('prevVolume',prevVolume)
    #             self.fo_contract[data['Token']-35000,[19,22,32]] = [data['LTP'],data['OpenInterest'],
    #                                                                 newVolume]
    #         elif(data['ID']==1501):
    #             # print(data)
    #             # prevData = self.fo_contract[data['Token'] - 35000]
    #             self.fo_contract[data['Token'] - 35000,[19,32,35]]=[data['LTP'],data['Volume'],data['ATP']]
    #
    #
    # #
    # #
    # #
    # #
    # def calculateIv(self,data):
    #
    #     if (data['Exch'] == 2):
    #         if(data['ID']==7202):
    #             prevData = self.fo_contract[data['Token'] - 35000]
    #             if(prevData[7]!=' ' and prevData[6]!= ''):
    #                 try:
    #                     futureToken = prevData[17]
    #                     fPrice = self.fo_contract[futureToken-35000,19]
    #                     exp = prevData[6]
    #                     strikeP = prevData[12]
    #                     optionType = prevData[8][0].lower()
    #                     expiryDay = datetime.datetime.strptime(exp,'%Y%m%d')
    #                     daysRemaaining1 =(expiryDay - self.todate).days
    #                     daysRemaaining = 1 if(daysRemaaining1==0) else daysRemaaining1
    #                     t = daysRemaaining / 365
    #                     # if(data['Token']==40688):
    #                     #
    #                     #     print(40688,exp,self.todate,daysRemaaining,t)
    #                     #     # print(40688,data['LTP'], fPrice, strikeP, t, self.r, optionType)
    #
    #                     imp_v = iv(data['LTP'], fPrice, strikeP, t, self.r, optionType)
    #
    #
    #                 except TypeError:
    #
    #                     print('jgh', prevData)
    #                     imp_v = 0.01
    #                 except BelowIntrinsicException:
    #                     imp_v = 0.01
    #                 except:
    #                     imp_v = 0.01
    #                     pass
    #
    #                 imp_v1=round(imp_v*100,2)
    #
    #                 dict1 = {'ID':'IV','Token':data['Token'],"Exch":data['Exch'],"iv":imp_v1}
    #                 self.sgDataIV_LTP.emit(dict1)
    #
    #                 # self.sender.sendData(dict1)
    #
    #
    #                 delt = delta(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 delt = round(delt , 4)
    #
    #                 gm = gamma(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 gm = round(gm , 4)
    #
    #                 # rh = rho(optionType, fPrice, strikeP, t, self.r, imp_v)
    #
    #                 tht = theta(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 tht = round(tht, 4)
    #
    #                 vg = vega(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 vg = round(vg, 4)
    #                 dict2 = {'ID':'Greeks','Token':data['Token'],'Exch':data['Exch'],'Delta':delt,'Gamma':gm,'Theta':tht,
    #                          'Vega':vg}
    #                 self.sgDataGreeks.emit(dict2)
    #                 # self.sender.sendData(dict2)
    #
    #
    #
    #
    #
    #
    #         elif (data['ID'] == 1501):
    #             prevData = self.fo_contract[data['Token'] - 35000]
    #             if (prevData[7] != ' ' and prevData[6] != ''):
    #                 try:
    #                     futureToken = prevData[17]
    #
    #                     fPrice = self.fo_contract[futureToken - 35000, 19]
    #                     exp = prevData[6]
    #                     strikeP = prevData[12]
    #                     optionType = prevData[8][0].lower()
    #
    #                     expiryDay = datetime.datetime.strptime(exp,'%Y%m%d')
    #                     daysRemaaining1 =(expiryDay - self.todate).days
    #                     daysRemaaining = 1 if(daysRemaaining1==0) else daysRemaaining1
    #                     t = daysRemaaining / 365
    #
    #                     imp_v= iv(data['LTP'], fPrice, strikeP, t, self.r, optionType)
    #
    #                     Bid_IV = iv(data['Bid'], fPrice, strikeP, t, self.r, optionType)
    #                     Ask_IV = iv(data['Ask'], fPrice, strikeP, t, self.r, optionType)
    #
    #                     # print('7202', imp_v, delt, gm, tht, vg, data['LTP'], fPrice, strikeP, optionType)
    #                 except AboveMaximumException:
    #                     imp_v = 0.01
    #                     Bid_IV = 0.01
    #                     Ask_IV = 0.01
    #
    #                 except ZeroDivisionError:
    #                     imp_v = 0.01
    #                     Bid_IV=0.01
    #                     Ask_IV=0.01
    #                     print('ZeroDivisionError',data['LTP'], fPrice, strikeP, t, self.r, optionType,exp)
    #
    #                 except TypeError:
    #                     imp_v = 0.01
    #                     Bid_IV = 0.01
    #                     Ask_IV = 0.01
    #
    #                     print('jgh', prevData)
    #                 except BelowIntrinsicException:
    #                     imp_v = 0.01
    #                     Bid_IV = 0.01
    #                     Ask_IV = 0.01
    #                 except:
    #                     imp_v = 0.01
    #                     Bid_IV = 0.01
    #                     Ask_IV = 0.01
    #
    #                 #
    #                 imp_v1 = round(imp_v * 100, 2)
    #
    #                 dict1 = {'ID': 'IV', 'Token': data['Token'], "Exch": data['Exch'], "iv": imp_v1}
    #                 self.sgDataIV_LTP.emit(dict1)
    #
    #                 # self.sender.sendData(dict1)
    #
    #                 dict1 = {'ID': 'Bid_Ask', 'Token': data['Token'], "Exch": data['Exch'], "Bid_iv": Bid_IV,"Ask_iv": Ask_IV}
    #
    #                 # self.sender.sendData(dict1)
    #
    #                 # dict1 = {'ID': 'Ask_IV', 'Token': data['Token'], "Exch": data['Exch'], "Ask_iv": Ask_IV}
    #                 # self.sender.sendData(dict1)
    #                 self.sgDataIV_BA.emit(dict1)
    #
    #                 delt = delta(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 delt = round(delt, 4)
    #
    #                 # gm = gamma(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 # gm = round(gm, 4)
    #                 #
    #                 # rh = rho(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 #
    #                 # tht = theta(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 # tht = round(tht, 4)
    #                 #
    #                 # vg = vega(optionType, fPrice, strikeP, t, self.r, imp_v)
    #                 # vg = round(vg , 4)
    #                 # dict2 = {'ID': 'Greeks', 'Token': data['Token'], 'Exch': data['Exch'], 'Delta': delt, 'Gamma': gm,
    #                 #          'Theta': tht,
    #                 #          'Vega': vg}
    #                 # self.sgDataGreeks.emit(dict2)
    #                 #
    #                 # # self.sender.sendData(dict2)
    #                 #
    #                 #     # self.fo_contract[data['Token'] - 35000, [24, 25, 26, 27, 28]] = [imp_v, delt, gm, tht, vg]
    #                 #




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Receiver(34044)
    form.join_grp()
    sys.exit(app.exec_())



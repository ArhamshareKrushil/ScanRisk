import psutil

import threading
from  py_vollib.black_scholes import black_scholes
from PyQt5 import uic
from PyQt5.QtCore import  *
from PyQt5 import QtCore, QtNetwork
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QKeySequence
from Application.Views.Login.Login import Ui_LogIn
from Application.Views.titlebar import tBar
from Application.Views.TWM.TWM import TerminalSummary
from Application.Views.POCW.POCW import PositionDetailsCW
from Application.Views.POTW.POTW import PositionDetailsTW
from Application.Views.CWM.CWM import ClientSummary
from Application.Views.TWSWM.TWSWM import TScriptSummary
from Application.Views.CWSWM.CWSWM import CScriptSummary
from Application.Views.GlobalMargin.GlobalMargin import GlobalMargin
from Application.Views.BWM.BWM import BranchSummary
from Application.Views.BWSWM.BWSWM import BranchScriptSummary
from Application.Views.Deposit.Deposit import UI_Deposit
from Application.Views.Limit.Limit import UI_Limit

from Application.Utils.support import getLogPath

from Application.Utils.all_slots import createSlots_main
from Application.Utils.configReader import read_API_config
# from Application.Utils.updation import updatePOTM,updateLTP_POCW,updatePOTW,updateLTP_POTW,updateCMPOTWpos,updateLTP_CMPOTW,updateLTP_CMPOCW


from Application.Views.BOD.bod import Ui_BOD
from Application.Views.CorporateAction.Action import Ui_CoAction
from Application.Views.TerminalMaster.Tmaster import UI_Tmaster
from Application.Views.ClientMaster.Cmaster import UI_Cmaster
from Application.Views.CMPOTW.CMPOTW import UI_CMPOTW
from Application.Views.CMPOCW.CMPOCW import UI_CMPOCW
from Application.Views.cframe import Ui_cframe
from Application.Views.feedManager import Ui_feedmanager
from Application.Views.CASH.CASH import Ui_CASH
from Application.Views.CMTWM.CMTWM import UI_CMTWM
from Application.Views.CMCWM.CMCWM import UI_CMCWM




from Application.Utils.support import *

from Application.Services.UDP.UDPSock import Receiver
from Resources.icons import icons_rc

from Themes.dt2 import dt1
import qdarkstyle

import traceback
import csv
import os
import platform
import json
from Application.Services.Socket.SocketClient import SioClient
from Application.Services.FastApi.ApiServices import versionCheck,DownloadVersionClicked



class Ui_Main(QMainWindow):
    sgopenPosPOTW=pyqtSignal(list)
    sgDB_TWSWM=pyqtSignal(list)
    sgDB_TWM=pyqtSignal(list)
    sgDB_CMPOTW=pyqtSignal(list)
    sgDB_CMTWM=pyqtSignal(list)


    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_Main, self).__init__()
        self.osType = platform.system()
        #########################################################
        getLogPath(self)
        ########################################################

        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'Main.ui')
        uic.loadUi(ui_login,self)


        self.setStyleSheet(dt1)


        osType = platform.system()

        self.maxwin=False
        self.menuhide=False
        self.r = 0.1

        todate = datetime.datetime.today().strftime('%Y%m%d')
        self.todate = datetime.datetime.strptime(todate, '%Y%m%d')

        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        else:
            flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.title = tBar('ScanRisk')
        self.headerFrame.layout().addWidget(self.title, 0, 1)
        self.title.sgPoss.connect(self.movWin)



        self.createObjects()
        loadDeposit(self)
        loadLimit(self)
        # event mapping
        createSlots_main(self)
        self.createTimers()

        versionCheck(self)










    def DownloadVersionClicked(self,i):
        DownloadVersionClicked(self,i)

    def createTimers(self):
        # self.timerBWM = QTimer()
        # self.timerBWM.setInterval(5000)
        # self.timerBWM.timeout.connect(lambda: updateBWM(self))

        self.timerGlobalM = QTimer()
        self.timerGlobalM.setInterval(6000)
        self.timerGlobalM.timeout.connect(lambda: updateBWSWM(self))
        self.timerGlobalM.timeout.connect(lambda: updateGlobalMargin(self))

        self.timerMTM = QTimer()
        self.timerMTM.setInterval(2000)
        self.timerMTM.timeout.connect(lambda: updateFOMTM(self))

        self.timerCMMTM = QTimer()
        self.timerCMMTM.setInterval(5000)
        self.timerCMMTM.timeout.connect(lambda :update_CASH_MTM(self))

        self.timerGreeks = QTimer()
        self.timerGreeks.setInterval(20000)
        self.timerGreeks.timeout.connect(lambda: update_Greeks_POTW(self))

        self.timerSCN = QTimer()
        self.timerSCN.setInterval(30000)
        self.timerSCN.timeout.connect(lambda: updateSCNPrice(self))







        # self.timergetPOTW = QTimer()
        # self.timergetPOTW.setInterval(300000)
        # self.timergetPOTW.timeout.connect(lambda: updatePOTW_DB(self))






    def createUserObject(self):
        read_API_config(self)

        if(self.UserType=='branch'):
            self.cFrame = Ui_cframe()
            self.mainFrame.layout().addWidget(self.cFrame, 0, 0)

            self.TWM = TerminalSummary()
            self.TWSWM = TScriptSummary()

            # self.CWM = ClientSummary()
            # self.CWSWM = CScriptSummary()

            self.POTW = PositionDetailsTW()
            # self.POCW = PositionDetailsCW()
            #
            self.GlobalM=GlobalMargin()

            # self.BWM = BranchSummary()
            self.BWSWM=BranchScriptSummary()
            #
            self.CASH=Ui_CASH()
            self.CMPOTW=UI_CMPOTW()
            self.CMTWM=UI_CMTWM()

            # self.CMPOCW=UI_CMPOCW()
            # self.CMCWM=UI_CMCWM()
            #
            #
            self.cFrame.DTWM.setWidget(self.TWM)
            self.cFrame.DTWSWM.setWidget(self.TWSWM)
            #
            # self.cFrame.DCWM.setWidget(self.CWM)
            # self.cFrame.DCWSWM.setWidget(self.CWSWM)
            #
            self.cFrame.DPOTW.setWidget(self.POTW)
            # self.cFrame.DPOCW.setWidget(self.POCW)
            #
            self.cFrame.DGlobal.setWidget(self.GlobalM)
            #
            # self.cFrame.DBWM.setWidget(self.BWM)
            self.cFrame.DBWSWM.setWidget(self.BWSWM)

        else:
            self.cFrame = Ui_cframe()
            self.mainFrame.layout().addWidget(self.cFrame, 0, 0)

            self.TWM = TerminalSummary()
            self.TWSWM = TScriptSummary()

            self.CWM = ClientSummary()
            self.CWSWM = CScriptSummary()

            self.POTW = PositionDetailsTW()
            self.POCW = PositionDetailsCW()

            self.GlobalM=GlobalMargin()

            self.BWM = BranchSummary()
            self.BWSWM=BranchScriptSummary()
            #
            self.CMPOTW=UI_CMPOTW()
            # self.CMPOCW=UI_CMPOCW()
            self.CASH=Ui_CASH()
            self.CMTWM=UI_CMTWM()
            # self.CMCWM=UI_CMCWM()
            #
            #
            self.cFrame.DTWM.setWidget(self.TWM)
            self.cFrame.DTWSWM.setWidget(self.TWSWM)
            #
            self.cFrame.DCWM.setWidget(self.CWM)
            self.cFrame.DCWSWM.setWidget(self.CWSWM)
            #
            self.cFrame.DPOTW.setWidget(self.POTW)
            self.cFrame.DPOCW.setWidget(self.POCW)

            self.cFrame.DGlobal.setWidget(self.GlobalM)
            #
            self.cFrame.DBWM.setWidget(self.BWM)
            self.cFrame.DBWSWM.setWidget(self.BWSWM)

        self.defaultWindowState()
        self.connectAllslots()
        # shareContract(self)
        # self.timerBWM.start()
        self.timerGlobalM.start()
        self.timerMTM.start()
        self.timerCMMTM.start()
        self.timerGreeks.start()
        self.timerSCN.start()



    def getSetting(self):
        loc=os.getcwd().split('Application')[0]
        # print(loc)
        path=os.path.join(loc,'Resources','config_json.json')
        # print(path)

        f = open(path)
        data1 = json.load(f)
        self.port_fo = data1["UDP_FO"]
        self.port_cash = data1["UDP_CASH"]


    def createObjects(self):
        self.login=Ui_LogIn()

        self.SioClient=SioClient()

        self.Deposit=UI_Deposit()
        self.Limit=UI_Limit()

        self.thread1 = QThread()
        self.SioClient.moveToThread(self.thread1)
        self.thread1.start()

        self.getSetting()
        self.Reciever = Receiver(self.port_fo)
        self.Reciever.join_grp()

        self.t1 = QThread()
        self.Reciever.moveToThread(self.t1)
        self.t1.start()

        self.RecieverCM = Receiver(self.port_cash)
        # print(self.port_cash)
        self.RecieverCM.join_grp()

        self.th34 = QThread()
        self.RecieverCM.moveToThread(self.th34)
        self.th34.start()




    def connectAllslots(self):

        self.TWM.tableView.doubleClicked.connect(lambda: TWMdoubleClicked(self))
        ################################################################

        self.headerFrame.setContextMenuPolicy(Qt.CustomContextMenu)
        self.headerFrame.customContextMenuRequested.connect(self.WindowRightclickedMenu)
        self.btnSttn.clicked.connect(self.menuhideshow)
        self.bt_min.clicked.connect(self.showMinimized)
        self.bt_close.clicked.connect(self.closeApp)
        self.bt_max.clicked.connect(self.showmaxORnormal)

        ##################### CASH #########################
        self.pbCash.clicked.connect(self.CASHshow)

        self.CASH.pbPOTW.clicked.connect(self.CMPOTWshow)
        self.CASH.pbTWM.clicked.connect(self.CMTWMshow)


        ################### Socket Client FO ##########################

        self.SioClient.sgOnPosition.connect(self.updatePOTW)
        self.SioClient.sgOnTWSWM.connect(self.updateTWSWM)
        self.SioClient.sgOnTWM.connect(self.updateTWM)

        ##################Socket Client CM ###########################
        self.SioClient.sgOnCMPosition.connect(self.updateCMPOTW)
        self.SioClient.sgOnCMTWM.connect(self.updateCMTWM)




        ######################## MAIN ###############################

        self.sgopenPosPOTW.connect(self.on_POTWOpenPosition)
        self.sgDB_TWSWM.connect(self.updateTWSWM)
        self.sgDB_TWM.connect(self.updateTWM)
        self.sgDB_CMPOTW.connect(self.updateCMPOTW)
        self.sgDB_CMTWM.connect(self.updateCMTWM)

        ####################### UDP Receiver FO #####################

        self.Reciever.sgData7202.connect(self.update7202)
        self.RecieverCM.sgCMData7202.connect(self.updateCM7202)
        self.RecieverCM.sgCMData7207.connect(self.updateCM7207)


        ###################Deposit############################
        self.pbDeposit.clicked.connect(self.Deposit.show)
        self.Limit.sgupdateLimitPOTW.connect(self.updateLimitPOTW)
        self.Deposit.sgupdateDepositPOTW.connect(self.updateDepositPOTW)

        self.pbLimit.clicked.connect(self.Limit.show)

    def updateDepositPOTW(self,data):
        updateDepositPOTW(self,data)
    def updateLimitPOTW(self,data):
        updateLimitPOTW(self,data)

    def closeApp(self):
        self.SioClient.sio.disconnect()
        sys.exit()
    def end_task(process_name='SCAN-RISK.exe'):
        for proc in psutil.process_iter():
            try:
                if proc.name() == process_name:
                    proc.kill()
                    print(f"{process_name} has been terminated.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            
    def CASHshow(self):
        self.CASH.show()

    def CMPOTWshow(self):
        self.CMPOTW.show()

    def CMTWMshow(self):
        self.CMTWM.show()


    @pyqtSlot(list)
    def updatePOTW(self,data):
        updatePOTW(self,data)

    @pyqtSlot(list)
    def updateCMPOTW(self, data):
        updateCMPOTW(self, data)

    @pyqtSlot(list)
    def updateCMTWM(self, data):
        updateCMTWM(self, data)

    def on_DB_TWSWM(self,data):

        update_DB_TWSWM(self,data)

    def updateTWSWM(self,data):
        updateTWSWM(self,data)

    def updateTWM(self,data):
        updateTWM(self,data)



    def on_DB_TWM(self,data):
        # update_DB_TWM(self,data)

        # print(data)
        # if(data['id']=='POTW'):
        update_DB_TWM(self,data)

    @QtCore.pyqtSlot(list)
    def on_POTWOpenPosition(self,data):

        # print(data)
        updatePOTWopenPosition(self,data)

    @QtCore.pyqtSlot(dict)
    def update7202(self, data):
        # print('data',data)
        # updateLTP_POCW(self, data)
        updateLTP_POTW(self, data)
        update_contract_fo(self, data)

    # @QtCore.pyqtSlot(dict)
    def updateCM7207(self, data):
        # pass
        # print()
        # print(data)
        # updateLTP_POCW(self, data)
        updateIndexes(self, data)
        # update_contract_fo(self, data)

    # def updateCM7203(self, data):
    #     # print(data)
    #     # updateLTP_POCW(self, data)
    #     # updateIndexes(self, data)
    #     # update_contract_fo(self, data)


    def updateCM7202(self, data):
        # print(data)
        # updateLTP_POCW(self, data)
        updateLTP_CMPOTW(self, data)
        # update_contract_fo(self,data)


    def WindowRightclickedMenu(self,position):
        # print('rightclicked')

        menu = QMenu()

        saveWindowState = menu.addAction("Save Window State")
        restoreWindowState = menu.addAction("Open Window State")

        action = menu.exec_(self.headerFrame.mapToGlobal(position))
        print(action)
        if action == saveWindowState:
            self.SaveWindowState()

        elif action == restoreWindowState:
            self.openWindowState()



    def defaultWindowState(self):
        loc = os.getcwd().split('Application')
        settingsFilePath = os.path.join(loc[0], 'Settings', 'Settings.json')
        f1 = open(settingsFilePath)
        pathDetails = json.load(f1)
        f1.close()
        lastCPFilePath = pathDetails['mainWindow']['defaultWindowState']
        with open(lastCPFilePath, 'rb') as f:
            binData = f.read()
        f.close()
        self.cFrame.restoreState(binData)

    def SaveWindowState(self):
        print('right clicked')

        defaultDir = os.path.join('WindowProfile')
        binData = self.cFrame.saveState()

        save = QFileDialog.getSaveFileName(self, 'Save file', defaultDir)[0]


        with open(save, 'wb') as f:
            f.write(binData)
        f.close()

        loc = os.getcwd().split('Application')
        settingsFilePath = os.path.join(loc[0], 'Settings', 'Settings.json')

        f1 = open(settingsFilePath)
        pathDetails = json.load(f1)
        f1.close()
        pathDetails['mainWindow']['defaultWindowState'] = save

        pathDetails_new = json.dumps(pathDetails, indent=4)

        f2 = open(settingsFilePath, 'w+')
        f2.write(pathDetails_new)
        # pathDetails= json.load(f1)
        f2.close()

    def openWindowState(self):
        # loc = os.getcwd().split('Application')[0]
        defaultDir = os.path.join('WindowProfile')

        save = QFileDialog.getOpenFileName(self, 'Open file', defaultDir)[0]

        with open(save, 'rb') as f:
            binData = f.read()
        f.close()

        self.cFrame.restoreState(binData)

    # def TWMdoubleClicked(self):
    #     TWMdoubleClicked(self)

    # def CWMdoubleClicked(self,table):
    #     CWMdoubleClicked(self)

    # def BWMdoubleClicked(self):
    #     BWMdoubleClicked(self)




    def menuhideshow(self):
        if(self.menuhide==False):
            self.settingsMenu.hide()
            self.menuhide =True
        else:
            self.settingsMenu.show()
            self.menuhide = False





    #
    # @QtCore.pyqtSlot(dict)
    # def updateCM7202(self,data):
    #     # print('cm7202')
    #     # updateLTP_POCW(self, data)
    #     updateLTP_CMPOTW(self, data)
    #     updateLTP_CMPOCW(self,data)

    def showmaxORnormal(self):
        if(self.maxwin==False):
            self.showMaximized()
            self.maxwin = True
        else:
            self.showNormal()
            self.maxwin = False



    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    # print('hellofhfhfh')
    form = Ui_Main()
    #
    # form.login.show()
    # form.show()
    sys.exit(app.exec_())

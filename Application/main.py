
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

from Application.Utils.support import getLogPath
from Application.Utils.all_slots import createSlots_main
from Application.Utils.configReader import readConfig_All
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

from Application.Utils.VAR.getVarFile import latest_var


from Application.Utils.support import *
from Application.Services.DCReader.FOReader import DCReader
from Application.Services.NotisReader.FOReader import FONotisReader
from Application.Services.NotisReader.CMReader import CMNotisReader
from Application.Services.DCReader.CMReader import CMDCReader

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
from Application.Utils.SPAN import SPAN1,terminalSPAN
from Application.Utils.VAR import terminalVAR,clientVAR
from Application.Utils.PhysicalDel import PhysicalDel

class Ui_Main(QMainWindow):
    sgopenPosPOTW=pyqtSignal(object)
    sgDB_TWSWM=pyqtSignal(object)
    sgDB_TWM=pyqtSignal(object)


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
        uic.loadUi(ui_login, self)

        dark =qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(dt1)


        osType = platform.system()

        self.maxwin=False
        self.menuhide=False

        todate = datetime.datetime.today().strftime('%Y%m%d')
        self.todate = datetime.datetime.strptime(todate, '%Y%m%d')


        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint )
        self.setWindowFlags(flags)
        self.title = tBar('ScanRisk')
        self.headerFrame.layout().addWidget(self.title, 0, 1)
        self.title.sgPoss.connect(self.movWin)



        self.createObjects()
        # event mapping
        createSlots_main(self)
        self.createTimers()
        self.connectAllslots()

        self.defaultWindowState()
        # self.csvtojson()

        # loadTmaster(self)
        # loadClientMaster(self)
        # QSizeGrip(self.frame_5)
        # latest_var(self)








    def createTimers(self):
        self.timerBWM = QTimer()
        self.timerBWM.setInterval(5000)
        self.timerBWM.timeout.connect(lambda: updateBWM(self))
        self.timerBWM.start()










    def createObjects(self):
        self.login=Ui_LogIn()
        self.SioClient=SioClient()

        self.cFrame = Ui_cframe()
        self.mainFrame.layout().addWidget(self.cFrame,0,0)


        self.TWM = TerminalSummary()
        self.TWSWM = TScriptSummary()

        # self.CWM = ClientSummary()
        # self.CWSWM = CScriptSummary()

        self.POTW = PositionDetailsTW()
        # self.POCW = PositionDetailsCW()
        #
        # self.GlobalM=GlobalMargin()

        self.BWM=BranchSummary()
        # self.BWSWM=BranchScriptSummary()
        #
        # self.CMPOTW=UI_CMPOTW()
        # self.CMPOCW=UI_CMPOCW()
        # self.CASH=Ui_CASH()
        # self.CMTWM=UI_CMTWM()
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
        # self.cFrame.DGlobal.setWidget(self.GlobalM)
        #
        self.cFrame.DBWM.setWidget(self.BWM)
        # self.cFrame.DBWSWM.setWidget(self.BWSWM)














    def connectAllslots(self):



        ################################################################

        self.headerFrame.setContextMenuPolicy(Qt.CustomContextMenu)
        self.headerFrame.customContextMenuRequested.connect(self.WindowRightclickedMenu)
        self.btnSttn.clicked.connect(self.menuhideshow)
        self.bt_min.clicked.connect(self.showMinimized)
        self.bt_close.clicked.connect(self.close)
        self.bt_max.clicked.connect(self.showmaxORnormal)

        ################### Socket Client ##########################

        self.SioClient.sgOnPosition.connect(self.updatePOTW)
        self.SioClient.sgOnTWSWM.connect(self.updateTWSWM)
        self.SioClient.sgOnTWM.connect(self.updateTWM)


        ######################## MAIN ###############################

        self.sgopenPosPOTW.connect(self.on_POTWOpenPosition)
        self.sgDB_TWSWM.connect(self.on_DB_TWSWM)
        self.sgDB_TWM.connect(self.on_DB_TWM)

    def CloseWindow(self):
        pass

    @pyqtSlot(list)
    def updatePOTW(self,data):

        # print(data)
        # if(data['id']=='POTW'):
        updatePOTW(self,data)

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

    def on_POTWOpenPosition(self,data):

        # print(data)
        updatePOTWopenPosition(self,data)


        # elif(data['id']=='POCW'):
        #     updatePOCW(self,data)






        # updateLTP_POTW(self,data,7202)
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




    # @QtCore.pyqtSlot(dict)
    # def update7202(self,data):
    #     updateLTP_POCW(self, data)
    #     updateLTP_POTW(self, data)
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

    # def CMPOTWhide(self):
    #     # self.timerCMTerminalMRG.stop()
    #     self.CMPOTW.hide()
    #
    #
    #
    # @QtCore.pyqtSlot(dict)
    # def update7202POTW(self,data):
    #     updateLTP_POTW(self, data)
    #     # updateLTP_POTW(self, data)
    #
    #     # th39=threading.Thread(target=updateLTP_POTW,args=(self,data))
    #     # th39.start()
    #
    # @QtCore.pyqtSlot(object)
    # def updateCMPOTWpos(self,data):
    #     updateCMPOTWpos(self,data)
    #
    # def update7208(self,data):
    #     pass
    #     # updateLTP_POCW(self, data)
    #     # updateLTP_POTW(self, data)
    #
    # @QtCore.pyqtSlot(object)
    # def updateCWM(self,data):
    #     # th1 = threading.Thread(target=updateCWM, args=(self, data))
    #     # th1.start()
    #     updateCWM(self,data)
    #
    # def updateCMTWM(self,data):
    #     # th1 = threading.Thread(target=updateCWM, args=(self, data))
    #     # th1.start()
    #     updateCMTWM(self,data)
    #
    # def updateCMCWM(self,data):
    #     # th1 = threading.Thread(target=updateCWM, args=(self, data))
    #     # th1.start()
    #     updateCMCWM(self,data)
    #
    # @QtCore.pyqtSlot(object)
    # def updateCWSWM(self,data):
    #     # th5 = threading.Thread(target=updateCWSWM, args=(self, data))
    #     # th5.start()
    #     updateCWSWM(self,data)
    #
    # @QtCore.pyqtSlot(object)
    # def updateTWM(self,data):
    #     # th1 = threading.Thread(target=updateCWM, args=(self, data))
    #     # th1.start()
    #     updateTWM(self,data)
    #
    # @QtCore.pyqtSlot(object)
    # def CWMPhysicalDelM(self,data):
    #     # th1 = threading.Thread(target=updateCWM, args=(self, data))
    #     # th1.start()
    #     CWMPhysicalDelM(self,data)
    #
    #
    #
    # @QtCore.pyqtSlot(object)
    # def updateTWSWM(self,data):
    #     # th5 = threading.Thread(target=updateCWSWM, args=(self, data))
    #     # th5.start()
    #     updateTWSWM(self,data)
    #
    #
    # def updateTWM_CASH_MTM(self):
    #
    #     # th5 = threading.Thread(target=updateCWSWM, args=(self, data))
    #     # th5.start()
    #     updateTWM_CASH_MTM(self)
    #
    # @QtCore.pyqtSlot(object)
    # def updatePOTM(self,data):
    #     updatePOTM(self,data)
    #
    # @QtCore.pyqtSlot(object)
    # def updatePOTW(self,data):
    #     updatePOTW(self,data)
    #     # self.DCreader.timer.start()
    #
    # @QtCore.pyqtSlot(object)
    # def sendDCtrade(self,data):
    #     sendtrade(self,data)
    #
    # @QtCore.pyqtSlot(object)
    # def sendCMDCtrade(self, data):
    #     sendCMtrade(self, data)
    #
    # @QtCore.pyqtSlot(object)
    # def sendNotistrade(self,data):
    #     sendNotistrade(self,data)
    #
    # def sendCMNotistrade(self,data):
    #     sendCMNotistrade(self,data)
    #
    #
    #
    #
    #
    # def BODshow(self):
    #     self.BOD.show()
    #
    # def TerminalMastershow(self):
    #     # loadTerminalMastertable(self)
    #     self.TM.show()
    #
    # def ClientMastershow(self):
    #     # loadClientMastertable(self)
    #     self.CM.show()
    #
    # def feedshow(self):
    #     self.feed.show()
    #
    # def coActionshow(self):
    #     self.coAction.show()
    #
    # def CASHshow(self):
    #     self.CASH.show()
    #
    # def CMPOTWshow(self):
    #     # if(self.BOD.isCMOpenPosupdated==True):
    #     #     self.timerCMTerminalMRG.start()
    #     self.CMPOTW.show()
    #
    # def CMPOCWshow(self):
    #     self.CMPOCW.show()
    #
    # def CMTWMshow(self):
    #     self.CMTWM.show()
    #
    # def CMCWMshow(self):
    #     self.CMCWM.show()

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # print('hellofhfhfh')
    form = Ui_Main()
    form.login.show()
    # form.show()
    sys.exit(app.exec_())

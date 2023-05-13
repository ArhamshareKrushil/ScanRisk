import  numpy as np
import csv
import os
import time
import traceback
import datetime

import pandas as pd
from Application.Views.titlebar import tBar

from Themes import dt3
import platform
from PyQt5 import uic
from PyQt5.QtCore import *
from Themes.dt3 import dt3
from PyQt5.QtWidgets import *
import qdarkstyle

from Application.Utils.support import getLogPath
from Application.Views.BOD.support import populateData
from Application.Views.BOD.support import *

class Ui_BOD(QMainWindow):
    sgCMPOTWopenpos=pyqtSignal(object)
    sgPOTM=pyqtSignal(object)

    sgsend=pyqtSignal(object)
    sgPOTMupdated = pyqtSignal()
    sgCMPOTWopenposupdated = pyqtSignal()
    sgPOTWOpenposupdated = pyqtSignal()
    sgPOTWopen=pyqtSignal(object)


    ################################# Intialization Here ##################################################
    def __init__(self):

        super(Ui_BOD, self).__init__()
        self.osType = platform.system()
        #########################################################
        getLogPath(self)
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'BOD1.ui')
        uic.loadUi(ui_login, self)
        dark = qdarkstyle.load_stylesheet_pyqt5()

        getbse2nse(self)

        self.rc=0
        self.isCMOpenPosupdated=False


        self.setStyleSheet(dt3)

        osType = platform.system()

        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        self.title = tBar('BOD')
        self.headerFrame.layout().addWidget(self.title, 0, 1)
        self.title.sgPoss.connect(self.movWin)



        populateData(self)

        showDefaultFrame(self)
        self.createTimers()
        self.createSlots()

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def createSlots(self):
        try:

            self.pb_mktdata.clicked.connect(lambda:Marketdatashow(self))
            self.pb_Downloads.clicked.connect(lambda:Downloadsshow(self))
            self.pb_Uploads.clicked.connect(lambda:Uploadssshow(self))
            self.pb_PeakMargin.clicked.connect(lambda:Peaksshow(self))
            # self.pb_TSettings.clicked.connect(print)
            self.pb_TSettings.clicked.connect(lambda:Tsettingsshow(self))

            self.tb_aelGen.clicked.connect(lambda:openAELGen(self))
            self.pbAelGup.clicked.connect(lambda: uploadAelGen(self))

            self.tb_aelSpc.clicked.connect(lambda:openAELSpc(self))
            self.pbAelSpc.clicked.connect(lambda:uploadAelSpc(self))

            self.tb_Openpos.clicked.connect(lambda:openpos(self))
            self.pbOpenpos.clicked.connect(lambda:uploadOpenpos(self))

            self.tbPOTM.clicked.connect(lambda:openPOTM(self))
            self.pbPOTM.clicked.connect(lambda: uploadPOTM(self))

            self.tbSheet.clicked.connect(lambda:openSheet(self))
            self.pbSheet.clicked.connect(lambda: uploadSheet(self))

            self.tbLedger.clicked.connect(lambda:openLedger(self))
            self.pbLedger.clicked.connect(lambda: uploadLedger(self))


            self.tbNfo.clicked.connect(lambda: openNotisFo(self))
            ## self.pbNfoA.clicked.connect(lambda: uploadNotisFo(self))

            # self.pbNfoA.clicked.connect(self.timertrades.start)

            self.pbNfoR.clicked.connect(lambda: RestartNotisFo(self))

            self.bt_close_3.clicked.connect(self.hide)
            self.bt_min_3.clicked.connect(self.showMinimized)


            # print('aaa')


        except:
            print(traceback.print_exc())

    def createTimers(self):
        pass


    def updateb2nSymbol(self,sym):
        sym1 = self.nse2bse[sym]
        # print('sym',sym,'sym1',sym1)
        return sym1


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_BOD()
    form.show()
    sys.exit(app.exec_())
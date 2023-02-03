import  numpy as np
import csv
import os
import time
import traceback
import datetime

import pandas as pd
from Application.Views.titlebar import tBar

from Themes import dt1
import platform
from PyQt5 import uic
from PyQt5.QtCore import *
from Themes.dt2 import dt1
from PyQt5.QtWidgets import *
import qdarkstyle

from Application.Utils.support import getLogPath
from Application.Views.BOD.support import populateData
from Application.Views.BOD.support import *

class Ui_CASH(QMainWindow):
    sgCMPOTWopenpos=pyqtSignal(object)
    sgPOTM=pyqtSignal(object)
    sgsend=pyqtSignal(object)
    sgPOTMupdated = pyqtSignal()
    sgPOTWOpenposupdated = pyqtSignal()
    sgPOTWopen=pyqtSignal(object)


    ################################# Intialization Here ##################################################
    def __init__(self):

        super(Ui_CASH, self).__init__()
        self.osType = platform.system()
        #########################################################
        getLogPath(self)
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'CASHdashboard.ui')
        uic.loadUi(ui_login, self)
        dark = qdarkstyle.load_stylesheet_pyqt5()

        getbse2nse(self)

        self.rc=0


        self.setStyleSheet(dt1)

        osType = platform.system()

        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        self.title = tBar('CASH')
        self.headerFrame.layout().addWidget(self.title, 0, 1)
        self.title.sgPoss.connect(self.movWin)




        self.createTimers()
        self.createSlots()

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def createSlots(self):
        try:

            self.bt_min.clicked.connect(self.showMinimized)
            self.bt_close.clicked.connect(self.hide)


            # print('aaa')


        except:
            print(traceback.print_exc())

    def createTimers(self):
        pass





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_CASH()
    form.show()
    sys.exit(app.exec_())
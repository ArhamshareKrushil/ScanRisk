import  numpy as np
import csv
import os
import time
import traceback
import datetime

import pandas as pd
from PyQt5.QtGui import QKeySequence

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

class Ui_LogIn(QMainWindow):



    ################################# Intialization Here ##################################################
    def __init__(self):

        super(Ui_LogIn, self).__init__()
        self.osType = platform.system()
        #########################################################
        getLogPath(self)
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'login1.ui')
        uic.loadUi(ui_login, self)

        self.createShortcuts()
        dark = qdarkstyle.load_stylesheet_pyqt5()




        self.setStyleSheet(dt1)

        osType = platform.system()

        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
        else:
            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
        self.setWindowFlags(flags)

        # self.title = tBar('BOD')
        # self.headerFrame.layout().addWidget(self.title, 0, 1)
        # self.login.connect(self.movWin)




        self.createTimers()
        self.createSlots()

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.showMinimized)

    def createSlots(self):
        pass


            # print('aaa')



    def createTimers(self):
        pass




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_LogIn()
    form.show()
    sys.exit(app.exec_())
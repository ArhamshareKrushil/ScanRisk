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
from Application.Views.CorporateAction.support import *

class Ui_CoAction(QMainWindow):
    sgPOTM=pyqtSignal(object)
    sgsend=pyqtSignal(object)
    sgPOTMupdated = pyqtSignal()
    sgPOTWOpenposupdated = pyqtSignal()
    sgPOTWopen=pyqtSignal(object)


    ################################# Intialization Here ##################################################
    def __init__(self):

        super(Ui_CoAction, self).__init__()
        self.osType = platform.system()
        #########################################################
        getLogPath(self)
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'corporateAction1.ui')
        uic.loadUi(ui_login, self)
        dark = qdarkstyle.load_stylesheet_pyqt5()




        self.setStyleSheet(dt1)

        osType = platform.system()

        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        self.title = tBar('Corporate Action')
        self.headerFrame.layout().addWidget(self.title, 0, 1)
        self.title.sgPoss.connect(self.movWin)






        self.createTimers()
        self.createSlots()

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)

    def createSlots(self):
        try:



            self.bt_close_3.clicked.connect(self.hide)
            self.bt_min_3.clicked.connect(self.showMinimized)

            self.tbinput.clicked.connect(lambda:openinputfile(self))
            self.tboutput.clicked.connect(lambda:openoutputfile(self))
            self.pbcreate.clicked.connect(lambda:createFile(self))


            # print('aaa')


        except:
            print(traceback.print_exc())

    def createTimers(self):
       pass

    # def openfile(self):
    #     cbtext=self.cbinput.currentText()
    #     print(cbtext)
    #
    #     if cbtext=='POTM':
    #
    #         try:
    #
    #
    #             # print(self.prevDate)
    #
    #             prvdate = self.prevDate.strftime('%d%m%Y')
    #
    #
    #             defaultDir = os.path.join(r"\\192.168.102.204\ba\FNO", prvdate)
    #             fname = QFileDialog.getOpenFileName(self, 'Open file', defaultDir)[0]
    #             self.leinput.setText(fname)
    #         except:
    #             print(traceback.print_exc())
    #     else:
    #
    #         defaultDir = r'\\192.168.102.59\close\REPORTS\focaps\46'
    #         fname = QFileDialog.getOpenFileName(self, 'Open file', defaultDir)[0]
    #         self.leinput.setText(fname)




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_CoAction()
    form.show()
    sys.exit(app.exec_())
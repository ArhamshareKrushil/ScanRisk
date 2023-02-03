import  numpy as np
import csv
import os
import traceback
from Themes import dt1
import platform
from PyQt5 import uic
from Themes.dt2 import dt1
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import qdarkstyle

from Application.Views.titlebar import tBar

class Ui_feedmanager(QMainWindow):
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_feedmanager, self).__init__()
        self.osType = platform.system()
        #########################################################
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'feedM.ui')
        uic.loadUi(ui_login, self)



        dark = qdarkstyle.load_stylesheet_pyqt5()

        self.setStyleSheet(dt1)

        osType = platform.system()

        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.connectSlots()

    def connectSlots(self):

        self.bt_close_3.clicked.connect(self.hide)





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_feedmanager()
    form.show()
    sys.exit(app.exec_())
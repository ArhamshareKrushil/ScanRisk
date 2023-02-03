import  numpy as np
import csv
import os
import traceback
from Themes import dt1
import platform
from PyQt5 import uic
from Themes.dt2 import dt1
from PyQt5.QtWidgets import *
import qdarkstyle

class Ui_cframe(QMainWindow):
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_cframe, self).__init__()
        self.osType = platform.system()
        #########################################################
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'cframe.ui')
        uic.loadUi(ui_login, self)
        dark = qdarkstyle.load_stylesheet_pyqt5()





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_cframe()
    form.show()
    sys.exit(app.exec_())
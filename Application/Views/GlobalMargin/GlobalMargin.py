from Themes import dt1
import platform
from PyQt5 import uic
from Themes.dt2 import dt1
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import qdarkstyle
import os

from Application.Views.titlebar import tBar

from PyQt5.QtGui import QIcon, QKeySequence
from Application.Utils.createTables import tables_details_GlobalM


class GlobalMargin(QMainWindow):
    ################################# Intialization Here ##################################################
    def __init__(self):

        super(GlobalMargin, self).__init__()
        self.osType = platform.system()
        #########################################################
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'tableGM.ui')
        uic.loadUi(ui_login, self)
        dark = qdarkstyle.load_stylesheet_pyqt5()
        self.lastSerialNo = 0

        osType = platform.system()

        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        # self.title = tBar('TradeBook')
        # self.headerFrame.layout().addWidget(self.title, 0, 0)
        # self.title.sgPoss.connect(self.movWin)

        tables_details_GlobalM(self)
        self.setStyleSheet(dt1)

        self.createSlots()

        self.createShortcuts()
        # QSizeGrip(self.frameGrip)


    def createSlots(self):
        # self.pbApply.clicked.connect(self.setLimit)
        pass

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)


    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = GlobalMargin()
    form.show()
    sys.exit(app.exec_())

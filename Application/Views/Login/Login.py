import os
import traceback

import qdarkstyle
import requests
from PyQt5 import QtCore, QtGui, QtWidgets, Qt, uic
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi



class Ui_LogIn(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_LogIn, self).__init__() # Call the inherited classes __init__ method
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'Login.ui')
        uic.loadUi(ui_login, self)
        dark = qdarkstyle.load_stylesheet_pyqt5()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.hideOtherWidgets()

        try:
            self.createObjects()
            # self.connectAllSlots()

            self.logo.setGeometry(240, 80, 241, 331)
            self.logo2.setGeometry(50, 10, 151, 61)
            self.logo.setMinimumSize(0, 0)
            # #


            # pixmap = QPixmap('dp1.jpg')
            # self.label.setPixmap(pixmap)
            # self.label.show()


            # self.resize(pixmap.width(), pixmap.height())
        except:
            print(traceback.print_exc())


    def createObjects(self):
        self.createMovies()
        # self.animation1()
        # self.animation2()

    def createMovies(self):
        try:
            loc = os.getcwd().split('Application')
            print(loc)
            path = os.path.join(loc[0], 'Resources', 'Welcome1.gif')
            self.movie = Qt.QMovie(path)
            self.logo.setMovie(self.movie)
            # print("ENTERRR")

            self.movie.start()
            self.movie.setSpeed(100)
            self.movie.setScaledSize(QtCore.QSize(240, 320))
        except:
            print(self.movie)

        QtCore.QTimer.singleShot(5000, self.hide_movie)
        loc=os.getcwd().split('Application')
        print(loc)
        path=os.path.join(loc[0],'Resources','Welcome1.gif')
        self.movie3 = Qt.QMovie(path)
        self.logo2.setMovie(self.movie3)
        self.movie3.setSpeed(120)
        self.movie3.start()
        self.movie3.setScaledSize(QtCore.QSize(141, 200))

    def hide_movie(self):
        self.movie.stop()
        self.logo.setVisible(False)


    # def animation1(self):
    #     self.anim1 = QPropertyAnimation(self.logo, b"geometry")
    #     self.anim1.setDuration(100)
    #     self.anim1.setStartValue(QRect(79, 20, 371, 281))
    #     self.anim1.setEndValue(QRect(159, 20, 241, 51))
    #     # self.anim1.start()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_LogIn()
    ui.show()
    sys.exit(app.exec_())

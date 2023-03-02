from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import sys


class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)


class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.pushButton = QPushButton("click me")

        self.setCentralWidget(self.pushButton)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.dialog = Second(self)

    def on_pushButton_clicked(self):
        self.dialog.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())
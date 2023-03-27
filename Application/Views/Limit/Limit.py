import time
import numpy as np
import pandas as pd
from Themes import dt1
import platform
from PyQt5 import uic
from Themes.dt2 import dt1
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import *
import qdarkstyle
import os
from PyQt5.QtWidgets import *

from Application.Views.titlebar import tBar

from PyQt5.QtGui import QIcon, QKeySequence
from Application.Utils.createTables import tables_details_Limit

loc = os.getcwd().split('Application')[0]


class UI_Limit(QMainWindow):
    sgupdateTWMwithTmaster=pyqtSignal(dict)

    ################################# Intialization Here ##################################################
    def __init__(self):

        super(UI_Limit, self).__init__()
        self.osType = platform.system()
        #########################################################
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'Limit.ui')
        uic.loadUi(ui_login, self)
        dark = qdarkstyle.load_stylesheet_pyqt5()
        self.lastSerialNo = 0

        osType = platform.system()

        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.title = tBar('Limit')
        self.headerFrame.layout().addWidget(self.title, 0, 1)
        self.title.sgPoss.connect(self.movWin)

        tables_details_Limit(self)
        self.setStyleSheet(dt1)

        self.createSlots()

        self.createShortcuts()
        # QSizeGrip(self.frameGrip)


    def createSlots(self):
        self.bt_close_3.clicked.connect(self.hide)
        self.bt_min_3.clicked.connect(self.showMinimized)
        self.pbAdd.clicked.connect(self.Addrow)
        self.pbUpdate.clicked.connect(self.Updaterow)
        self.pbRemove.clicked.connect(self.REMOVErow)
        self.le_text.textChanged.connect(self.TextFilter)
        self.cbHeads.currentIndexChanged.connect(self.setfilterColumn)
        self.pbGetExcel.clicked.connect(self.export)

    def export(self):
        # abc = pd.DataFrame(self.table)

        loc = os.getcwd().split('Application')
        defaultDir = os.path.join(loc[0], 'Resources', 'ExcelReports')
        save = QFileDialog.getSaveFileName(self, 'Save file', defaultDir, "CSV (*.csv)")[0]

        # abc.to_csv(save, index=False, header=False)

        rc = self.smodel.rowCount()
        cc = self.smodel.columnCount()
        with open(save, 'w') as f:
            #########headings#########
            a = ''
            for i in self.model.heads:
                a = a + i + ','
            f.write(a + '\n')
            ######################
            for i in range(rc):
                a = ''
                for j in range(cc):
                    x = self.smodel.index(i, j).data()
                    a = a + str(x) + ','
                f.write(a + '\n')
                print(a)
        f.close()

    # def export(self):
    #     self.model.DelRows(0,self.lastSerialNo)
    #     self.model.lastSerialNo=0
    #     self.lastSerialNo=0
    #     self.model.rowCount()



    def setfilterColumn(self):
        self.smodel.setFilterKeyColumn(self.cbHeads.currentIndex())

    # def FillcbHeads(self):
    #     self.cbHeads.addItems(self.heads)
    #     self.smodel.setFilterKeyColumn(0)


    def TextFilter(self, text):
        self.smodel.setFilterFixedString(text)

    # def ClearFilter(self):
    #     self.smodel.setFilterFixedString('')
    #     self.smodel.setFilterKeyColumn(0)


    def Addrow(self):
        # self.table[self.model.lastSerialNo] = ['','','','','','']

        self.table[1:self.lastSerialNo+1]=self.table[:self.lastSerialNo]

        self.table[0] =['','']


        self.lastSerialNo += 1
        self.model.lastSerialNo += 1
        self.model.insertRows()
        self.model.rowCount()
        ind = self.model.index(0, 0)
        ind1 = self.model.index(0, 1)
        self.model.dataChanged.emit(ind, ind1)



    def Updaterow(self):
        st=time.time()

        self.sgupdateTWMwithTmaster.emit(self.model.updatedrow)
        path=os.path.join(loc,'Uploads','Deposit.csv')

        np.savetxt(path, self.table[:self.lastSerialNo], delimiter=",", header='UserID,Deposit', fmt='%s')
        # print(self.model.updatedrow)
        self.model.updatedrow={}



        et=time.time()
        print('time',et-st)

    def REMOVErow(self):
        i=self.tableView.selectionModel().selectedRows()[0].row()
        abc = self.tableView.selectedIndexes()[0].data()
        # print(i)

        self.model._data=np.delete(self.model._data, i, axis=0)
        # self.model._data=self.model._data[np.where(self.model._data[:,0] != abc)]
        self.lastSerialNo -= 1
        self.model.lastSerialNo -= 1

        self.model.rowCount()
        self.model.DelRows()


        ind = self.model.index(0, 0)
        ind1 = self.model.index(0, 1)
        self.model.dataChanged.emit(ind, ind1)


    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)


    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = UI_Tmaster()
    form.show()
    sys.exit(app.exec_())

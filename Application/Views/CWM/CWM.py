import  json
import traceback
import pandas as pd
from Themes import dt3
import platform
from PyQt5 import uic
from Themes.dt3 import dt3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import qdarkstyle
import os

from Application.Views.titlebar import tBar

from PyQt5.QtGui import QIcon, QKeySequence
from Application.Utils.createTables import tables_details_CWM


class ClientSummary(QMainWindow):
    ################################# Intialization Here ##################################################
    def __init__(self):

        super(ClientSummary, self).__init__()
        self.osType = platform.system()
        #########################################################
        ########################################################
        #########################################################
        loc1 = os.getcwd().split('Application')
        ui_login = os.path.join(loc1[0], 'Resources', 'UI', 'tableCWM.ui')
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

        tables_details_CWM(self)
        self.setStyleSheet(dt3)

        self.FillcbHeads()

        self.createSlots()

        self.createShortcuts()
        self.defaultColumnProfile()
        # QSizeGrip(self.gripFolio)

    def createSlots(self):
        self.pbClearfilter.clicked.connect(self.ClearFilter)
        self.le_text.textChanged.connect(self.TextFilter)
        self.cbHeads.currentIndexChanged.connect(self.setfilterColumn)
        self.pbGetExcel.clicked.connect(self.export)
        self.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.horizontalHeader().customContextMenuRequested.connect(self.headerRightClickMenu)
        self.tableView.customContextMenuRequested.connect(self.tableRightClickMenu)

    def saveAsDefaultColumnProfile(self):
        try:
            loc1 = os.getcwd().split('Application')
            defaultDir = os.path.join(loc1[0], 'Resources', 'CWM_ColPro', 'ColumnProfile')

            binData = self.tableView.horizontalHeader().saveState()
            save = QFileDialog.getSaveFileName(self, 'Save file', defaultDir)[0]
            print('save CWM save column profile', save)

            with open(save, 'wb') as f:
                f.write(binData)
            f.close()

            # loc = os.getcwd().split('Application')[0]
            settingsFilePath = os.path.join(loc1[0], 'Settings', 'Settings.json')

            f1 = open(settingsFilePath)
            pathDetails = json.load(f1)
            f1.close()
            pathDetails['CWM']['defaultColumnProfile'] = save

            pathDetails_new = json.dumps(pathDetails, indent=4)

            f2 = open(settingsFilePath, 'w+')
            f2.write(pathDetails_new)
            # pathDetails= json.load(f1)
            f2.close()

        except:
            print(traceback.print_exc())

    def defaultColumnProfile(self):
        loc = os.getcwd().split('Application')
        settingsFilePath = os.path.join(loc[0], 'Settings', 'Settings.json')
        f1 = open(settingsFilePath)
        pathDetails = json.load(f1)
        f1.close()
        lastCPFilePath = pathDetails['CWM']['defaultColumnProfile']
        with open(lastCPFilePath, 'rb') as f:
            binData = f.read()
        f.close()
        self.tableView.horizontalHeader().restoreState(binData)

    def ResetDefaultColumnProfile(self):
        loc = os.getcwd().split('Application')
        settingsFilePath = os.path.join(loc[0], 'Settings', 'Settings.json')
        f1 = open(settingsFilePath)
        pathDetails = json.load(f1)
        f1.close()
        lastCPFilePath = pathDetails['CWM']['defaultColumnProfile']
        with open(lastCPFilePath, 'rb') as f:
            binData = f.read()
        f.close()
        self.tableView.horizontalHeader().restoreState(binData)

    def saveColumnProfile(self):
        try:
            loc = os.getcwd().split('Application')
            defaultDir = os.path.join(loc[0], 'Resources', 'CWM_ColPro', 'ColumnProfile')
            # defaultDir = r'../Resources/CWM_ColPro/ColumnProfile'

            binData = self.tableView.horizontalHeader().saveState()
            save = QFileDialog.getSaveFileName(self, 'Save file', defaultDir)[0]
            print('save CWSW save column profile', save)

            with open(save, 'wb') as f:
                f.write(binData)
            f.close()

            loc = os.getcwd().split('Application')
            settingsFilePath = os.path.join(loc[0], 'Settings', 'Settings.json')

            f1 = open(settingsFilePath)
            pathDetails = json.load(f1)
            f1.close()
            pathDetails['CWM']['lastSavedColumnProfile'] = save

            pathDetails_new = json.dumps(pathDetails, indent=4)

            f2 = open(settingsFilePath, 'w+')
            f2.write(pathDetails_new)
            # pathDetails= json.load(f1)
            f2.close()

        except:
            print(traceback.print_exc())

    def openColumnProfile(self):
        loc = os.getcwd().split('Application')
        defaultDir = os.path.join(loc[0], 'Resources', 'CWM_ColPro', 'ColumnProfile')

        openF = QFileDialog.getOpenFileName(self, 'Open file', defaultDir)[0]

        with open(openF, 'rb') as f:
            binData = f.read()
        f.close()

        self.tableView.horizontalHeader().restoreState(binData)

    def headerRightClickMenu(self, position):
        try:
            # print('dfdsfdsf')
            # a=(self.tableView.selectedIndexes()[0].data())
            menu = QMenu()

            saveColumnProfile = menu.addAction("Save New Col profile")
            restoreColumnProfile = menu.addAction("Open Col Profile")
            saveAsDefault = menu.addAction("SaveAs Defalt Col Profile")
            hideColumn = menu.addAction("Hide")
            reset = menu.addAction("Reset")

            # cancelAction = menu.addAction("Cancel")
            action = menu.exec_(self.tableView.horizontalHeader().mapToGlobal(position))
            if action == saveColumnProfile:
                self.saveColumnProfile()
            elif (action == restoreColumnProfile):
                self.openColumnProfile()
            elif (action == saveAsDefault):
                self.saveAsDefaultColumnProfile()
            elif (action == hideColumn):
                x = (self.tableView.horizontalHeader().logicalIndexAt(position))
                self.tableView.horizontalHeader().hideSection(x)

            elif (action == reset):
                if self.tableView.horizontalHeader().sectionsHidden():

                    count = self.tableView.horizontalHeader().count()
                    for i in range(count):
                        if self.tableView.horizontalHeader().isSectionHidden(i):
                            self.tableView.horizontalHeader().showSection(i)

                # self.ResetDefaultColumnProfile()

        except:
            print(sys.exc_info()[1])

    def tableRightClickMenu(main, position):
        try:
            # a=(self.tableView.selectedIndexes()[0].data())
            Menu = QMenu()
            Help = Menu.addAction("Help")
            action = Menu.exec_(main.tableView.mapToGlobal(position))

            if action == Help:
                pass

        except:
            print(sys.exc_info()[1])
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
            #########################
            for i in range(rc):
                a = ''
                for j in range(cc):
                    x = self.smodel.index(i, j).data()
                    a = a + str(x) + ','
                f.write(a + '\n')
                print(a)
        f.close()



    def setfilterColumn(self):
        self.smodel.setFilterKeyColumn(self.cbHeads.currentIndex())

    def FillcbHeads(self):
        self.cbHeads.addItems(self.heads)
        self.smodel.setFilterKeyColumn(0)


    def TextFilter(self, text):
        self.smodel.setFilterFixedString(text)

    def ClearFilter(self):
        self.smodel.setFilterFixedString('')
        self.smodel.setFilterKeyColumn(0)

    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)


    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)


    def getCsv(self):
        rc = self.smodel.rowCount()
        cc = self.smodel.columnCount()
        with open('d:/abc.csv','w') as f:
            for i in range(rc):
                a = ''
                for j in range(cc):
                    x = self.smodel.index(i,j).data()
                    a = a + str(x)+ ','
                f.write(a+'\n')
                # print(a)
        f.close()
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = ClientSummary()
    form.show()
    sys.exit(app.exec_())

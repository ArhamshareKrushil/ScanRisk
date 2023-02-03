# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
import logging
import linecache
from PyQt5.QtCore import QObject,pyqtSlot,pyqtSignal,QTimer
from database_conn import *
from download_master import *
import time
# import pyodbc
import sqlalchemy
import pandas as pd

import traceback
import numpy as np
import datetime
import csv
import os


class uploader_fo(QObject):
    sgUserTrd = pyqtSignal(object)
    sgNewTrade = pyqtSignal()

    sgLTCheck = pyqtSignal(str)
    sgLTT = pyqtSignal(str)
    sgTCount = pyqtSignal(int)
    sgTradeError = pyqtSignal(str)

    sgFileNotFound = pyqtSignal(bool)

    def __init__(self):
        super(uploader_fo, self).__init__()
        today = (datetime.datetime.today() - datetime.timedelta(days=0)).strftime('%m%d')

        # self.changeFilename()
        #
        # self.fileName = os.path.join(self.filePath ,  '%sTRD.TXT' % today)
        self.fileName = r'C:\OdinIntegrated\Admin\OnLineBackup\Nse Derivatives\Trades\%sTRD.TXT' % today
#        """ C:\OdinIntegrated\Admin\OnLineBackup\NSE Derivatives\Trades\0924TRD.TXT"""
        self.rc = 0
        self.user = []
        self.techid = []
        self.isStart = False
        self.pause = False
        self.isReset = False
        self.NewTrade =False
        self.isFileFound =False

        # self.Contract_df, self.summary_df = get_contract_master_FNO(False)


    def upload(self):
        try:
            if(self.isStart == True):
                tyty = datetime.datetime.now()

                lines = linecache.getlines(self.fileName)
                # print(len(lines))
                if (lines != []):
                    self.isFileFound=False
                    self.sgFileNotFound.emit(False)


                    newLines = lines[self.rc:]
                    # print(newLines)
                    for k in newLines:
                        i  = k.split(',')

                        if (i[11] in self.user):
                            # print('i',self.user)
                            symbol = i[7].replace(' ', '')
                            if(symbol == ''):
                                token = int(i[2])
                                fltr = np.asarray([token])
                                lua1 = self.summary_df[np.in1d(self.summary_df[:, 2], fltr)]
                                lua = self.summary_df[np.in1d(self.summary_df[:, 2], fltr)]
                                if (lua1.size == 0):
                                    lua = self.Contract_df[np.in1d(self.Contract_df[:, 2], fltr)]
                                    self.summary_df = np.vstack([self.summary_df, lua])
                                price = float(i[15]) / 100
                                print(price,float(i[15]))
                            else:


                                fltr = np.asarray([symbol])
                                lua = self.summary_df[np.in1d(self.summary_df[:, 4], fltr)]
                                if (lua.size == 0):
                                    lua = self.Contract_df[np.in1d(self.Contract_df[:, 4], fltr)]
                                    self.summary_df = np.vstack([self.summary_df, lua])
                                    # print('inner lua',lua)
                                    token = lua[0][2]

                                else:
                                    token = lua[0][2]
                                price = float(i[15])

                            # print(lua)
                            bs = int(i[13])
                            qty = -int(i[14]) if bs == 2 else int(i[14])
                            # price = float(i[15])
                            amt = -qty * price
                            # token = lua[0][2]

                            abc = dt.Frame([[token],
                                            [lua[0][4]], [lua[0][3]], [lua[0][6]], [lua[0][7]], [lua[0][8]],
                                            [qty], [amt], [price], [int(lua[0][11])], [int(lua[0][14])],
                                            [lua[0][0]], [lua[0][5]], [lua[0][9]], [lua[0][10]]]).to_numpy()

                            self.sgUserTrd.emit(abc)
                            self.NewTrade = True
                        self.sgLTT.emit(i[22])
                        self.rc = self.rc + 1
                        self.sgTCount.emit(self.rc)

                    tyty1 = datetime.datetime.now().strftime('%X')
                    self.sgLTCheck.emit(tyty1)
                    # print(self.rc)
                    linecache.clearcache()

                else:
                    self.isFileFound = True
                    self.sgFileNotFound.emit(True)
                    linecache.clearcache()


        except FileNotFoundError:
            print(sys.exc_info(),self.fileName)
            if(self.isFileFound==False):
                self.isFileFound = True
                self.sgFileNotFound.emit(True)
        except:
            print(traceback.print_exc())
            print(sys.exc_info()[1],'abc')
            self.sgTradeError.emit(str(sys.exc_info()[1]))




    def setUploadStart(self):
        print('uploader has started')
        self.isStart =True
    def setUploadStop(self):
        self.isStart =False

    # def loadFilePath(self):
    #     loc1 = os.getcwd().split('Application')
    #
    #     fileobject = os.path.join(loc1[0], 'Settings', 'TSettings.json')
    #     f = open(fileobject)
    #     jSettings = json.load(f)
    #     self.filePath = jSettings['filename_FO']
    # def changeFilename(self,a):
    #     pass
    #




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = uploader_fo()
    # form.show()
    sys.exit(app.exec_())

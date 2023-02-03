import traceback
import os
# import bod
from PyQt5.QtWidgets import *
import pandas as pd
import datetime
import csv
import numpy as np
from Application.Utils.configReader import readConfig_All
from Application.Utils.support import *
import datetime


loc1 = os.getcwd().split('Application')

uploadLoc = os.path.join(loc1[0], 'Downloads')


def openinputfile(self):
    self.cbtext = self.cbinput.currentText()
    # print(self.cbtext)

    if self.cbtext == 'POTM':

        try:

            # print(self.prevDate)

            prvdate = self.prevDate.strftime('%d%m%Y')

            defaultDir = os.path.join(r"\\192.168.102.204\ba\FNO", prvdate)
            fname = QFileDialog.getOpenFileName(self, 'Open file', defaultDir)[0]
            self.leinput.setText(fname)
        except:
            print(traceback.print_exc())
    else:

        defaultDir = r'\\192.168.102.59\close\REPORTS\focaps\46'
        fname = QFileDialog.getOpenFileName(self, 'Open file', defaultDir)[0]
        self.leinput.setText(fname)

def openoutputfile(self):
    if self.cbtext =='POTM':
        defaultDir=os.path.join(uploadLoc,'POTM')
        fname = QFileDialog.getSaveFileName(self, 'Save file', defaultDir,"CSV (*.csv)")[0]
        self.leoutput.setText(fname)
    else:
        defaultDir = os.path.join(uploadLoc, 'OpenPos')
        fname = QFileDialog.getSaveFileName(self, 'Save file', defaultDir, "CSV (*.csv)")[0]
        self.leoutput.setText(fname)




def createFile(self):



    path=self.leinput.text()
    path1 = self.leoutput.text()

    cbcol = self.cbcolumn.currentText()
    cbtype = self.cbtype.currentText()
    symbol = self.leSymbol.text()
    value = self.levalue.text()

    if self.cbtext == 'POTM':
        # print(path1)





        with open(path, 'r') as f1:
            with open(path1, 'w+') as f:
                reader = csv.reader(f1, lineterminator="\n")
                writer = csv.writer(f, lineterminator="\n")

                for j, row in enumerate(reader):
                    # print(row[10])
                    if(row[9]==symbol):
                        # print(row[12],row)
                        if cbcol=='Symbol':
                            row[10]=value
                        elif cbcol== 'Strike':
                            if cbtype=='ADD':
                                print('ADD')
                                row[12] = str(float(row[12])+float(value))
                            elif cbtype=='SUB':
                                row[12] = str(float(row[12]) - float(value))
                            elif cbtype=='MULTIPLY':
                                row[12] = str(float(row[12]) * float(value))
                            elif cbtype=='DIVIDE':
                                row[12] = str(float(row[12]) / float(value))
                        elif cbcol =='Expiry':
                            # print(value)
                            exp=datetime.datetime.strptime(value, '%d-%m-%Y').strftime('%d-%b-%y')
                            row[11]=str(exp)

                        # print(row[10])
                    writer.writerow(row)
                # writer.writerow('\n')
            f.close()
        f1.close()

    else:
        # print('inelse')
        with open(path1,'w+') as sp:
            with open(path,'r') as f:
                c = csv.reader(f)
                for i, row in enumerate(c):
                    if (i < 4):
                        pass
                    else:
                        ada = str(row[1])
                        if (ada.startswith('IO')):
                            it = 'OPTIDX'
                        elif (ada.startswith('IF')):
                            it = 'FUTIDX'
                        elif (ada.startswith('EO')):
                            it = 'OPTSTK'
                        else:
                            it = 'FUTSTK'
                        b = ada.split(' ', 5)
                        if (it == 'OPTIDX' or it == 'OPTSTK'):
                            sym = b[2]
                            exp = datetime.datetime.strptime(b[3], '%d%b%y').strftime('%Y%m%d')
                            spr = format(float(b[4]), '.2f')
                            ot = b[1]
                        else:
                            sym = b[1]
                            exp = datetime.datetime.strptime(b[2], '%d%b%y').strftime('%Y%m%d')
                            spr = ' '
                            ot = ' '
                        # print('hello')
                        if (sym == symbol and it in ['OPTSTK','OPTIDX']):
                            # print(sym,symbol)
                            # print(row[12],row)
                            if cbcol == 'Symbol':
                                pass
                            elif cbcol == 'Strike':
                                if cbtype == 'ADD':
                                    print('ADD')
                                    spr = float(spr) +float(value)
                                elif cbtype == 'SUB':
                                    spr = float(spr) - float(value)
                                elif cbtype == 'MULTIPLY':
                                    spr = float(spr) * float(value)
                                elif cbtype == 'DIVIDE':
                                    spr = float(spr) / float(value)
                            elif cbcol == 'Expiry':
                                exp = datetime.datetime.strptime(value, '%d-%m-%Y').strftime('%Y%m%d')


                        #
                        # elif(sym == 'PETRONET' and it=='OPTSTK'):
                        #     spr = float(spr) - 4.85


                        sp.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ((
                            row[0], it, sym, exp, spr, ot, ada, row[2], row[3], row[4], row[5], row[6], row[7],
                            row[8])))
            f.close()
        sp.close()




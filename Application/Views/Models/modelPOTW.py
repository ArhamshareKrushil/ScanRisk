import sys
import traceback
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
from PyQt5.QtWidgets import QTableView
import time

from PyQt5 import QtGui
from PyQt5.QtGui import QBrush

class ModelTS(QtCore.QAbstractTableModel):

    def __init__(self, data,heads,isReset=False):
        super(ModelTS, self).__init__()
        self._data = data
        # self.dta1 = []

        # self.color = []
        # self._data1 = data
        self.heads=heads
        if(isReset):
            self.flastSerialNo = data.shape[0]
        else:
            self.flastSerialNo = 0


    def data(self, index, role):
        try:
            value = self._data[index.row(), index.column()]
            if role == Qt.DisplayRole:

                if index.column() in [9, 11, 14, 16, 20, 21, 22, 23,31,32]:
                    value = int(value)
                    return value


                elif index.column() in [24,25,26,27,28,29,30]:
                    value = float(value)
                    return value

                return value

            if role == Qt.TextAlignmentRole:
                value = self._data[index.row(), index.column()]

                if index.column() in [9, 11, 14, 16, 20, 21, 22, 23,24,25,26,27,28,29,30,31,32]:
                    # Align right, vertical middle.
                    return Qt.AlignVCenter + Qt.AlignRight


            # if role == Qt.BackgroundColorRole:
            #     # print(role)
            #     value = self._data[index.row(), index.column()]
            #     if(index.column() in [7,8,9,10]):
            #         # print("there is meeeeeeeeeeee")
            #         print("dataaaaaaaaaaa",self.dta1)
            #         if(len(self.dta1) != 0):
            #             # print(value,type(value), self.dta1[index.row()], type(self.dta1[index.row()]))
            #
            #
            #             if(value > self.dta1[index.row()][index.column()-7]):
            #                 self.color[index.row()][index.column()-7] = '#4FB7E0'
            #                 return QtGui.QColor('#4FB7E0')
            #
            #             elif (value < self.dta1[index.row()][index.column()-7]):
            #                 self.color[index.row()][index.column()-7] = '#c2364b'
            #
            #                 return QtGui.QColor('#c2364b')
            #             else:
            #                 return QtGui.QColor(self.color[index.row()][index.column()-7])
            #
            #     # if(index.column() in [13,15]):
            #     #     return QtGui.QColor(48, 57, 63)



        except:
            print(traceback.print_exc())
    def rowCount(self, index=''):
        return self.flastSerialNo



    def columnCount(self, index):
        return len(self.heads)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.heads[section])

    def insertRows(self, position=0, rows=1, index=QModelIndex()):
        try:
            # self.beginInsertRows(QModelIndex(), position, position + rows - 1)
            self.beginInsertRows(QModelIndex(), self.flastSerialNo - 1, self.flastSerialNo - 1)
            self.endInsertRows()
            return True
        except:
            print(sys.exc_info())

    def insertMultiRows(self, position=0, rows=1, index=QModelIndex()):
        try:
            self.beginInsertRows(QModelIndex(), position, position + rows - 1)
            # self.beginInsertRows(QModelIndex(), self.flastSerialNo - 1, self.flastSerialNo - 1)
            self.endInsertRows()
            return True
        except:
            print(sys.exc_info())

    def DelRows(self, position=0, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, rows)
        self.endRemoveRows()
        return  True


    def DelAllRows(self, position=0, rows=1, index=QModelIndex()):

        rrr = self.rowCount()
        self.beginRemoveRows(QModelIndex(),0,rrr-1)


        self.endRemoveRows()
        return  True
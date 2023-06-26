import numpy as np
import sys
import traceback
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
import time

from PyQt5 import QtGui
from PyQt5.QtGui import QBrush

class ModelTS(QtCore.QAbstractTableModel):

    def __init__(self, data,heads,isReset=False):
        super(ModelTS, self).__init__()
        self._data = data
        # self._data1 = data
        self.heads=heads
        self.updatedrow={}
        if(isReset):
            self.lastSerialNo = data.shape[0]
        else:
            self.lastSerialNo = 0


    def data(self, index, role):
        try:
            value = self._data[index.row(), index.column()]
            if role == Qt.DisplayRole:

                if isinstance(value, int):
                    value = int(value)
                    return value
                elif isinstance(value, float):
                    if(value > 1000000):
                        value = int(value)
                    return value
                else:
                    return str(value)

            elif role == Qt.TextAlignmentRole:
                value = self._data[index.row(), index.column()]

                if isinstance(value, int) or isinstance(value, float):
                    # Align right, vertical middle.
                    return Qt.AlignVCenter + Qt.AlignRight

            elif role == Qt.EditRole:
                value = self._data[index.row(), index.column()]
                # value=self.editvalue
                # self._data[index.row(), index.column()]=''
                # print(self.editvalue)
                return str(value)



        except:
            print(traceback.print_exc())

    def setData(self, index, value, role=None):
        # print('dd')
        if role == Qt.EditRole:
            if value == self._data[index.row()][index.column()]:
                return False
            else:
                if value=='':
                    return False

                else:
                    Tid=self._data[index.row()][0]
                    if Tid!='':

                        if Tid not in self.updatedrow:
                            Uid=self._data[index.row()][1]

                            self.updatedrow[Tid]={}
                            self.updatedrow[Tid]['Oldid']=Uid
                            self.updatedrow[Tid]['Newid']=str(value)
                        else:
                            self.updatedrow[Tid]['Newid'] = str(value)



                    self._data[index.row()][index.column()] = str(value)
                    return True





    def flags(self, index):
        return  Qt.ItemIsEnabled | Qt.ItemIsEditable


    def rowCount(self, index=''):
        return self.lastSerialNo



    def columnCount(self, index):
        return len(self.heads)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.heads[section])

    def insertRows(self, position=0, rows=1, index=QModelIndex()):
        try:
            # self.beginInsertRows(QModelIndex(), position, position + rows - 1)
            # self.beginInsertRows(QModelIndex(), position, position + rows - 1)
            self.beginInsertRows(QModelIndex(), self.lastSerialNo - 1, self.lastSerialNo - 1)
            self.endInsertRows()
            return True
        except:
            print(sys.exc_info())

    def DelRows(self, position=0, rows=0, index=QModelIndex()):


        self.beginRemoveRows(QModelIndex(),position,position+rows)
        self.endRemoveRows()


        return  True
    #
    #
    # def DelRows(self, position=0, rows=1, index=QModelIndex()):
    #     self.beginRemoveRows(QModelIndex(), 0, 0)
    #     self.endRemoveRows()
    #     return  True
    #

    def DelAllRows(self, position=0, rows=1, index=QModelIndex()):

        rrr = self.rowCount()
        self.beginRemoveRows(QModelIndex(),0,rrr-1)


        self.endRemoveRows()
        return  True
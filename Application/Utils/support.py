import  datetime
import time
import traceback
from py_vollib.black_scholes import black_scholes
import numpy as np
import json
import datetime
import os
import logging

from PyQt5.QtCore import *
import datatable as dt
import pandas as pd
from  PyQt5 import QtCore


def getLogPath(xclass):
    today =  datetime.datetime.today().strftime('%Y%m%d')
    loc1 = os.getcwd().split('Application')
    xclass.loc1 = loc1
    logDir = os.path.join(loc1[0] , 'Logs','%s'%today)
    # print('logDir',logDir)
    try:
        os.makedirs(logDir)
    except OSError as e:
        pass
    ls=os.listdir(logDir)
    attempt =1

    for i in ls:
        x=i.replace('.log','')
        y=x.split('_')
        if( int(y[1]) >= attempt):
            attempt=int(y[1])+1

    # print('attempt',attempt)
    xclass.logPath= os.path.join(logDir, '%s_%s.log'%(today,attempt))


    # print('main.logPath',xclass.logPath)
    logging.basicConfig(filename=xclass.logPath, filemode='a+', level=logging.INFO,
                        format='%(asctime)s    %(levelname)s    %(module)s  %(funcName)s   %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')


@pyqtSlot(list)
def updatePOTW(main,data):

    # print(data,data[0],data[2])

    fltrarr1 = main.POTW.table[np.where((main.POTW.table[:main.POTW.model.lastSerialNo, 0] == data[0]) & (
            main.POTW.table[:main.POTW.model.lastSerialNo, 2] == data[2]))]

    if (fltrarr1.size != 0):
        # print('update')
        #     isRecordExist=True
        #
        # if(isRecordExist):
        #     # print('exist')

        SerialNo = fltrarr1[0][12]



        editList = [8, 9, 15, 16, 20, 23]
        main.POTW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23]]

        for i in editList:
            ind = main.POTW.model.index(SerialNo, i)
            main.POTW.model.dataChanged.emit(ind, ind)



    else:

        main.POTW.table[main.POTW.model.lastSerialNo, :] = [data[0], data[1], data[2], data[3], data[4], data[5],
                                                            data[6], data[7], data[8], data[9], data[10],
                                                            data[11], main.POTW.model.lastSerialNo, data[13], data[14], data[15], data[16], data[17], data[18],
                                                            data[19], data[20], data[21], data[22], data[23]]

        # main.POTW.table[main.POTW.model.lastSerialNo, :] = data

        main.POTW.lastSerialNo += 1
        main.POTW.model.lastSerialNo += 1
        main.POTW.model.insertRows()
        main.POTW.model.rowCount()
        ind = main.POTW.model.index(0, 0)
        ind1 = main.POTW.model.index(0, 1)
        main.POTW.model.dataChanged.emit(ind, ind1)

        main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])

    # print('ppp', main.POTW.lastSerialNo)



    # main.isPOTWupdated = True

    # if UserID not in main.POTW.clientList:
    #     main.POTW.clientList.append(UserID)



# def updatePOTWopenPosition(main,data):
#     # st=time.time()
#     main.POTW.table[:data.shape[0], :] = data
#     # main.POTW.model._data[:data.shape[0], :] = data[:, 1:]
#
#     main.POTW.lastSerialNo += data.shape[0]
#
#     main.POTW.model.lastSerialNo += data.shape[0]
#
#     main.POTW.model.insertMultiRows(rows=data.shape[0])
#
#     main.POTW.model.rowCount()
#     ind = main.POTW.model.index(0, 0)
#     ind1 = main.POTW.model.index(0, 1)
#     main.POTW.model.dataChanged.emit(ind, ind1)
#     # et=time.time()
#     # print('timettt',et-st)
#
#     # main.POTW.table[main.POTW.model.lastSerialNo, :] = [data['UserID'], data['Exchange'], data['Token'], , sym, exp,
#     #                                                     strike, opt, TQty, Tamt, 0,
#     #                                                     0, main.POTW.model.lastSerialNo, 0, 0, TQty, Tamt, 0.0, 0.0,
#     #                                                     0.0, netPrem, 0.0, 0.0, premMrg]
#     # main.POTW.table[main.POTW.model.lastSerialNo, :] = data
#
#     # main.POTW.lastSerialNo += 1
#     # main.POTW.model.lastSerialNo += 1
#     # main.POTW.model.insertRows()
#     # main.POTW.model.rowCount()
#     # ind = main.POTW.model.index(0, 0)
#     # ind1 = main.POTW.model.index(0, 1)
#     # main.POTW.model.dataChanged.emit(ind, ind1)

def updatePOTWopenPosition(main,data):
    # st=time.time()
    # print(data)

    fltrarr1 = main.POTW.table[np.where((main.POTW.table[:main.POTW.model.lastSerialNo, 0] == data[0]) & (
            main.POTW.table[:main.POTW.model.lastSerialNo, 2] == data[2]))]

    if (fltrarr1.size != 0):
        # print('update')
        #     isRecordExist=True
        #
        # if(isRecordExist):
        #     # print('exist')

        SerialNo = fltrarr1[0][12]

        editList = [8, 9, 15, 16, 20, 23]
        main.POTW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23]]

        for i in editList:
            ind = main.POTW.model.index(SerialNo, i)
            main.POTW.model.dataChanged.emit(ind, ind)



    else:

        main.POTW.table[main.POTW.model.lastSerialNo, :] = [data[0], data[1], data[2], data[3], data[4], data[5],
                                                            data[6], data[7], data[8], data[9], data[10],
                                                            data[11], main.POTW.model.lastSerialNo, data[13], data[14],
                                                            data[15], data[16], data[17], data[18],
                                                            data[19], data[20], data[21], data[22], data[23]]

        # main.POTW.table[main.POTW.model.lastSerialNo, :] = data

        main.POTW.lastSerialNo += 1
        main.POTW.model.lastSerialNo += 1
        main.POTW.model.insertRows()
        main.POTW.model.rowCount()
        ind = main.POTW.model.index(0, 0)
        ind1 = main.POTW.model.index(0, 1)
        main.POTW.model.dataChanged.emit(ind, ind1)

        main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])

    # print('ppp', main.POTW.lastSerialNo)

    # main.POTW.table[:data.shape[0], :] = data
    # # main.POTW.model._data[:data.shape[0], :] = data[:, 1:]
    #
    # main.POTW.lastSerialNo += data.shape[0]
    #
    # main.POTW.model.lastSerialNo += data.shape[0]
    #
    # main.POTW.model.insertMultiRows(rows=data.shape[0])
    #
    # main.POTW.model.rowCount()
    # ind = main.POTW.model.index(0, 0)
    # ind1 = main.POTW.model.index(0, 1)
    # main.POTW.model.dataChanged.emit(ind, ind1)
    # # et=time.time()
    # print('timettt',et-st)

    # main.POTW.table[main.POTW.model.lastSerialNo, :] = [data['UserID'], data['Exchange'], data['Token'], , sym, exp,
    #                                                     strike, opt, TQty, Tamt, 0,
    #                                                     0, main.POTW.model.lastSerialNo, 0, 0, TQty, Tamt, 0.0, 0.0,
    #                                                     0.0, netPrem, 0.0, 0.0, premMrg]
    # main.POTW.table[main.POTW.model.lastSerialNo, :] = data

    # main.POTW.lastSerialNo += 1
    # main.POTW.model.lastSerialNo += 1
    # main.POTW.model.insertRows()
    # main.POTW.model.rowCount()
    # ind = main.POTW.model.index(0, 0)
    # ind1 = main.POTW.model.index(0, 1)
    # main.POTW.model.dataChanged.emit(ind, ind1)


def update_DB_TWSWM(main,data):
    main.TWSWM.table[:data.shape[0], :] = data
    # main.POTW.model._data[:data.shape[0], :] = data[:, 1:]

    main.TWSWM.lastSerialNo += data.shape[0]

    main.TWSWM.model.lastSerialNo += data.shape[0]

    main.TWSWM.model.insertMultiRows(rows=data.shape[0])

    main.TWSWM.model.rowCount()
    ind = main.TWSWM.model.index(0, 0)
    ind1 = main.TWSWM.model.index(0, 1)
    main.TWSWM.model.dataChanged.emit(ind, ind1)


@QtCore.pyqtSlot(list)
def updateTWSWM(main, data):
    # print('TWSWM', data)
    rowarray = np.where((main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 0] == data[0]) & (main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 1] == data[1]))[0]



    if (rowarray.size !=0):



        rowNo = rowarray[0]



        editList = [2,3,4,5,6,7,8]
        main.TWSWM.table[rowNo, editList] = [data[2], data[3],data[4], data[5],data[6],data[7],data[8]]

        for i in editList:
            ind = main.TWSWM.model.index(rowNo, i)
            main.TWSWM.model.dataChanged.emit(ind, ind)

    else:





        main.TWSWM.table[main.TWSWM.model.lastSerialNo,[0,1,2,3,4,8,9]] = [data[0],data[1],data[2],data[3],data[4],data[8],data[9]]

        main.TWSWM.lastSerialNo += 1
        main.TWSWM.model.lastSerialNo += 1
        main.TWSWM.model.insertRows()
        main.TWSWM.model.rowCount()
        ind = main.TWSWM.model.index(0, 0)
        ind1 = main.TWSWM.model.index(0, 1)
        main.TWSWM.model.dataChanged.emit(ind, ind1)


def update_DB_TWM(main,data):
    main.TWM.table[:data.shape[0], :] = data
    # main.POTW.model._data[:data.shape[0], :] = data[:, 1:]

    main.TWM.lastSerialNo += data.shape[0]

    main.TWM.model.lastSerialNo += data.shape[0]

    main.TWM.model.insertMultiRows(rows=data.shape[0])

    main.TWM.model.rowCount()
    ind = main.TWM.model.index(0, 0)
    ind1 = main.TWM.model.index(0, 1)
    main.TWM.model.dataChanged.emit(ind, ind1)



@QtCore.pyqtSlot(object)
def updateTWM(main, data):
    # print('TWM', data)


    rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == data[0])[0]
    # print(fltrarr)

    # if (fltrarr.size != 0):
    #         isRecordExist = True

    if (rowarray.size != 0):
        # print('exist')


        # rowNo = np.where(main.TWM.table[:, 0] == data[0])[0][0]
        rowNo=rowarray[0]


        editList = [1, 2,3,4,5,8,9,12,13,14]
        main.TWM.table[rowNo, editList] = [data[1], data[2],data[3], data[4],data[5],data[8],data[9],data[12],data[13],data[14]]

        for i in editList:
            ind = main.TWM.model.index(rowNo, i)
            main.TWM.model.dataChanged.emit(ind, ind)

    else:

        main.TWM.table[main.TWM.model.lastSerialNo,[0,1,2,3,6,7,9,10,12,13,14]] =[data[0],data[1], data[2],data[3], data[6],data[7],data[9],data[10],data[12],data[13],data[14]]

        main.TWM.lastSerialNo += 1
        main.TWM.model.lastSerialNo += 1
        main.TWM.model.insertRows()
        main.TWM.model.rowCount()
        ind = main.TWM.model.index(0, 0)
        ind1 = main.TWM.model.index(0, 1)
        main.TWM.model.dataChanged.emit(ind, ind1)





def updateBWM(main):
    if(main.TWM.model.lastSerialNo !=0):

        df3 = dt.Frame(main.TWM.table[:main.TWM.model.lastSerialNo,
                       [6, 1,2,13,4,5,8,9,10,14]],
                       names=['Branch', 'ExpoM', 'SpanM', 'netM', 'futmtm', 'optMTM','FNO_MTM','PRM_MRG','Sheet','PeakMRG'])

        df3[1:] = dt.float64

        x = df3[:, dt.sum(dt.f[1:]), dt.by('Branch')]


        for i in x.to_numpy():
            rowarray = np.where(main.BWM.table[:main.BWM.model.lastSerialNo, 0] == i[0])[0]
            # print(fltrarr)

            # if (fltrarr.size != 0):
            #         isRecordExist = True

            if (rowarray.size != 0):
                # print('exist')

                # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
                rowNo = rowarray[0]




                # print('rowNo',rowNo)

                editList = [1, 2, 3, 4, 5,6,7,8,9]
                main.BWM.table[rowNo, editList] = [i[1], i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]]

                for i in editList:
                    ind = main.BWM.model.index(rowNo, i)
                    main.BWM.model.dataChanged.emit(ind, ind)

            else:

                main.BWM.table[main.BWM.model.lastSerialNo] = i

                main.BWM.lastSerialNo += 1
                main.BWM.model.lastSerialNo += 1
                main.BWM.model.insertRows()
                main.BWM.model.rowCount()
                ind = main.BWM.model.index(0, 0)
                ind1 = main.BWM.model.index(0, 1)
                main.BWM.model.dataChanged.emit(ind, ind1)



@QtCore.pyqtSlot(dict)
def updateLTP_POTW(main,data):
    try:
        if (main.POTW.model.lastSerialNo !=0):
            # print("pt")
            # x = (np.unique(main.POTW.table[:main.POTW.lastSerialNo, 2]))


            # if (data['Token'] in x ):
             #   print("2")
            fltr = np.asarray([data['Token']])
            x = main.POTW.table[np.in1d(main.POTW.table[:, 2], fltr), 12]
            # print(x)

            for i in x:
                netValue = main.POTW.table[i, 16]
                qty = main.POTW.table[i, 15]
                ins=main.POTW.table[i, 3]

                mtm = (qty * data['LTP']) + netValue

                if(ins in ['FUTSTK' ,'FUTIDX']):
                    editableList = [10, 11,21]
                else:
                    editableList = [10, 11, 22]


                main.POTW.table[i, editableList] = [data['LTP'],  mtm,mtm]

                for j in editableList:
                    ind = main.POTW.model.index(i, j)
                    # ind1 = main.marketW.model.index(i,1)
                    main.POTW.model.dataChanged.emit(ind, ind)


    except:

        print(traceback.print_exc())


def updateGlobalMargin(main):

    EXPOM=main.TWM.table[:, 1].sum()
    SPANM=main.TWM.table[:, 2].sum()
    NET_MRG=main.TWM.table[:,13].sum()
    # NET_MRG=main.TWM.table[:, 3].sum()
    FUT_MTM=main.TWM.table[:, 4].sum()
    OPT_MTM=main.TWM.table[:, 5].sum()
    FNO_MTM=FUT_MTM+OPT_MTM
    PRM_MRG=main.TWM.table[:, 12].sum()


    if(main.GlobalM.lastSerialNo !=0):

        editList = [0, 1,2, 3, 4,5,6]
        main.GlobalM.table[editList,1] = [SPANM,EXPOM,NET_MRG,FUT_MTM,OPT_MTM,FNO_MTM,PRM_MRG]

        # print(main.GlobalM.table)
        # print(main.GlobalM.table)

        for i in editList:
            ind = main.GlobalM.model.index(i, 1)
            main.GlobalM.model.dataChanged.emit(ind, ind)
    else:

        # main.GlobalM.table[main.GlobalM.lastSerialNo] = [SPANM,EXPOM,TotalM,FUT_MTM,OPT_MTM,FNO_MTM]

        main.GlobalM.table[:7,0]=['SPANM','EXPOM','TotalM','FUT_MTM','OPT_MTM','FNO_MTM','PRM_MRG']

        main.GlobalM.table[:7,1] = [SPANM, EXPOM, NET_MRG, FUT_MTM, OPT_MTM, FNO_MTM,PRM_MRG]

        for i in range(7):
            main.GlobalM.lastSerialNo += 1
            main.GlobalM.model.lastSerialNo += 1
            main.GlobalM.model.insertRows()
            main.GlobalM.model.rowCount()
            ind = main.GlobalM.model.index(0, 0)
            ind1 = main.GlobalM.model.index(0, 1)
            main.GlobalM.model.dataChanged.emit(ind, ind1)

    # main.GlobalM.lbllimit.setText(str(perc))


def updateMTM(main):
    if main.POTW.lastSerialNo!=0:


        df3 = dt.Frame(main.POTW.table[:main.POTW.model.lastSerialNo,
                       [0,4,11,21,22]],
                       names=['UserID', 'Symbol', 'MTM','FUT_MTM','OPT_MTM'])

        df3[2:] = dt.float64

        x = df3[:, dt.sum(dt.f[2:]), dt.by('UserID', 'Symbol')]

        x1=x[:, dt.sum(dt.f[2:]), dt.by('UserID')]




        for i in x.to_numpy():
            rowarray = np.where((main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 0] == i[0])& (main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 1] == i[1]))[0]
            # print(fltrarr)

            # if (fltrarr.size != 0):
            #         isRecordExist = True

            if (rowarray.size != 0):
                # print('exist')

                # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
                rowNo = rowarray[0]

                # print('rowNo',rowNo)

                editList = [5, 6, 7]
                main.TWSWM.table[rowNo, editList] = [i[3], i[4], i[2]]

                for i in editList:
                    ind = main.TWSWM.model.index(rowNo, i)
                    main.TWSWM.model.dataChanged.emit(ind, ind)

        for i in x1.to_numpy():
            rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == i[0])[0]
            # print(fltrarr)

            # if (fltrarr.size != 0):
            #         isRecordExist = True

            if (rowarray.size != 0):
                # print('exist')

                # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
                rowNo = rowarray[0]

                # print('rowNo',rowNo)

                editList = [4,5, 8]
                main.TWM.table[rowNo, editList] = [i[2], i[3], i[1]]

                for i in editList:
                    ind = main.TWM.model.index(rowNo, i)
                    main.TWM.model.dataChanged.emit(ind, ind)







def TWMdoubleClicked(main):
    UserID = main.TWM.tableView.selectedIndexes()[0].data()

    main.cFrame.DPOTW.show()
    main.cFrame.DPOTW.raise_()

    main.POTW.smodel.setClientCode(UserID)
    main.POTW.smodel.setFilterFixedString(UserID)

    main.POTW.le_text.setText(UserID)

    main.TWSWM.smodel.setClientCode(UserID)
    main.TWSWM.smodel.setFilterFixedString(UserID)





















































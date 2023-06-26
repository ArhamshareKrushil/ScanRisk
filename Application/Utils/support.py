import  datetime
import requests
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

from py_vollib.black_scholes.implied_volatility import implied_volatility as iv
from py_vollib.black_scholes.greeks.analytical import delta
from py_vollib.black_scholes.greeks.analytical import gamma
from py_vollib.black_scholes.greeks.analytical import rho
from py_vollib.black_scholes.greeks.analytical import theta
from py_vollib.black_scholes.greeks.analytical import vega
from py_vollib.helpers.exceptions import PriceIsBelowIntrinsic
from py_lets_be_rational.exceptions import BelowIntrinsicException,AboveMaximumException


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
                        format='%(asctime)s    %(levelname)s    %(module)s  %(funcName)s   %(message)s')


# @QtCore.pyqtSlot(object)
# def updatePOCW(main,data):
#
#
#
#     #data[0]=clientID  data[2]=Token
#     fltrarr1 = main.POCW.table[np.where((main.POCW.table[:main.POCW.lastSerialNo,0]==data[0]) & (main.POCW.table[:main.POCW.lastSerialNo,2]==data[2]))]
#
#
#
#
#     if (fltrarr1.size != 0):
#         #     isRecordExist=True
#         #
#         # if(isRecordExist):
#         #     # print('exist')
#
#
#         SerialNo = fltrarr1[0][12]
#         # print(SerialNo)
#         # rowNo = np.where(main.POCW.table[:, 12] == SerialNo)[0][0]
#         # print('rowNo',rowNo)
#
#         TOC = fltrarr1[0][30]
#
#         if TOC < data[26]:
#
#
#             editList = [8, 9, 15, 16, 19, 20, 30]
#             main.POCW.table[SerialNo, editList] = [data[8],data[9],data[15], data[16],data[19],data[20],data[26]]
#
#             for i in editList:
#                 ind = main.POCW.model.index(SerialNo, i)
#                 main.POCW.model.dataChanged.emit(ind, ind)
#
#
#
#
#     else:
#
#         # if (data[0] == 0 or data[0] == '0'):
#         #     print('kkkkkk')
#
#         main.POCW.table[main.POCW.lastSerialNo, :] = [data[0], 'NSEFO', data[2], data[3], data[4],  data[5],data[6],  data[7], data[8], data[9], data[10],data[11], main.POCW.lastSerialNo, data[13], data[14], data[15], data[16], data[17], data[18], data[19],data[20],data[21],data[22],data[23],data[24],data[25],0.0,0.0,0.0,0.0,data[26]]
#
#
#
#         main.POCW.lastSerialNo += 1
#
#         main.POCW.model.lastSerialNo += 1
#         main.POCW.model.insertRows()
#         main.POCW.model.rowCount()
#         ind = main.POCW.model.index(0, 0)
#         ind1 = main.POCW.model.index(0, 1)
#         main.POCW.model.dataChanged.emit(ind, ind1)
#
#         Ftoken = main.fo_contract[data[2] - 35000, 17]
#         main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
#         main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)
#
#         if main.tokenDict.get(data[2]):
#                 main.tokenDict[data[2]]['POCW'].append(main.POCW.model.lastSerialNo - 1)
#         else:
#             main.tokenDict[data[2]] = {}
#             main.tokenDict[data[2]]['POCW'] = [main.POCW.model.lastSerialNo - 1]
#             main.tokenDict[data[2]]['POTW'] = []
#
#
#
#
#
#     #data[0]=clientID  data[2]=Token


@QtCore.pyqtSlot(object)
def updateCWSWM(main, data):



    rowarray = np.where((main.CWSWM.table[:main.CWSWM.lastSerialNo, 0] == data[0]) & (
                main.CWSWM.table[:main.CWSWM.lastSerialNo, 1] == data[1]))[0]

    if (rowarray.size != 0):
        # print('exist')

        rowNo = rowarray[0]
        # print('rowNo',rowNo)
                #Expo,Span,totalMrg,premMRG,NetPrem
        editList = [2, 3, 4,8,9]
        main.CWSWM.table[rowNo, editList] = [data[2], data[3], data[4],data[8],data[9]]

        for i in editList:
            ind = main.CWSWM.model.index(rowNo, i)
            main.CWSWM.model.dataChanged.emit(ind, ind)



    else:

        main.CWSWM.table[main.CWSWM.lastSerialNo,[0,1,2,3,4,5,6,7,8,9]] = [data[0],data[1],data[2], data[3], data[4],data[5]
                                                                             ,data[6],data[7],data[8],data[9]]



        main.CWSWM.lastSerialNo += 1
        main.CWSWM.model.lastSerialNo += 1
        main.CWSWM.model.insertRows()
        main.CWSWM.model.rowCount()
        ind = main.CWSWM.model.index(0, 0)
        ind1 = main.CWSWM.model.index(0, 1)
        main.CWSWM.model.dataChanged.emit(ind, ind1)

        if main.cwswmDict.get(data[0]):
            main.cwswmDict[data[0]][data[1]] = main.CWSWM.lastSerialNo - 1
        else:
            main.cwswmDict[data[0]]={}
            main.cwswmDict[data[0]][data[1]] = main.CWSWM.lastSerialNo - 1

@QtCore.pyqtSlot(object)
def updateCWM(main, data):


    # rowarray = np.where(main.CWM.table[:main.CWM.lastSerialNo, 0] == data[0])[0]
    # print(fltrarr)

    # if (fltrarr.size != 0):
    #         isRecordExist = True
    rowNo=main.cwmDict.get(data[0])

    # if (rowarray.size != 0):
    if (rowNo != None):
        # print('exist')

        # rowNo = np.where(main.CWM.table[:, 0] == data[0])[0][0]
        # rowNo = rowarray[0]
        Data = main.CWM.table[rowNo, :]
        CashMRG = Data[23]

        NetMRG = data[9] + CashMRG


        # Expo,Span,totalMrg,DayPREM,premMRG,NETMRG,NetPRem,PeakMrg
        editList = [1, 2, 3, 7,8, 9,11,12]
        main.CWM.table[rowNo, editList] = [data[1], data[2], data[3], data[7], data[8], NetMRG,data[11],data[12]]

        for i in editList:
            ind = main.CWM.model.index(rowNo, i)
            main.CWM.model.dataChanged.emit(ind, ind)

    else:

        # fltr = main.CMCWM.table[np.where(main.CMCWM.table[:main.CMCWM.lastSerialNo, 0] == data[0])]
        # if fltr.size != 0:
        row=main.cmcwmDict.get(data[0])
        if row!=None:
            fltr=main.CMCWM.table[row,:]
            CashMRG = fltr[1]
            data[9] = data[9] + CashMRG
        else:
            CashMRG = 0.0

        main.CWM.table[main.CWM.lastSerialNo,[0,1,2,3,7,8,9,10,11,12,13,14,23]] = [data[0],data[1], data[2], data[3], data[7],
                                                       data[8], data[9], data[10],data[11],data[12],data[13],data[14],CashMRG]

        main.CWM.lastSerialNo += 1
        main.CWM.model.lastSerialNo += 1
        main.CWM.model.insertRows()
        main.CWM.model.rowCount()
        ind = main.CWM.model.index(0, 0)
        ind1 = main.CWM.model.index(0, 1)
        main.CWM.model.dataChanged.emit(ind, ind1)

        main.cwmDict[data[0]] = main.CWM.lastSerialNo - 1



def loadTerminalMaster(main,data):
    main.TerminalM.table[main.TerminalM.model.lastSerialNo] = data

    main.TerminalM.model.lastSerialNo += 1
    main.TerminalM.lastSerialNo += 1
    main.TerminalM.model.rowCount()
    main.TerminalM.model.insertRows()


    ind = main.TerminalM.model.index(0, 0)
    ind1 = main.TerminalM.model.index(0, 1)
    main.TerminalM.model.dataChanged.emit(ind, ind1)


def updateDepositPOTW(main,data):
    if data:
        for i in data:

            Uid=i
            # editable=d[0]
            # print('type',type)




            deposit=data[i]

            if i in main.TWM.table[:main.TWM.lastSerialNo,0]:

                # newBranch=main.CM.table[np.where(main.CM.table[:main.CM.model.lastSerialNo, 0] == i)][0][2]
                # fltrarr = main.TWM.table[np.where(main.TWM.table[:main.TWM.lastSerialNo, 0] == i)]
                # print('fltarr',fltrarr)

                # main.TWM.table[np.where(main.TWM.table[:main.TWM.lastSerialNo, 0] == i),16]=Deposit

                rowNo= np.where(main.TWM.table[:main.TWM.lastSerialNo, 0] == i)[0][0]
                Data = main.TWM.table[rowNo, :]


                NetPrem=Data[15]
                FnoMTM=Data[4]
                Ans = FnoMTM - NetPrem

                if Ans < 0:


                    if deposit > 0:
                        RiskPer = abs(Ans) / deposit
                    else:
                        RiskPer = 0.0
                else:
                    RiskPer=0.0

                editList = [16,20]
                main.TWM.table[rowNo, editList] = [ deposit,RiskPer]

                ind = main.TWM.model.index(0, 0)
                ind1 = main.TWM.model.index(0, 1)
                main.TWM.model.dataChanged.emit(ind, ind1)


def updateLimitPOTW(main, data):
    if data:
        for i in data:

            Uid = i
            # editable=d[0]
            # print('type',type)

            LIMIT = data[i]

            if i in main.TWM.table[:main.TWM.lastSerialNo, 0]:

                # newBranch=main.CM.table[np.where(main.CM.table[:main.CM.model.lastSerialNo, 0] == i)][0][2]
                # fltrarr = main.TWM.table[np.where(main.TWM.table[:main.TWM.lastSerialNo, 0] == i)]
                # print('fltarr',fltrarr)

                # main.TWM.table[np.where(main.TWM.table[:main.TWM.lastSerialNo, 0] == i),16]=Deposit

                rowNo = np.where(main.TWM.table[:main.TWM.lastSerialNo, 0] == i)[0][0]
                Data = main.TWM.table[rowNo, :]

                NetMRG = Data[13]


                if (NetMRG > LIMIT):
                    try:
                        AccessMRGuti = NetMRG / LIMIT * 100.0
                    except:
                        AccessMRGuti = 0.0
                else:
                    AccessMRGuti = 0.0

                editList = [17, 21]
                main.TWM.table[rowNo, editList] = [LIMIT, AccessMRGuti]

                ind = main.TWM.model.index(0, 0)
                ind1 = main.TWM.model.index(0, 1)
                main.TWM.model.dataChanged.emit(ind, ind1)



def loadDeposit(main):
    loc = os.getcwd().split('Application')[0]
    # path = os.path.join(loc,'Application','DB','terminal_masterNew.json')
    # # f = open(r'..\Application\DB\terminal_master.json')
    # f = open(path)
    # main.Tmaster = json.load(f)

    path1 = os.path.join(loc,'Uploads', 'Deposit.csv')

    df = pd.read_csv(path1)
    main.DepositDict = dict(df.values)
    main.Depositarray = df.to_numpy()
    # main.Depositarray[:, 0] = main.Depositarray[:, 0].astype('str')


    for i in main.Depositarray:
        # print(i)
        main.Deposit.table[main.Deposit.model.lastSerialNo] = i

        main.Deposit.model.lastSerialNo += 1
        main.Deposit.lastSerialNo += 1
        main.Deposit.model.rowCount()
        main.Deposit.model.insertRows()

    ind = main.Deposit.model.index(0, 0)
    ind1 = main.Deposit.model.index(0, 1)
    main.Deposit.model.dataChanged.emit(ind, ind1)

    # main.Deposit.table[:, 0] = main.Deposit.table[:, 0].astype('str')
    # main.isTmasterloaded = True
def loadLimit(main):
    loc = os.getcwd().split('Application')[0]
    # path = os.path.join(loc,'Application','DB','terminal_masterNew.json')
    # # f = open(r'..\Application\DB\terminal_master.json')
    # f = open(path)
    # main.Tmaster = json.load(f)

    path1 = os.path.join(loc,'Uploads', 'Limit.csv')

    df = pd.read_csv(path1)
    main.LimitDict=dict(df.values)
    main.Limitarray=df.to_numpy()
    # print('typw',type(main.Limitarray[0,0]))
    # main.Limitarray[:, 0] = main.Limitarray[:, 0].astype('str')


    for i in main.Limitarray:
        # print(i)
        main.Limit.table[main.Limit.model.lastSerialNo] = i

        main.Limit.model.lastSerialNo += 1
        main.Limit.lastSerialNo += 1
        main.Limit.model.rowCount()
        main.Limit.model.insertRows()

    ind = main.Limit.model.index(0, 0)
    ind1 = main.Limit.model.index(0, 1)
    main.Limit.model.dataChanged.emit(ind, ind1)

    # main.Limit.table[:, 0] = main.Limit.table[:, 0].astype('str')
    # main.isTmasterloaded = True

# @pyqtSlot(list)
# def updatePOTW(main,data):
#
#
#     # print(data,data[0],data[2])
#     try:
#
#         fltrarr1 = main.POTW.table[np.where((main.POTW.table[:main.POTW.lastSerialNo, 0] == data[0]) & (
#                 main.POTW.table[:main.POTW.lastSerialNo, 2] == data[2]))]
#
#         if (fltrarr1.size != 0):
#             # print('update')
#             #     isRecordExist=True
#             #
#             # if(isRecordExist):
#             #     # print('exist')
#
#             SerialNo = fltrarr1[0][12]
#
#             TOC = fltrarr1[0][33]
#
#             if TOC < data[29]:
#
#
#
#                 editList = [8, 9, 15, 16, 20, 23,33]
#                 main.POTW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],data[29]]
#
#                 for i in editList:
#                     ind = main.POTW.model.index(SerialNo, i)
#                     main.POTW.model.dataChanged.emit(ind, ind)
#
#
#
#         else:
#
#             main.POTW.table[main.POTW.lastSerialNo] = [data[0],
#                                                              data[1], data[2], data[3], data[4], data[5],
#                                                             data[6], data[7], data[8], data[9],data[10],
#                                                              data[11], main.POTW.lastSerialNo,data[13], data[14],data[15],
#                                                              data[16], data[17], data[18],data[19], data[20],
#                                                        data[21],data[22], data[23],data[24],data[25],
#                                                              data[26],data[27],data[28],0.0,0.0,
#                                                              0.0,0.0,data[29]]
#
#             # main.POTW.table[main.POTW.lastSerialNo, :] = data
#
#             main.POTW.lastSerialNo += 1
#             main.POTW.lastSerialNo += 1
#             main.POTW.model.insertRows()
#             main.POTW.model.rowCount()
#             ind = main.POTW.model.index(0, 0)
#             ind1 = main.POTW.model.index(0, 1)
#             main.POTW.model.dataChanged.emit(ind, ind1)
#
#             Ftoken = main.fo_contract[data[2] - 35000, 17]
#             main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
#             main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)
#
#             if main.tokenDict.get(data[2]):
#                 main.tokenDict[data[2]]['POTW'].append(main.POTW.lastSerialNo-1)
#             else:
#                 main.tokenDict[data[2]]={}
#                 main.tokenDict[data[2]]['POTW'] = [main.POTW.lastSerialNo-1]
#                 main.tokenDict[data[2]]['POCW'] = []
#
#
#     except:
#         print(traceback.print_exc(), len(data))
#
#     # print('ppp', main.POTW.lastSerialNo)
#
#
#
#     # main.isPOTWupdated = True
#
#     # if UserID not in main.POTW.clientList:
#     #     main.POTW.clientList.append(UserID)


# @pyqtSlot(list)
# def updateFilterPOTW(main,data):
#
#
#     # print(data,data[0],data[2])
#     try:
#
#         if data[0]==main.POTW.FilterTable[0,0]:
#
#
#
#             fltrarr1=np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo,2]==data[2])[0]
#
#
#             # fltrarr1 = np.where((main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 0] == data[0]) & (
#             #         main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 2] == data[2]))[0]
#
#             if (fltrarr1.size != 0):
#                 # print('update')
#                 #     isRecordExist=True
#                 #
#                 # if(isRecordExist):
#                 #     # print('exist')
#
#
#                 # SerialNo = fltrarr1[0][12]
#                 SerialNo = fltrarr1[0]
#
#                 fltrarr1 = main.POTW.FilterTable[SerialNo, :]
#                 rowNo=fltrarr1[12]
#
#
#                 TOC = fltrarr1[33]
#
#                 if TOC < data[29]:
#
#
#
#                     editList = [8, 9, 15, 16, 20, 23,33]
#                     main.POTW.FilterTable[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],data[29]]
#                     main.POTW.table[rowNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],data[29]]
#
#                     for i in editList:
#                         ind = main.POTW.model.index(SerialNo, i)
#                         main.POTW.model.dataChanged.emit(ind, ind)
#
#
#
#             else:
#
#                 main.POTW.table[main.POTW.lastSerialNo] = [data[0],
#                                                              data[1], data[2], data[3], data[4], data[5],
#                                                             data[6], data[7], data[8], data[9],data[10],
#                                                              data[11], main.POTW.lastSerialNo,data[13], data[14],data[15],
#                                                              data[16], data[17], data[18],data[19], data[20],
#                                                        data[21],data[22], data[23],data[24],data[25],
#                                                              data[26],data[27],data[28],0.0,0.0,
#                                                              0.0,0.0,data[29]]
#
#                 # main.POTW.FilterTable[main.POTW.model.flastSerialNo, :] = data
#
#                 main.POTW.FilterTable[main.POTW.model.flastSerialNo] = [data[0],
#                                                            data[1], data[2], data[3], data[4], data[5],
#                                                            data[6], data[7], data[8], data[9], data[10],
#                                                            data[11], main.POTW.lastSerialNo, data[13], data[14],
#                                                            data[15],
#                                                            data[16], data[17], data[18], data[19], data[20],
#                                                            data[21], data[22], data[23], data[24], data[25],
#                                                            data[26], data[27], data[28], 0.0, 0.0,
#                                                            0.0, 0.0, data[29]]
#                 main.POTW.lastSerialNo += 1
#                 main.POTW.model.flastSerialNo += 1
#                 main.POTW.model.insertRows()
#                 main.POTW.model.rowCount()
#                 ind = main.POTW.model.index(0, 0)
#                 ind1 = main.POTW.model.index(0, 1)
#                 main.POTW.model.dataChanged.emit(ind, ind1)
#
#                 Ftoken = main.fo_contract[data[2] - 35000, 17]
#                 main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
#                 main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)
#
#                 if main.tokenDict.get(data[2]):
#                     main.tokenDict[data[2]]['POTW'].append(main.POTW.model.flastSerialNo - 1)
#                 else:
#                     main.tokenDict[data[2]] = {}
#                     main.tokenDict[data[2]]['POTW'] = [main.POTW.model.flastSerialNo - 1]
#                     main.tokenDict[data[2]]['POCW'] = []
#
#                 if main.maintokenDict.get(data[2]):
#                     main.maintokenDict[data[2]]['POTW'].append(main.POTW.lastSerialNo - 1)
#                 else:
#                     main.maintokenDict[data[2]] = {}
#                     main.maintokenDict[data[2]]['POTW'] = [main.POTW.lastSerialNo - 1]
#                     main.maintokenDict[data[2]]['POCW'] = []
#
#
#         else:
#             fltrarr1 = main.POTW.table[np.where((main.POTW.table[:main.POTW.lastSerialNo, 0] == data[0]) & (
#                     main.POTW.table[:main.POTW.lastSerialNo, 2] == data[2]))]
#
#             if (fltrarr1.size != 0):
#                 # print('update')
#                 #     isRecordExist=True
#                 #
#                 # if(isRecordExist):
#                 #     # print('exist')
#
#                 SerialNo = fltrarr1[0][12]
#                 # SerialNo = fltrarr1[0]
#
#                 # fltrarr1 = main.POTW.FilterTable[SerialNo, :]
#                 # rowNo = fltrarr1[12]
#
#                 TOC = fltrarr1[0][33]
#
#                 if TOC < data[29]:
#                     editList = [8, 9, 15, 16, 20, 23, 33]
#
#                     main.POTW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],
#                                                         data[29]]
#             else:
#                 if main.POTW.lastSerialNo ==0:
#                     main.POTW.FilterTable[main.POTW.model.flastSerialNo] = [data[0],
#                                                                            data[1], data[2], data[3], data[4], data[5],
#                                                                            data[6], data[7], data[8], data[9], data[10],
#                                                                            data[11], main.POTW.lastSerialNo,
#                                                                            data[13], data[14],
#                                                                            data[15],
#                                                                            data[16], data[17], data[18], data[19],
#                                                                            data[20],
#                                                                            data[21], data[22], data[23], data[24],
#                                                                            data[25],
#                                                                            data[26], data[27], data[28], 0.0, 0.0,
#                                                                            0.0, 0.0, data[29]]
#                     main.POTW.model.flastSerialNo += 1
#                     main.POTW.model.insertRows()
#                     main.POTW.model.rowCount()
#                     ind = main.POTW.model.index(0, 0)
#                     ind1 = main.POTW.model.index(0, 1)
#                     main.POTW.model.dataChanged.emit(ind, ind1)
#
#                     if main.tokenDict.get(data[2]):
#                         main.tokenDict[data[2]]['POTW'].append(main.POTW.model.flastSerialNo - 1)
#                     else:
#                         main.tokenDict[data[2]] = {}
#                         main.tokenDict[data[2]]['POTW'] = [main.POTW.model.flastSerialNo - 1]
#                         main.tokenDict[data[2]]['POCW'] = []
#
#
#
#                 main.POTW.table[main.POTW.lastSerialNo] = [data[0],
#                                                            data[1], data[2], data[3], data[4], data[5],
#                                                            data[6], data[7], data[8], data[9], data[10],
#                                                            data[11], main.POTW.lastSerialNo, data[13], data[14],
#                                                            data[15],
#                                                            data[16], data[17], data[18], data[19], data[20],
#                                                            data[21], data[22], data[23], data[24], data[25],
#                                                            data[26], data[27], data[28], 0.0, 0.0,
#                                                            0.0, 0.0, data[29]]
#                 main.POTW.lastSerialNo+=1
#
#
#                 Ftoken = main.fo_contract[data[2] - 35000, 17]
#                 main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
#                 main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)
#
#                 if main.maintokenDict.get(data[2]):
#                     main.maintokenDict[data[2]]['POTW'].append(main.POTW.lastSerialNo - 1)
#                 else:
#                     main.maintokenDict[data[2]] = {}
#                     main.maintokenDict[data[2]]['POTW'] = [main.POTW.lastSerialNo - 1]
#                     main.maintokenDict[data[2]]['POCW'] = []
#
#
#     except:
#         print(traceback.print_exc(), rowNo,fltrarr1[12])
#
#     # print('ppp', main.POTW.lastSerialNo)
#
#
#
#     # main.isPOTWupdated = True
#
#     # if UserID not in main.POTW.clientList:
#     #     main.POTW.clientList.append(UserID)

@pyqtSlot(list)
def updateFilterPOTW(main,data):


    # print(data,data[0],data[2])
    try:


        if data[0]==main.POTW.FilterTable[0,0]:



            fltrarr1=np.where((main.POTW.FilterTable[:main.POTW.model.flastSerialNo,34]==data[30]) &(main.POTW.FilterTable[:main.POTW.model.flastSerialNo,0]==data[0]) & (main.POTW.FilterTable[:main.POTW.model.flastSerialNo,2]==data[2]))[0]


            # fltrarr1 = np.where((main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 0] == data[0]) & (
            #         main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 2] == data[2]))[0]

            if (fltrarr1.size != 0):
                # print('update')
                #     isRecordExist=True
                #
                # if(isRecordExist):
                #     # print('exist')


                # SerialNo = fltrarr1[0][12]
                SerialNo = fltrarr1[0]

                fltrarr1 = main.POTW.FilterTable[SerialNo, :]
                rowNo=fltrarr1[12]


                TOC = fltrarr1[33]

                if data[29]>=0:



                    editList = [8, 9, 15, 16, 20, 23,33]
                    main.POTW.FilterTable[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],data[29]]
                    main.POTW.table[rowNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],data[29]]

                    for i in editList:
                        ind = main.POTW.model.index(SerialNo, i)
                        main.POTW.model.dataChanged.emit(ind, ind)





            else:

                main.POTW.table[main.POTW.lastSerialNo] = [data[0],
                                                             data[1], data[2], data[3], data[4], data[5],
                                                            data[6], data[7], data[8], data[9],data[10],
                                                             data[11], main.POTW.lastSerialNo,data[13], data[14],data[15],
                                                             data[16], data[17], data[18],data[19], data[20],
                                                       data[21],data[22], data[23],data[24],data[25],
                                                             data[26],data[27],data[28],0.0,0.0,
                                                             0.0,0.0,data[29],data[30]]

                # main.POTW.FilterTable[main.POTW.model.flastSerialNo, :] = data

                main.POTW.FilterTable[main.POTW.model.flastSerialNo] = [data[0],
                                                           data[1], data[2], data[3], data[4], data[5],
                                                           data[6], data[7], data[8], data[9], data[10],
                                                           data[11], main.POTW.lastSerialNo, data[13], data[14],
                                                           data[15],
                                                           data[16], data[17], data[18], data[19], data[20],
                                                           data[21], data[22], data[23], data[24], data[25],
                                                           data[26], data[27], data[28], 0.0, 0.0,
                                                           0.0, 0.0, data[29],data[30]]
                main.POTW.lastSerialNo += 1
                main.POTW.model.flastSerialNo += 1
                main.POTW.model.insertRows()
                main.POTW.model.rowCount()
                ind = main.POTW.model.index(0, 0)
                ind1 = main.POTW.model.index(0, 1)
                main.POTW.model.dataChanged.emit(ind, ind1)

                Ftoken = main.fo_contract[data[2] - 35000, 17]
                main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
                main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)

                if main.tokenDict.get(data[2]):
                    main.tokenDict[data[2]]['POTW'].append(main.POTW.model.flastSerialNo - 1)
                else:
                    main.tokenDict[data[2]] = {}
                    main.tokenDict[data[2]]['POTW'] = [main.POTW.model.flastSerialNo - 1]
                    main.tokenDict[data[2]]['POCW'] = []

                if main.maintokenDict.get(data[2]):
                    main.maintokenDict[data[2]]['POTW'].append(main.POTW.lastSerialNo - 1)
                else:
                    main.maintokenDict[data[2]] = {}
                    main.maintokenDict[data[2]]['POTW'] = [main.POTW.lastSerialNo - 1]
                    main.maintokenDict[data[2]]['POCW'] = []


        else:
            fltrarr1 = main.POTW.table[np.where((main.POTW.table[:main.POTW.lastSerialNo, 34] == data[30]) & (main.POTW.table[:main.POTW.lastSerialNo, 0] == data[0]) & (
                    main.POTW.table[:main.POTW.lastSerialNo, 2] == data[2]))]

            if (fltrarr1.size != 0):
                # print('update')
                #     isRecordExist=True
                #
                # if(isRecordExist):
                #     # print('exist')

                SerialNo = fltrarr1[0][12]
                # SerialNo = fltrarr1[0]

                # fltrarr1 = main.POTW.FilterTable[SerialNo, :]
                # rowNo = fltrarr1[12]

                TOC = fltrarr1[0][33]

                if data[29]>=0:
                    editList = [8, 9, 15, 16, 20, 23, 33]

                    main.POTW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],
                                                        data[29]]

            else:
                if main.POTW.lastSerialNo ==0:
                    main.POTW.FilterTable[main.POTW.model.flastSerialNo] = [data[0],
                                                                           data[1], data[2], data[3], data[4], data[5],
                                                                           data[6], data[7], data[8], data[9], data[10],
                                                                           data[11], main.POTW.lastSerialNo,
                                                                           data[13], data[14],
                                                                           data[15],
                                                                           data[16], data[17], data[18], data[19],
                                                                           data[20],
                                                                           data[21], data[22], data[23], data[24],
                                                                           data[25],
                                                                           data[26], data[27], data[28], 0.0, 0.0,
                                                                           0.0, 0.0, data[29],data[30]]
                    main.POTW.model.flastSerialNo += 1
                    main.POTW.model.insertRows()
                    main.POTW.model.rowCount()
                    ind = main.POTW.model.index(0, 0)
                    ind1 = main.POTW.model.index(0, 1)
                    main.POTW.model.dataChanged.emit(ind, ind1)

                    if main.tokenDict.get(data[2]):
                        main.tokenDict[data[2]]['POTW'].append(main.POTW.model.flastSerialNo - 1)
                    else:
                        main.tokenDict[data[2]] = {}
                        main.tokenDict[data[2]]['POTW'] = [main.POTW.model.flastSerialNo - 1]
                        main.tokenDict[data[2]]['POCW'] = []



                main.POTW.table[main.POTW.lastSerialNo] = [data[0],
                                                           data[1], data[2], data[3], data[4], data[5],
                                                           data[6], data[7], data[8], data[9], data[10],
                                                           data[11], main.POTW.lastSerialNo, data[13], data[14],
                                                           data[15],
                                                           data[16], data[17], data[18], data[19], data[20],
                                                           data[21], data[22], data[23], data[24], data[25],
                                                           data[26], data[27], data[28], 0.0, 0.0,
                                                           0.0, 0.0, data[29],data[30]]
                main.POTW.lastSerialNo+=1


                Ftoken = main.fo_contract[data[2] - 35000, 17]
                main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
                main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)

                if main.maintokenDict.get(data[2]):
                    main.maintokenDict[data[2]]['POTW'].append(main.POTW.lastSerialNo - 1)
                else:
                    main.maintokenDict[data[2]] = {}
                    main.maintokenDict[data[2]]['POTW'] = [main.POTW.lastSerialNo - 1]
                    main.maintokenDict[data[2]]['POCW'] = []


    except:
        print(traceback.print_exc(), rowNo,fltrarr1[12])

    # print('ppp', main.POTW.lastSerialNo)



    # main.isPOTWupdated = True

    # if UserID not in main.POTW.clientList:
    #     main.POTW.clientList.append(UserID)

@QtCore.pyqtSlot(object)
def updatePOCW(main,data):


    if data[0] == main.POCW.FilterTable[0, 0]:
        fltrarr1 = np.where(main.POCW.FilterTable[:main.POCW.model.flastSerialNo, 2] == data[2])[0]

        if (fltrarr1.size != 0):
            #     isRecordExist=True
            #
            # if(isRecordExist):
            #     # print('exist')

            # SerialNo = fltrarr1[0][12]
            SerialNo = fltrarr1[0]

            fltrarr1 = main.POCW.FilterTable[SerialNo, :]
            rowNo = fltrarr1[12]

            TOC = fltrarr1[30]

            if TOC < data[26]:

                editList = [8, 9, 15, 16, 19, 20, 30]
                main.POCW.FilterTable[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[19], data[20],
                                                       data[26]]
                main.POCW.table[rowNo, editList] = [data[8], data[9], data[15], data[16], data[19], data[20],
                                                       data[26]]

                for i in editList:
                    ind = main.POCW.model.index(SerialNo, i)
                    main.POCW.model.dataChanged.emit(ind, ind)




        else:

            main.POCW.table[main.POCW.lastSerialNo, :] = [data[0], 'NSEFO', data[2], data[3], data[4], data[5], data[6],
                                                          data[7], data[8], data[9], data[10], data[11],
                                                          main.POCW.lastSerialNo, data[13], data[14], data[15],
                                                          data[16], data[17], data[18], data[19], data[20], data[21],
                                                          data[22], data[23], data[24], data[25], 0.0, 0.0, 0.0, 0.0,
                                                          data[26]]
            main.POCW.FilterTable[main.POCW.model.flastSerialNo, :] = [data[0], 'NSEFO', data[2], data[3], data[4], data[5], data[6],
                                                          data[7], data[8], data[9], data[10], data[11],
                                                          main.POCW.lastSerialNo, data[13], data[14], data[15],
                                                          data[16], data[17], data[18], data[19], data[20], data[21],
                                                          data[22], data[23], data[24], data[25], 0.0, 0.0, 0.0, 0.0,
                                                          data[26]]

            main.POCW.lastSerialNo += 1

            main.POCW.model.flastSerialNo += 1
            main.POCW.model.insertRows()
            main.POCW.model.rowCount()
            ind = main.POCW.model.index(0, 0)
            ind1 = main.POCW.model.index(0, 1)
            main.POCW.model.dataChanged.emit(ind, ind1)

            Ftoken = main.fo_contract[data[2] - 35000, 17]
            main.Reciever.subscribedlist('POcW', 'NSEFO', data[2])
            main.Reciever.subscribedlist('POCW', 'NSEFO', Ftoken)

            if main.maintokenDict.get(data[2]):
                main.maintokenDict[data[2]]['POCW'].append(main.POCW.lastSerialNo - 1)
            else:
                main.maintokenDict[data[2]] = {}
                main.maintokenDict[data[2]]['POCW'] = [main.POCW.lastSerialNo - 1]
                main.maintokenDict[data[2]]['POTW'] = []

            if main.tokenDict.get(data[2]):
                main.tokenDict[data[2]]['POCW'].append(main.POCW.model.flastSerialNo - 1)
            else:
                main.tokenDict[data[2]] = {}
                main.tokenDict[data[2]]['POCW'] = [main.POCW.model.flastSerialNo - 1]
                main.tokenDict[data[2]]['POTW'] = []


    else:
        fltrarr1 = main.POCW.table[np.where((main.POCW.table[:main.POCW.lastSerialNo, 0] == data[0]) & (
                    main.POCW.table[:main.POCW.lastSerialNo, 2] == data[2]))]

        if (fltrarr1.size != 0):
            #     isRecordExist=True
            #
            # if(isRecordExist):
            #     # print('exist')

            SerialNo = fltrarr1[0][12]
            # print(SerialNo)
            # rowNo = np.where(main.POCW.table[:, 12] == SerialNo)[0][0]
            # print('rowNo',rowNo)

            TOC = fltrarr1[0][30]

            if TOC < data[26]:

                editList = [8, 9, 15, 16, 19, 20, 30]
                main.POCW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[19], data[20],
                                                       data[26]]






        else:
            if main.POCW.lastSerialNo == 0:
                main.POCW.FilterTable[main.POCW.model.flastSerialNo] = [data[0], 'NSEFO', data[2], data[3], data[4], data[5], data[6],
                                                          data[7], data[8], data[9], data[10], data[11],
                                                          main.POCW.lastSerialNo, data[13], data[14], data[15],
                                                          data[16], data[17], data[18], data[19], data[20], data[21],
                                                          data[22], data[23], data[24], data[25], 0.0, 0.0, 0.0, 0.0,
                                                          data[26]]
                main.POCW.model.flastSerialNo += 1
                main.POCW.model.insertRows()
                main.POCW.model.rowCount()
                ind = main.POCW.model.index(0, 0)
                ind1 = main.POCW.model.index(0, 1)
                main.POCW.model.dataChanged.emit(ind, ind1)

                if main.tokenDict.get(data[2]):
                    main.tokenDict[data[2]]['POCW'].append(main.POCW.model.flastSerialNo - 1)
                else:
                    main.tokenDict[data[2]] = {}
                    main.tokenDict[data[2]]['POCW'] = [main.POCW.model.flastSerialNo - 1]
                    main.tokenDict[data[2]]['POTW'] = []



            main.POCW.table[main.POCW.lastSerialNo, :] = [data[0], 'NSEFO', data[2], data[3], data[4], data[5], data[6],
                                                          data[7], data[8], data[9], data[10], data[11],
                                                          main.POCW.lastSerialNo, data[13], data[14], data[15],
                                                          data[16], data[17], data[18], data[19], data[20], data[21],
                                                          data[22], data[23], data[24], data[25], 0.0, 0.0, 0.0, 0.0,
                                                          data[26]]

            main.POCW.lastSerialNo += 1



            Ftoken = main.fo_contract[data[2] - 35000, 17]
            main.Reciever.subscribedlist('POCW', 'NSEFO', data[2])
            main.Reciever.subscribedlist('POCW', 'NSEFO', Ftoken)

            if main.maintokenDict.get(data[2]):
                main.maintokenDict[data[2]]['POCW'].append(main.POCW.lastSerialNo - 1)
            else:
                main.maintokenDict[data[2]] = {}
                main.maintokenDict[data[2]]['POCW'] = [main.POCW.lastSerialNo - 1]
                main.maintokenDict[data[2]]['POTW'] = []





    #data[0]=clientID  data[2]=Token

# def updateFilterPOTWopenPosition(main,data):
#     try:
#
#         fltrarr1 = np.where((main.POTW.FilterTable[:main.POTW.lastSerialNo, 0] == data[0]) & (
#                 main.POTW.FilterTable[:main.POTW.lastSerialNo, 2] == data[2]))[0]
#
#         if (fltrarr1.size != 0):
#             # print('update')
#             #     isRecordExist=True
#             #
#             # if(isRecordExist):
#             #     # print('exist')
#
#             # SerialNo = fltrarr1[0][12]
#             SerialNo = fltrarr1[0]
#
#             fltrarr1 = main.POTW.FilterTable[SerialNo, :]
#             rowNo = fltrarr1[12]
#
#             TOC = fltrarr1[33]
#
#             if TOC < data[29]:
#
#                 editList = [8, 9, 15, 16, 20, 23, 33]
#                 main.POTW.FilterTable[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],
#                                                              data[29]]
#                 main.POTW.table[rowNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23], data[29]]
#
#                 for i in editList:
#                     ind = main.POTW.model.index(SerialNo, i)
#                     main.POTW.model.dataChanged.emit(ind, ind)
#
#
#
#         else:
#
#             main.POTW.table[main.POTW.lastSerialNo] = [data[0],
#                                                        data[1], data[2], data[3], data[4], data[5],
#                                                        data[6], data[7], data[8], data[9], data[10],
#                                                        data[11], main.POTW.lastSerialNo, data[13], data[14],
#                                                        data[15],
#                                                        data[16], data[17], data[18], data[19], data[20],
#                                                        data[21], data[22], data[23], data[24], data[25],
#                                                        data[26], data[27], data[28], 0.0, 0.0,
#                                                        0.0, 0.0, data[29]]
#
#             # main.POTW.FilterTable[main.POTW.lastSerialNo, :] = data
#
#             if data[0] == main.POTW.FilterTable[0, 0]:
#                 # print('dddd')
#                 main.POTW.FilterTable[main.POTW.lastSerialNo] = [data[0],
#                                                                        data[1], data[2], data[3], data[4], data[5],
#                                                                        data[6], data[7], data[8], data[9], data[10],
#                                                                        data[11], main.POTW.lastSerialNo, data[13],
#                                                                        data[14],
#                                                                        data[15],
#                                                                        data[16], data[17], data[18], data[19], data[20],
#                                                                        data[21], data[22], data[23], data[24], data[25],
#                                                                        data[26], data[27], data[28], 0.0, 0.0,
#                                                                        0.0, 0.0, data[29]]
#                 # main.POTW.lastSerialNo += 1
#                 main.POTW.lastSerialNo += 1
#                 main.POTW.model.insertRows()
#                 main.POTW.model.rowCount()
#                 ind = main.POTW.model.index(0, 0)
#                 ind1 = main.POTW.model.index(0, 1)
#                 main.POTW.model.dataChanged.emit(ind, ind1)
#
#             Ftoken = main.fo_contract[data[2] - 35000, 17]
#             main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
#             main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)
#
#             if main.tokenDict.get(data[2]):
#                 main.tokenDict[data[2]]['POTW'].append(main.POTW.lastSerialNo - 1)
#             else:
#                 main.tokenDict[data[2]] = {}
#                 main.tokenDict[data[2]]['POTW'] = [main.POTW.lastSerialNo - 1]
#                 main.tokenDict[data[2]]['POCW'] = []
#
#
#     except:
#         print(traceback.print_exc(), len(data))
#
#     # print('ppp', main.POTW.lastSerialNo)
#
#     # main.POTW.table[:data.shape[0], :] = data
#     # # main.POTW.model._data[:data.shape[0], :] = data[:, 1:]
#     #
#     # main.POTW.lastSerialNo += data.shape[0]
#     #
#     # main.POTW.lastSerialNo += data.shape[0]
#     #
#     # main.POTW.model.insertMultiRows(rows=data.shape[0])
#     #
#     # main.POTW.model.rowCount()
#     # ind = main.POTW.model.index(0, 0)
#     # ind1 = main.POTW.model.index(0, 1)
#     # main.POTW.model.dataChanged.emit(ind, ind1)
#     # # et=time.time()
#     # print('timettt',et-st)
#
#     # main.POTW.table[main.POTW.lastSerialNo, :] = [data['UserID'], data['Exchange'], data['Token'], , sym, exp,
#     #                                                     strike, opt, TQty, Tamt, 0,
#     #                                                     0, main.POTW.lastSerialNo, 0, 0, TQty, Tamt, 0.0, 0.0,
#     #                                                     0.0, netPrem, 0.0, 0.0, premMrg]
#     # main.POTW.table[main.POTW.lastSerialNo, :] = data
#
#     # main.POTW.lastSerialNo += 1
#     # main.POTW.lastSerialNo += 1
#     # main.POTW.model.insertRows()
#     # main.POTW.model.rowCount()
#     # ind = main.POTW.model.index(0, 0)
#     # ind1 = main.POTW.model.index(0, 1)
#     # main.POTW.model.dataChanged.emit(ind, ind1)
def updatePOTWopenPosition(main,data):
    try:
    # st=time.time()
    # print(data)

        fltrarr1 = main.POTW.table[np.where((main.POTW.table[:main.POTW.lastSerialNo, 0] == data[0]) & (
                main.POTW.table[:main.POTW.lastSerialNo, 2] == data[2]))]

        if (fltrarr1.size != 0):
            # print('update')
            #     isRecordExist=True
            #
            # if(isRecordExist):
            #     # print('exist')

            SerialNo = fltrarr1[0][12]

            TOC=fltrarr1[0][33]

            if TOC <data[29]:


                editList = [8, 9, 15, 16, 20, 23,33]
                main.POTW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],data[29]]

                for i in editList:
                    ind = main.POTW.model.index(SerialNo, i)
                    main.POTW.model.dataChanged.emit(ind, ind)



        else:

            main.POTW.table[main.POTW.lastSerialNo] = [data[0], data[1], data[2], data[3], data[4], data[5],
                                                   data[6], data[7], data[8], data[9],data[10],data[11], main.POTW.lastSerialNo,
                                                   data[13], data[14],
                                                   data[15], data[16], data[17], data[18],
                                                   data[19], data[20],data[21],data[22] ,data[23],data[24],data[25],data[26],data[27],data[28],0.0,0.0,0.0,0.0,data[29]]

            # main.POTW.table[main.POTW.lastSerialNo, :] = data

            main.POTW.lastSerialNo += 1
            main.POTW.lastSerialNo += 1
            main.POTW.model.insertRows()
            main.POTW.model.rowCount()
            ind = main.POTW.model.index(0, 0)
            ind1 = main.POTW.model.index(0, 1)
            main.POTW.model.dataChanged.emit(ind, ind1)

            Ftoken = main.fo_contract[data[2] - 35000, 17]
            main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
            main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)

            if main.tokenDict.get(data[2])!=None:
                main.tokenDict[data[2]]['POTW'].append(main.POTW.lastSerialNo-1)
            else:
                main.tokenDict[data[2]]={}
                main.tokenDict[data[2]]['POTW'] = [main.POTW.lastSerialNo-1]
                main.tokenDict[data[2]]['POCW'] = []
    except:

        print(traceback.print_exc(),main.fo_contract.size,data[2])

    # print('ppp', main.POTW.lastSerialNo)

    # main.POTW.table[:data.shape[0], :] = data
    # # main.POTW.model._data[:data.shape[0], :] = data[:, 1:]
    #
    # main.POTW.lastSerialNo += data.shape[0]
    #
    # main.POTW.lastSerialNo += data.shape[0]
    #
    # main.POTW.model.insertMultiRows(rows=data.shape[0])
    #
    # main.POTW.model.rowCount()
    # ind = main.POTW.model.index(0, 0)
    # ind1 = main.POTW.model.index(0, 1)
    # main.POTW.model.dataChanged.emit(ind, ind1)
    # # et=time.time()
    # print('timettt',et-st)

    # main.POTW.table[main.POTW.lastSerialNo, :] = [data['UserID'], data['Exchange'], data['Token'], , sym, exp,
    #                                                     strike, opt, TQty, Tamt, 0,
    #                                                     0, main.POTW.lastSerialNo, 0, 0, TQty, Tamt, 0.0, 0.0,
    #                                                     0.0, netPrem, 0.0, 0.0, premMrg]
    # main.POTW.table[main.POTW.lastSerialNo, :] = data

    # main.POTW.lastSerialNo += 1
    # main.POTW.lastSerialNo += 1
    # main.POTW.model.insertRows()
    # main.POTW.model.rowCount()
    # ind = main.POTW.model.index(0, 0)
    # ind1 = main.POTW.model.index(0, 1)
    # main.POTW.model.dataChanged.emit(ind, ind1)





@QtCore.pyqtSlot(list)
def updateTWSWM(main, data):
    # print('TWSWM', data)
    rowarray = np.where((main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 0] == data[0]) & (main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 1] == data[1]))[0]



    if (rowarray.size !=0):



        rowNo = rowarray[0]



        editList = [2,3,4,8]
        main.TWSWM.table[rowNo, editList] = [data[2], data[3],data[4],data[8]]

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

        if main.twswmDict.get(data[0]):
            main.twswmDict[data[0]][data[1]] = main.TWSWM.lastSerialNo - 1
        else:
            main.twswmDict[data[0]]={}
            main.twswmDict[data[0]][data[1]] = main.TWSWM.lastSerialNo - 1






@QtCore.pyqtSlot(object)
def updateTWM(main, data):
    # print('TWM', data)


    # rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == data[0])[0]
    # print(fltrarr)

    # if (fltrarr.size != 0):
    #         isRecordExist = True
    rowNo=main.twmDict.get(data[0])
    # if (rowarray.size != 0):
    if (rowNo!= None):

        # print('exist')


        # rowNo = np.where(main.TWM.table[:, 0] == data[0])[0][0]
        # rowNo=rowarray[0]

        Data=main.TWM.table[rowNo,:]
        LIMIT=Data[17]
        CashMRG=Data[25]

        NetMRG=data[13]+CashMRG

        if(data[13]>LIMIT):
            try:
                AccessMRGuti = data[13] / LIMIT * 100.0
            except:
                AccessMRGuti = 0.0
        else:
            AccessMRGuti = 0.0


        editList = [1, 2, 3, 9, 12, 13, 14, 15,21]
        # print(data[13])
        main.TWM.table[rowNo, editList] = [data[1], data[2], data[3], data[9], data[12],
                                           NetMRG, data[14], data[15],AccessMRGuti]
        # else:
        #
        #     editList = [1, 2,3,9,12,13,14,15]
        #     main.TWM.table[rowNo, editList] = [data[1], data[2],data[3],data[9],data[12],NetMRG,data[14],data[15]]

        for i in editList:
            ind = main.TWM.model.index(rowNo, i)
            main.TWM.model.dataChanged.emit(ind, ind)

    else:
        # main.Deposit.table[main.Deposit.lastSerialNo]=[data[0],100000]
        # main.Deposit.model.lastSerialNo += 1
        # main.Deposit.lastSerialNo += 1
        # main.Deposit.model.rowCount()
        # main.Deposit.model.insertRows()
        # ind = main.Deposit.model.index(0, 0)
        # ind1 = main.Deposit.model.index(0, 1)
        # main.Deposit.model.dataChanged.emit(ind, ind1)

        # limitarr=main.Limit.table[np.where(main.Limit.table[:main.Limit.model.lastSerialNo,0]==data[0])]
        # if limitarr.size!=0:
        limit = main.LimitDict.get(data[0])
        if limit!=None:
            LIMIT = limit
        else:
            # print('mmmm',data[0],main.Limit.table[:main.Limit.lastSerialNo,0])
            LIMIT=0.0

        # depositarr = main.Deposit.table[np.where(main.Deposit.table[:main.Deposit.model.lastSerialNo, 0] == data[0])]
        # if depositarr.size!=0:
        deposit = main.DepositDict.get(data[0])
        if deposit != None:
            Deposit = deposit
        else:
            Deposit=0.0

        if(LIMIT >0):
            if data[13]>LIMIT:
                AccessMRGuti = data[13] / LIMIT * 100.0
            else:
                AccessMRGuti=0.0
        else:
            AccessMRGuti = 0.0

        # fltr=main.CMTWM.table[np.where(main.CMTWM.table[:main.CMTWM.lastSerialNo,0]==data[0])]
        # if fltr.size!=0:
        row=main.cmtwmDict.get(data[0])
        if row!=None:
            # CashMRG=fltr[0][3]
            fltr=main.CMTWM.table[row,:]
            CashMRG=fltr[3]
            data[13]=data[13]+CashMRG
        else:
            CashMRG=0.0


        main.TWM.table[main.TWM.model.lastSerialNo,[0,1,2,3,6,7,9,10,12,13,14,15,16,17,21,25]] =[data[0],data[1], data[2],data[3], data[6],data[7],data[9],data[10],data[12],data[13],data[14],data[15],Deposit,LIMIT,AccessMRGuti,CashMRG]

        main.TWM.lastSerialNo += 1
        main.TWM.model.lastSerialNo += 1
        main.TWM.model.insertRows()
        main.TWM.model.rowCount()
        ind = main.TWM.model.index(0, 0)
        ind1 = main.TWM.model.index(0, 1)
        main.TWM.model.dataChanged.emit(ind, ind1)

        main.twmDict[data[0]]=main.TWM.lastSerialNo-1












# @QtCore.pyqtSlot(dict)
# def updateLTP_POCW(main,data):
#     try:
#         st=time.time()
#         if (main.POCW.model.lastSerialNo !=0):
#             # print("pt")
#             # x = (np.unique(main.POCW.table[:main.POCW.lastSerialNo, 2]))
#
#
#             # if (data['Token'] in x ):
#              #   print("2")
#             fltr = np.asarray([data['Token']])
#             x = main.POCW.table[np.in1d(main.POCW.table[:, 2], fltr), 12]
#             # print(x)
#             if x.size != 0:
#                 for i in x:
#                     netValue = main.POCW.table[i, 16]
#                     qty = main.POCW.table[i, 15]
#                     ins=main.POCW.table[i, 3]
#
#                     mtm = (qty * data['LTP']) + netValue
#
#                     if(ins in ['FUTSTK' ,'FUTIDX']):
#                         editableList = [10, 11,17]
#                     else:
#                         editableList = [10, 11, 18]
#
#
#                     main.POCW.table[i, editableList] = [data['LTP'],  mtm,mtm]
#
#                     for j in editableList:
#                         ind = main.POCW.model.index(i, j)
#                         # ind1 = main.marketW.model.index(i,1)
#                         main.POCW.model.dataChanged.emit(ind, ind)
#
#         et = time.time()
#         # print('timePOCWLTP', et - st)
#
#
#     except:
#
#         print(traceback.print_exc())

@QtCore.pyqtSlot(dict)
def updateLTP_POCW(main,data):
    try:
        st=time.time()
        if (main.POCW.lastSerialNo !=0):
            # print('kdkk')
            # if main.tokenDict.get(data['Token']):
            #     listSno = main.tokenDict[data['Token']]['POCW']
            #     if listSno!=[]:
            #         Fsno=listSno[0]
            #         isFilterUpdate=True
            #     else:
            #         isFilterUpdate=False
            # else:
            #     isFilterUpdate = False


            if main.maintokenDict.get(data['Token']):
                x = main.maintokenDict[data['Token']]['POCW']



                if x !=[]:
                    for i in x:
                        netValue = main.POCW.table[i, 16]
                        qty = main.POCW.table[i, 15]
                        ins=main.POCW.table[i, 3]

                        mtm = (qty * data['LTP']) + netValue

                        if(ins in ['FUTSTK' ,'FUTIDX']):
                            editableList = [10, 11,17]
                        else:
                            editableList = [10, 11, 18]


                        main.POCW.table[i, editableList] = [data['LTP'],  mtm,mtm]



                        # for j in editableList:
                        #     ind = main.POCW.model.index(i, j)
                        #     # ind1 = main.marketW.model.index(i,1)
                        #     main.POCW.model.dataChanged.emit(ind, ind)

            # fltrarr1 = np.where(main.POCW.FilterTable[:main.POCW.model.flastSerialNo, 2] == data['Token'])[0]
            # print('kdkdkk',fltrarr1)

            if main.tokenDict.get(data['Token']):
                x = main.tokenDict[data['Token']]['POCW']

                if x != []:

                    # print('jfj')
                    rowNo = x[0]
                    # netValue = main.POCW.FilterTable[rowNo, 16]
                    # qty = main.POCW.FilterTable[rowNo, 15]
                    # ins = main.POCW.FilterTable[rowNo, 3]
                    sNo = main.POCW.FilterTable[rowNo, 12]
                    mainData = main.POCW.table[sNo, :]

                    # mtm = (qty * data['LTP']) + netValue
                    #
                    # if ins in ['FUTSTK', 'FUTIDX']:
                    #     editableList = [10, 11, 17]
                    # else:
                    #     editableList = [10, 11, 18]

                    editableList = [10, 11, 17,18]
                    main.POCW.FilterTable[rowNo, editableList] = [mainData[10], mainData[11], mainData[17],mainData[18]]

                    for j in editableList:
                        ind = main.POCW.model.index(rowNo, j)
                        main.POCW.model.dataChanged.emit(ind, ind)



        et = time.time()
        # print('timePOCWLTP', et - st)


    except:

        print(traceback.print_exc())



# @QtCore.pyqtSlot(dict)
# def updateLTP_POTW(main,data):
#     try:
#         st=time.time()
#         if (main.POTW.lastSerialNo !=0):
#             # print("pt")
#             # x = (np.unique(main.POTW.table[:main.POTW.lastSerialNo, 2]))
#
#
#             # if (data['Token'] in x ):
#              #   print("2")
#             fltr = np.asarray([data['Token']])
#             x = main.POTW.table[np.in1d(main.POTW.table[:, 2], fltr), 12]
#             # print(x)
#             if x.size != 0:
#                 for i in x:
#                     netValue = main.POTW.table[i, 16]
#                     qty = main.POTW.table[i, 15]
#                     ins=main.POTW.table[i, 3]
#
#                     mtm = (qty * data['LTP']) + netValue
#
#                     if ins in ['FUTSTK' , 'FUTIDX']:
#                         editableList = [10, 11,21]
#                     else:
#                         editableList = [10, 11, 22]
#
#
#                     main.POTW.table[i, editableList] = [data['LTP'],  mtm,mtm]
#
#                     for j in editableList:
#                         ind = main.POTW.model.index(i, j)
#                         # ind1 = main.marketW.model.index(i,1)
#                         main.POTW.model.dataChanged.emit(ind, ind)
#
#         et=time.time()
#         # print('timePOTWLTP',et-st)
#     except:
#
#         print(traceback.print_exc())


@QtCore.pyqtSlot(dict)
def updateLTP_POTW(main,data):
    try:
        st=time.time()
        # if data['Token']==50134 or data['Token']==50099 or data['Token']==50102 or data['Token']==50132 :
        #     print('jf',data['LTP'],data['Token'],time.time())
        if (main.POTW.lastSerialNo !=0):


            # if main.tokenDict.get(data['Token']):
            #     listSno = main.tokenDict[data['Token']]['POCW']
            #     if listSno!=[]:
            #         Fsno=listSno[0]
            #         isFilterUpdate=True
            #     else:
            #         isFilterUpdate=False
            # else:
            #     isFilterUpdate = False



            if main.maintokenDict.get(data['Token']):
                x=main.maintokenDict[data['Token']]['POTW']

                #72448
                # print(x)
                if x!= []:

                    for i in x:
                        netValue = main.POTW.table[i, 16]
                        qty = main.POTW.table[i, 15]
                        ins=main.POTW.table[i, 3]

                        mtm = (qty * data['LTP']) + netValue

                        if ins in ['FUTSTK' , 'FUTIDX']:
                            editableList = [10, 11,21]
                        else:
                            editableList = [10, 11, 22]


                        main.POTW.table[i, editableList] = [data['LTP'],  mtm,mtm]
                        # if isFilterUpdate==True:
                        #     if Fsno==i:


                        # for j in editableList:
                        #     ind = main.POTW.model.index(i, j)
                        #     main.POTW.model.dataChanged.emit(ind, ind)

            if main.tokenDict.get(data['Token']):
                x = main.tokenDict[data['Token']]['POTW']
            # fltrarr1 = np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 2] == data['Token'])[0]
            # print('kdkdkk',fltrarr1)

                if x!=[]:
                    # print('jfj')
                    rowNo=x[0]
                    # netValue = main.POTW.FilterTable[rowNo, 12]
                    # qty = main.POTW.FilterTable[rowNo, 15]
                    # ins = main.POTW.FilterTable[rowNo, 3]

                    sNo = main.POTW.FilterTable[rowNo, 12]
                    mainData = main.POTW.table[sNo,:]



                    # mtm = (qty * data['LTP']) + netValue
                    #
                    # if ins in ['FUTSTK', 'FUTIDX']:
                    #     editableList = [10, 11, 21]
                    # else:
                    #     editableList = [10, 11, 22]

                    editableList = [10, 11, 21,22]
                    main.POTW.FilterTable[rowNo, editableList] = [mainData[10], mainData[11], mainData[21],mainData[22]]

                    for j in editableList:
                        ind = main.POTW.model.index(rowNo, j)
                        main.POTW.model.dataChanged.emit(ind, ind)



        et=time.time()
        # print('timePOTWLTP',et-st)
    except:

        print(traceback.print_exc())



def updateLTP_CMPOTW(main,data):
    try:
        st=time.time()
        if (main.CMPOTW.model.lastSerialNo != 0):
            # print('ddd')
            #print("1")
            # x = (np.unique(main.CMPOTW.table[:main.CMPOTW.lastSerialNo, 2]))


            # if (data['Token'] in x ):
             #   print("2")
            # fltr = np.asarray([data['Token']])
            # x = main.CMPOTW.table[np.in1d(main.CMPOTW.table[:, 2], fltr), 9]
            # print(x)
            if main.CMtokenDict.get(data['Token']):
                x=main.CMtokenDict[data['Token']]['POTW']
                for i in x:
                    netValue = main.CMPOTW.table[i, 13]
                    qty = main.CMPOTW.table[i, 12]
                    # print(type(qty),type(data['LTP']))


                    mtm = (qty * data['LTP']) + netValue

                    # if(ins in ['FUTSTK' ,'FUTIDX']):
                    #     editableList = [10, 11,21]
                    # else:
                    #     editableList = [10, 11, 22]

                    editableList = [7,8]
                    main.CMPOTW.table[i, editableList] = [data['LTP'],  mtm]

                    for j in editableList:
                        ind = main.CMPOTW.model.index(i, j)
                        # ind1 = main.marketW.model.index(i,1)
                        main.CMPOTW.model.dataChanged.emit(ind, ind)
        et=time.time()
        # print('timecmpotw',et-st)

    except:

        print(traceback.print_exc())
def updateLTP_CMPOCW(main,data):
    try:
        st=time.time()
        if (main.CMPOCW.model.lastSerialNo != 0):
            # print('ddd')
            #print("1")
            # x = (np.unique(main.CMPOTW.table[:main.CMPOTW.lastSerialNo, 2]))


            # if (data['Token'] in x ):
             #   print("2")
            # fltr = np.asarray([data['Token']])
            # x = main.CMPOTW.table[np.in1d(main.CMPOTW.table[:, 2], fltr), 9]
            # print(x)
            if main.CMtokenDict.get(data['Token']):
                x=main.CMtokenDict[data['Token']]['POCW']
                for i in x:
                    netValue = main.CMPOCW.table[i, 13]
                    qty = main.CMPOCW.table[i, 12]
                    # print(type(qty),type(data['LTP']))


                    mtm = (qty * data['LTP']) + netValue

                    # if(ins in ['FUTSTK' ,'FUTIDX']):
                    #     editableList = [10, 11,21]
                    # else:
                    #     editableList = [10, 11, 22]

                    editableList = [7,8]
                    main.CMPOCW.table[i, editableList] = [data['LTP'],  mtm]

                    for j in editableList:
                        ind = main.CMPOCW.model.index(i, j)
                        # ind1 = main.marketW.model.index(i,1)
                        main.CMPOCW.model.dataChanged.emit(ind, ind)
        et=time.time()
        # print('timecmpotw',et-st)

    except:

        print(traceback.print_exc())



def update_CASH_MTMPOTW(main):
    try:
        # print('timer')
        st = time.time()

        if main.CMPOTW.lastSerialNo!=0:
            Tmtm=dt.Frame(main.CMPOTW.table[:main.CMPOTW.model.lastSerialNo,[0,8,15]],names=['Uid','MTM','TOC'])

            Tmtm[1:] = dt.float64

            x = Tmtm[:, dt.sum(dt.f[1:]), dt.by('Uid')].to_numpy()

            for i in x:


                if (main.TWM.model.lastSerialNo !=0) :

                    # rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == i[0])[0]

                    rowNo = main.twmDict.get(i[0])

                    if (rowNo!=None):
                        # rowNo = rowarray[0]

                        data=main.TWM.table[rowNo,:]
                        fnomtm=data[8]
                        FNOTOC=data[24]
                        NetTOC=FNOTOC + i[2]

                        netMTM=fnomtm+i[1]-NetTOC


                        editList = [11,26,27,28]
                        main.TWM.table[rowNo, editList] = [i[1],netMTM,i[2],NetTOC]

                        for t in editList:
                            ind = main.TWM.model.index(rowNo, t)
                            main.TWM.model.dataChanged.emit(ind, ind)

                if (main.CMTWM.model.lastSerialNo !=0) :
                    # print('ijf',i)
                    # rowarray = np.where(main.CMTWM.table[:main.CMTWM.model.lastSerialNo, 0] == i[0])[0]
                    # if (rowarray.size != 0):
                    rowNo = main.cmtwmDict.get(i[0])

                    if (rowNo != None):
                        # rowNo = rowarray[0]

                        editList = [4]
                        main.CMTWM.table[rowNo, editList] = [i[1]]

                        for t in editList:
                            ind = main.CMTWM.model.index(rowNo, t)
                            main.CMTWM.model.dataChanged.emit(ind, ind)
        et = time.time()
        # print('CMMTMPOTW', et - st)
    except:
        print('nnn',traceback.print_exc(),)
def update_CASH_MTMPOCW(main):
    # print('timer')
    try:
        st = time.time()

        if main.CMPOCW.lastSerialNo!=0:
            Tmtm=dt.Frame(main.CMPOCW.table[:main.CMPOCW.model.lastSerialNo,[0,8,15]],names=['Uid','MTM','TOC'])

            Tmtm[1:] = dt.float64

            x = Tmtm[:, dt.sum(dt.f[1:]), dt.by('Uid')].to_numpy()

            for i in x:


                if (main.CWM.model.lastSerialNo !=0) :

                    # rowarray = np.where(main.CWM.table[:main.CWM.model.lastSerialNo, 0] == i[0])[0]
                    # if (rowarray.size != 0):
                    rowNo = main.cwmDict.get(i[0])

                    if (rowNo != None):
                        # rowNo = rowarray[0]

                        data=main.CWM.table[rowNo,:]
                        fnomtm=data[6]
                        FNOTOC=data[22]
                        NetTOC=FNOTOC + i[2]

                        netMTM=fnomtm+i[1]-NetTOC


                        editList = [16,24,25,26]
                        main.CWM.table[rowNo, editList] = [i[1],netMTM,i[2],NetTOC]

                        for t in editList:
                            ind = main.CWM.model.index(rowNo, t)
                            main.CWM.model.dataChanged.emit(ind, ind)

                if (main.CMCWM.model.lastSerialNo !=0) :
                    # print('ijf',i)
                    # rowarray = np.where(main.CMCWM.table[:main.CMCWM.model.lastSerialNo, 0] == i[0])[0]
                    # if (rowarray.size != 0):
                    rowNo = main.cmcwmDict.get(i[0])

                    if (rowNo != None):
                        # rowNo = rowarray[0]

                        editList = [2]
                        main.CMCWM.table[rowNo, editList] = [i[1]]

                        for t in editList:
                            ind = main.CMCWM.model.index(rowNo, t)
                            main.CMCWM.model.dataChanged.emit(ind, ind)
        et = time.time()
        # print('CMMTMPOCW', et - st)
    except:
        print(data,traceback.print_exc())



def updateGlobalMargin(main):
    # print('updateGlobalMargin')
    EXPOM=main.TWM.table[:, 1].sum()
    SPANM=main.TWM.table[:, 2].sum()

    NET_MRG=main.TWM.table[:,13].sum()

    # NET_MRG=main.TWM.table[:, 3].sum()
    FUT_MTM=main.TWM.table[:, 4].sum()
    OPT_MTM=main.TWM.table[:, 5].sum()
    FNO_MTM=FUT_MTM+OPT_MTM
    PRM_MRG=main.TWM.table[:, 12].sum()

    UpSCNMTM=main.TWM.table[:, 22].sum()
    DownSCNMTM=main.TWM.table[:, 23].sum()


    if(main.GlobalM.lastSerialNo !=0):

        editList = [0, 1,2, 3, 4,5,6,7,8]
        main.GlobalM.table[editList,1] = [SPANM,EXPOM,NET_MRG,FUT_MTM,OPT_MTM,FNO_MTM,PRM_MRG,UpSCNMTM,DownSCNMTM]

        # print(main.GlobalM.table)
        # print(main.GlobalM.table)

        for i in editList:
            ind = main.GlobalM.model.index(i, 1)
            main.GlobalM.model.dataChanged.emit(ind, ind)
    else:

        # main.GlobalM.table[main.GlobalM.lastSerialNo] = [SPANM,EXPOM,TotalM,FUT_MTM,OPT_MTM,FNO_MTM]

        main.GlobalM.table[:9,0]=['SPANM','EXPOM','TotalM','FUT_MTM','OPT_MTM','FNO_MTM','PRM_MRG','UpSCNMTM','DownSCNMTM']

        main.GlobalM.table[:9,1] = [SPANM, EXPOM, NET_MRG, FUT_MTM, OPT_MTM, FNO_MTM,PRM_MRG,UpSCNMTM,DownSCNMTM]

        for i in range(9):
            main.GlobalM.lastSerialNo += 1
            main.GlobalM.model.lastSerialNo += 1
            main.GlobalM.model.insertRows()
            main.GlobalM.model.rowCount()
            ind = main.GlobalM.model.index(0, 0)
            ind1 = main.GlobalM.model.index(0, 1)
            main.GlobalM.model.dataChanged.emit(ind, ind1)

    # main.GlobalM.lbllimit.setText(str(perc))
def updateGlobalMarginMainUser(main):

    EXPOM=main.CWM.table[:, 1].sum()
    SPANM=main.CWM.table[:, 2].sum()

    NET_MRG=main.CWM.table[:,9].sum()

    # NET_MRG=main.TWM.table[:, 3].sum()
    FUT_MTM=main.CWM.table[:, 4].sum()
    OPT_MTM=main.CWM.table[:, 5].sum()
    FNO_MTM=FUT_MTM+OPT_MTM
    PRM_MRG=main.CWM.table[:, 8].sum()

    UpSCNMTM=main.CWM.table[:, 20].sum()
    DownSCNMTM=main.CWM.table[:, 21].sum()


    if(main.GlobalM.lastSerialNo !=0):

        editList = [0, 1,2, 3, 4,5,6,7,8]
        main.GlobalM.table[editList,1] = [SPANM,EXPOM,NET_MRG,FUT_MTM,OPT_MTM,FNO_MTM,PRM_MRG,UpSCNMTM,DownSCNMTM]

        # print(main.GlobalM.table)
        # print(main.GlobalM.table)

        for i in editList:
            ind = main.GlobalM.model.index(i, 1)
            main.GlobalM.model.dataChanged.emit(ind, ind)
    else:

        # main.GlobalM.table[main.GlobalM.lastSerialNo] = [SPANM,EXPOM,TotalM,FUT_MTM,OPT_MTM,FNO_MTM]

        main.GlobalM.table[:9,0]=['SPANM','EXPOM','TotalM','FUT_MTM','OPT_MTM','FNO_MTM','PRM_MRG','UpSCNMTM','DownSCNMTM']

        main.GlobalM.table[:9,1] = [SPANM, EXPOM, NET_MRG, FUT_MTM, OPT_MTM, FNO_MTM,PRM_MRG,UpSCNMTM,DownSCNMTM]

        for i in range(9):
            main.GlobalM.lastSerialNo += 1
            main.GlobalM.model.lastSerialNo += 1
            main.GlobalM.model.insertRows()
            main.GlobalM.model.rowCount()
            ind = main.GlobalM.model.index(0, 0)
            ind1 = main.GlobalM.model.index(0, 1)
            main.GlobalM.model.dataChanged.emit(ind, ind1)

    # main.GlobalM.lbllimit.setText(str(perc))


def updateFOMTMPOTW(main):
    try:
        st=time.time()
        if main.POTW.lastSerialNo!=0:


            df3 = dt.Frame(main.POTW.table[:main.POTW.lastSerialNo,
                           [0,4,11,21,22,25,26,27,28,31,32,33]],
                           names=['UserID', 'Symbol', 'MTM','FUT_MTM','OPT_MTM','Delta',
                          'Theta','Gama','Vega','UpSCNMTM','DownSCNMTM','TOC'])

            df3[2:] = dt.float64



            x = df3[:, dt.sum(dt.f[2:]), dt.by('UserID', 'Symbol')]

            x1=x[:, dt.sum(dt.f[2:]), dt.by('UserID')]


            for i in x.to_numpy():
                # rowarray = np.where((main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 0] == i[0])& (main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 1] == i[1]))[0]

                try:
                    rowNo=main.twswmDict.get(i[0]).get(i[1])
                except:
                    rowNo=None
                # print(fltrarr)

                # if (fltrarr.size != 0):
                #         isRecordExist = True

                if (rowNo!=None):
                    # print('exist')

                    # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
                    # rowNo = rowarray[0]

                    # print('rowNo',rowNo)

                    editList = [5, 6, 7,10,11,12,13,14,15,16]
                    main.TWSWM.table[rowNo, editList] = [i[3], i[4], i[2],i[5], i[6], i[7],i[8], i[9], i[10],i[11]]

                    for t in editList:
                        ind = main.TWSWM.model.index(rowNo, t)
                        main.TWSWM.model.dataChanged.emit(ind, ind)

            # ind = main.TWSWM.model.index(0, 0)
            # ind1 = main.TWSWM.model.index(0, 1)
            # main.TWSWM.model.dataChanged.emit(ind, ind1)

            for i in x1.to_numpy():
                # rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == i[0])[0]
                # print(fltrarr)

                # if (fltrarr.size != 0):
                #         isRecordExist = True

                rowNo = main.twmDict.get(i[0])
                if (rowNo != None):
                    # print('exist')

                    # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
                    # rowNo = rowarray[0]

                    data=main.TWM.table[rowNo,:]


                    NetPrem=data[15]
                    cashMTM=data[11]

                    cashTOC = data[27]

                    NetTOC = cashTOC + i[10]

                    NetMTM= i[1]+  cashMTM - NetTOC

                    #FNOMTM -NETPRem
                    Ans=i[1] - NetPrem

                    if Ans <0:
                        deposit = data[16]

                        if deposit>0:
                            RiskPer=abs(Ans)/deposit
                        else:
                            RiskPer=0.0
                    else:
                        RiskPer=0.0

                    editList=[4,5, 8,20,22,23,24,26,27,28]
                    main.TWM.table[rowNo, editList] = [i[2], i[3], i[1],RiskPer,i[8],i[9],i[10],NetMTM,cashTOC,NetTOC]



                    for t in editList:
                        ind = main.TWM.model.index(rowNo, t)
                        main.TWM.model.dataChanged.emit(ind, ind)
            # ind = main.TWM.model.index(0, 0)
            # ind1 = main.TWM.model.index(0, 1)
            # main.TWM.model.dataChanged.emit(ind, ind1)
        et = time.time()
        # print('FOMTMPOTW',et-st)
    except:
        print('hhh',traceback.print_exc())

# def updateFOMTMPOTW(main):
#     try:
#         st=time.time()
#         if main.POTW.lastSerialNo!=0:
#
#
#             df3 = dt.Frame(main.POTW.table[:main.POTW.lastSerialNo,
#                            [0,4,11,21,22,25,26,27,28,31,32,33,2,15,16,3]],
#                            names=['UserID', 'Symbol', 'MTM','FUT_MTM','OPT_MTM','Delta',
#                           'Theta','Gama','Vega','UpSCNMTM','DownSCNMTM','TOC','Token','netQty','netVal','instrument'])
#
#             df3[2:12] = dt.float64
#             df3[12:14] = dt.int64
#             df3[14] = dt.float64
#
#             df4=dt.Frame(main.fo_contract[:,[2,19]],names=['Token','LTP'])
#             df4[0] = dt.int64
#             df4[1] = dt.float64
#             df4.key = "Token"
#             df3 = df3[:, :, dt.join(df4)]
#
#
#             df3[:, dt.update(MTM=dt.f['netQty'] * dt.abs(dt.f['LTP']) + dt.f['netVal'])]
#             df3[:, dt.update(FUT_MTM=dt.ifelse((dt.f['instrument'] == 'FUTSTK') | (dt.f['instrument'] == 'FUTIDX'), dt.f.MTM,0.0))]
#             df3[:, dt.update(OPT_MTM=dt.ifelse((dt.f['instrument'] == 'OPTSTK') | (dt.f['instrument'] == 'OPTIDX'), dt.f.MTM,0.0))]
#
#
#
#
#             x = df3[:, dt.sum(dt.f[2:15]), dt.by('UserID', 'Symbol')]
#
#             x1=x[:, dt.sum(dt.f[2:15]), dt.by('UserID')]
#
#
#             for i in x.to_numpy():
#                 # rowarray = np.where((main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 0] == i[0])& (main.TWSWM.table[:main.TWSWM.model.lastSerialNo, 1] == i[1]))[0]
#
#                 try:
#                     rowNo=main.twswmDict.get(i[0]).get(i[1])
#                 except:
#                     rowNo=None
#                 # print(fltrarr)
#
#                 # if (fltrarr.size != 0):
#                 #         isRecordExist = True
#
#                 if (rowNo!=None):
#                     # print('exist')
#
#                     # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
#                     # rowNo = rowarray[0]
#
#                     # print('rowNo',rowNo)
#
#                     editList = [5, 6, 7,10,11,12,13,14,15,16]
#                     main.TWSWM.table[rowNo, editList] = [i[3], i[4], i[2],i[5], i[6], i[7],i[8], i[9], i[10],i[11]]
#
#                     # for t in editList:
#                     #     ind = main.TWSWM.model.index(rowNo, t)
#                     #     main.TWSWM.model.dataChanged.emit(ind, ind)
#
#             ind = main.TWSWM.model.index(0, 0)
#             ind1 = main.TWSWM.model.index(0, 1)
#             main.TWSWM.model.dataChanged.emit(ind, ind1)
#
#             for i in x1.to_numpy():
#                 # rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == i[0])[0]
#                 # print(fltrarr)
#
#                 # if (fltrarr.size != 0):
#                 #         isRecordExist = True
#
#                 rowNo = main.twmDict.get(i[0])
#                 if (rowNo != None):
#                     # print('exist')
#
#                     # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
#                     # rowNo = rowarray[0]
#
#                     data=main.TWM.table[rowNo,:]
#
#
#                     NetPrem=data[15]
#                     cashMTM=data[11]
#
#                     cashTOC = data[27]
#
#                     NetTOC = cashTOC + i[10]
#
#                     NetMTM= i[1]+  cashMTM - NetTOC
#
#                     #FNOMTM -NETPRem
#                     Ans=i[1] - NetPrem
#
#                     if Ans <0:
#                         deposit = data[16]
#
#                         if deposit>0:
#                             RiskPer=abs(Ans)/deposit
#                         else:
#                             RiskPer=0.0
#                     else:
#                         RiskPer=0.0
#
#                     editList=[4,5, 8,20,22,23,24,26,27,28]
#                     main.TWM.table[rowNo, editList] = [i[2], i[3], i[1],RiskPer,i[8],i[9],i[10],NetMTM,cashTOC,NetTOC]
#
#
#
#                     # for t in editList:
#                     #     ind = main.TWM.model.index(rowNo, t)
#                     #     main.TWM.model.dataChanged.emit(ind, ind)
#             ind = main.TWM.model.index(0, 0)
#             ind1 = main.TWM.model.index(0, 1)
#             main.TWM.model.dataChanged.emit(ind, ind1)
#
#         et = time.time()
#         # print('FOMTMPOTW',et-st)
#     except:
#         print('hhh',traceback.print_exc())
def updateFOMTMPOCW(main):
    st = time.time()
    try:

        if main.POCW.lastSerialNo!=0:


            df3 = dt.Frame(main.POCW.table[:main.POCW.lastSerialNo,
                            [0,4,11,17,18,22,23,24,25,28,29,30]],
                            names=['UserID', 'Symbol', 'MTM','FUT_MTM','OPT_MTM','Delta',
                            'Theta','Gama','Vega','UpSCNMTM','DownSCNMTM','TOC'])

            df3[2:] = dt.float64
            df3[0:2]=dt.str64

            x = df3[:, dt.sum(dt.f[2:]), dt.by('UserID', 'Symbol')]

            x1=x[:, dt.sum(dt.f[2:]), dt.by('UserID')]




            for i in x.to_numpy():
                # rowarray = np.where((main.CWSWM.table[:main.CWSWM.model.lastSerialNo, 0] == i[0])& (main.CWSWM.table[:main.CWSWM.model.lastSerialNo, 1] == i[1]))[0]
                # print(fltrarr)

                # if (fltrarr.size != 0):
                #         isRecordExist = True

                # if main.cwswmDict.get(i[0]):
                    try:
                        rowNo = main.cwswmDict.get(i[0]).get(i[1])
                    except:
                        rowNo=None

                    if (rowNo!=None):
                        # print('exist')

                        # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
                        # rowNo = rowarray[0]

                        # print('rowNo',rowNo)

                        editList = [5, 6, 7,10,11,12,13,14,15,16]
                        main.CWSWM.table[rowNo, editList] = [i[3], i[4], i[2],i[5], i[6], i[7],i[8], i[9], i[10],i[11]]

                        for t in editList:
                            ind = main.CWSWM.model.index(rowNo, t)
                            main.CWSWM.model.dataChanged.emit(ind, ind)

            # ind = main.CWSWM.model.index(0, 0)
            # ind1 = main.CWSWM.model.index(0, 1)
            # main.CWSWM.model.dataChanged.emit(ind, ind1)

            for i in x1.to_numpy():
                # rowarray = np.where(main.CWM.table[:main.CWM.model.lastSerialNo, 0] == i[0])[0]
                # print(fltrarr)

                # if (fltrarr.size != 0):
                #         isRecordExist = True

                rowNo = main.cwmDict.get(i[0])

                if (rowNo!=None):
                    # print('exist')

                    # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
                    # rowNo = rowarray[0]

                    data=main.CWM.table[rowNo,:]


                    NetPrem=data[11]
                    cashMTM=data[16]

                    cashTOC = data[25]

                    NetTOC = cashTOC + i[10]

                    NetMTM= i[1]+  cashMTM - NetTOC

                    #FNOMTM -NETPRem
                    Ans=i[1] - NetPrem

                    if Ans <0:
                        ledger = data[13]

                        if ledger>0:
                            RiskPer=abs(Ans)/ledger
                        else:
                            RiskPer=0.0
                    else:
                        RiskPer=0.0

                    editList=[4,5, 6,18 ,20,21,22,24,25,26]
                    main.CWM.table[rowNo, editList] = [i[2], i[3], i[1],RiskPer,i[8],i[9],i[10],NetMTM,cashTOC,NetTOC]



                    for t in editList:
                        ind = main.CWM.model.index(rowNo, t)
                        main.CWM.model.dataChanged.emit(ind, ind)

            # ind = main.CWM.model.index(0, 0)
            # ind1 = main.CWM.model.index(0, 1)
            # main.CWM.model.dataChanged.emit(ind, ind1)


        et = time.time()
        # print('FOMTMPOCW', et - st)
    except:
        print('errorFOPOCW',traceback.print_exc(),main.POCW.table[0:main.POCW.lastSerialNo,0])
        # main.POCW.table[0:main.POCW.lastSerialNo, 0].

        # main.POCW.table[0:main.POCW.lastSerialNo, 0].tofile('d:/dddddata2.csv', sep=',')

# def updateFOMTMPOCW(main):
#     st = time.time()
#     try:
#
#         if main.POCW.lastSerialNo!=0:
#
#
#             df3 = dt.Frame(main.POCW.table[:main.POCW.lastSerialNo,
#                             [0,4,11,17,18,22,23,24,25,28,29,30,2,15,16,3]],
#                             names=['UserID', 'Symbol', 'MTM','FUT_MTM','OPT_MTM','Delta',
#                             'Theta','Gama','Vega','UpSCNMTM','DownSCNMTM','TOC','Token','netQty','netVal','instrument'])
#
#             # df3[2:] = dt.float64
#             df3[0:2]=dt.str64
#
#             df3[2:12] = dt.float64
#             df3[12:14] = dt.int64
#             df3[14] = dt.float64
#
#             df4 = dt.Frame(main.fo_contract[:, [2, 19]], names=['Token', 'LTP'])
#             df4[0] = dt.int64
#             df4[1] = dt.float64
#             df4.key = "Token"
#             df3 = df3[:, :, dt.join(df4)]
#
#             df3[:, dt.update(MTM=dt.f['netQty'] * dt.abs(dt.f['LTP']) + dt.f['netVal'])]
#             df3[:, dt.update(FUT_MTM=dt.ifelse((dt.f['instrument'] == 'FUTSTK') | (dt.f['instrument'] == 'FUTIDX'), dt.f.MTM, 0.0))]
#             df3[:, dt.update(OPT_MTM=dt.ifelse((dt.f['instrument'] == 'OPTSTK') | (dt.f['instrument'] == 'OPTIDX'), dt.f.MTM, 0.0))]
#
#             x = df3[:, dt.sum(dt.f[2:15]), dt.by('UserID', 'Symbol')]
#
#             x1=x[:, dt.sum(dt.f[2:15]), dt.by('UserID')]
#
#
#
#
#             for i in x.to_numpy():
#                 # rowarray = np.where((main.CWSWM.table[:main.CWSWM.model.lastSerialNo, 0] == i[0])& (main.CWSWM.table[:main.CWSWM.model.lastSerialNo, 1] == i[1]))[0]
#                 # print(fltrarr)
#
#                 # if (fltrarr.size != 0):
#                 #         isRecordExist = True
#
#                 # if main.cwswmDict.get(i[0]):
#                     try:
#                         rowNo = main.cwswmDict.get(i[0]).get(i[1])
#                     except:
#                         rowNo=None
#
#                     if (rowNo!=None):
#                         # print('exist')
#
#                         # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
#                         # rowNo = rowarray[0]
#
#                         # print('rowNo',rowNo)
#
#                         editList = [5, 6, 7,10,11,12,13,14,15,16]
#                         main.CWSWM.table[rowNo, editList] = [i[3], i[4], i[2],i[5], i[6], i[7],i[8], i[9], i[10],i[11]]
#
#             ind = main.CWSWM.model.index(0, 0)
#             ind1 = main.CWSWM.model.index(0, 1)
#             main.CWSWM.model.dataChanged.emit(ind, ind1)
#
#             for i in x1.to_numpy():
#                 # rowarray = np.where(main.CWM.table[:main.CWM.model.lastSerialNo, 0] == i[0])[0]
#                 # print(fltrarr)
#
#                 # if (fltrarr.size != 0):
#                 #         isRecordExist = True
#
#                 rowNo = main.cwmDict.get(i[0])
#
#                 if (rowNo!=None):
#                     # print('exist')
#
#                     # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
#                     # rowNo = rowarray[0]
#
#                     data=main.CWM.table[rowNo,:]
#
#
#                     NetPrem=data[11]
#                     cashMTM=data[16]
#
#                     cashTOC = data[25]
#
#                     NetTOC = cashTOC + i[10]
#
#                     NetMTM= i[1]+  cashMTM - NetTOC
#
#                     #FNOMTM -NETPRem
#                     Ans=i[1] - NetPrem
#
#                     if Ans <0:
#                         ledger = data[13]
#
#                         if ledger>0:
#                             RiskPer=abs(Ans)/ledger
#                         else:
#                             RiskPer=0.0
#                     else:
#                         RiskPer=0.0
#
#                     editList=[4,5, 6,18 ,20,21,22,24,25,26]
#                     main.CWM.table[rowNo, editList] = [i[2], i[3], i[1],RiskPer,i[8],i[9],i[10],NetMTM,cashTOC,NetTOC]
#
#
#
#             # for t in editList:
#             #     ind = main.CWM.model.index(rowNo, t)
#             #     main.CWM.model.dataChanged.emit(ind, ind)
#
#             ind = main.CWM.model.index(0, 0)
#             ind1 = main.CWM.model.index(0, 1)
#             main.CWM.model.dataChanged.emit(ind, ind1)
#
#
#         et = time.time()
#         # print('FOMTMPOCW', et - st)
#     except:
#         print('errorFOPOCW',traceback.print_exc(),main.POCW.table[0:main.POCW.lastSerialNo,0])
#         # main.POCW.table[0:main.POCW.lastSerialNo, 0].
#
#         # main.POCW.table[0:main.POCW.lastSerialNo, 0].tofile('d:/dddddata2.csv', sep=',')

@QtCore.pyqtSlot(object)
def updateCMCWM(main, data):

    # rowarray = np.where(main.CMCWM.table[:main.CMCWM.lastSerialNo, 0] == data[0])[0]
    # print(fltrarr)

    # if (fltrarr.size != 0):
    #         isRecordExist = True
    rowNo = main.cmcwmDict.get(data[0])
    # if (rowarray.size != 0):
    if (rowNo!=None):
        # print('exist')

        # rowNo = np.where(main.CMCWM.table[:, 0] == data[0])[0][0]
        # rowNo = rowarray[0]
        # print('rowNo',rowNo)


        editList = [1, 2,3,4]
        main.CMCWM.table[rowNo, editList] = [data[1], data[2],data[3],data[4]]

        for i in editList:
            ind = main.CMCWM.model.index(rowNo, i)
            main.CMCWM.model.dataChanged.emit(ind, ind)



    else:

        main.CMCWM.table[main.CMCWM.lastSerialNo] = data

        main.CMCWM.lastSerialNo += 1
        main.CMCWM.model.lastSerialNo += 1
        main.CMCWM.model.insertRows()
        main.CMCWM.model.rowCount()
        ind = main.CMCWM.model.index(0, 0)
        ind1 = main.CMCWM.model.index(0, 1)
        main.CMCWM.model.dataChanged.emit(ind, ind1)

        main.cmcwmDict[data[0]] = main.CMCWM.lastSerialNo - 1


    # rowarray = np.where(main.CWM.table[:main.CWM.model.lastSerialNo, 0] == data[0])[0]
    # if rowarray.size != 0:

    rowNo = main.cwmDict.get(data[0])
    if rowNo!=None:
        # rowNo = rowarray[0]
        d = main.CWM.table[rowNo, :]
        netmrg = d[9] + data[1]

        editList = [9, 15, 23]
        main.CWM.table[rowNo, editList] = [netmrg, data[4], data[1]]

        for i in editList:
            ind = main.CWM.model.index(rowNo, i)
            main.CWM.model.dataChanged.emit(ind, ind)

        # main.RecieverCM.subscribedlist('CMPOTW', 'NSECM', data[2])


@QtCore.pyqtSlot(object)
def updateCMPOCW(main,data):
    # 'ClentID', 'Series', 'Symbol','Qty', 'Tradeamt','Price', 'BQty', 'SQty','BAmt', 'SAmt','IntraDayQty','BuyIntra','SellIntra','TotalIntra'
    # print(data)

    # token = int(data[4])
    # clientcode=data[2]
    # sym = data[3]
    # # exp = datetime.datetime.fromtimestamp(int(data[26]))
    # # exp = exp.replace(2022)
    # # exp = datetime.datetime.strftime(exp, '%Y%m%d')
    # # strike = float(int(data[27]) / 100)
    # Series = data[8].split('\n')[0]
    #
    # buysell = data[7]
    #
    # TQty = int(data[4]) if buysell == '1' else -int(data[4])
    # Tamt = float(data[5]) * -TQty

    #data[2]=symbol
    #data[1]=series
    # try:
    #     farr=main.eq_contract[np.where((main.eq_contract[:,3]==data[2]) & (main.eq_contract[:,6]==data[1]))][0]
    #     token=farr[2]
    # except:
    #     print('symser',data[2],data[1])
    # try:
    #
    #     VAR = main.var_Mrg[np.where(main.var_Mrg[:, 4] == token)][0]
    #     #data[4]=tradeAmt
    #     MRG = data[4] * (VAR[3] / 100)
    #     # print('token',token)
    # except:
    #     #data[4]=tradeAmt
    #     MRG= data[4]
    #     # print('symser',data[2],data[1],token)

    # 'ClientID',
    # 'Exchange', 'Pn', 'Series', 'symbol', 'dayQty',
    # 'dayValue', 'LTP', 'MTM', 'SerialNO', 'OpenQty',
    # 'OpenAmt', 'netQty', 'NetValue', 'MRG', 'TOC'


    fltrarr1 = main.CMPOCW.table[np.where((main.CMPOCW.table[:main.CMPOCW.lastSerialNo, 0] == data[0]) & (
            main.CMPOCW.table[:main.CMPOCW.lastSerialNo, 2] == data[2]))]

    if (fltrarr1.size != 0):
        #     isRecordExist=True
        #
        # if(isRecordExist):
        #     # print('exist')

        SerialNo = fltrarr1[0][9]





        editList = [5, 6, 12, 13,14,15]
        # main.CMPOCW.table[SerialNo, editList] = [newDQty, newDValue, newQty, newValue,newMRG,expense]
        main.CMPOCW.table[SerialNo, editList] = [data[5], data[6], data[12], data[13],data[14],data[15]]

        for i in editList:
            ind = main.CMPOCW.model.index(SerialNo, i)
            main.CMPOCW.model.dataChanged.emit(ind, ind)




    else:


        main.CMPOCW.table[main.CMPOCW.lastSerialNo, :] = [data[0], data[1], data[2], data[3],
                                                          data[4], data[5], data[6], 0,
                                                          0, main.CMPOCW.lastSerialNo, 0, 0, data[12], data[13],data[14],data[15]]

        main.CMPOCW.lastSerialNo += 1
        main.CMPOCW.model.lastSerialNo += 1
        main.CMPOCW.model.insertRows()
        main.CMPOCW.model.rowCount()
        ind = main.CMPOCW.model.index(0, 0)
        ind1 = main.CMPOCW.model.index(0, 1)
        main.CMPOCW.model.dataChanged.emit(ind, ind1)

        main.RecieverCM.subscribedlist('CMPOCW', 'NSECM', data[2])

        if main.CMtokenDict.get(data[2]) != None:
            main.CMtokenDict[data[2]]['POCW'].append(main.CMPOCW.model.lastSerialNo - 1)
        else:
            main.CMtokenDict[data[2]] = {}
            main.CMtokenDict[data[2]]['POCW'] = [main.CMPOCW.model.lastSerialNo - 1]
            main.CMtokenDict[data[2]]['POTW'] = []

def updateCMPOTW(main,data):
    fltrarr1 = main.CMPOTW.table[np.where((main.CMPOTW.table[:main.CMPOTW.model.lastSerialNo, 0] == data[0]) & (
            main.CMPOTW.table[:main.CMPOTW.model.lastSerialNo, 2] == data[2]))]

    if (fltrarr1.size != 0):
        #     isRecordExist=True
        #
        # if(isRecordExist):
        #     # print('exist')

        SerialNo = fltrarr1[0][9]




        editList = [5, 6, 12, 13,14,15]
        main.CMPOTW.table[SerialNo, editList] = [data[5], data[6], data[12], data[13],data[14],data[15]]

        for i in editList:
            ind = main.CMPOTW.model.index(SerialNo, i)
            main.CMPOTW.model.dataChanged.emit(ind, ind)



    else:


        main.CMPOTW.table[main.CMPOTW.model.lastSerialNo, [0,1,2,3,4,5,6,9,10,11,12,13,14,15]] = [data[0], data[1], data[2], data[3], data[4], data[5],
                                                            data[6], main.CMPOTW.model.lastSerialNo , data[10],
                                                            data[11],data[12], data[13], data[14],data[15]
                                                            ]

        main.CMPOTW.lastSerialNo += 1
        main.CMPOTW.model.lastSerialNo += 1
        main.CMPOTW.model.insertRows()
        main.CMPOTW.model.rowCount()
        ind = main.CMPOTW.model.index(0, 0)
        ind1 = main.CMPOTW.model.index(0, 1)
        main.CMPOTW.model.dataChanged.emit(ind, ind1)

        main.RecieverCM.subscribedlist('CMPOTW', 'NSECM', data[2])

        if main.CMtokenDict.get(data[2]) != None:
            main.CMtokenDict[data[2]]['POTW'].append(main.CMPOTW.model.lastSerialNo - 1)
        else:
            main.CMtokenDict[data[2]] = {}
            main.CMtokenDict[data[2]]['POTW'] = [main.CMPOTW.model.lastSerialNo - 1]
            main.CMtokenDict[data[2]]['POCW'] = []


def updateCMTWM(main,data):
    # rowarray = np.where(main.CMTWM.table[:main.CMTWM.model.lastSerialNo, 0] == data[0])[0]
    # print(fltrarr)

    # if (fltrarr.size != 0):
    #         isRecordExist = True
    rowNo=main.cmtwmDict.get(data[0])

    # if (rowarray.size != 0):
    if (rowNo != None):
        # print('exist')

        # rowNo = np.where(main.CMTWM.table[:, 0] == data[0])[0][0]
        # rowNo = rowarray[0]
        # print('rowNo',rowNo)

        editList = [3,6,7]
        main.CMTWM.table[rowNo, editList] = [data[3],data[6],data[7]]

        for i in editList:
            ind = main.CMTWM.model.index(rowNo, i)
            main.CMTWM.model.dataChanged.emit(ind, ind)

    else:


        main.CMTWM.table[main.CMTWM.model.lastSerialNo,[0,1,2,3,5,6,7]] = [data[0], data[1], data[2], data[3], data[5],data[6],data[7]]

        main.CMTWM.lastSerialNo += 1
        main.CMTWM.model.lastSerialNo += 1
        main.CMTWM.model.insertRows()
        main.CMTWM.model.rowCount()
        ind = main.CMTWM.model.index(0, 0)
        ind1 = main.CMTWM.model.index(0, 1)
        main.CMTWM.model.dataChanged.emit(ind, ind1)

        main.cmtwmDict[data[0]] = main.CMTWM.lastSerialNo - 1

    # rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == data[0])[0]
    # if rowarray.size!=0:
    rowNo = main.twmDict.get(data[0])
    if rowNo!=None:

        # rowNo=rowarray[0]
        d=main.TWM.table[rowNo,:]
        netmrg=d[13]+data[3]

        editList = [13, 18, 25]
        main.TWM.table[rowNo, editList] = [netmrg, data[7],data[3]]

        for i in editList:
            ind = main.TWM.model.index(rowNo, i)
            main.TWM.model.dataChanged.emit(ind, ind)


    # main.TWM.table[np.where(main.TWM.table[:main.TWM.lastSerialNo,0]==data[0]),[18,25]]=[data[7],data[3]]





def updateSCNPricePOTW(main):
    if main.POTW.lastSerialNo != 0:

        Tokens = np.unique(main.POTW.table[:main.POTW.lastSerialNo, 2])

        for i in Tokens:

            # fltr = np.asarray([i])
            # x = main.POTW.table[np.in1d(main.POTW.table[:, 2], fltr)]

            if main.maintokenDict.get(i):
                x=main.maintokenDict[i]['POTW']

                if x!=[]:
                    Data = main.POTW.table[x[0], :]

                    if Data[10] != 0:
                        # print('dkfj',Data)

                        if Data[7] in ['CE', 'PE']:
                            # futureToken = Data[25]
                            futureToken = main.fo_contract[i - 35000, 17]
                            fPrice = main.fo_contract[futureToken - 35000, 19]
                            # fPrice = Data[25]
                            # exp = datetime.datetime.strftime()[5]
                            # print('exp...',Data[5])
                            exp = datetime.datetime.strptime(Data[5], "%Y%m%d")

                            exp1 = exp.strftime("%d%b%Y")
                            # print('exp',exp,type(exp))
                            optionType = Data[7][0].lower()

                            strikeP = float(Data[6])
                            expiryDay = datetime.datetime.strptime(exp1, '%d%b%Y')

                            daysRemaaining1 = (expiryDay - main.todate).days
                            # print('days',daysRemaaining1)
                            daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
                            t = daysRemaaining / 365
                            # ltp = Data[10]

                            price = (fPrice * 10) / 100
                            UpFprice = fPrice + price

                            price = (fPrice * 10) / 100
                            DownFprice = fPrice - price


                            UPscnPrice = black_scholes(optionType, UpFprice, strikeP, t, 0.01, Data[24]/100)
                            DOWNscnPrice1 = black_scholes(optionType, DownFprice, strikeP, t, 0.01, Data[24]/100)

                            # if (Data[4] == 'ABBOTINDIA'):
                            #     print('ABBOTINDIA , up', UpFprice,UPscnPrice, strikeP, t)
                            #     print('down', DownFprice,DOWNscnPrice1, strikeP, t,DOWNscnPrice1)

                            for s in x:
                                i = main.POTW.table[s, :]

                                editableList = [29,30,31,32]

                                UPscnMTM= (i[15] * UPscnPrice) + i[16]
                                DownscnMTM=(i[15] * DOWNscnPrice1) + i[16]


                                main.POTW.table[i[12], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]
                                row = np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 12] == i[12])[0]
                                if row.size != 0:
                                    main.POTW.FilterTable[row[0], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]

                            ind = main.POTW.model.index(0, 0)
                            ind1 = main.POTW.model.index(0, 1)
                            main.POTW.model.dataChanged.emit(ind, ind1)

                        else:

                            price = (Data[10] * 10) / 100
                            UPscnPrice = Data[10] + price

                            price = (Data[10]) / 100
                            DOWNscnPrice1 = Data[10] - price

                            for s in x:
                                i = main.POTW.table[s, :]

                                editableList = [29,30,31,32]

                                UPscnMTM= (i[15] * UPscnPrice) + i[16]
                                DownscnMTM=(i[15] * DOWNscnPrice1) + i[16]


                                main.POTW.table[i[12], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]
                                row = np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 12] == i[12])[0]
                                if row.size != 0:
                                    main.POTW.FilterTable[row[0], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]

                            ind = main.POTW.model.index(0, 0)
                            ind1 = main.POTW.model.index(0, 1)
                            main.POTW.model.dataChanged.emit(ind, ind1)


# def updateSCNPricePOTW(main):
#     if main.POTW.lastSerialNo != 0:
#
#         Tokens = np.unique(main.POTW.table[:main.POTW.lastSerialNo, 2])
#
#         for i in Tokens:
#
#             # fltr = np.asarray([i])
#             # x = main.POTW.table[np.in1d(main.POTW.table[:, 2], fltr)]
#
#             if main.maintokenDict.get(i):
#                 x=main.maintokenDict[i]['POTW']
#
#             # Data = main.POTW.table[x[0][12], :]
#                 Data = main.POTW.table[x[0], :]
#                 LTPdata = main.fo_contract[i - 35000, :]
#
#                 if LTPdata[19] != 0:
#                 # if Data[10] != 0:
#                     # print('dkfj',Data)
#
#                     if Data[7] in ['CE', 'PE']:
#                         # futureToken = Data[25]
#                         futureToken = LTPdata[17]
#                         fPrice = main.fo_contract[futureToken - 35000, 19]
#                         # fPrice = Data[25]
#                         # exp = datetime.datetime.strftime()[5]
#                         # print('exp...',Data[5])
#                         exp = datetime.datetime.strptime(Data[5], "%Y%m%d")
#
#                         exp1 = exp.strftime("%d%b%Y")
#                         # print('exp',exp,type(exp))
#                         optionType = Data[7][0].lower()
#
#                         strikeP = float(Data[6])
#                         expiryDay = datetime.datetime.strptime(exp1, '%d%b%Y')
#
#                         daysRemaaining1 = (expiryDay - main.todate).days
#                         # print('days',daysRemaaining1)
#                         daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
#                         t = daysRemaaining / 365
#                         # ltp = Data[10]
#
#                         price = (fPrice * 10) / 100
#                         UpFprice = fPrice + price
#
#                         price = (fPrice * 10) / 100
#                         DownFprice = fPrice - price
#
#
#                         UPscnPrice = black_scholes(optionType, UpFprice, strikeP, t, 0.01, Data[24]/100)
#                         DOWNscnPrice1 = black_scholes(optionType, DownFprice, strikeP, t, 0.01, Data[24]/100)
#
#                         # if (Data[4] == 'ABBOTINDIA'):
#                         #     print('ABBOTINDIA , up', UpFprice,UPscnPrice, strikeP, t)
#                         #     print('down', DownFprice,DOWNscnPrice1, strikeP, t,DOWNscnPrice1)
#
#                         for s in x:
#                             i = main.POTW.table[s, :]
#
#                             editableList = [29,30,31,32]
#
#                             UPscnMTM= (i[15] * UPscnPrice) + i[16]
#                             DownscnMTM=(i[15] * DOWNscnPrice1) + i[16]
#
#
#                             main.POTW.table[i[12], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]
#                             row = np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 12] == i[12])[0]
#                             if row.size != 0:
#                                 main.POTW.FilterTable[row[0], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]
#
#                         ind = main.POTW.model.index(0, 0)
#                         ind1 = main.POTW.model.index(0, 1)
#                         main.POTW.model.dataChanged.emit(ind, ind1)

def updateSCNPricePOCW(main):
    if main.POCW.lastSerialNo != 0:

        Tokens = np.unique(main.POCW.table[:main.POCW.lastSerialNo, 2])

        for i in Tokens:
            # fltr = np.asarray([i])
            # x = main.POCW.table[np.in1d(main.POCW.table[:, 2], fltr)]
            if main.maintokenDict.get(i):
                x=main.maintokenDict[i]['POCW']

            # Data = main.POCW.table[x[0][12], :]
                if x != []:
                    Data = main.POCW.table[x[0], :]

                    if Data[10] != 0:
                        # print('dkfj',Data)

                        if Data[7] in ['CE', 'PE']:
                            # futureToken = Data[25]
                            futureToken = main.fo_contract[i - 35000, 17]
                            fPrice = main.fo_contract[futureToken - 35000, 19]
                            # fPrice = Data[25]
                            # exp = datetime.datetime.strftime()[5]
                            # print('exp...',Data[5])
                            exp = datetime.datetime.strptime(Data[5], "%Y%m%d")

                            exp1 = exp.strftime("%d%b%Y")
                            # print('exp',exp,type(exp))
                            optionType = Data[7][0].lower()

                            strikeP = float(Data[6])
                            expiryDay = datetime.datetime.strptime(exp1, '%d%b%Y')

                            daysRemaaining1 = (expiryDay - main.todate).days
                            # print('days',daysRemaaining1)
                            daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
                            t = daysRemaaining / 365
                            # ltp = Data[10]

                            price = (fPrice * 10) / 100
                            UpFprice = fPrice + price

                            price = (fPrice * 10) / 100
                            DownFprice = fPrice - price


                            UPscnPrice = black_scholes(optionType, UpFprice, strikeP, t, 0.01, Data[24]/100)
                            DOWNscnPrice1 = black_scholes(optionType, DownFprice, strikeP, t, 0.01, Data[24]/100)

                            # if (Data[4] == 'ABBOTINDIA'):
                            #     print('ABBOTINDIA , up', UpFprice,UPscnPrice, strikeP, t)
                            #     print('down', DownFprice,DOWNscnPrice1, strikeP, t,DOWNscnPrice1)

                            for s in x:
                                i = main.POCW.table[s, :]
                                editableList = [26,27,28,29]

                                UPscnMTM= (i[15] * UPscnPrice) + i[16]
                                DownscnMTM=(i[15] * DOWNscnPrice1) + i[16]


                                main.POCW.table[i[12], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]
                                row = np.where(main.POCW.FilterTable[:main.POCW.model.flastSerialNo, 12] == i[12])[0]
                                if row.size != 0:
                                    main.POCW.FilterTable[row[0], editableList] = [UPscnPrice, DOWNscnPrice1, UPscnMTM,
                                                                                                               DownscnMTM]
                            ind = main.POCW.model.index(0, 0)
                            ind1 = main.POCW.model.index(0, 1)
                            main.POCW.model.dataChanged.emit(ind, ind1)

                        else:

                            price = (Data[10] * 10) / 100
                            UPscnPrice = Data[10] + price

                            price = (Data[10]) / 100
                            DOWNscnPrice1 = Data[10] - price

                            for s in x:
                                i = main.POTW.table[s, :]

                                editableList = [29, 30, 31, 32]

                                UPscnMTM = (i[15] * UPscnPrice) + i[16]
                                DownscnMTM = (i[15] * DOWNscnPrice1) + i[16]

                                main.POTW.table[i[12], editableList] = [UPscnPrice, DOWNscnPrice1, UPscnMTM, DownscnMTM]
                                row = np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 12] == i[12])[0]
                                if row.size != 0:
                                    main.POTW.FilterTable[row[0], editableList] = [UPscnPrice, DOWNscnPrice1, UPscnMTM,
                                                                                   DownscnMTM]

                            ind = main.POTW.model.index(0, 0)
                            ind1 = main.POTW.model.index(0, 1)
                            main.POTW.model.dataChanged.emit(ind, ind1)


# def updateSCNPricePOCW(main):
#     if main.POCW.lastSerialNo != 0:
#
#         Tokens = np.unique(main.POCW.table[:main.POCW.lastSerialNo, 2])
#
#         for i in Tokens:
#             # fltr = np.asarray([i])
#             # x = main.POCW.table[np.in1d(main.POCW.table[:, 2], fltr)]
#             if main.maintokenDict.get(i):
#                 x=main.maintokenDict[i]['POCW']
#
#             # Data = main.POCW.table[x[0][12], :]
#                 Data = main.POCW.table[x[0], :]
#
#                 LTPdata = main.fo_contract[i - 35000, :]
#
#                 if LTPdata[19] != 0:
#                 # if Data[10] != 0:
#                     # print('dkfj',Data)
#
#                     if Data[7] in ['CE', 'PE']:
#                         # futureToken = Data[25]
#                         futureToken = LTPdata[17]
#                         fPrice = main.fo_contract[futureToken - 35000, 19]
#                         # fPrice = Data[25]
#                         # exp = datetime.datetime.strftime()[5]
#                         # print('exp...',Data[5])
#                         exp = datetime.datetime.strptime(Data[5], "%Y%m%d")
#
#                         exp1 = exp.strftime("%d%b%Y")
#                         # print('exp',exp,type(exp))
#                         optionType = Data[7][0].lower()
#
#                         strikeP = float(Data[6])
#                         expiryDay = datetime.datetime.strptime(exp1, '%d%b%Y')
#
#                         daysRemaaining1 = (expiryDay - main.todate).days
#                         # print('days',daysRemaaining1)
#                         daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
#                         t = daysRemaaining / 365
#                         # ltp = Data[10]
#
#                         price = (fPrice * 10) / 100
#                         UpFprice = fPrice + price
#
#                         price = (fPrice * 10) / 100
#                         DownFprice = fPrice - price
#
#
#                         UPscnPrice = black_scholes(optionType, UpFprice, strikeP, t, 0.01, Data[24]/100)
#                         DOWNscnPrice1 = black_scholes(optionType, DownFprice, strikeP, t, 0.01, Data[24]/100)
#
#                         # if (Data[4] == 'ABBOTINDIA'):
#                         #     print('ABBOTINDIA , up', UpFprice,UPscnPrice, strikeP, t)
#                         #     print('down', DownFprice,DOWNscnPrice1, strikeP, t,DOWNscnPrice1)
#
#                         for s in x:
#                             i = main.POCW.table[s, :]
#                             editableList = [26,27,28,29]
#
#                             UPscnMTM= (i[15] * UPscnPrice) + i[16]
#                             DownscnMTM=(i[15] * DOWNscnPrice1) + i[16]
#
#
#                             main.POCW.table[i[12], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]
#                             row = np.where(main.POCW.FilterTable[:main.POCW.model.flastSerialNo, 12] == i[12])[0]
#                             if row.size != 0:
#                                 main.POCW.FilterTable[row[0], editableList] = [UPscnPrice, DOWNscnPrice1, UPscnMTM,
#                                                                                DownscnMTM]
#                         ind = main.POCW.model.index(0, 0)
#                         ind1 = main.POCW.model.index(0, 1)
#                         main.POCW.model.dataChanged.emit(ind, ind1)


def update_Greek_SCNMTM(main):
    pass








def update_Greeks_POTWAPI(main):
    st=time.time()
    DBLTP_url = main.FastApiURL + '/v3/dbLTP'
    DBheaders = {
        'Content-Type': 'application/json'
    }
    req = requests.request("POST", DBLTP_url, headers=DBheaders)
    dataLTP = req.json()

    # print(type(dataLTP),dataLTP)

    for p in main.POTW.table[:main.POTW.lastSerialNo]:

        if p[10]!=0:
            d = dataLTP.get(str(p[2]))
            if d:
                #p[10]=d['LTP']

                # (qty * data['LTP']) + netValue
                # p[11]=(p[15]*d['LTP'])+p[16]
                print('djfkdjfk')

                p[24]=d['IV']
                p[25]=d['Delta'] *p[15]
                p[26]=d['Theta']*p[15]
                p[27]=d['Gama']*p[15]
                p[28]=d['Vega']*p[15]

                # if (p[3] in ['FUTIDX','FUTSTK']):
                #     p[21]=p[11]
                # else:
                #     p[22]=p[11]

    ind = main.POTW.model.index(0, 0)
    ind1 = main.POTW.model.index(0, 1)
    main.POTW.model.dataChanged.emit(ind, ind1)

    et=time.time()
    # print('time:POTWGreek',et-st)



            # if (p[3] in ['FUTIDX', 'FUTSTK']):
            #     p[17] = p[11]
            # else:
            #     p[18] = p[11]

        # main.sgDB_POCW.emit(p)

def update_Greeks_POTW(main):

    st=time.time()
    if main.POTW.lastSerialNo != 0:

        Tokens = np.unique(main.POTW.table[:main.POTW.lastSerialNo, 2])

        for i in Tokens:
            # fltr = np.asarray([i])
            # x = main.POTW.table[np.in1d(main.POTW.table[:, 2], fltr)]

            if main.maintokenDict.get(i):
                x=main.maintokenDict[i]['POTW']

                # Data = main.POTW.table[x[0][12], :]
                Data = main.POTW.table[x[0], :]

                if Data[10]!=0:
                    # print('dkfj',Data)

                    if Data[7] in ['CE', 'PE']:
                        # futureToken = Data[25]
                        futureToken = main.fo_contract[i - 35000, 17]
                        fPrice = main.fo_contract[futureToken - 35000, 19]
                        # fPrice = Data[25]
                        # exp = datetime.datetime.strftime()[5]
                        # print('exp...',Data[5])
                        exp = datetime.datetime.strptime(Data[5], "%Y%m%d")

                        exp1 = exp.strftime("%d%b%Y")
                        # print('exp',exp,type(exp))
                        optionType = Data[7][0].lower()

                        strikeP = float(Data[6])
                        expiryDay = datetime.datetime.strptime(exp1, '%d%b%Y')

                        daysRemaaining1 = (expiryDay - main.todate).days
                        # print('days',daysRemaaining1)
                        daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
                        t = daysRemaaining / 365
                        ltp = Data[10]

                        # print('nnnnn',type(fPrice),type(strikeP),type(ltp))
                        # if(i==40688):
                        #
                        #     print(40688,exp,main.todate,daysRemaaining,t)
                        #     # print(40688,data['LTP'], fPrice, strikeP, t, main.r, optionType)
                        try:
                            # print('jfkdjf',ltp,fPrice,strikeP,t,main.r,optionType)
                            imp_v = iv(ltp, fPrice, strikeP, t, main.r, optionType)


                        except TypeError:

                            # print('jgh', Data)
                            imp_v = 0.01
                        except BelowIntrinsicException:
                            imp_v = 0.01
                        except:
                            imp_v = 0.01

                        # imp_v1=round(imp_v*100,2)

                        # main.sender.sendData(dict1)
                        try:

                            delt = delta(optionType, fPrice, strikeP, t, main.r, imp_v)
                            # delt = delta('c', 1064.35, 1100.0, t, main.r, imp_v)
                            delt = round(delt, 4)

                            gm = gamma(optionType, fPrice, strikeP, t, main.r, imp_v)
                            gm = round(gm, 4)

                            # rh = rho(optionType, fPrice, strikeP, t, main.r, imp_v)

                            tht = theta(optionType, fPrice, strikeP, t, main.r, imp_v)
                            tht = round(tht, 4)

                            vg = vega(optionType, fPrice, strikeP, t, main.r, imp_v)
                            vg = round(vg, 4)

                            # print('IV', imp_v * 100,delt,vg,tht,gm,Data[4])

                            # print(x)

                            for s in x:
                                i = main.POTW.table[s, :]
                                editableList = [24, 25, 26, 27, 28]
                                main.POTW.table[i[12], editableList] = [imp_v * 100, delt*i[15], tht*i[15], gm*i[15], vg*i[15]]

                                row = np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 12] == i[12])[0]
                                if row.size!=0:

                                    main.POTW.FilterTable[row[0],editableList]=[imp_v * 100, delt*i[15], tht*i[15], gm*i[15], vg*i[15]]
                            ind = main.POTW.model.index(0, 0)
                            ind1 = main.POTW.model.index(0, 1)
                            main.POTW.model.dataChanged.emit(ind, ind1)

                        except:
                            print(traceback.print_exc(), optionType, type(fPrice), type(strikeP), type(ltp), optionType, t,
                                  main.r, imp_v, fPrice, strikeP)

                else:
                    for s in x:
                        i = main.POTW.table[s, :]
                        editableList = [25]
                        main.POTW.table[i[12], editableList] = [i[15]]
                        row = np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 12] == i[12])[0]
                        if row.size != 0:
                            main.POTW.FilterTable[row[0],editableList] = [i[15]]
                    ind = main.POTW.model.index(0, 0)
                    ind1 = main.POTW.model.index(0, 1)
                    main.POTW.model.dataChanged.emit(ind, ind1)

    et = time.time()
    # print('timegreeks', et - st)

# def update_Greeks_POTW(main):
#
#     st=time.time()
#     if main.POTW.lastSerialNo != 0:
#
#         Tokens = np.unique(main.POTW.table[:main.POTW.lastSerialNo, 2])
#
#         for i in Tokens:
#             # fltr = np.asarray([i])
#             # x = main.POTW.table[np.in1d(main.POTW.table[:, 2], fltr)]
#
#             if main.maintokenDict.get(i):
#                 x=main.maintokenDict[i]['POTW']
#
#                 # Data = main.POTW.table[x[0][12], :]
#                 Data = main.POTW.table[x[0], :]
#                 LTPdata=main.fo_contract[i - 35000, :]
#
#                 if LTPdata[19]!=0:
#                     # print('dkfj',Data)
#
#                     if Data[7] in ['CE', 'PE']:
#                         # futureToken = Data[25]
#                         futureToken = LTPdata[17]
#                         fPrice = main.fo_contract[futureToken - 35000, 19]
#                         # fPrice = Data[25]
#                         # exp = datetime.datetime.strftime()[5]
#                         # print('exp...',Data[5])
#                         exp = datetime.datetime.strptime(Data[5], "%Y%m%d")
#
#                         exp1 = exp.strftime("%d%b%Y")
#                         # print('exp',exp,type(exp))
#                         optionType = Data[7][0].lower()
#
#                         strikeP = float(Data[6])
#                         expiryDay = datetime.datetime.strptime(exp1, '%d%b%Y')
#
#                         daysRemaaining1 = (expiryDay - main.todate).days
#                         # print('days',daysRemaaining1)
#                         daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
#                         t = daysRemaaining / 365
#                         ltp = LTPdata[19]
#
#                         # print('nnnnn',type(fPrice),type(strikeP),type(ltp))
#                         # if(i==40688):
#                         #
#                         #     print(40688,exp,main.todate,daysRemaaining,t)
#                         #     # print(40688,data['LTP'], fPrice, strikeP, t, main.r, optionType)
#                         try:
#                             # print('jfkdjf',ltp,fPrice,strikeP,t,main.r,optionType)
#                             imp_v = iv(ltp, fPrice, strikeP, t, main.r, optionType)
#
#
#                         except TypeError:
#
#                             # print('jgh', Data)
#                             imp_v = 0.01
#                         except BelowIntrinsicException:
#                             imp_v = 0.01
#                         except:
#                             imp_v = 0.01
#
#                         # imp_v1=round(imp_v*100,2)
#
#                         # main.sender.sendData(dict1)
#                         try:
#
#                             delt = delta(optionType, fPrice, strikeP, t, main.r, imp_v)
#                             # delt = delta('c', 1064.35, 1100.0, t, main.r, imp_v)
#                             delt = round(delt, 4)
#
#                             gm = gamma(optionType, fPrice, strikeP, t, main.r, imp_v)
#                             gm = round(gm, 4)
#
#                             # rh = rho(optionType, fPrice, strikeP, t, main.r, imp_v)
#
#                             tht = theta(optionType, fPrice, strikeP, t, main.r, imp_v)
#                             tht = round(tht, 4)
#
#                             vg = vega(optionType, fPrice, strikeP, t, main.r, imp_v)
#                             vg = round(vg, 4)
#
#                             # print('IV', imp_v * 100,delt,vg,tht,gm,Data[4])
#
#                             # print(x)
#
#                             for s in x:
#                                 i = main.POTW.table[s, :]
#                                 editableList = [24, 25, 26, 27, 28]
#                                 main.POTW.table[i[12], editableList] = [imp_v * 100, delt*i[15], tht*i[15], gm*i[15], vg*i[15]]
#                             #     row=np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 12] == i[12])[0]
#                             #     if row.size!=0:
#                             #
#                             #         main.POTW.FilterTable[row[0],editableList]=[imp_v * 100, delt*i[15], tht*i[15], gm*i[15], vg*i[15]]
#                             # ind = main.POTW.model.index(0, 0)
#                             # ind1 = main.POTW.model.index(0, 1)
#                             # main.POTW.model.dataChanged.emit(ind, ind1)
#
#                         except:
#                             print(traceback.print_exc(), optionType, type(fPrice), type(strikeP), type(ltp), optionType, t,
#                                   main.r, imp_v, fPrice, strikeP)
#
#                 else:
#                     for s in x:
#                         i = main.POTW.table[s, :]
#                         editableList = [25]
#                         main.POTW.table[i[12], editableList] = [i[15]]
#                         row = np.where(main.POTW.FilterTable[:main.POTW.model.flastSerialNo, 12] == i[12])[0]
#                         if row.size != 0:
#                             main.POTW.FilterTable[row[0],editableList] = [i[15]]
#                     ind = main.POTW.model.index(0, 0)
#                     ind1 = main.POTW.model.index(0, 1)
#                     main.POTW.model.dataChanged.emit(ind, ind1)
#
#     et = time.time()
#     # print('timegreeks', et - st)

def update_Greeks_POCW(main):
    st=time.time()
    if main.POCW.lastSerialNo != 0:

        Tokens = np.unique(main.POCW.table[:main.POCW.lastSerialNo, 2])

        for i in Tokens:


            # fltr = np.asarray([i])
            # x = main.POCW.table[np.in1d(main.POCW.table[:, 2], fltr)]

            if main.maintokenDict.get(i):
                x=main.maintokenDict[i]['POCW']


            # Data = main.POCW.table[x[0][12], :]
                Data = main.POCW.table[x[0], :]

                if Data[10]!=0:
                    # print('dkfj',Data)

                    if Data[7] in ['CE', 'PE']:
                        # futureToken = Data[25]
                        futureToken = main.fo_contract[i - 35000, 17]
                        fPrice = main.fo_contract[futureToken - 35000, 19]
                        # fPrice = Data[25]
                        # exp = datetime.datetime.strftime()[5]
                        # print('exp...',Data[5])
                        exp = datetime.datetime.strptime(Data[5], "%Y%m%d")

                        exp1 = exp.strftime("%d%b%Y")
                        # print('exp',exp,type(exp))
                        optionType = Data[7][0].lower()

                        strikeP = float(Data[6])
                        expiryDay = datetime.datetime.strptime(exp1, '%d%b%Y')

                        daysRemaaining1 = (expiryDay - main.todate).days
                        # print('days',daysRemaaining1)
                        daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
                        t = daysRemaaining / 365
                        ltp = Data[10]

                        # print('nnnnn',type(fPrice),type(strikeP),type(ltp))
                        # if(i==40688):
                        #
                        #     print(40688,exp,main.todate,daysRemaaining,t)
                        #     # print(40688,data['LTP'], fPrice, strikeP, t, main.r, optionType)
                        try:
                            # print('jfkdjf',ltp,fPrice,strikeP,t,main.r,optionType)
                            imp_v = iv(ltp, fPrice, strikeP, t, main.r, optionType)


                        except TypeError:

                            # print('jgh', Data)
                            imp_v = 0.01
                        except BelowIntrinsicException:
                            imp_v = 0.01
                        except:
                            imp_v = 0.01

                        # imp_v1=round(imp_v*100,2)

                        # main.sender.sendData(dict1)
                        try:

                            delt = delta(optionType, fPrice, strikeP, t, main.r, imp_v)
                            # delt = delta('c', 1064.35, 1100.0, t, main.r, imp_v)
                            delt = round(delt, 4)

                            gm = gamma(optionType, fPrice, strikeP, t, main.r, imp_v)
                            gm = round(gm, 4)

                            # rh = rho(optionType, fPrice, strikeP, t, main.r, imp_v)

                            tht = theta(optionType, fPrice, strikeP, t, main.r, imp_v)
                            tht = round(tht, 4)

                            vg = vega(optionType, fPrice, strikeP, t, main.r, imp_v)
                            vg = round(vg, 4)

                            # print('IV', imp_v * 100,delt,vg,tht,gm,Data[4])

                            # print(x)

                            for s in x:
                                i= main.POCW.table[s, :]
                                editableList = [21, 22, 23, 24, 25]
                                main.POCW.table[i[12], editableList] = [imp_v * 100, delt*i[15], tht*i[15], gm*i[15], vg*i[15]]

                                row = np.where(main.POCW.FilterTable[:main.POCW.model.flastSerialNo, 12] == i[12])[0]
                                if row.size != 0:
                                    main.POCW.FilterTable[row[0], editableList] = [imp_v * 100, delt * i[15],
                                                                                   tht * i[15], gm * i[15], vg * i[15]]


                            ind = main.POCW.model.index(0, 0)
                            ind1 = main.POCW.model.index(0, 1)
                            main.POCW.model.dataChanged.emit(ind, ind1)

                        except:
                            print(traceback.print_exc(), optionType, type(fPrice), type(strikeP), type(ltp), optionType, t,
                                  main.r, imp_v, fPrice, strikeP)

                else:
                    for s in x:
                        i = main.POCW.table[s, :]
                        editableList = [22]
                        main.POCW.table[i[12], editableList] = [i[15]]
                        row = np.where(main.POCW.FilterTable[:main.POCW.model.flastSerialNo, 12] == i[12])[0]
                        if row.size != 0:
                            main.POCW.FilterTable[row[0], editableList] = [i[15]]
                    ind = main.POCW.model.index(0, 0)
                    ind1 = main.POCW.model.index(0, 1)
                    main.POCW.model.dataChanged.emit(ind, ind1)
    et=time.time()
    # print('timegreeksPOCW',et-st)

# def update_Greeks_POCW(main):
#     st = time.time()
#     if main.POCW.lastSerialNo != 0:
#
#         Tokens = np.unique(main.POCW.table[:main.POCW.lastSerialNo, 2])
#
#         for i in Tokens:
#
#             # fltr = np.asarray([i])
#             # x = main.POCW.table[np.in1d(main.POCW.table[:, 2], fltr)]
#
#             if main.maintokenDict.get(i):
#                 x = main.maintokenDict[i]['POCW']
#
#                 # Data = main.POCW.table[x[0][12], :]
#                 Data = main.POCW.table[x[0], :]
#                 LTPdata = main.fo_contract[i - 35000, :]
#
#                 if LTPdata[19] != 0:
#
#
#                     # print('dkfj',Data)
#
#                     if Data[7] in ['CE', 'PE']:
#                         # futureToken = Data[25]
#                         futureToken = LTPdata[17]
#                         fPrice = main.fo_contract[futureToken - 35000, 19]
#                         # fPrice = Data[25]
#                         # exp = datetime.datetime.strftime()[5]
#                         # print('exp...',Data[5])
#                         exp = datetime.datetime.strptime(Data[5], "%Y%m%d")
#
#                         exp1 = exp.strftime("%d%b%Y")
#                         # print('exp',exp,type(exp))
#                         optionType = Data[7][0].lower()
#
#                         strikeP = float(Data[6])
#                         expiryDay = datetime.datetime.strptime(exp1, '%d%b%Y')
#
#                         daysRemaaining1 = (expiryDay - main.todate).days
#                         # print('days',daysRemaaining1)
#                         daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
#                         t = daysRemaaining / 365
#                         ltp = LTPdata[19]
#
#                         # print('nnnnn',type(fPrice),type(strikeP),type(ltp))
#                         # if(i==40688):
#                         #
#                         #     print(40688,exp,main.todate,daysRemaaining,t)
#                         #     # print(40688,data['LTP'], fPrice, strikeP, t, main.r, optionType)
#                         try:
#                             # print('jfkdjf',ltp,fPrice,strikeP,t,main.r,optionType)
#                             imp_v = iv(ltp, fPrice, strikeP, t, main.r, optionType)
#
#
#                         except TypeError:
#
#                             # print('jgh', Data)
#                             imp_v = 0.01
#                         except BelowIntrinsicException:
#                             imp_v = 0.01
#                         except:
#                             imp_v = 0.01
#
#                         # imp_v1=round(imp_v*100,2)
#
#                         # main.sender.sendData(dict1)
#                         try:
#
#                             delt = delta(optionType, fPrice, strikeP, t, main.r, imp_v)
#                             # delt = delta('c', 1064.35, 1100.0, t, main.r, imp_v)
#                             delt = round(delt, 4)
#
#                             gm = gamma(optionType, fPrice, strikeP, t, main.r, imp_v)
#                             gm = round(gm, 4)
#
#                             # rh = rho(optionType, fPrice, strikeP, t, main.r, imp_v)
#
#                             tht = theta(optionType, fPrice, strikeP, t, main.r, imp_v)
#                             tht = round(tht, 4)
#
#                             vg = vega(optionType, fPrice, strikeP, t, main.r, imp_v)
#                             vg = round(vg, 4)
#
#                             # print('IV', imp_v * 100,delt,vg,tht,gm,Data[4])
#
#                             # print(x)
#
#                             for s in x:
#                                 i = main.POCW.table[s, :]
#                                 editableList = [21, 22, 23, 24, 25]
#                                 main.POCW.table[i[12], editableList] = [imp_v * 100, delt * i[15], tht * i[15],
#                                                                         gm * i[15], vg * i[15]]
#
#                             ind = main.POCW.model.index(0, 0)
#                             ind1 = main.POCW.model.index(0, 1)
#                             main.POCW.model.dataChanged.emit(ind, ind1)
#
#                         except:
#                             print(traceback.print_exc(), optionType, type(fPrice), type(strikeP), type(ltp), optionType,
#                                   t,
#                                   main.r, imp_v, fPrice, strikeP)
#
#                 else:
#                     for s in x:
#                         i = main.POCW.table[s, :]
#                         editableList = [22]
#                         main.POCW.table[i[12], editableList] = [i[15]]
#                         row = np.where(main.POCW.FilterTable[:main.POCW.model.flastSerialNo, 12] == i[12])[0]
#                         if row.size != 0:
#                             main.POCW.FilterTable[row[0],editableList] = [i[15]]
#                     ind = main.POCW.model.index(0, 0)
#                     ind1 = main.POCW.model.index(0, 1)
#                     main.POCW.model.dataChanged.emit(ind, ind1)
#     et = time.time()
#     # print('timegreeksPOCW',et-st)


def update_contract_fo(main,data):
    # print('data1',data)
    # st=time.time()
    if(data['Exch'] == 2):
        if(data['ID']==7202):
            prevData = main.fo_contract[data['Token'] - 35000]
            prevVolume = prevData[32]
            newVolume = prevVolume + data['FillVolume']
            # print('prevVolume',prevVolume)
            main.fo_contract[data['Token']-35000,[19,22,32]] = [data['LTP'],data['OpenInterest'],
                                                                newVolume]
        elif(data['ID']==1501):
            # print(data)
            # prevData = self.fo_contract[data['Token'] - 35000]
            main.fo_contract[data['Token'] - 35000,[19,32,35]]=[data['LTP'],data['Volume'],data['ATP']]



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


def updateBWSWM(main):
    if(main.TWSWM.model.lastSerialNo !=0):

        df3 = dt.Frame(main.TWSWM.table[:main.TWSWM.model.lastSerialNo,
                       [9, 1,2,3,4,5,6,7,8,10,11,12,13,14,15]],
                       names=['Branch',
                              'Symbol','ExpoM', 'SpanM', 'netM', 'futmtm',
                              'optMTM','FNO_MTM','PRM_MRG','Delta','Theta',
                              'Gama','Vega','UpSCNMTM','DownSCNMTM'])

        df3[2:] = dt.float64

        x = df3[:, dt.sum(dt.f[2:]), dt.by('Branch','Symbol')]

        # x2 = df3[:, dt.sum(dt.f[4]), dt.by('Branch')].to_numpy()



        for i in x.to_numpy():
            rowarray = np.where((main.BWSWM.table[:main.BWSWM.model.lastSerialNo, 0] == i[0]) & (main.BWSWM.table[:main.BWSWM.model.lastSerialNo, 1] == i[1]))[0]


            try:
                # print(BN)
                BN = main.BWM.table[np.where(main.BWM.table[:main.BWM.model.lastSerialNo, 0] == i[0])]
                TotalM = BN[0][3]
                MarginPer=(i[4]*100)/TotalM
            except:
                MarginPer=0.0
                # print(traceback.print_exc(),i[0],i[4],BN,TotalM)

            # print(fltrarr)

            # if (fltrarr.size != 0):
            #         isRecordExist = True

            if (rowarray.size != 0):
                # print('exist')

                # rowNo = np.where(main.BWM.table[:, 0] == data[0])[0][0]
                rowNo = rowarray[0]




                # print('rowNo',rowNo)

                editList = [2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15]
                main.BWSWM.table[rowNo, editList] = [i[2],i[3],i[4],i[5],i[6],i[7],i[8],MarginPer,i[9],i[10],i[11],i[12],i[13],i[14]]

                for i in editList:
                    ind = main.BWSWM.model.index(rowNo, i)
                    main.BWSWM.model.dataChanged.emit(ind, ind)

            else:

                main.BWSWM.table[main.BWSWM.model.lastSerialNo] = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],MarginPer,i[9],i[10],i[11],i[12],i[13],i[14]]

                main.BWSWM.lastSerialNo += 1
                main.BWSWM.model.lastSerialNo += 1
                main.BWSWM.model.insertRows()
                main.BWSWM.model.rowCount()
                ind = main.BWSWM.model.index(0, 0)
                ind1 = main.BWSWM.model.index(0, 1)
                main.BWSWM.model.dataChanged.emit(ind, ind1)

def updateIndexes(main,data):

    # print(data)
    per=data['PercentChange']/100
    if(per<0):
        per=str(per)+'%'
    else:
        per='+'+str(per)+'%'

    if(data['IndexName']=='Nifty 50'):
        main.PrcNFT.setText(str(data['IndexValue']))
        main.percentageNFT.setText(per)

    elif (data['IndexName'] == 'Nifty Bank'):
        main.PrcBNF.setText(str(data['IndexValue']))
        main.percentageBNF.setText(per)

    elif (data['IndexName'] == 'India VIX'):
        main.PrcVIX.setText(str(data['IndexValue']))
        main.percentageVIX.setText(per)



def updatePhysicalMRG(main):
    pass




# def updatePOTWopenPosition(main,data):
#     # st=time.time()
#     main.POTW.table[:data.shape[0], :] = data
#     # main.POTW.model._data[:data.shape[0], :] = data[:, 1:]
#
#     main.POTW.lastSerialNo += data.shape[0]
#
#     main.POTW.lastSerialNo += data.shape[0]
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
#     # main.POTW.table[main.POTW.lastSerialNo, :] = [data['UserID'], data['Exchange'], data['Token'], , sym, exp,
#     #                                                     strike, opt, TQty, Tamt, 0,
#     #                                                     0, main.POTW.lastSerialNo, 0, 0, TQty, Tamt, 0.0, 0.0,
#     #                                                     0.0, netPrem, 0.0, 0.0, premMrg]
#     # main.POTW.table[main.POTW.lastSerialNo, :] = data
#
#     # main.POTW.lastSerialNo += 1
#     # main.POTW.lastSerialNo += 1
#     # main.POTW.model.insertRows()
#     # main.POTW.model.rowCount()
#     # ind = main.POTW.model.index(0, 0)
#     # ind1 = main.POTW.model.index(0, 1)
#     # main.POTW.model.dataChanged.emit(ind, ind1)

# def TWMdoubleClicked(main):
#     UserID = main.TWM.tableView.selectedIndexes()[0].data()
#
#     main.cFrame.DPOTW.show()
#     main.cFrame.DPOTW.raise_()
#
#     main.POTW.smodel.setClientCode(UserID)
#     main.POTW.smodel.setFilterFixedString(UserID)
#
#     main.POTW.le_text.setText(UserID)
#
#     main.TWSWM.smodel.setClientCode(UserID)
#     main.TWSWM.smodel.setFilterFixedString(UserID)
def TWMdoubleClicked(main):
    UserID = main.TWM.tableView.selectedIndexes()[0].data()



    main.cFrame.DPOTW.show()
    main.cFrame.DPOTW.raise_()

    temp = np.zeros_like(main.POTW.FilterTable[0:main.POTW.model.flastSerialNo, :])

    main.POTW.FilterTable[0:main.POTW.model.flastSerialNo, :] = temp

    main.POTW.model.DelRows(0, main.POTW.model.flastSerialNo)

    # main.OrderBook.modelO.DelRows()
    main.POTW.model.flastSerialNo = 0
    main.POTW.model.rowCount()
    # st=time.time()
    fltr=main.POTW.table[np.where(main.POTW.table[:main.POTW.lastSerialNo,0]==UserID)]

    for i in main.tokenDict:
        main.tokenDict[i]['POTW'] = []
    for data in fltr:
        main.POTW.FilterTable[main.POTW.model.flastSerialNo] = [data[0],
                                                                data[1], data[2], data[3], data[4], data[5],
                                                                data[6], data[7], data[8], data[9], data[10],
                                                                data[11], data[12], data[13], data[14],
                                                                data[15],
                                                                data[16], data[17], data[18], data[19], data[20],
                                                                data[21], data[22], data[23], data[24], data[25],
                                                                data[26], data[27], data[28], data[29], data[30],
                                                                data[31],data[32], data[33],data[34]]

        main.POTW.model.flastSerialNo += 1
        main.POTW.model.insertRows()
        main.POTW.model.rowCount()

        if main.tokenDict.get(data[2]):
            main.tokenDict[data[2]]['POTW'].append(main.POTW.model.flastSerialNo - 1)
        else:
            main.tokenDict[data[2]] = {}
            main.tokenDict[data[2]]['POTW'] = [main.POTW.model.flastSerialNo - 1]
            main.tokenDict[data[2]]['POCW'] = []





    ind = main.POTW.model.index(0, 0)
    ind1 = main.POTW.model.index(0, 1)
    main.POTW.model.dataChanged.emit(ind, ind1)

    # main.POTW.smodel.setClientCode(UserID)
    # main.POTW.smodel.setFilterFixedString(UserID)

    main.POTW.le_text.setText(UserID)

    main.TWSWM.smodel.setClientCode(UserID)
    main.TWSWM.smodel.setFilterFixedString(UserID)


def CWMdoubleClicked(main):
    clientcode = main.CWM.tableView.selectedIndexes()[0].data()
    # print('cwm double click data',index)

    # rowNo = table.row()
    #
    # clientcode = main.CWM.table[rowNo, 0]
    #
    # main.POCW.smodel.setFilterKeyColumn(0)
    main.cFrame.DPOCW.show()
    main.cFrame.DPOCW.raise_()

    temp = np.zeros_like(main.POCW.FilterTable[0:main.POCW.model.flastSerialNo, :])

    main.POCW.FilterTable[0:main.POCW.model.flastSerialNo, :] = temp

    main.POCW.model.DelRows(0, main.POCW.model.flastSerialNo)


    main.POCW.model.flastSerialNo = 0
    main.POCW.model.rowCount()
    # ind = main.POCW.model.index(0, 0)
    # ind1 = main.POCW.model.index(0, 1)
    # main.POCW.model.dataChanged.emit(ind, ind1)

    # st=time.time()
    fltr = main.POCW.table[np.where(main.POCW.table[:main.POCW.lastSerialNo, 0] == clientcode)]

    for i in main.tokenDict:
        main.tokenDict[i]['POCW'] = []
    for data in fltr:
        main.POCW.FilterTable[main.POCW.model.flastSerialNo, :] = [data[0], data[1], data[2], data[3], data[4], data[5],
                                                                   data[6],
                                                                   data[7], data[8], data[9], data[10], data[11],
                                                                   data[12], data[13], data[14], data[15],
                                                                   data[16], data[17], data[18], data[19], data[20],
                                                                   data[21],
                                                                   data[22], data[23], data[24], data[25], data[26],
                                                                   data[27],
                                                                   data[28], data[29],
                                                                   data[30]]

        main.POCW.model.flastSerialNo += 1
        main.POCW.model.insertRows()
        main.POCW.model.rowCount()

        if main.tokenDict.get(data[2]):
            main.tokenDict[data[2]]['POCW'].append(main.POCW.model.flastSerialNo - 1)
        else:
            main.tokenDict[data[2]] = {}
            main.tokenDict[data[2]]['POCW'] = [main.POCW.model.flastSerialNo - 1]
            main.tokenDict[data[2]]['POTW'] = []

    ind = main.POCW.model.index(0, 0)
    ind1 = main.POCW.model.index(0, 1)
    main.POCW.model.dataChanged.emit(ind, ind1)

    # main.POCW.smodel.setClientCode(clientcode)
    # main.POCW.smodel.setFilterFixedString(clientcode)

    main.POCW.le_text.setText(clientcode)

    main.CWSWM.smodel.setClientCode(clientcode)
    main.CWSWM.smodel.setFilterFixedString(clientcode)

def CMCWMdoubleClicked(main):
    clientcode = main.CMCWM.tableView.selectedIndexes()[0].data()
    # print('cwm double click data',index)

    # rowNo = table.row()
    #
    # clientcode = main.CWM.table[rowNo, 0]
    #
    # main.POCW.smodel.setFilterKeyColumn(0)
    # main.CMPOCW.smodel.setClientCode(clientcode)
    # main.CMPOCW.smodel.setFilterFixedString(clientcode)
    main.CMPOCW.show()
    main.CMPOCW.smodel.setFilterKeyColumn(0)
    main.CMPOCW.smodel.setFilterFixedString(clientcode)

def CMTWMdoubleClicked(main):
    UserID = main.CMTWM.tableView.selectedIndexes()[0].data()
    # print('cwm double click data',index)

    # rowNo = table.row()
    #
    # clientcode = main.CWM.table[rowNo, 0]
    #
    # main.POCW.smodel.setFilterKeyColumn(0)
    # main.CMPOCW.smodel.setClientCode(clientcode)
    # main.CMPOCW.smodel.setFilterFixedString(clientcode)
    main.CMPOTW.show()
    main.CMPOTW.smodel.setFilterKeyColumn(0)
    main.CMPOTW.smodel.setFilterFixedString(UserID)

def CMPOCWdoubleClicked(main):
    Token = main.CMPOCW.tableView.selectedIndexes()[2].data()
    # print('cwm double click data',index)

    # rowNo = table.row()
    #
    # clientcode = main.CWM.table[rowNo, 0]
    #
    # main.POCW.smodel.setFilterKeyColumn(0)
    # main.CMPOCW.smodel.setClientCode(clientcode)
    # main.CMPOCW.smodel.setFilterFixedString(clientcode)
    main.CMPOTW.show()
    main.CMPOTW.smodel.setFilterKeyColumn(2)
    main.CMPOTW.smodel.setFilterFixedString(str(Token))




# def TWMdoubleClicked(main):
#     UserID = main.TWM.tableView.selectedIndexes()[0].data()
#
#     main.cFrame.DPOTW.show()
#     main.cFrame.DPOTW.raise_()
#
#     main.POTW.smodel.setClientCode(UserID)
#     main.POTW.smodel.setFilterFixedString(UserID)
#
#     main.POTW.le_text.setText(UserID)
#
#     main.TWSWM.smodel.setClientCode(UserID)
#     main.TWSWM.smodel.setFilterFixedString(UserID)

def POCWdoubleClicked(main):
    # Token = main.POCW.tableView.selectedIndexes()[2].data()
    rowNo = main.POCW.tableView.selectedIndexes()[main.POCW.SerialNO].data()

    Token=main.POCW.table[rowNo,2]
    print(rowNo,Token,main.POCW.SerialNO)

    main.POTW.smodel.setToken(str(Token))
    main.POTW.smodel.setFilterFixedString(str(Token))

    # main.POTW.smodel.setFilterKeyColumn(2)
    # main.POTW.smodel.setFilterFixedString(str(Token))


def BWMdoubleClicked(main):
    Branch = main.BWM.tableView.selectedIndexes()[0].data()

    main.TWM.smodel.setFilterKeyColumn(6)
    main.TWM.smodel.setFilterFixedString(Branch)


def UserIDfilterPOTW(main):


    UserID=main.POTW.le_text.text()
    # main.cFrame.DPOTW.show()
    # main.cFrame.DPOTW.raise_()

    temp = np.zeros_like(main.POTW.FilterTable[0:main.POTW.model.flastSerialNo, :])

    main.POTW.FilterTable[0:main.POTW.model.flastSerialNo, :] = temp

    main.POTW.model.DelRows(0, main.POTW.model.flastSerialNo)

    # main.OrderBook.modelO.DelRows()
    main.POTW.model.flastSerialNo = 0
    main.POTW.model.rowCount()
    # st=time.time()
    fltr = main.POTW.table[np.where(main.POTW.table[:main.POTW.lastSerialNo, 0] == UserID)]



    for i in main.tokenDict:
        main.tokenDict[i]['POTW']=[]

    for data in fltr:
        main.POTW.FilterTable[main.POTW.model.flastSerialNo] = [data[0],
                                                                data[1], data[2], data[3], data[4], data[5],
                                                                data[6], data[7], data[8], data[9], data[10],
                                                                data[11], data[12], data[13], data[14],
                                                                data[15],
                                                                data[16], data[17], data[18], data[19], data[20],
                                                                data[21], data[22], data[23], data[24], data[25],
                                                                data[26], data[27], data[28], data[29], data[30],
                                                                data[31], data[32], data[33],data[34]]

        main.POTW.model.flastSerialNo += 1
        main.POTW.model.insertRows()
        main.POTW.model.rowCount()

        if main.tokenDict.get(data[2]):
            main.tokenDict[data[2]]['POTW'].append(main.POTW.model.flastSerialNo - 1)
        else:
            main.tokenDict[data[2]] = {}
            main.tokenDict[data[2]]['POTW'] = [main.POTW.model.flastSerialNo - 1]
            main.tokenDict[data[2]]['POCW'] = []

    ind = main.POTW.model.index(0, 0)
    ind1 = main.POTW.model.index(0, 1)
    main.POTW.model.dataChanged.emit(ind, ind1)

    # main.POTW.smodel.setClientCode(UserID)
    # main.POTW.smodel.setFilterFixedString(UserID)

    # main.POTW.le_text.setText(UserID)

    # main.TWSWM.smodel.setClientCode(UserID)
    # main.TWSWM.smodel.setFilterFixedString(UserID)


def UserIDfilterPOCW(main):


    clientcode=main.POCW.le_text.text()
    # main.cFrame.DPOTW.show()
    # main.cFrame.DPOTW.raise_()

    temp = np.zeros_like(main.POCW.FilterTable[0:main.POCW.model.flastSerialNo, :])

    main.POCW.FilterTable[0:main.POCW.model.flastSerialNo, :] = temp

    main.POCW.model.DelRows(0, main.POCW.model.flastSerialNo)

    # main.OrderBook.modelO.DelRows()
    main.POCW.model.flastSerialNo = 0
    main.POCW.model.rowCount()
    ind = main.POCW.model.index(0, 0)
    ind1 = main.POCW.model.index(0, 1)
    main.POCW.model.dataChanged.emit(ind, ind1)
    # st=time.time()
    fltr = main.POCW.table[np.where(main.POCW.table[:main.POCW.lastSerialNo, 0] == clientcode)]

    for i in main.tokenDict:
        main.tokenDict[i]['POCW'] = []
    for data in fltr:
        main.POCW.FilterTable[main.POCW.model.flastSerialNo, :] = [data[0], data[1], data[2], data[3], data[4], data[5],
                                                                   data[6],
                                                                   data[7], data[8], data[9], data[10], data[11],
                                                                  data[12], data[13], data[14], data[15],
                                                                   data[16], data[17], data[18], data[19], data[20],
                                                                   data[21],
                                                                   data[22], data[23], data[24], data[25],data[26],data[27],
                                                                   data[28], data[29],
                                                                   data[30]]

        main.POCW.model.flastSerialNo += 1
        main.POCW.model.insertRows()
        main.POCW.model.rowCount()

        if main.tokenDict.get(data[2]):
            main.tokenDict[data[2]]['POCW'].append(main.POCW.model.flastSerialNo - 1)
        else:
            main.tokenDict[data[2]] = {}
            main.tokenDict[data[2]]['POCW'] = [main.POCW.model.flastSerialNo - 1]
            main.tokenDict[data[2]]['POTW'] = []

    ind = main.POCW.model.index(0, 0)
    ind1 = main.POCW.model.index(0, 1)
    main.POCW.model.dataChanged.emit(ind, ind1)

    # main.POTW.smodel.setClientCode(UserID)
    # main.POTW.smodel.setFilterFixedString(UserID)

    # main.POTW.le_text.setText(UserID)

    # main.TWSWM.smodel.setClientCode(UserID)
    # main.TWSWM.smodel.setFilterFixedString(UserID)
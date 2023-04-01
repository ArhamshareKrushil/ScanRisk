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
                        format='%(asctime)s    %(levelname)s    %(module)s  %(funcName)s   %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')


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
    main.Depositarray = pd.read_csv(path1).to_numpy()
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
    main.Limitarray = pd.read_csv(path1).to_numpy()
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

@pyqtSlot(list)
def updatePOTW(main,data):


    # print(data,data[0],data[2])
    try:

        fltrarr1 = main.POTW.table[np.where((main.POTW.table[:main.POTW.model.lastSerialNo, 0] == data[0]) & (
                main.POTW.table[:main.POTW.model.lastSerialNo, 2] == data[2]))]

        if (fltrarr1.size != 0):
            # print('update')
            #     isRecordExist=True
            #
            # if(isRecordExist):
            #     # print('exist')

            SerialNo = fltrarr1[0][12]



            editList = [8, 9, 15, 16, 20, 23,33]
            main.POTW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],data[29]]

            for i in editList:
                ind = main.POTW.model.index(SerialNo, i)
                main.POTW.model.dataChanged.emit(ind, ind)



        else:

            main.POTW.table[main.POTW.model.lastSerialNo] = [data[0],
                                                             data[1], data[2], data[3], data[4], data[5],
                                                            data[6], data[7], data[8], data[9],data[10],
                                                             data[11], main.POTW.model.lastSerialNo,data[13], data[14],data[15],
                                                             data[16], data[17], data[18],data[19], data[20],
                                                       data[21],data[22], data[23],data[24],data[25],
                                                             data[26],data[27],data[28],0.0,0.0,
                                                             0.0,0.0,data[29]]

            # main.POTW.table[main.POTW.model.lastSerialNo, :] = data

            main.POTW.lastSerialNo += 1
            main.POTW.model.lastSerialNo += 1
            main.POTW.model.insertRows()
            main.POTW.model.rowCount()
            ind = main.POTW.model.index(0, 0)
            ind1 = main.POTW.model.index(0, 1)
            main.POTW.model.dataChanged.emit(ind, ind1)

            Ftoken = main.fo_contract[data[2] - 35000, 17]
            main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
            main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)
    except:
        print(traceback.print_exc(), len(data))

    # print('ppp', main.POTW.lastSerialNo)



    # main.isPOTWupdated = True

    # if UserID not in main.POTW.clientList:
    #     main.POTW.clientList.append(UserID)


def updatePOTWopenPosition(main,data):
    try:
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

            editList = [8, 9, 15, 16, 20, 23,33]
            main.POTW.table[SerialNo, editList] = [data[8], data[9], data[15], data[16], data[20], data[23],data[29]]

            for i in editList:
                ind = main.POTW.model.index(SerialNo, i)
                main.POTW.model.dataChanged.emit(ind, ind)



        else:

            main.POTW.table[main.POTW.model.lastSerialNo] = [data[0], data[1], data[2], data[3], data[4], data[5],
                                                   data[6], data[7], data[8], data[9],data[10],data[11], main.POTW.model.lastSerialNo,
                                                   data[13], data[14],
                                                   data[15], data[16], data[17], data[18],
                                                   data[19], data[20],data[21],data[22] ,data[23],data[24],data[25],data[26],data[27],data[28],0.0,0.0,0.0,0.0,data[29]]

            # main.POTW.table[main.POTW.model.lastSerialNo, :] = data

            main.POTW.lastSerialNo += 1
            main.POTW.model.lastSerialNo += 1
            main.POTW.model.insertRows()
            main.POTW.model.rowCount()
            ind = main.POTW.model.index(0, 0)
            ind1 = main.POTW.model.index(0, 1)
            main.POTW.model.dataChanged.emit(ind, ind1)

            Ftoken = main.fo_contract[data[2] - 35000, 17]
            main.Reciever.subscribedlist('POTW', 'NSEFO', data[2])
            main.Reciever.subscribedlist('POTW', 'NSEFO', Ftoken)
    except:
        pass
        # print(traceback.print_exc(),main.fo_contract.size,data[2])

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

        limitarr=main.Limit.table[np.where(main.Limit.table[:main.Limit.model.lastSerialNo,0]==data[0])]
        if limitarr.size!=0:
            LIMIT = limitarr[0][1]
        else:
            # print('mmmm',data[0],main.Limit.table[:main.Limit.lastSerialNo,0])
            LIMIT=0.0

        depositarr = main.Deposit.table[np.where(main.Deposit.table[:main.Deposit.model.lastSerialNo, 0] == data[0])]
        if depositarr.size!=0:
            Deposit = depositarr[0][1]
        else:
            Deposit=0.0

        if(LIMIT >0):
            if data[13]>LIMIT:
                AccessMRGuti = data[13] / LIMIT * 100.0
            else:
                AccessMRGuti=0.0
        else:
            AccessMRGuti = 0.0

        fltr=main.CMTWM.table[np.where(main.CMTWM.table[:main.CMTWM.lastSerialNo,0]==data[0])]
        if fltr.size!=0:
            CashMRG=fltr[0][3]
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
            if x.size != 0:
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


def updateLTP_CMPOTW(main,data):
    try:
        if (main.CMPOTW.model.lastSerialNo != 0):
            # print('ddd')
            #print("1")
            # x = (np.unique(main.CMPOTW.table[:main.CMPOTW.lastSerialNo, 2]))


            # if (data['Token'] in x ):
             #   print("2")
            fltr = np.asarray([data['Token']])
            x = main.CMPOTW.table[np.in1d(main.CMPOTW.table[:, 2], fltr), 9]
            # print(x)

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

    except:

        print(traceback.print_exc())

def update_CASH_MTM(main):
    # print('timer')
    Tmtm=dt.Frame(main.CMPOTW.table[:main.CMPOTW.model.lastSerialNo,[0,8,15]],names=['Uid','MTM','TOC'])

    Tmtm[1:] = dt.float64

    x = Tmtm[:, dt.sum(dt.f[1:]), dt.by('Uid')].to_numpy()

    for i in x:


        if (main.TWM.model.lastSerialNo !=0) :

            rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == i[0])[0]
            if (rowarray.size != 0):
                rowNo = rowarray[0]

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
            rowarray = np.where(main.CMTWM.table[:main.CMTWM.model.lastSerialNo, 0] == i[0])[0]
            if (rowarray.size != 0):
                rowNo = rowarray[0]

                editList = [4]
                main.CMTWM.table[rowNo, editList] = [i[1]]

                for t in editList:
                    ind = main.CMTWM.model.index(rowNo, t)
                    main.CMTWM.model.dataChanged.emit(ind, ind)



def updateGlobalMargin(main):

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


def updateFOMTM(main):
    if main.POTW.lastSerialNo!=0:


        df3 = dt.Frame(main.POTW.table[:main.POTW.model.lastSerialNo,
                       [0,4,11,21,22,25,26,27,28,31,32,33]],
                       names=['UserID', 'Symbol', 'MTM','FUT_MTM','OPT_MTM','Delta',
                      'Theta','Gama','Vega','UpSCNMTM','DownSCNMTM','TOC'])

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

                editList = [5, 6, 7,10,11,12,13,14,15,16]
                main.TWSWM.table[rowNo, editList] = [i[3], i[4], i[2],i[5], i[6], i[7],i[8], i[9], i[10],i[11]]

                for t in editList:
                    ind = main.TWSWM.model.index(rowNo, t)
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


def updateCMTWM(main,data):
    rowarray = np.where(main.CMTWM.table[:main.CMTWM.model.lastSerialNo, 0] == data[0])[0]
    # print(fltrarr)

    # if (fltrarr.size != 0):
    #         isRecordExist = True

    if (rowarray.size != 0):
        # print('exist')

        # rowNo = np.where(main.CMTWM.table[:, 0] == data[0])[0][0]
        rowNo = rowarray[0]
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

    rowarray = np.where(main.TWM.table[:main.TWM.model.lastSerialNo, 0] == data[0])[0]
    if rowarray.size!=0:
        rowNo=rowarray[0]
        d=main.TWM.table[rowNo,:]
        netmrg=d[13]+data[3]

        editList = [13, 18, 25]
        main.TWM.table[rowNo, editList] = [netmrg, data[7],data[3]]

        for i in editList:
            ind = main.TWM.model.index(rowNo, i)
            main.TWM.model.dataChanged.emit(ind, ind)


    # main.TWM.table[np.where(main.TWM.table[:main.TWM.lastSerialNo,0]==data[0]),[18,25]]=[data[7],data[3]]





def updateSCNPrice(main):
    if main.POTW.lastSerialNo != 0:

        Tokens = np.unique(main.POTW.table[:main.POTW.lastSerialNo, 2])

        for i in Tokens:
            fltr = np.asarray([i])
            x = main.POTW.table[np.in1d(main.POTW.table[:, 2], fltr)]

            Data = main.POTW.table[x[0][12], :]

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

                    for i in x:
                        editableList = [29,30,31,32]

                        UPscnMTM= (i[15] * UPscnPrice) + i[16]
                        DownscnMTM=(i[15] * DOWNscnPrice1) + i[16]


                        main.POTW.table[i[12], editableList] = [UPscnPrice, DOWNscnPrice1,UPscnMTM,DownscnMTM ]
                        ind = main.POTW.model.index(0, 0)
                        ind1 = main.POTW.model.index(0, 1)
                        main.POTW.model.dataChanged.emit(ind, ind1)


def update_Greek_SCNMTM(main):
    pass









def update_Greeks_POTW(main):
    if main.POTW.lastSerialNo != 0:

        Tokens = np.unique(main.POTW.table[:main.POTW.lastSerialNo, 2])

        for i in Tokens:
            fltr = np.asarray([i])
            x = main.POTW.table[np.in1d(main.POTW.table[:, 2], fltr)]

            Data = main.POTW.table[x[0][12], :]

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

                        for i in x:
                            editableList = [24, 25, 26, 27, 28]
                            main.POTW.table[i[12], editableList] = [imp_v * 100, delt*i[15], tht*i[15], gm*i[15], vg*i[15]]
                            ind = main.POTW.model.index(0, 0)
                            ind1 = main.POTW.model.index(0, 1)
                            main.POTW.model.dataChanged.emit(ind, ind1)

                    except:
                        print(traceback.print_exc(), optionType, type(fPrice), type(strikeP), type(ltp), optionType, t,
                              main.r, imp_v, fPrice, strikeP)

                else:
                    for i in x:
                        editableList = [25]
                        main.POTW.table[i[12], editableList] = [i[15]]
                        ind = main.POTW.model.index(0, 0)
                        ind1 = main.POTW.model.index(0, 1)
                        main.POTW.model.dataChanged.emit(ind, ind1)


def update_contract_fo(main,data):
    # print('data1',data)
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

def TWMdoubleClicked(main):
    UserID = main.TWM.tableView.selectedIndexes()[0].data()

    main.cFrame.DPOTW.show()
    main.cFrame.DPOTW.raise_()

    main.POTW.smodel.setClientCode(UserID)
    main.POTW.smodel.setFilterFixedString(UserID)

    main.POTW.le_text.setText(UserID)

    main.TWSWM.smodel.setClientCode(UserID)
    main.TWSWM.smodel.setFilterFixedString(UserID)





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
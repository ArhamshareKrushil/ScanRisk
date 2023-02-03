import time
import datatable as dt
import logging
import sys
import threading
import linecache
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




def populateData(bod):
    bod.MDheaders, bod.IAheaders, bod.MDtoken, bod.IAToken, bod.URL, bod.userID, bod.Source, \
    bod.MDKey, bod.MDSecret, bod.IAKey, bod.IASecret, bod.clist, bod.DClient, bod.broadcastMode = readConfig_All()

    bod.lb_md_appKey.setText(bod.MDKey)
    bod.lb_md_secretKey.setText(bod.MDSecret)
    
    
def exp123(a):
    b=datetime.datetime.strptime(a,'%d-%b-%Y').strftime('%Y%m%d')
    return b


def getcalSprd(bod):
    Ymd_today = datetime.datetime.today().strftime("%Y%m%d")

    loc1 = os.getcwd().split('Application')

    path = os.path.join(loc1[0], 'Downloads', 'SPAN', Ymd_today,'calspred.csv')

    # path = r'D:\scanRisk\Downloads\SPAN'+'\/'+ Ymd_today +'\calspred.csv'

    my_data = dt.fread(path).to_numpy()
    my_data = my_data[:, 1:3]
    my_data1 = my_data.astype('U20')
    v, r = np.unique(my_data1, return_counts=True, axis=0)
    newData = v[np.where(r != 1)]
    bod.calSprd = np.zeros((newData.shape[0], 4), dtype=object)
    bod.calSprd[:, 0] = newData[:, 0].astype('f4')
    bod.calSprd[:, 1] = newData[:, 1]

    fltr = bod.fo_contract[np.in1d(bod.fo_contract[:, 5], ['FUTSTK', 'FUTIDX'])]
    fltr1 = fltr[np.in1d(fltr[:, 37], [4, 5])]

    for i in fltr1:

        SYMBOL = i[3]
        TOKEN = i[2]
        ael = bod.AelMargin[TOKEN - 35000, 5]
        # fprice = bod.fo_contract[TOKEN - 35000, 18]
        futureToken = bod.fo_contract[TOKEN - 35000, 9] #assetToken
        try:
            fprice = bod.eq_contract[int(futureToken) - 36970, 18]  #cashPrice
            bod.calSprd[np.where(bod.calSprd[:, 1] == SYMBOL), 3] = fprice

        except:
            print('Token',TOKEN)

        bod.calSprd[np.where(bod.calSprd[:, 1] == SYMBOL), 2] = ael


    # print(bod.calSprd)

def uploadAelSpc(bod):
    try:
        path = bod.le_aelS.text()

        tab123 = pd.read_csv(path, names=['ins', 'symbol', 'exp', 'strike', 'opt', 'a', 'ael'])
        tab123['exp'] = tab123['exp'].apply(exp123)
        #         print(tab123[tab123['ins'] =='OPTIDX'])
        contract = pd.DataFrame(bod.fo_contract[:, [2, 5, 3, 6, 7, 8, 12]],
                                columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])
        #         span1.iloc[:, 4] = span1.iloc[:, 4].fillna(' ')
        #         span1.iloc[:, 3] = span1.iloc[:, 3].fillna(0.0)
        tab123.iloc[:, 2] = tab123.iloc[:, 2].astype(str)

        aelMargin9 = pd.merge(contract, tab123, how='inner', left_on=['symbol', 'exp', 'strk1', 'opt'],
                              right_on=['symbol', 'exp', 'strike', 'opt']).to_numpy()

        for i in aelMargin9:
            #             print(i)
            bod.AelMargin[i[0] - 35000, 5] = i[10]

        # np.savetxt("d:/finalael.csv", bod.AelMargin, delimiter=",", fmt='%s')

        getcalSprd(bod)


    except:
        print(traceback.print_exc())
        

def openAELGen(bod):
    try:

        a = datetime.datetime.today()
        try:
            prvdate=bod.prevDate.strftime('%d%m%Y')
        except:
            prvdate = '22092022'

        defaultDir = os.path.join(r"\\192.168.102.204\ba\FNO", prvdate)
        fname = QFileDialog.getOpenFileName(bod, 'Open file', defaultDir)[0]
        bod.le_aelG.setText(fname)
    except:
        print(traceback.print_exc())

def openAELSpc(bod):
    try:

        # a = datetime.datetime.today()

        try:
            prvdate=bod.prevDate.strftime('%d%m%Y')
        except:
            prvdate = '22092022'

        defaultDir = os.path.join(r"\\192.168.102.204\ba\FNO", prvdate)
        fname = QFileDialog.getOpenFileName(bod, 'Open file', defaultDir)[0]
        bod.le_aelS.setText(fname)
    except:
        print(traceback.print_exc())

def openpos(bod):
    # loc1 = os.getcwd().split('Uploads')
    defaultDir = r'\\192.168.102.59\close\REPORTS\focaps\46'
    fname = QFileDialog.getOpenFileName(bod, 'Open file', defaultDir)[0]
    bod.leOpenpos.setText(fname)

def openPOTM(bod):
    try:
        # loc1 = os.getcwd().split('Uploads')

        # print('asdg')
        defaultDir = r'\\192.168.102.204\ba\FNO\20092022'
        fname = QFileDialog.getOpenFileName(bod, 'Open file', defaultDir)[0]
        bod.lePOTM.setText(fname)
    except:
        print(traceback.print_exc())


def openSheet(bod):
    try:
        # loc1 = os.getcwd().split('Uploads')

        # print('asdg')
        defaultDir = r'\\192.168.102.59\close\Reports\focaps\890\expiry/all'
        fname = QFileDialog.getOpenFileName(bod, 'Open file', defaultDir)[0]
        bod.leSheet.setText(fname)
    except:
        print(traceback.print_exc())

def openLedger(bod):
    try:
        # loc1 = os.getcwd().split('Uploads')

        # print('asdg')
        defaultDir = r'\\192.168.102.204\ba\FNO\20092022'
        fname = QFileDialog.getOpenFileName(bod, 'Open file', defaultDir)[0]
        bod.leSheet.setText(fname)
    except:
        print(traceback.print_exc())

def uploadLedger(bod):
    pass

def openNotisFo(bod):
    try:
        # loc1 = os.getcwd().split('Uploads')
        # print('asdg')
        today=datetime.datetime.today().strftime('%Y%m%d')
        defaultDir = r'\\192.168.102.222\Shared\OnlineTrades\%s'%(today)
        fname = QFileDialog.getOpenFileName(bod, 'Open file', defaultDir)[0]
        bod.leNfo.setText(fname)
    except:
        print(traceback.print_exc())




def RestartNotisFo(bod):
    for i in bod.ClientOPoss:
        bod.sgPOTM.emit(i)



def getbse2nse(bod):
    loc = os.getcwd().split('Application')[0]
    path = os.path.join(loc,'Uploads','PS03','bse2nseSymbols.csv')


    # path = r'D:\scanRisk\Uploads\PS03\bse2nseSymbols.csv'
    bod.nse2bse = {}
    with open(path, 'r') as f:
        c = csv.reader(f)
        for i in c:
            bod.nse2bse[i[0]] = i[1]
    f.close()
    # print(bod.nse2bse)





def uploadPOTM(bod):
    try:
        path = bod.lePOTM.text()
        # loc1 = os.getcwd().split('Application')
        # path = os.path.join(loc1[0], 'Downloads', 'POTM', 'POTM.csv')
        POTM1 = pd.read_csv(path)
        POTM2 = POTM1.iloc[:,[0,7,10,11,12,13,16,18,20,22,34]]

        POTM2.columns = ['Date','ClientCode','symbol','exp','strk','opt','bfLong','bfShort','dayBq','daySQ','SettlementP']
        bod.ClientOPoss = updatePOTM(bod,POTM2)

        today = datetime.datetime.today()
        today1 = today.strftime('%Y%m%d')
        today2 = datetime.datetime.strptime(today1, '%Y%m%d')

        for i in bod.ClientOPoss:

            dt=datetime.datetime.strptime(i[3],'%Y%m%d')
            # print(dt)

            # print(today2,dt)

            if(dt < today2):
                pass
            else:
                bod.sgPOTM.emit(i)


        bod.sgPOTMupdated.emit()


    except:

        print(traceback.print_exc())

def updatePOTMexp(exp):
    exp1 = datetime.datetime.strptime(exp,'%d %b %Y').strftime('%Y%m%d')
    return exp1


def updatePOTM(bod,POTM):




    POTM['symbol'] = POTM['symbol'].apply(bod.updateb2nSymbol)
    POTM['NetQ'] = POTM['bfLong'] - POTM['bfShort'] + POTM['dayBq'] - POTM['daySQ']
    POTM['exp'] = POTM['exp'].apply(updatePOTMexp)
    POTM['opt'] = POTM['opt'].fillna(' ')
    # POTM['strk'] = POTM['strk'].astype('str')
    # POTM['strk'] = POTM['strk'].replace('0.0',' ')
    tempContract = pd.DataFrame(bod.fo_contract[:, [2, 5, 3, 6, 7, 8, 12]],
                                columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])


    POTM1 = pd.merge(POTM, tempContract, how='left', left_on=['symbol', 'exp', 'strk', 'opt'],
                        right_on=['symbol', 'exp', 'strk1', 'opt'])

    # print(POTM1)
    POTM1.to_csv('ooo.csv')
    return POTM1.to_numpy()



#
# def updateb2nSymbol(sym,bod):
#     sym1 = bod.nse2bse[sym]
#     return sym1
def uploadOpenpos(bod):
    try:
        inPath=bod.leOpenpos.text()

        loc1 = os.getcwd().split('Application')
        outPath = os.path.join(loc1[0], 'Uploads', 'OpenPosition', 'openPos.csv')
        # outPath = r'D:\scanRisk\Uploads\OpenPosition\openPos.csv'
        with open(outPath,'w+') as sp:
            with open(inPath,'r') as f:
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
                        # print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %((fn,row[0], it, sym, exp, spr, ot, ada, row[2], row[3], row[5], row[6], row[7])))
                        if (sym == 'LTI'):
                            # print(row[12],row)
                            sym= 'LTIM'
                        #
                        # elif(sym == 'PETRONET' and it=='OPTSTK'):
                        #     spr = float(spr) - 4.85


                        sp.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ((
                            row[0], it, sym, exp, spr, ot, ada, row[2], row[3], row[4], row[5], row[6], row[7],
                            row[8])))
            f.close()
        sp.close()
        # tempPos = pd.read_csv(outPath,columns = ['CLIENT_ID','Scrip','Net Qty','Cl.Price','Cl.Amt','Exposure Mrg','Span_Mrg','Total_Margin','% Margin','x'])
        tempPos = pd.read_csv(outPath,names = ['CLIENT_ID','ins', 'symbol', 'exp', 'strk', 'opt','StockName','NetQty','ClPrice','ClAmt','Exposure_Mrg','Span_Mrg','Total_Margin','%_Margin'])
        tempContract = pd.DataFrame(bod.fo_contract[:, [2, 5, 3, 6, 7, 8, 12,18]],
                                    columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1','close'])
        tempPos.iloc[:, 4] = tempPos.iloc[:,4].astype('str')
        tempPos.iloc[:, 3] = tempPos.iloc[:,3].astype('str')

        # tempContract.iloc[:,0]
        # print(tempContract.head(2).to_numpy())
        # print(tempPos['symbol'].head(2).to_numpy())

        tempPos1 = pd.merge(tempPos,tempContract, how='left', left_on=['symbol','exp','strk','opt'], right_on = ['symbol','exp','strk','opt']).to_csv('ppp.csv')
        tempPos12 = pd.merge(tempPos,tempContract, how='left', left_on=['symbol','exp','strk','opt'], right_on = ['symbol','exp','strk','opt']).to_numpy()

        for i in tempPos12:
            bod.sgPOTWopen.emit(i)

        bod.sgPOTWOpenposupdated.emit()

    except:
        print(traceback.print_exc())

def uploadSheet(bod):
    path = bod.leSheet.text()
    # sheet=pd.read_csv(path,skiprows=2)

    sheet=dt.fread(path)

    sheet1=sheet[3:,[0,7]]

    sheet1[1]=dt.float64
    bod.sheet=sheet1[:,dt.sum(dt.f[1]),dt.by(dt.f[0])].to_numpy()

    # print(bod.sheet)


    finalsheet=sheet[dt.f[1]=='CAPITAL',:].to_numpy()

    tmp=np.zeros((finalsheet.shape[0],3))
    finalsheet=np.hstack((finalsheet,tmp))



    # bod.prevDate=datetime.datetime.strftime(bod.prevDate,'%d%m%Y')
    # path1=r'\\192.168.102.204\ba\CMPOTW\%s\BSE_Scrip_Series_Mapping_29112022.csv'%(bod.prevDate)
    # bsescript=dt.fread(path1).to_numpy()
    EQmaster=bod.eq_contract[np.in1d(bod.eq_contract[:,6],['BE','BZ','E1','EQ','IT','SM','ST'])]
    # print(EQmaster)

    for i in finalsheet:
        # print(i[2])
        symbol=i[2].split(' ')[0]
        # print(symbol)

        # data=bsescript[np.where(bsescript[:,1]==scrcode)][0]
        # symbol=data[4]
        # series=data[5]
        try:

            data=EQmaster[np.where(EQmaster[:,3]==symbol)][0]
            token = data[2]
            series= data[6]
            i[16] = symbol
            i[17] =  series
            i[18]=token
            # print('tt', symbol, token,series)
        except:
            print('sym',symbol)


    finalsheet=finalsheet[np.where(finalsheet[:,18]!=0.0)]
    print(finalsheet)

    for i in finalsheet:
        bod.sgCMPOTWopenpos.emit(i)

    bod.sgCMPOTWopenposupdated.emit()

    bod.isCMOpenPosupdated=True























def uploadAelGen(bod):
    try:

        path=bod.le_aelG.text()
        AelMargin = bod.fo_contract[:,[0,1,2,3,41]]

        bdf = np.zeros((AelMargin.shape[0], 5))
        bod.AelMargin = np.hstack([AelMargin, bdf])

        ael_for_index_OTM = 3
        ael_for_index_OTH = 2
        indexDict = ["BANKNIFTY", "NIFTY", "FINNIFTY", "MIDCPNIFTY"]

        path1 = os.path.join(loc1[0], 'Downloads','expoM','aelGen.csv')





        with open(path, 'r') as f1:
            with open(path1, 'w+') as f:
                reader = csv.reader(f1, lineterminator="\n")
                writer = csv.writer(f, lineterminator="\n")



                for j, row in enumerate(reader):
                    writer.writerow(row)
                # writer.writerow('\n')
            f.close()
        f1.close()



        with open(path1, 'a+') as f:
            for i in indexDict:
                f.write("1,%s,OTH,%s,0,%s\n2,%s,OTM,%s,0,%s\n" % (i, ael_for_index_OTH, ael_for_index_OTH, i, ael_for_index_OTM, ael_for_index_OTM))
            # print("done adding NBFM data.............................")
        f.close()
        # f1.close()

        with open(path1) as f:
            c=csv.reader(f)

            for j,i in enumerate(c):
                if(j>1):
                    # print(i)
                    symbol=i[1]
                    # print(symbol)
                    moneyness = i[2]
                    rate = float(i[5])



                    if(i[2]=='OTH'):
                        # print(symbol,moneyness,rate)
                        fltr = bod.fo_contract[np.in1d(bod.fo_contract[:,3],[symbol])]
                        tokenList= fltr[np.where(fltr[:,41]==2),2][0]
                        tokenList1 = np.subtract(tokenList, 35000).tolist()

                        tokenList2 = fltr[np.where(fltr[:, 41] == 0), 2][0]
                        tokenList21 = np.subtract(tokenList2, 35000).tolist()
                        bod.AelMargin[tokenList21, 5] = rate


                    elif(i[2]=='OTM'):
                        print(symbol,moneyness,rate)
                        fltr = bod.fo_contract[np.in1d(bod.fo_contract[:,3],[symbol])]
                        tokenList= fltr[np.where(fltr[:,41]==1),2][0]
                        tokenList1 = np.subtract(tokenList, 35000).tolist()

                    bod.AelMargin[tokenList1, 5] =rate

        f.close()

    except:
        print(traceback.print_exc())

def Marketdatashow(bod):
    bod.fTSettings.hide()
    bod.fUploads.hide()
    bod.fDwlds.hide()
    bod.fPeak.hide()
    bod.fMasters.show()

def Downloadsshow(bod):
    try:

        bod.fTSettings.hide()
        bod.fUploads.hide()
        bod.fDwlds.show()
        bod.fPeak.hide()
        bod.fMasters.hide()

        Ymd_today = datetime.datetime.today().strftime("%Y%m%d")

        loc1 = os.getcwd().split('Application')
        downloadLoc = os.path.join(loc1[0], 'Downloads', 'SPAN', Ymd_today)


        if (os.path.exists(downloadLoc)):
            bod.pbSpanProcess.setEnabled(True)

        Ymd_today = datetime.datetime.today().strftime("%d%m%Y")
        downloadLoc1 = os.path.join(loc1[0], 'Downloads', 'VAR', Ymd_today)
        if (os.path.exists(downloadLoc1)):
            bod.pbVarProcess.setEnabled(True)

    except:
        print(traceback.print_exc())

def Peaksshow(bod):
    try:
        print('PeakShow')
        bod.fTSettings.hide()
        bod.fUploads.hide()
        bod.fDwlds.hide()
        bod.fPeak.show()
        bod.fMasters.hide()
    except:
        print(traceback.print_exc())

def Tsettingsshow(bod):
    bod.fTSettings.show()
    bod.fUploads.hide()
    bod.fDwlds.hide()
    bod.fPeak.hide()
    bod.fMasters.hide()



def Uploadssshow(bod):
    bod.fTSettings.hide()
    bod.fUploads.show()
    bod.fDwlds.hide()
    bod.fPeak.hide()
    bod.fMasters.hide()

def showDefaultFrame(bod):
    bod.fTSettings.hide()
    bod.fUploads.hide()
    bod.fDwlds.hide()
    bod.fPeak.hide()
    bod.fTSettings.hide()

    bod.setMaximumWidth(800)

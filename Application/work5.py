####################################### Get Master ######################################

import pyarrow as pa

import pandas as pd
import numpy as np
import time
import os
import datetime

global nse2bse
nse2bse = {}


def getMaster():
    # contract_df = pd.read_csv(contractDir,low_memory=False,)
    file_contract_fo = r'D:\scanRisk\Application\Masters\contract_fo.csv'
    file_contract_eq = r'D:\scanRisk\Application\Masters\contract_eq.csv'
    file_contract_cd = r'D:\scanRisk\Application\Masters\contract_cd.csv'

    contract_fo = pd.read_csv(file_contract_fo, low_memory=False, header=None).to_numpy()
    nan_array = np.where(contract_fo[:, 1] == 'x')
    non_nan_array = np.where(contract_fo[:, 1] != 'x')
    contract_fo[nan_array, 6] = ''

    contract_fo[non_nan_array, 6] = contract_fo[non_nan_array, 6].astype('int')
    contract_fo[non_nan_array, 6] = contract_fo[non_nan_array, 6].astype('str')

    contract_eq = pd.read_csv(file_contract_eq, low_memory=False, header=None).to_numpy()
    contract_cd = pd.read_csv(file_contract_cd, low_memory=False, header=None).to_numpy()

    # contract_dt = dt.Frame(contract_df)
    # contract_full = contract_dt.to_numpy()
    heads = ['Exchange',
             'Segment', 'Token', 'symbol', 'Stock_name', 'instrument_type',
             'exp', 'strike_price', 'option_type', 'asset_token', 'tick_size',
             'lot_size', 'strike1', 'Multiplier', 'FreezeQty', 'pbHigh',  # pb priceband
             'pbLow', 'futureToken', 'close', 'ltp', 'bid',
             'ask', 'oi', 'prev_day_oi', 'iv', 'delta',
             'gamma', 'theta', 'vega', 'theoritical_price', 'PPR',
             'moneyness', 'Volume', 'amt', 'Avg1MVol', 'ATP',
             'strike_diff', 'expiry_type', 'cpToken', 'days2Exp', 'moneyness',
             '41', '42', '43'
             ]

    ############ option chain master #########################
    return contract_fo, contract_eq, contract_cd, heads


contract_fo, contract_eq, contract_cd, heads = getMaster()



#################################### span parse #########################################
downloadLoc=r'D:\scanRisk\Downloads\SPAN'

rrr = time.time()

spanFile = os.path.join(downloadLoc, 'span.csv')
span1 = pd.read_csv(spanFile,
                    names=['ins', 'symbol', 'exp', 'strk', 'opt', 'close', 's1', 's2', 's3', 's4', 's5', 's6',
                           's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 'delta'])

contract = pd.DataFrame(contract_fo[:, [2, 5, 3, 6, 7, 8, 12]],
                        columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])
span1.iloc[:, 4] = span1.iloc[:, 4].fillna(' ')
span1.iloc[:, 3] = span1.iloc[:, 3].fillna(0.0)
span1.iloc[:, 2] = span1.iloc[:, 2].astype(str)

spanMargin = pd.merge(contract, span1, how='left', left_on=['symbol', 'exp', 'strk1', 'opt'],
             right_on=['symbol', 'exp', 'strk', 'opt']).to_numpy()
print(spanMargin)

import csv
import traceback

global AelMargin
AelMargin = contract_fo[:, [0, 1, 2, 3, 41]]


bdf = np.zeros((AelMargin.shape[0], 5))
AelMargin = np.hstack([AelMargin, bdf])


def uploadAelGen():
    try:

        #         path=bod.le_aelG.text()
        path = r'\\192.168.102.204\ba\FNO\10102022\ael_11102022.csv'

        ael_for_index_OTM = 2
        ael_for_index_OTH = 1.5
        indexDict = ["BANKNIFTY", "NIFTY", "FINNIFTY", "MIDCPNIFTY"]

        with open(path, 'a+') as f:
            for i in indexDict:
                f.write("1,%s,OTH,%s,0,%s\n2,%s,OTM,%s,0,%s\n" % (
                    i, ael_for_index_OTH, ael_for_index_OTH, i, ael_for_index_OTM, ael_for_index_OTM))
            print("done adding NBFM data.............................")
        f.close()

        with open(path) as f:
            c = csv.reader(f)

            for j, i in enumerate(c):
                if (j > 1):
                    # print(i)
                    symbol = i[1]
                    moneyness = i[2]
                    rate = float(i[5])

                    if (i[2] == 'OTH'):
                        #                         print(symbol,moneyness,rate)
                        fltr = contract_fo[np.in1d(contract_fo[:, 3], [symbol])]
                        tokenList = fltr[np.where(fltr[:, 41] == 2), 2][0]
                        tokenList1 = np.subtract(tokenList, 35000).tolist()

                        tokenList2 = fltr[np.where(fltr[:, 41] == 0), 2][0]
                        tokenList21 = np.subtract(tokenList2, 35000).tolist()
                        AelMargin[tokenList21, 5] = rate



                    elif (i[2] == 'OTM'):
                        #                         print(symbol,moneyness,rate)
                        fltr = contract_fo[np.in1d(contract_fo[:, 3], [symbol])]
                        tokenList = fltr[np.where(fltr[:, 41] == 1), 2][0]
                        tokenList1 = np.subtract(tokenList, 35000).tolist()

                    AelMargin[tokenList1, 5] = rate

        f.close()

    except:
        print(traceback.print_exc())

    print(AelMargin.shape)


uploadAelGen()
# for i in AelMargin:
#     print(i)


def exp123(a):
    b = datetime.datetime.strptime(a, '%d-%b-%Y').strftime('%Y%m%d')
    return b


def uploadAelSpc():
    try:
        #         path = bod.le_aelS.text()
        path = r'\\192.168.102.204\ba\FNO\10102022\F_AEL_OTM_CONTRACTS_11102022.csv'
        tab123 = pd.read_csv(path, names=['ins', 'symbol', 'exp', 'strike', 'opt', 'a', 'ael'])
        tab123['exp'] = tab123['exp'].apply(exp123)
        #         print(tab123[tab123['ins'] =='OPTIDX'])
        contract = pd.DataFrame(contract_fo[:, [2, 5, 3, 6, 7, 8, 12]],
                                columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])
        #         span1.iloc[:, 4] = span1.iloc[:, 4].fillna(' ')
        #         span1.iloc[:, 3] = span1.iloc[:, 3].fillna(0.0)
        tab123.iloc[:, 2] = tab123.iloc[:, 2].astype(str)

        aelMargin9 = pd.merge(contract, tab123, how='inner', left_on=['symbol', 'exp', 'strk1', 'opt'],
                              right_on=['symbol', 'exp', 'strike', 'opt']).to_numpy()

        for i in aelMargin9:
            #             print(i)
            AelMargin[i[0] - 35000, 5] = i[10]


    except:
        print(traceback.print_exc())


uploadAelSpc()
# for i in AelMargin:
#     print(i)
print(AelMargin[0, :])
print(AelMargin.shape)
print('done ael')



import datatable as dt
path=r'D:\scanRisk\Downloads\SPAN\calspred.csv'

my_data= dt.fread(path).to_numpy()
my_data = my_data[:,1:3]
my_data1=my_data.astype('U20')
v,r= np.unique(my_data1,return_counts =  True, axis= 0)
newData = v[np.where(r!=1)]
calSprd = np.zeros((newData.shape[0],4),dtype =object)
calSprd[:,0] = newData[:,0].astype('f4')
calSprd[:,1] = newData[:,1]


fltr = contract_fo[np.in1d(contract_fo[:,5],['FUTSTK','FUTIDX'])]
fltr1 = fltr[np.in1d(fltr[:,37],[4,5])]

print('l333333333')
for i in fltr1:
    SYMBOL = i[3]
    TOKEN = i[2]
    ael = AelMargin[TOKEN-35000,5]
    fprice = contract_fo[TOKEN-35000,18]
    calSprd[np.where(calSprd[:,1]==SYMBOL),[2,3]] = [ael,fprice]


def getbse2nse():
    #     loc = os.getcwd().split('Application')[0]
    #     path = os.path.join(loc,'Uploads','PS03','bse2nseSymbols.csv')

    path = r'D:\scanRisk\Uploads\PS03\bse2nseSymbols.csv'
    #    nse2bse = {}
    with open(path, 'r') as f:
        c = csv.reader(f)
        for i in c:
            nse2bse[i[0]] = i[1]
    f.close()
    return nse2bse





nse2bse = getbse2nse()



def updateb2nSymbol(sym):
    try:

        sym1 = nse2bse[sym]
        #         print(sym1)
        return sym1
    except:
        symbol = 'NIFTY'
        print('error at nse2 bse con ', sym + 'abc', nse2bse)

        return symbol

def updatePOTMexp(exp):
    exp1 = datetime.datetime.strptime(exp,'%d %b %Y').strftime('%Y%m%d')
    return exp1


import datatable as dt

from datatable import *
global POCW,lastSerialNo
print('l4444444444')





# POCW=np.zeros((10000,20),dtype=object)

#         path = bod.lePOTM.text()
path=r'\\192.168.102.204\ba\FNO\10102022\POTM_6405_20221010-01.CSV'
POTM1 = pd.read_csv(path)
POTM = POTM1.iloc[:,[0,7,10,11,12,13,16,18,20,22,34]]
POTM.columns = ['Date','ClientCode','symbol','exp','strk','opt','bfLong','bfShort','dayBq','daySQ','SettlementP']


POTM['symbol'] = POTM['symbol'].apply(updateb2nSymbol)

POTM['NetQ'] = POTM['bfLong'] - POTM['bfShort'] + POTM['dayBq'] - POTM['daySQ']

POTM['exp'] = POTM['exp'].apply(updatePOTMexp)


POTM['opt'] = POTM['opt'].fillna(' ')
# POTM['strk'] = POTM['strk'].astype('str')
# POTM['strk'] = POTM['strk'].replace('0.0',' ')
tempContract = pd.DataFrame(contract_fo[:, [2, 5, 3, 6, 7, 8, 12]],
                            columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])


ClientOPoss = pd.merge(POTM, tempContract, how='left', left_on=['symbol', 'exp', 'strk', 'opt'],
                    right_on=['symbol', 'exp', 'strk1', 'opt']).to_numpy()



POCW = np.zeros((10000, 20), dtype=object)
lastSerialNo=0

for data in ClientOPoss:
    openAmt =  - data[11] *data[10]
    if(data[13] in ['OPTSTK','OPTIDX']):
        netPrem = -openAmt
    else:
        netPrem =0.0
    newRec = dt.Frame([[data[1]],
           ['NSEFO'],[data[12]],[data[13]],[data[2]],[data[3]],
                       [data[4]],[data[5]],[0],[0.0],[data[10]],
           [0.0],[lastSerialNo],[data[11]],[openAmt],[data[11]],
                                           [openAmt],[0.0],[0.0],[netPrem]]).to_numpy()



    POCW[lastSerialNo] = newRec
    lastSerialNo+=1

#########################Complete Process################

st = time.time()

spanTableCW = np.zeros((20000, 32), dtype=object)
j = 0

for i in POCW[:lastSerialNo, :]:
    if (i[5] != '20221006'):
        scn = spanMargin[i[2] - 35000, :]
        expo = AelMargin[i[2] - 35000]
        FPrice = contract_fo[i[2] - 35000, 18]
        ###################################################
        PFQ = 0
        NFQ = 0
        PCD = 0
        NCD = 0
        if (i[3] in ['OPTSTK', 'OPTIDX']):
            iexpoM = 0.0 if (i[15] > 0) else expo[5] * abs(i[15]) * FPrice
        else:
            iexpoM = expo[5] * abs(i[15]) * FPrice
            if (i[15] > 0):
                PFQ = i[15]
            else:
                NFQ = abs(i[15])
                ###################################################

        spanTableCW[j, :32] = [i[0],
                               i[2], i[15], scn[10] * i[15], scn[11] * i[15], scn[12] * i[15],
                               scn[13] * i[15], scn[14] * i[15], scn[15] * i[15], scn[16] * i[15], scn[17] * i[15],
                               scn[18] * i[15], scn[19] * i[15], scn[20] * i[15], scn[21] * i[15], scn[22] * i[15],
                               scn[23] * i[15], scn[24] * i[15], scn[25] * i[15], scn[9], iexpoM,
                               i[3], i[4], i[5], i[6], i[7],
                               i[19], scn[26] * i[15], PFQ, NFQ,
                               PCD, NCD]
        j += 1
print(spanTableCW[:20,[0,22,20]])
# df3 = dt.Frame(
#     spanTableCW[:j, [0, 22, 23, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 26, 27, 28, 29, 30, 31, 20]],
#     names=['clientcode', 'Symbol', 'exp', 'scn1', 'scn2', 'scn3', 'scn4', 'scn5', 'scn6',
#            'scn7', 'scn8', 'scn9', 'scn10', 'scn11', 'scn12', 'scn13', 'scn14', 'scn15', 'scn16', 'NetPrem', 'Cdelta',
#            'PFQ', 'NFQ', 'PCD', 'NCD', 'iexpoM'])
# df3[3:] = dt.float64
#
# x = df3[:, dt.sum(dt.f[3:]), by('clientcode', 'Symbol', 'exp')]
# x[:, dt.update(PCD=ifelse(dt.f.Cdelta > 0, dt.f.Cdelta, 0.0))]
# x[:, dt.update(NCD=ifelse(dt.f.Cdelta > 0, 0.0, -dt.f.Cdelta))]
# x1 = x[:, dt.sum(dt.f[3:]), by('clientcode', 'Symbol')]
#
# # x1
#
# x1[:, 'FSQ'] = 0.0
# x1[:, 'CDSQ'] = 0.0
# x1[:, 'spreadChrg'] = 0.0
# x1[:, 'spreadBeni'] = 0.0
# x1[:, 'maxVal'] = 0.0
# x1[:, 'spanMargin'] = 0.0
#
# x1[:, dt.update(FSQ=ifelse(dt.f.PFQ > dt.f.NFQ, dt.f.NFQ, dt.f.PFQ))]
# x1[:, dt.update(CDSQ=ifelse(dt.f.PCD > dt.f.NCD, dt.f.NCD, dt.f.PCD))]
# x1[:, dt.update(maxVal=dt.rowmax(dt.f[2:18]))]
# x1[:, dt.update(spanMargin=dt.f[29] - dt.f[18])]
# x1[:, dt.update(index=range(x1.nrows))]
#
# x2 = x1[:, [31, 0, 1, 18, 24, 25, 26, 27, 28, 29, 30]]
#
# for i in range(x2.nrows):
#
#     if (x2[i, 5] != 0 or x2[i, 6] != 0):
#         cc = x2[i, 1]
#         sym = x2[i, 2]
#
#         fsq = x2[i, 5]
#         cdsq = x2[i, 6]
#         data = calSprd[np.where(calSprd[:, 1] == sym)]
#
#         ael = data[0][2]
#         fprice = data[0][3]
#         calsc = data[0][0]
#
#         bvalue = fsq * 2 / 3 * ael * fprice
#         sprdC = cdsq * calsc
#         x2[i, dt.update(spanMargin=dt.f[10] + sprdC)]
#         x2[i, dt.update(iexpoM=dt.f[4] - bvalue)]
#
# final = x2[:, [dt.sum(dt.f[4]), dt.sum(dt.f[10])], by(dt.f[1])]
# et = time.time()
# print(et - st)
#
# print(final)







# ####################################### Get Master ######################################
#
# import pyarrow as pa
#
# import pandas as pd
# import numpy as np
# import time
# import os
# import datetime
#
# global nse2bse
# nse2bse = {}
#
#
# def getMaster():
#     # contract_df = pd.read_csv(contractDir,low_memory=False,)
#     file_contract_fo = r'D:\scanRisk\Application\Masters\contract_fo.csv'
#     file_contract_eq = r'D:\scanRisk\Application\Masters\contract_eq.csv'
#     file_contract_cd = r'D:\scanRisk\Application\Masters\contract_cd.csv'
#
#     contract_fo = pd.read_csv(file_contract_fo, low_memory=False, header=None).to_numpy()
#     nan_array = np.where(contract_fo[:, 1] == 'x')
#     non_nan_array = np.where(contract_fo[:, 1] != 'x')
#     contract_fo[nan_array, 6] = ''
#
#     contract_fo[non_nan_array, 6] = contract_fo[non_nan_array, 6].astype('int')
#     contract_fo[non_nan_array, 6] = contract_fo[non_nan_array, 6].astype('str')
#
#     contract_eq = pd.read_csv(file_contract_eq, low_memory=False, header=None).to_numpy()
#     contract_cd = pd.read_csv(file_contract_cd, low_memory=False, header=None).to_numpy()
#
#     # contract_dt = dt.Frame(contract_df)
#     # contract_full = contract_dt.to_numpy()
#     heads = ['Exchange',
#              'Segment', 'Token', 'symbol', 'Stock_name', 'instrument_type',
#              'exp', 'strike_price', 'option_type', 'asset_token', 'tick_size',
#              'lot_size', 'strike1', 'Multiplier', 'FreezeQty', 'pbHigh',  # pb priceband
#              'pbLow', 'futureToken', 'close', 'ltp', 'bid',
#              'ask', 'oi', 'prev_day_oi', 'iv', 'delta',
#              'gamma', 'theta', 'vega', 'theoritical_price', 'PPR',
#              'moneyness', 'Volume', 'amt', 'Avg1MVol', 'ATP',
#              'strike_diff', 'expiry_type', 'cpToken', 'days2Exp', 'moneyness',
#              '41', '42', '43'
#              ]
#
#     ############ option chain master #########################
#     return contract_fo, contract_eq, contract_cd, heads
#
#
# contract_fo, contract_eq, contract_cd, heads = getMaster()
#
#
#
# #################################### span parse #########################################
# downloadLoc=r'D:\scanRisk\Downloads\SPAN'
#
# rrr = time.time()
#
# spanFile = os.path.join(downloadLoc, 'span.csv')
# span1 = pd.read_csv(spanFile,
#                     names=['ins', 'symbol', 'exp', 'strk', 'opt', 'close', 's1', 's2', 's3', 's4', 's5', 's6',
#                            's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 'delta'])
#
# contract = pd.DataFrame(contract_fo[:, [2, 5, 3, 6, 7, 8, 12]],
#                         columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])
# span1.iloc[:, 4] = span1.iloc[:, 4].fillna(' ')
# span1.iloc[:, 3] = span1.iloc[:, 3].fillna(0.0)
# span1.iloc[:, 2] = span1.iloc[:, 2].astype(str)
#
# spanMargin = pd.merge(contract, span1, how='left', left_on=['symbol', 'exp', 'strk1', 'opt'],
#              right_on=['symbol', 'exp', 'strk', 'opt'])
# print(spanMargin)
#
# import csv
# import traceback
#
# global AelMargin
# AelMargin = contract_fo[:, [0, 1, 2, 3, 41]]
#
# bdf = np.zeros((AelMargin.shape[0], 5))
# AelMargin = np.hstack([AelMargin, bdf])
#
#
# def uploadAelGen():
#     try:
#
#         #         path=bod.le_aelG.text()
#         path = r'\\192.168.102.204\ba\FNO\07102022\ael_10102022.csv'
#
#         ael_for_index_OTM = 2
#         ael_for_index_OTH = 1.5
#         indexDict = ["BANKNIFTY", "NIFTY", "FINNIFTY", "MIDCPNIFTY"]
#
#         with open(path, 'a+') as f:
#             for i in indexDict:
#                 f.write("1,%s,OTH,%s,0,%s\n2,%s,OTM,%s,0,%s\n" % (
#                     i, ael_for_index_OTH, ael_for_index_OTH, i, ael_for_index_OTM, ael_for_index_OTM))
#             print("done adding NBFM data.............................")
#         f.close()
#
#         with open(path) as f:
#             c = csv.reader(f)
#
#             for j, i in enumerate(c):
#                 if (j > 1):
#                     # print(i)
#                     symbol = i[1]
#                     moneyness = i[2]
#                     rate = float(i[5])
#
#                     if (i[2] == 'OTH'):
#                         #                         print(symbol,moneyness,rate)
#                         fltr = contract_fo[np.in1d(contract_fo[:, 3], [symbol])]
#                         tokenList = fltr[np.where(fltr[:, 41] == 2), 2][0]
#                         tokenList1 = np.subtract(tokenList, 35000).tolist()
#
#                         tokenList2 = fltr[np.where(fltr[:, 41] == 0), 2][0]
#                         tokenList21 = np.subtract(tokenList2, 35000).tolist()
#                         AelMargin[tokenList21, 5] = rate
#
#
#
#                     elif (i[2] == 'OTM'):
#                         #                         print(symbol,moneyness,rate)
#                         fltr = contract_fo[np.in1d(contract_fo[:, 3], [symbol])]
#                         tokenList = fltr[np.where(fltr[:, 41] == 1), 2][0]
#                         tokenList1 = np.subtract(tokenList, 35000).tolist()
#
#                     AelMargin[tokenList1, 5] = rate
#
#         f.close()
#
#     except:
#         print(traceback.print_exc())
#
#     print(AelMargin.shape)
#
#
# uploadAelGen()
# # for i in AelMargin:
# #     print(i)
#
#
# def exp123(a):
#     b = datetime.datetime.strptime(a, '%d-%b-%Y').strftime('%Y%m%d')
#     return b
#
#
# def uploadAelSpc():
#     try:
#         #         path = bod.le_aelS.text()
#         path = r'\\192.168.102.204\ba\FNO\07102022\F_AEL_OTM_CONTRACTS_10102022.csv'
#         tab123 = pd.read_csv(path, names=['ins', 'symbol', 'exp', 'strike', 'opt', 'a', 'ael'])
#         tab123['exp'] = tab123['exp'].apply(exp123)
#         #         print(tab123[tab123['ins'] =='OPTIDX'])
#         contract = pd.DataFrame(contract_fo[:, [2, 5, 3, 6, 7, 8, 12]],
#                                 columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])
#         #         span1.iloc[:, 4] = span1.iloc[:, 4].fillna(' ')
#         #         span1.iloc[:, 3] = span1.iloc[:, 3].fillna(0.0)
#         tab123.iloc[:, 2] = tab123.iloc[:, 2].astype(str)
#
#         aelMargin9 = pd.merge(contract, tab123, how='inner', left_on=['symbol', 'exp', 'strk1', 'opt'],
#                               right_on=['symbol', 'exp', 'strike', 'opt']).to_numpy()
#
#         for i in aelMargin9:
#             #             print(i)
#             AelMargin[i[0] - 35000, 5] = i[10]
#
#
#     except:
#         print(traceback.print_exc())
#
#
# uploadAelSpc()
# # for i in AelMargin:
# #     print(i)
# print(AelMargin[0, :])
# print(AelMargin.shape)
# print('done ael')
#
#
#
# import datatable as dt
# path=r'D:\scanRisk\Downloads\SPAN\calspred.csv'
#
# my_data= dt.fread(path).to_numpy()
# my_data = my_data[:,1:3]
# my_data1=my_data.astype('U20')
# v,r= np.unique(my_data1,return_counts =  True, axis= 0)
# newData = v[np.where(r!=1)]
# calSprd = np.zeros((newData.shape[0],4),dtype =object)
# calSprd[:,0] = newData[:,0].astype('f4')
# calSprd[:,1] = newData[:,1]
#
#
# fltr = contract_fo[np.in1d(contract_fo[:,5],['FUTSTK','FUTIDX'])]
# fltr1 = fltr[np.in1d(fltr[:,37],[4,5])]
#
# print('l333333333')
# for i in fltr1:
#     SYMBOL = i[3]
#     TOKEN = i[2]
#     ael = AelMargin[TOKEN-35000,5]
#     fprice = contract_fo[TOKEN-35000,18]
#     calSprd[np.where(calSprd[:,1]==SYMBOL),[2,3]] = [ael,fprice]
#
#
# def getbse2nse():
#     #     loc = os.getcwd().split('Application')[0]
#     #     path = os.path.join(loc,'Uploads','PS03','bse2nseSymbols.csv')
#
#     path = r'D:\scanRisk\Uploads\PS03\bse2nseSymbols.csv'
#     #    nse2bse = {}
#     with open(path, 'r') as f:
#         c = csv.reader(f)
#         for i in c:
#             nse2bse[i[0]] = i[1]
#     f.close()
#     return nse2bse
#
#
#
#
#
# nse2bse = getbse2nse()
#
#
#
# def updateb2nSymbol(sym):
#     try:
#
#         sym1 = nse2bse[sym]
#         #         print(sym1)
#         return sym1
#     except:
#         symbol = 'NIFTY'
#         print('error at nse2 bse con ', sym + 'abc', nse2bse)
#
#         return symbol
#
# def updatePOTMexp(exp):
#     exp1 = datetime.datetime.strptime(exp,'%d %b %Y').strftime('%Y%m%d')
#     return exp1
#
#
# import datatable as dt
#
# from datatable import *
# global POCW,lastSerialNo
# print('l4444444444')
#
#
#
#
#
# # POCW=np.zeros((10000,20),dtype=object)
#
# #         path = bod.lePOTM.text()
# path=r'\\192.168.102.204\ba\FNO\07102022\POTM_6405_20221007-01.CSV'
# POTM1 = pd.read_csv(path)
# POTM = POTM1.iloc[:,[0,7,10,11,12,13,16,18,20,22,34]]
# POTM.columns = ['Date','ClientCode','symbol','exp','strk','opt','bfLong','bfShort','dayBq','daySQ','SettlementP']
#
#
# POTM['symbol'] = POTM['symbol'].apply(updateb2nSymbol)
#
# POTM['NetQ'] = POTM['bfLong'] - POTM['bfShort'] + POTM['dayBq'] - POTM['daySQ']
#
# POTM['exp'] = POTM['exp'].apply(updatePOTMexp)
#
#
# POTM['opt'] = POTM['opt'].fillna(' ')
# # POTM['strk'] = POTM['strk'].astype('str')
# # POTM['strk'] = POTM['strk'].replace('0.0',' ')
# tempContract = pd.DataFrame(contract_fo[:, [2, 5, 3, 6, 7, 8, 12]],
#                             columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])
#
#
# ClientOPoss = pd.merge(POTM, tempContract, how='left', left_on=['symbol', 'exp', 'strk', 'opt'],
#                     right_on=['symbol', 'exp', 'strk1', 'opt'])
#
#
# print(ClientOPoss.columns)
#
# ClientOPoss1 = dt.Frame(ClientOPoss.loc[:,['Token', 'ClientCode', 'symbol', 'exp', 'strk_x', 'opt', 'bfLong',
#        'bfShort', 'dayBq', 'daySQ', 'SettlementP', 'NetQ', 'ins',
#        'strk_y', 'strk1']])
#
# ClientOPoss1[:, dt.update(lastSerialNo=range(ClientOPoss1.nrows))]
#
#
# ClientOPoss1[:,10] = dt.float64
# ClientOPoss1[:,11] = dt.int64
# ClientOPoss1[:, dt.update(openAmt = dt.f[10]*dt.f[11])]
#
#
# ClientOPoss1[:,'Token']
#
# ClientOPoss1[:, dt.update(netPrem = ifelse(((dt.f[12] =='OPTSTK') | (dt.f[12] == 'OPTIDX')),  -dt.f.openAmt,0.0))]
#
# ClientOPoss1[:, dt.update(netAmt = dt.f.openAmt)]
#
#
# ClientOPoss1['Token']=dt.float64
#
#
# spanmargindt=dt.Frame(spanMargin)
#
# spanmargindt['Token']=dt.float64
#
#
#
# print(ClientOPoss1)
# print(spanmargindt)
#
# try:
#     spanmargindt.key="symbol"
#     dtjoin=ClientOPoss1[:, :, dt.join(spanmargindt)]
# except:
#     print(traceback.print_exc())
#
#
# print(dtjoin)



# import datatable as dt
#
# DT = dt.Frame([range(5), [4, 3, 9, 11, -1]], names=("A", "B"))
# DT[:, dt.update(C = dt.f.A * 2,
#              D = dt.f.B // 3,
#              A = dt.f.A * 4,
#              B = dt.f.B + 1)]
# print(DT)
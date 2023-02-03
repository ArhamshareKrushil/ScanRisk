import threading
import traceback


import numpy as np
import datatable as dt
import time
import pandas as pd


def process(main):
    try:

        if (main.POTW.clientList!=[]):
            # print(main.POTW.clientList)
            # main.isPOTWupdated = False
            # print('clientlist',main.POTW.clientList)

            filterarr = main.POTW.table[np.in1d(main.POTW.table[:, 0], main.POTW.clientList)]

            main.POTW.clientList.clear()
            st = time.time()
            # spanTableTW = np.zeros((20000, 34), dtype=object)
            j = 0

            for i in filterarr:
                if (i[5] != '20221020'):
                    # try:
                    #
                    #     scn = main.spanMargin[i[2] - 35000, :]
                    #     expo = main.BOD.AelMargin[i[2] - 35000]
                    # except:
                    #     print(i,i[2])

                    scn = main.spanMargin[i[2] - 35000, :]
                    expo = main.BOD.AelMargin[i[2] - 35000]



                    futureToken = main.fo_contract[i[2] - 35000, 9]
                    FPrice = main.eq_contract[int(futureToken) - 36970, 18]
                    if (i[3] in ['FUTIDX', 'OPTIDX']):
                        FPrice=main.index_bhav[int(futureToken)-26000,3]
                    ###################################################
                    PFQ = 0
                    NFQ = 0
                    PCD = 0
                    NCD = 0
                    if (i[3] in ['OPTSTK', 'OPTIDX']):
                        iexpoM = 0.0 if (i[15] > 0) else expo[5]/100.0 * abs(i[15]) * FPrice
                    else:
                        iexpoM = expo[5]/100.0 * abs(i[15]) * FPrice
                        if (i[15] > 0):
                            PFQ = i[15]
                        else:
                            NFQ = abs(i[15])
                            ###################################################

                    main.spanTableTW[j, :35] = [i[0],
                                           i[2], i[15], scn[10] * i[15], scn[11] * i[15], scn[12] * i[15],
                                           scn[13] * i[15], scn[14] * i[15], scn[15] * i[15], scn[16] * i[15], scn[17] * i[15],
                                           scn[18] * i[15], scn[19] * i[15], scn[20] * i[15], scn[21] * i[15], scn[22] * i[15],
                                           scn[23] * i[15], scn[24] * i[15], scn[25] * i[15], scn[9], iexpoM,
                                           i[3], i[4], i[5], i[6], i[7],
                                           i[20], scn[26] * i[15], PFQ, NFQ,
                                           PCD, NCD,i[21],i[22],i[23]]
                    j += 1

            # DF = pd.DataFrame(main.spanTableTW)
            #
            # DF.to_csv(r"D:\TWS.csv")
            #
            # DF34 = pd.DataFrame(main.spanMargin)
            # DF34.to_csv(r"D:\spanscn.csv")


            df3 = dt.Frame(main.spanTableTW[:j,
                           [0, 22, 23, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 26, 27, 28, 29, 30, 31, 20,32,33,34]],
                           names=['UserID', 'Symbol', 'exp', 'scn1', 'scn2', 'scn3', 'scn4', 'scn5', 'scn6',
                                  'scn7', 'scn8', 'scn9', 'scn10', 'scn11', 'scn12', 'scn13', 'scn14', 'scn15', 'scn16',
                                  'NetPrem', 'Cdelta', 'PFQ', 'NFQ', 'PCD', 'NCD', 'iexpoM','FUTMTM','OPTMTM','PRM_MRG'])

            df3[3:] = dt.float64





            x = df3[:, dt.sum(dt.f[3:]), dt.by('UserID', 'Symbol', 'exp')]


            x[:, dt.update(PCD =dt.ifelse(dt.f.Cdelta > 0, dt.f.Cdelta, 0.0))]
            x[:, dt.update(NCD=dt.ifelse(dt.f.Cdelta > 0, 0.0, -dt.f.Cdelta))]

            x1 = x[:, dt.sum(dt.f[3:]), dt.by('UserID', 'Symbol')]


            x1[:, 'FSQ'] = 0.0
            x1[:, 'CDSQ'] = 0.0
            x1[:, 'spreadChrg'] = 0.0
            x1[:, 'spreadBeni'] = 0.0
            x1[:, 'maxVal'] = 0.0
            x1[:, 'spanMargin'] = 0.0

            x1[:, dt.update(FSQ=dt.ifelse(dt.f.PFQ > dt.f.NFQ, dt.f.NFQ, dt.f.PFQ))]
            x1[:, dt.update(CDSQ=dt.ifelse(dt.f.PCD > dt.f.NCD, dt.f.NCD, dt.f.PCD))]
            x1[:, dt.update(maxVal=dt.rowmax(dt.f[2:18]))]
            x1[:, dt.update(spanMargin=dt.f[32] - dt.f[18])]
            x1[:, dt.update(index=range(x1.nrows))]

            # print('namesssssss',x1.names)

         #index,Clientcode,Symbol,NetPrem,iexpoM,FSQ(futsq),CDSQ(combinedeltasq),sprdchrg,,sprdben,maxval,spanmargin,futmtm,optmtm,prm_mrg
            x2=x1[:,[34,0,1,18,24,28,29,30,31,32,33,25,26,27]]



            for i in range(x2.nrows):

                if (x2[i, 5] != 0 or x2[i, 6] != 0):
                    cc = x2[i, 1]
                    sym = x2[i, 2]

                    fsq = x2[i, 5]
                    cdsq = x2[i, 6]
                    data = main.BOD.calSprd[np.where(main.BOD.calSprd[:, 1] == sym)]

                    ael = data[0][2]
                    fprice = data[0][3]
                    calsc = data[0][0]

                    bvalue = fsq * 2 / 3 * ael/100 * fprice
                    sprdC = cdsq * calsc
                    x2[i, dt.update(spanMargin=dt.f[10] + sprdC)]
                    x2[i, dt.update(iexpoM=dt.f[4] - bvalue)]


            x2[:,dt.update(Total_Margin=dt.f[10] + dt.f[4])]
            x2[:, dt.update(FNO_MTM=dt.f[11] + dt.f[12])]

            # ClientCode,Symbol,Expo,Span,totalMrg,futmtm,optmtm,FNO_mtm,premMRG
            TWSWM=x2[:,[1,2,4,10,14,11,12,15,13]]


            # UserID,Expo,Span,totalMrg,futmtm,optmtm,FNO_mtm,dayPrem,premMargin,netMargin
            TWM = TWSWM[:, [dt.sum(dt.f[2:])], dt.by(dt.f[0])]


            TWM[:, dt.update(premMargin=dt.ifelse(dt.f[7] > 0, dt.f[7], 0))]
            TWM[:, dt.update(netMargin=dt.f[3] + dt.f[8])]

            th6=threading.Thread(target=twswloop,args=(main,TWSWM,TWM))
            th6.start()
            et = time.time()
            print('time',et - st)



    except:
        print(traceback.print_exc())


def twswloop(main,TWSWM,TWM):
    for i in TWSWM.to_numpy():
        main.sgTWSWM.emit(i)

    for i in TWM.to_numpy():
        main.sgTWM.emit(i)
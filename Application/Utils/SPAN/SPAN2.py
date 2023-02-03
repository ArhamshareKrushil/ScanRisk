import threading
import traceback

import numpy as np
import datatable as dt
import time
import pandas as pd


def process(main):
    try:

        if( main.POCW.clientList!=[]):
            # print('clientlist',main.POCW.clientList)
            # main.isPOCWupdated = False

            filterarr=main.POCW.table[np.in1d(main.POCW.table[:,0],main.POCW.clientList)]


            main.POCW.clientList.clear()

            st = time.time()
            # spanTableCW = np.zeros((20000, 34), dtype=object)
            j = 0

            for i in filterarr:
                if (i[5] != '20221006'):
                    # try:
                    #     print('token',i[2],i)
                    # except:
                    #     print(traceback.print_exc())
                    try:
                        scn = main.spanMargin[i[2] - 35000, :]
                    except:
                        print('token',i[2],i)

                    scn = main.spanMargin[i[2] - 35000, :]
                    expo = main.BOD.AelMargin[i[2] - 35000]
                    Ftoken = main.fo_contract[i[2] - 35000, 9]   #assetToken
                    FPrice = main.eq_contract[int(Ftoken) - 36970, 18]   #cashprice
                    if (i[3] in ['FUTIDX', 'OPTIDX']):
                        FPrice=main.index_bhav[int(Ftoken)-26000,3]

                    # print('ael working check', i[2],FPrice, Ftoken)
                    ##################################################


                    ###################################################
                    PFQ = 0
                    NFQ = 0
                    PCD = 0
                    NCD = 0
                    PHdelQty=0

                    if (i[3] in ['OPTSTK', 'OPTIDX']):
                        iexpoM = 0.0 if (i[15] > 0) else expo[5]/100.0 * abs(i[15]) * FPrice
                    else:
                        iexpoM = expo[5]/100.0 * abs(i[15]) * FPrice
                        if (i[15] > 0):
                            PFQ = i[15]
                        else:
                            NFQ = abs(i[15])
                    ###################################################
                    if (i[3] in ['OPTSTK']):
                        if(i[8]=='CE' ):
                            if(i[7] < FPrice):
                                PHdelQty=i[15]
                        else:
                            if (i[7] > FPrice):
                                PHdelQty = -(i[15])









                    main.spanTableCW[j, :35] = [ i[0],
                                           i[2], i[15], scn[10] * i[15], scn[11] * i[15], scn[12] * i[15],
                                           scn[13] * i[15], scn[14] * i[15], scn[15] * i[15], scn[16] * i[15], scn[17] * i[15],
                                           scn[18] * i[15], scn[19] * i[15], scn[20] * i[15], scn[21] * i[15], scn[22] * i[15],
                                           scn[23] * i[15], scn[24] * i[15], scn[25] * i[15], PHdelQty, iexpoM,
                                           i[3], i[4], i[5], i[6], i[7],
                                           i[19], scn[26] * i[15], PFQ, NFQ,
                                           PCD, NCD,i[17],i[18] ,i[20]]
                    j += 1

                    # if(i[0]=='A0017'):
                    #     print('ashgd',i[15],FPrice,expo[5],i,iexpoM)

            # print(j)

            # with open('d:/span.csv', 'w') as f:
            #     for i in range(j):
            #         a = ''
            #         for w in range(main.spanTableCW.shape[1]):
            #             x = main.spanTableCW[i, w]
            #             a = a + str(x) + ','
            #         f.write(a + '\n')
            #         # print(a)
            # f.close()


            # print(j)

            df3 = dt.Frame(main.spanTableCW[:j,
                           [0, 22, 23, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 26, 27, 28, 29, 30, 31, 20,32,33,34,19]],
                           names=['clientcode', 'Symbol', 'exp', 'scn1', 'scn2', 'scn3', 'scn4', 'scn5', 'scn6',
                                  'scn7', 'scn8', 'scn9', 'scn10', 'scn11', 'scn12', 'scn13', 'scn14', 'scn15', 'scn16',
                                  'NetPrem', 'Cdelta', 'PFQ', 'NFQ', 'PCD', 'NCD', 'iexpoM','FUTMTM','OPTMTM','Prem_Mrg','PHdelQty'])

            df3[3:] = dt.float64

            # with open('d:/df3.csv', 'w') as f:
            #     for i in range(df3.shape[0]):
            #         a = ''
            #         for j in range(df3.shape[1]):
            #             x = df3[i,j]
            #             a = a + str(x) + ','
            #         f.write(a + '\n')
            #         # print(a)
            # f.close()

            x = df3[:, dt.sum(dt.f[3:]), dt.by('clientcode', 'Symbol', 'exp')]




            x[:, dt.update(PCD =dt.ifelse(dt.f.Cdelta > 0, dt.f.Cdelta, 0.0))]
            x[:, dt.update(NCD=dt.ifelse(dt.f.Cdelta > 0, 0.0, -dt.f.Cdelta))]

            # with open('d:/exp.csv', 'w') as f:
            #     for i in range(x.shape[0]):
            #         a = ''
            #         for j in range(x.shape[1]):
            #             y = x[i,j]
            #             a = a + str(y) + ','
            #         f.write(a + '\n')
            #         # print(a)
            # f.close()

            x1 = x[:, dt.sum(dt.f[3:]), dt.by('clientcode', 'Symbol')]

            ####expiry removed from table

            x1[:, 'FSQ'] = 0.0     #29
            x1[:, 'CDSQ'] = 0.0       #30
            x1[:, 'spreadChrg'] = 0.0   #31
            x1[:, 'spreadBeni'] = 0.0   #32
            x1[:, 'maxVal'] = 0.0       #33
            x1[:, 'spanMargin'] = 0.0   #34

            x1[:, dt.update(FSQ=dt.ifelse(dt.f.PFQ > dt.f.NFQ, dt.f.NFQ, dt.f.PFQ))]
            x1[:, dt.update(CDSQ=dt.ifelse(dt.f.PCD > dt.f.NCD, dt.f.NCD, dt.f.PCD))]
            x1[:, dt.update(maxVal=dt.rowmax(dt.f[2:18]))]
            x1[:, dt.update(spanMargin=dt.f[33] - dt.f[18])]
            x1[:, dt.update(index=range(x1.nrows))]

            # with open('d:/x1.csv', 'w') as f:
            #     for i in range(x1.shape[0]):
            #         a = ''
            #         for j in range(x1.shape[1]):
            #             y = x1[i,j]
            #             a = a + str(y) + ','
            #         f.write(a + '\n')
            #         # print(a)
            # f.close()

         #index,Clientcode,Symbol,NetPrem,iexpoM,FSQ(futsq),CDSQ(combinedeltasq),sprdchrg,,sprdben,maxval,spanmargin,futmtm,optmtm,prem_mrg,PHdelQty
            x2=x1[:,[35,0,1,18,24,29,30,31,32,33,34,25,26,27,28]]

            x1[:, 'PHdelM'] = 0.0


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

                    bvalue = fsq * 2 / 3 * ael/100.0 * fprice
                    sprdC = cdsq * calsc
                    x2[i, dt.update(spanMargin=dt.f[10] + sprdC)]

                    # if(cc=='A0017' and sym =='INDHOTEL'):
                    #     print('8889999',ael)

                    x2[i, dt.update(iexpoM=dt.f[4] - bvalue)]

                    x2[i,dt.update(PHdelM=dt.f[14] * fprice)]


            x2[:,dt.update(Total_Margin=dt.f[10] + dt.f[4] )]
            x2[:,dt.update(FNO_MTM=dt.f[11] + dt.f[12])]


            # with open('d:/x2.csv', 'w') as f:
            #     for i in range(x2.shape[0]):
            #         a = ''
            #         for j in range(x2.shape[1]):
            #             x = x2[i,j]
            #             a = a + str(x) + ','
            #         f.write(a + '\n')
            #         # print(a)
            # f.close()


            #ClientCode,Symbol,Expo,Span,totalMrg,futmtm,optmtm,FNO_mtm,premMRG,PHdelQty,PHdelM
            CWSWM=x2[:,[1,2,4,10,16,11,12,17,13,14,15]]

            # for i in CWSWM.to_numpy():
            #     main.sgCWSWM.emit(i)

            # with open('d:/x3.csv', 'w') as f:
            #     for i in range(CWSWM.shape[0]):
            #         a = ''
            #         for j in range(CWSWM.shape[1]):
            #             x = CWSWM[i,j]
            #             a = a + str(x) + ','
            #         f.write(a + '\n')
            #         # print(a)
            # f.close()


            # CWM = x2[:, [dt.sum(dt.f[4]), dt.sum(dt.f[10]),dt.sum(dt.f[14]),dt.sum(dt.f[11:14])], dt.by(dt.f[1])]

            # ClientCode,Expo,Span,totalMrg,futmtm,optmtm,FNO_mtm,dayPrem,PHdelQty,PHdelM,premMargin,netMargin
            CWM = CWSWM[:, [dt.sum(dt.f[2:])], dt.by(dt.f[0])]
            CWM[:, dt.update(premMargin=dt.ifelse(dt.f[7] > 0, dt.f[7], 0))]
            CWM[:,dt.update(netMargin=dt.f[3] + dt.f[10])]

            # CWM1 = CWM[:, [0, 1, 2, 9, 4, 5, 6, 8]]



            # with open('d:/x4.csv', 'w') as f:
            #     for i in range(CWSWM.shape[0]):
            #         a = ''
            #         for j in range(CWSWM.shape[1]):
            #             x = CWSWM[i,j]
            #             a = a + str(x) + ','
            #         f.write(a + '\n')
            #         # print(a)
            # f.close()



            th5=threading.Thread(target=cwswloop,args=(main,CWSWM,CWM))
            th5.start()

            et = time.time()
            print('time',et - st)



    except:
        print(traceback.print_exc())


def cwswloop(main,CWSWM,CWM):
    for i in CWSWM.to_numpy():
        main.sgCWSWM.emit(i)

    for i in CWM.to_numpy():
        main.sgCWM.emit(i)




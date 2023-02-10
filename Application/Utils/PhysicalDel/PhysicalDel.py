import threading
import traceback

import numpy as np
import datatable as dt
import time
import os
import sqlite3
import pandas as pd

loc = os.getcwd().split('Application')
filepath = os.path.join(loc[0], 'Application', 'data1.csv')


# loc = os.getcwd().split('Application')
# DBpath = os.path.join(loc[0], 'Database', 'mainDB.db')
# conn = sqlite3.connect(DBpath)

# conn = sqlite3.connect(':memory:')
# conn = sqlite3.connect('file:cachedb?mode=memory&cache=shared')
# conn.execute("CREATE TABLE POCW(ClientCode	CHAR(50),Exchange	CHAR(50),Token INTEGER  ,InstrumentType CHAR(50), Symbol TEXT,Expiry TEXT,Strike  REAL,OptionType TEXT,DayQTY INT,dayValue REAL,LTP REAL,MTM  real,SerialNO int,OpenQty int,OpenAmt real,netQty int,NetValue real,FUT_MTM  real, OPT_MTM real,NET_PREM real, Prem_Margin real,PRIMARY KEY (Token,Clientcode))")


# import sqlalchemy as db
# # engine = db.create_engine('mssql+pyodbc://super:951753@192.168.102.172:1433/ANVdb')
# engine = db.create_engine("mssql+pyodbc://super:951753@192.168.102.172:1433/ANVdb?driver=ODBC+Driver+17+for+SQL+Server")
# conn = engine.connect()

# mssql+pymssql://{domain}\{username}:{password}@{hostip}/{db}

# import  pyodbc
#
# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=192.168.102.172;'
#                       'Database=ANVdb;'
#                       'UID=sa;PWD=Super@123;'
#                       )


# print(conn)

# import  pymssql
# conn = pymssql.connect(
#     host='192.168.102.172',
#     user='sa',
#     password='Super@123',
#     database='ANVdb'
# )
# cursor=conn.cursor()
# print(conn)

# import mysql.connector
# mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="Admin@123",
#         database="anvdb"
#     )
# mycursor = mydb.cursor()


def sqltonumpy(main):
    try:
        st = time.time()
        if (main.CWM.model.lastSerialNo != 0):
            df = pd.read_sql("select * from PhysicalM where TotalMargin!=0.0", conn).to_numpy()

            # print(df)
            main.CWM.table[:main.CWM.model.lastSerialNo, 10] = 0.0
            for i in df:
                main.sgPhysicalDelM.emit(i)

            et = time.time()
            print('time1', et - st)

    except:
        print(traceback.print_exc())



def process(main):
    try:
        st = time.time()
        if(main.POCW.model.lastSerialNo!=0):
            # print(main.POCW.table.shape)


            fltr1=main.POCW.table[np.where(main.POCW.table[:main.POCW.model.lastSerialNo,3]=='OPTSTK')]
            # print(fltr1)

            fltr2=fltr1[np.where(fltr1[:,5]=='20230125')]
            # print(fltr2)

            DF = pd.DataFrame(fltr2).to_csv("D:\shared\POCW.csv",index=False)

            # save the dataframe as a csv file
            # DF.to_csv("D:\shared\data1.csv",index=False)




            # conn.execute("Delete from POCW")
            # df=pd.DataFrame(main.POCW.table[:main.POCW.model.lastSerialNo,:],columns=['ClientCode',
            #               'Exchange','Token','InstrumentType','Symbol','Expiry',
            #           'Strike','OptionType','dayQty','dayValue','LTP',
            #               'MTM','SerialNO','OpenQty','OpenAmt','netQty',
            #               'NetValue','FUT_MTM','OPT_MTM','NET_PREM','Prem_Margin'])
            # # with np.printoptions(threshold=np.inf):
            # #     # print(arr)
            # #     print(df['Token'].to_numpy())
            #
            # df.to_sql('POCW',conn,index=False,if_exists='append')





            # #
            # # recordList = list(map(tuple, main.POCW.table[:main.POCW.model.lastSerialNo]))
            # # sqlite_insert_query="INSERT INTO POCW VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # # cursor.executemany(sqlite_insert_query, recordList)
            #
            #
            # main.POCW.table[:main.POCW.model.lastSerialNo].tofile("data1.csv",sep = ',')

            # main.POCW.table[:main.POCW.model.lastSerialNo].tofile(r"\\192.168.102.172\shared\data1.csv",sep = ',')

            # np.savetxt(r"\\192.168.102.172\shared\data1.csv", main.POCW.table[:main.POCW.model.lastSerialNo],delimiter=",",fmt="%s")
            # np.savetxt("data1.csv", main.POCW.table[:main.POCW.model.lastSerialNo],delimiter=",",fmt="%s")

            # cursor.execute("Delete from POCW")
            # DF = pd.DataFrame(main.POCW.table[:main.POCW.model.lastSerialNo])
            # # save the dataframe as a csv file
            # DF.to_csv(r"\\192.168.102.172\shared\data1.csv",index=False)
            # # filepath=r'\\192.168.102.169\shared\data1.csv'
            # # qry = "BULK INSERT POCW FROM "+ filepath+" WITH   (  FIELDTERMINATOR =',',  ROWTERMINATOR ='\n'  );"
            # # # Execute the query
            # #
            # qry="BULK INSERT POCW  FROM 'C:\shared\data1.csv' WITH (FORMAT = 'CSV', FIRSTROW = 2)"
            # # #
            # # #
            # # #
            # cursor.execute(qry)


            ###########with Pandas ##############
            # conn.execute("Delete from POCW")
            # df=pd.DataFrame(main.POCW.table[:main.POCW.model.lastSerialNo,:],columns=['ClientCode',
            #               'Exchange','Token','InstrumentType','Symbol','Expiry',
            #           'Strike','OptionType','dayQty','dayValue','LTP',
            #               'MTM','SerialNO','OpenQty','OpenAmt','netQty',
            #               'NetValue','FUT_MTM','OPT_MTM','NET_PREM','Prem_Margin'])
            # df.to_sql('POCW',conn,index=False,if_exists='append')

            ###########with Numpy###############
            # conn.execute("Delete from POCW")
            # for i in main.POCW.table[:main.POCW.model.lastSerialNo]:
            #     # conn.execute("INSERT INTO POCW VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            #     #              (i[0], i[1], i[2], i[3], i[4],
            #     #               i[5], i[6], i[7], i[8], i[9],
            #     #               i[10], i[11], i[12], i[13], i[14],
            #     #               i[15], i[16], i[17], i[18], i[19],
            #     #               i[20]))
            #
            #     conn.execute("INSERT INTO POCW VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) on conflict(Token,Clientcode) do update set DayQTY=?,dayValue=?,LTP=?,MTM=?, netQty=?,NetValue=?,FUT_MTM=?,OPT_MTM=?,NET_PREM=?,Prem_Margin=?",
            #                  (i[0], i[1], i[2], i[3], i[4],
            #                   i[5], i[6], i[7], i[8], i[9],
            #                   i[10], i[11], i[12], i[13], i[14],
            #                   i[15], i[16], i[17], i[18], i[19],
            #                   i[20],i[8],i[9],i[10],i[11],i[15],i[16],i[17],i[18],i[19],i[20]))

            # qry="LOAD DATA INFILE 'data1.csv' INTO TABLE POCW FIELDS TERMINATED BY ','LINES TERMINATED BY '\n'IGNORE 1 ROWS"

            # qry="LOAD DATA INFILE 'D:\scanRisk\\Application\\data1.csv' INTO TABLE POCW FIELDS TERMINATED BY ','  LINES TERMINATED BY '\n'"

            # mycursor.execute(qry)
            # mydb.commit()

            # conn.commit()

            # conn.close()




        # # spanTableCW = np.zeros((20000, 34), dtype=object)
        # j = 0
        # if(main.POCW.model.lastSerialNo !=0):
        #     print('ttt')
        #
        #     fltr1=main.POCW.table[np.where(main.POCW.table[:main.POCW.model.lastSerialNo,3]=='OPTSTK')]
        #     # print('fltr1',fltr1)
        #     # exp = main.fo_contract[np.where((main.fo_contract[:, 5] == 'OPTSTK')&(main.fo_contract[:, 37] == 4)) , 6][0][0]
        #     # print('exp',exp)
        #
        #     fltr2=fltr1[np.where(fltr1[:,5]=='20230125')]
        #     fltrArrayCE=fltr2[np.where(fltr2[:,7]=='CE')]
        #     fltrArrayPE=fltr2[np.where(fltr2[:,7]=='PE')]
        #
        #
        #     arayBase = np.zeros((5000,21),dtype=object)
        #     arayCE = np.zeros((5000,21),dtype=object)
        #     arayPE = np.zeros((5000,21),dtype=object)
        #
        #
        #     # print('fltr2',fltr2)
        #
        #
        #
        #     # uniqueClient=np.unique(fltr2[:,0])
        #     # print(uniqueClient)
        #     # for i in uniqueClient:
        #     #     uniqueSymbol = fltr2[np.where(fltr2[:, 0]==i),4][0]
        #     #     for ik in uniqueSymbol:
        #     #         fltr3 = fltr2[np.where((fltr2[:, 0]==i) & (fltr2[:, 4]==ik))]
        #     #         # print('ff',fltr3)
        #     #
        #     #         Ftoken = main.fo_contract[np.where(main.fo_contract[:,3]==ik),9][0][0]  # assetToken
        #     #         # print(Ftoken)
        #     #         cashprice = main.eq_contract[int(Ftoken) - 36970, 18]  # cashprice
        #     #
        #     #         fltr4=fltr3[np.where((fltr3[:,7]=='CE') & (fltr3[:,6]<cashprice)),15]
        #     #         fltr5=fltr3[np.where((fltr3[:,7]=='PE') & (fltr3[:,6]>cashprice)),15]
        #
        #
        #
        #
        #     # uniqueSym = np.unique(fltr2[:, 4])
        #     # for i in uniqueSym:
        #     #     Ftoken = main.fo_contract[np.where(main.fo_contract[:, 3] == i), 9][0][0]  # assetToken
        #     #     # print(Ftoken)
        #     #     cashprice = main.eq_contract[int(Ftoken), 18]  # cashprice
        #     #     uniqueClient = fltr2[np.where(fltr2[:, 4]==i),0][0]
        #     #     for ik in uniqueClient:
        #     #         fltr3 = fltr2[np.where((fltr2[:, 0]==ik) & (fltr2[:, 4]==i))]
        #     #         # print('ff',fltr3)
        #     #
        #     #
        #     #
        #     #         fltr4=fltr3[np.where((fltr3[:,7]=='CE') & (fltr3[:,6]<cashprice)),15]
        #     #         fltr5=fltr3[np.where((fltr3[:,7]=='PE') & (fltr3[:,6]>cashprice)),15]
        #
        #     uniqueSym = np.unique(fltr2[:, 4])
        #
        #
        #     for i in uniqueSym:
        #         arayCE[:5000,:] = arayBase[:5000,:]
        #         dim = np.where(fltr2[:,4]==i)
        #         # print(dim[0])
        #         assetToken = main.fo_contract[fltr2[dim[0][0],2]-35000,9]
        #         cashprice = main.eq_contract[int(assetToken), 18]
        #         # print('hh',i,assetToken)

                # Ftoken = main.fo_contract[np.where(main.fo_contract[:, 3] == i), 9][0][0]  # assetToken

                # token=fltr2[np.where(fltr2[:,4]==i),2][0][0]
                # Ftoken = main.fo_contract[token - 35000, 9]  # assetToken
                # cashprice = main.eq_contract[int(Ftoken), 18]   #cashprice
                #

                # print(Ftoken)
                # cashprice = main.eq_contract[int(Ftoken), 18]  # cashprice


                # # fltr3 = fltr2[np.where((fltr2[:, 4] == i) & (fltr2[:, 7] == 'CE') & (fltr2[:, 6] < cashprice))]
                # # fltr4 = fltr2[np.where((fltr2[:, 4] == i) & (fltr2[:, 7] == 'PE') & (fltr2[:, 6] > cashprice))]
                # fltr3 = fltr2[np.where((fltr2[:, 4] == i) & (fltr2[:, 7] == 'CE') )]
                # fltr4 = fltr2[np.where((fltr2[:, 4] == i) & (fltr2[:, 7] == 'PE') )]


                # for i in fltr3:
                #     main.PSS[j]=i
                #     j+=1
                # for i in fltr4:
                #     main.PSS[j]=i
                #     j+=1



                # for ik in uniqueClient:
                #     fltr3 = fltr2[np.where((fltr2[:, 0] == ik) & (fltr2[:, 4] == i))]
                #     # print('ff',fltr3)
                #
                #     fltr4 = fltr3[np.where((fltr3[:, 7] == 'CE') & (fltr3[:, 6] < cashprice)), 15]
                #     fltr5 = fltr3[np.where((fltr3[:, 7] == 'PE') & (fltr3[:, 6] > cashprice)), 15]

        et = time.time()
        print('time1',et-st)
    except:
        print(traceback.print_exc())







def process1(main):
    st = time.time()
    # spanTableCW = np.zeros((20000, 34), dtype=object)
    j = 0
    try:
        for i in main.POCW.table[:main.POCW.model.lastSerialNo]:
            PHdelQty = 0
            FPrice = 0
            if i[4] != 'TCS':
                Ftoken = main.fo_contract[i[2] - 35000, 9]  # assetToken
                FPrice = main.eq_contract[int(Ftoken) - 36970, 18]  # cashprice

                ###################################################




                ###################################################
                if (i[3]==['OPTSTK'] and i[5] =='20230119'):
                    if (i[8] == 'CE'):
                        if (i[7] < FPrice):
                            PHdelQty = i[15]
                    else:
                        if (i[7] > FPrice):
                            PHdelQty = -(i[15])

            main.spanTableCW[j, :4] = [i[0],
                                        i[4], PHdelQty,FPrice
                                       ]
            j += 1

        df3 = dt.Frame(main.spanTableCW[:j,
                       [0, 1, 2, 3]],
                       names=['clientcode', 'Symbol',
                              'PHdelQty','cashPrice'])

        df3[2:] = dt.float64

        x1 = df3[:, dt.sum(dt.f[2]), dt.by('clientcode', 'Symbol','cashPrice')]

        et = time.time()
        print('time1',et-st)
        print(x1)
    except:
        print(traceback.print_exc(),i[2],i)




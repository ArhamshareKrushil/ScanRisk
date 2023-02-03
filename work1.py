import  os
import  json
import numpy as np

# #############  Adding Branch from cllient master to terminalmaster ######################
#
#
# loc = os.getcwd().split('Application')[0]
# path = os.path.join(loc, 'Application', 'DB', 'terminal_master.json')
# # f = open(r'..\Application\DB\terminal_master.json')
# f = open(path)
# Tmaster = json.load(f)
#
#
# loc = os.getcwd().split('Application')[0]
# path = os.path.join(loc, 'Application', 'DB', 'client_master.json')
# # f = open(r'..\Application\DB\terminal_master.json')
# f = open(path)
# Cmaster = json.load(f)
#
#
# for i in Cmaster:
#     Cmaster[i]['Branch']=Cmaster[i]['Branch'].upper()
#
# with open(r'Application\DB\client_masterNew.json', 'w') as j:
#     j.write(json.dumps(Cmaster, indent=4))

#
# for i in Tmaster:
#         # print('i[UID]',Tmaster[i]['UserID'])
#         # print('j',j)
#     if Tmaster[i]['UserID'] in Cmaster:
#         UID=Tmaster[i]['UserID']
#         Tmaster[i]['Branch']=Cmaster[UID]['Branch'].upper()
#         Tmaster[i]['GRP']=Cmaster[UID]['GRP'].upper()
#         Tmaster[i]['Name']=Cmaster[UID]['Name']
#         Tmaster[i]['active']=Cmaster[UID]['active']
#     else:
#         Tmaster[i]['Name'] = ' '
#
#         # Cmaster[i]['Branch']=Cmaster[i]['Branch'].upper()
#
#
#
# with open(r'Application\DB\terminal_masterNew.json', 'w') as j:
#     j.write(json.dumps(Tmaster, indent=4))
#
#
###################json to csv#####################

# import csv
#
# loc = os.getcwd().split('Application')[0]
# path1 = os.path.join(loc, 'clientmasternew.csv')
#
# datafile=open(path1,'w',newline='')
# writer=csv.writer(datafile)
#
# count=0
# for data in Cmaster:
#     if count==0:
#         header=Cmaster[data].keys()
#         writer.writerow(header)
#         count+=1
#     i=Cmaster[data].values()
#     writer.writerow(i)
# datafile.close()
#
#
#
#
# #############################################################
# arr=np.zeros((10,5),dtype=object)
#
# arr[0,1]=85
# arr[1,1]=55
# arr[1,3]=1
# arr[2,3]=2
# arr[8,3]=78
#
# print(arr)
# arr=np.delete(arr,0,axis=0)
# print(arr)
# #
#
#
# arr[:,2]=arr[:,3]+arr[:,1]
#
# # arr[:,2]=arr[:,3] if arr[:,1]>1 else 23
#
# arr[:,3]=np.where(arr[:,1] > 0, -arr[:,2],0)
#
# arr[:,4] = np.amax(arr[:,0:3], axis=1)
# print(arr[:,0:2])
#
#
#
# arr[:6,4]=['df','dfdf','dsfs','df','sdf','sdf']
# print(arr)
#
# arr1=arr[np.in1d(arr[:,4], ['df','dfdf'])]
#
# print(arr1)




# import os
# import datetime
#
# Ymd_today = datetime.datetime.today().strftime("%Y%m%d")
#
# loc1 = os.getcwd().split('Application')
# downloadLoc = os.path.join(loc1[0], 'Downloads', 'SPAN',Ymd_today)
# if(os.path.exists(downloadLoc)):
#     print('file exist')
# else:
#     os.makedirs(downloadLoc)

import datatable as dt
# arr=np.zeros((10,4))
# arr[0,1]=85
# arr[1,1]=55
# arr[1,3]=1
# arr[2,3]=2
# arr[8,3]=78.23
# df3 = dt.Frame(arr[:,[0,1,2,3]])
# df3[0:] = dt.int64
# df3[0:] = dt.float64
# print(df3.ltypes)



#
# aa=format(343,'.2f')
# print(type(aa))
# print(aa)
#
#
# print(float('785.00'))
#
#
#
# a = 1
# print('Value before conversion:',a)
# print('Data type:',type(a))
# a = a+0.0000
# print('Value after conversion',a)
# print('Data type:',type(a))
#
# import datetime
#
# a=1353110400
# exp=datetime.datetime.fromtimestamp(1353057302)
#
# exp=datetime.datetime.fromtimestamp(1353057302)
#
#
#
# exp=exp.replace(2022)
#
#
# exp = datetime.datetime.strftime(exp, '%Y%m%d')
#
#
# print(exp)

# import csv
#
# path=r'\\192.168.102.204\ba\FNO\18112022\POTM_6405_20221118-01.CSV'
# loc1 = os.getcwd().split('Application')
# path1 = os.path.join(loc1[0], 'Uploads','OpenPosition','openPos1.csv')
#
# loc1 = os.getcwd().split('Application')
# path1 = os.path.join(loc1[0], 'Uploads','OpenPosition','openPos1.csv')
# with open(path, 'r') as f1:
#     with open(path1, 'w+') as f:
#         reader = csv.reader(f1, lineterminator="\n")
#         writer = csv.writer(f, lineterminator="\n")
#
#         for j, row in enumerate(reader):
#             # print(row[10])
#             if(row[9]=='ONGCOPT'):
#                 # print(row[12],row)
#                 row[12] = str(float(row[12])-6.75)
#                 # print(row[10])
#             writer.writerow(row)
#         # writer.writerow('\n')
#     f.close()
# f1.close()


# import numpy as np
# arr = np.array([[1,2,3],[4,5,6]])
# row = np.array([7,8,9])
# row_n = arr.shape[0] ##last row
# arr = np.insert(arr,0,[row],axis= 0)
# print(arr)
#
#
# clientList=[1]
# if 1 not in clientList:
#     clientList.append(1)
#
# print(clientList)
#
#
# from datetime import datetime
# date_string = '30-12-2022'
# datetime = datetime.strptime(date_string, '%d-%m-%Y').strftime('%d-%b-%y')
# print(datetime)



# arr=np.zeros((10,5),dtype=object)
#
# arr[0,1]=85
# arr[1,1]=55
# arr[1,3]=1
# arr[2,3]=2
# arr[8,3]=78
#
# # print(arr)
# # arr=np.delete(arr,0,axis=0)
# # print(arr)
# #
#
#
# arr[:,2]=arr[:,3]+arr[:,1]
#
# # arr[:,2]=arr[:,3] if arr[:,1]>1 else 23
#
# arr[:,3]=np.where(arr[:,1] > 0, -arr[:,2],0)
# print(arr)
# ad=np.where((arr[:,1]==85) & (arr[:,2]==85))[0]
# # ad=np.where((arr[:,2]==56))[0]
# print(ad)


# import datetime
# expiryDay = datetime.datetime.strptime('20230112', '%Y%m%d')
# print(expiryDay)
#
# if ik[8] == 'CE':
#     opt = 'c'
# else:
#     opt = 'p'
# # fprice = main.fo_contract[ik[17]-35000,19]
# price = (ik[19] * UP_Scn) / 100
# ltp = ik[19] + price
#
# # print(type(i[6]),i[6])
# expiryDay = datetime.datetime.strptime(ik[6], '%Y%m%d')
# daysRemaaining1 = (expiryDay - main.todate).days
# daysRemaaining = 1 if (daysRemaaining1 == 0) else daysRemaaining1
# t = daysRemaaining / 365
#
# scnPrice = black_scholes(opt, ltp, ik[12], t, 0.001, 0.2)


import numpy as np

# # Create a 2d array
# arr = np.array([[28, 49, 78, 88], [92, 81, 98, 45], [22, 67, 54, 69], [69, 80, 80, 99]])
#
# # Displaying our array
# print("Array...",arr)
#
# # Get the datatype
# print("Array datatype...",arr.dtype)
#
# # Get the dimensions of the Array
# print("Array Dimensions...",arr.ndim)
#
# # Get the shape of the Array
# print("Our Array Shape...",arr.shape)
#
# # Get the number of elements of the Array
# print("Elements in the Array...",arr.size)
#
# # The destination
# arrRes = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15,16]]
#
# # To copy values from one array to another, broadcasting as necessary, use the numpy.copyto() method in Python Numpy
# # The 1st parameter is the source array
# # The 2nd parameter is the destination array
# res = np.copyto(arr, arrRes)
# print("Result...",arrRes)

#
# import numpy as np
#
# np_arr = np.array([[1, 2], [3, 4]])
# tuple_arr = list(map(tuple, np_arr))
# print(tuple_arr)

#list of dictnories to numpy arra

# import pandas as pd
# data = [{'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044},
# {'x': -0.002222188049927354, 'y': 0.014999999664723873, 'z': -0.45333319902420044}]
#
# a=pd.DataFrame(data)[['x', 'y','z']].values
# print(a)


import pyodbc

# con = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = '192.168.102.172')
# print(con)

import sqlalchemy as db
# engine = db.create_engine('mssql+pyodbc://sa:Super@123@192.168.102.172:1433/ANVdb?driver=SQL Server')
engine = db.create_engine("mssql+pyodbc://main:951753@192.168.102.172/ANVdb?driver=ODBC+Driver+17+for+SQL+Server")
conn = engine.connect()
print(conn)


# import  pymssql
# conn = pymssql.connect(
#     host='192.168.102.172',
#     user='sa',
#     password='Super@123',
#     # database='ANVdb'
# )
# print(conn)
#
#
#
# import  pyodbc
#
# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=192.168.102.172;'
#                       'UID=sa;PWD=Super@123;'
#                       )
#
#
# print(conn)


from  datatable import dt
dt.fread()




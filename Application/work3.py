import datatable as  dt
import datetime
import linecache
import time
import os



today = datetime.datetime.today().strftime('%Y%m%d')
defaultDir = r'\\192.168.102.222\shared\OnlineTrades\%s' % (today)
defaultDir = r'\\192.168.102.222\shared\OnlineTrades\%s' % (today)
print(defaultDir)
path  = os.path.join(defaultDir,'20220929.txt')
path  = '20220929.txt'
st = time.time()

st=time.time()

for i in range(20):
    # with open(path) as f:
    #     a =f.read()
    # f.close()

    lines = linecache.getlines(path)
    # ax =lines[100]

    linecache.clearcache()
    # for ix in range(100):
    #     xx=ix
    # a= lines
    # for k in lines:
    #     i = k.split(',')
    #     Clicode = int(i[0])
    #     token = int(i[2])
    #     dQty = int(i[8])
    #     damt = float(i[9])
    #     sym = i[3].replace(' ', '')
    #
    #     strike = float(i[5])
    #
    #     abc = dt.Frame([[Clicode],
    #                     ['NSEFO'], [token], [i[7]], [sym], [i[4]], [strike], [i[6]], [dQty], [damt], [0], [0], [0], [0],
    #                     [0], [dQty], [damt]]).to_numpy()
    #
    #     # abc = dt.Frame([[i[0]],
    #     #                 ['NSEFO'], [i[1]], [i[7]], [i[3]], [i[4]], [i[4]], [i[6]], [i[5]], [i[6]], [0], [0], [0], [0],
    #     #                 [0], [i[5]], [i[6]]]).to_numpy()
    #
    # print(len(lines))
et=time.time()
print('time',et-st)
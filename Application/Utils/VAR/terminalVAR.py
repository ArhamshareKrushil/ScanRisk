import threading
import traceback


import numpy as np
import datatable as dt
import time
import pandas as pd


def process(main):
    # print('terminalVAR')

    # st = time.time()
    # # spanTableCW = np.zeros((20000, 34), dtype=object)
    # j = 0
    #
    # for i in main.CMPOTW.table[:main.CMPOTW.model.lastSerialNo]:
    #
    #         # try:
    #         #     print('token',i[2],i)
    #         # except:
    #         #     print(traceback.print_exc())
    #
    #     VAR = main.VARMargin[np.where(main.VARMargin[:,4]==i[2])][0]
    #
    #     # print('VAR', VAR[3])
    #
    #
    #     main.varTableTW[j, :8] = [i[0],i[2],i[3],i[4],i[5],i[6],i[6]*(VAR[3]/100),i[8]]
    #
    #     j += 1

    df3 = dt.Frame(main.CMPOTW.table[:main.CMPOTW.model.lastSerialNo,[0,14,8]],names=['UserID', 'MRG','MTM'])

    df3[1:] = dt.float64

    x = df3[:, dt.sum(dt.f[1:]), dt.by('UserID')]
    # print(x)

    th6 = threading.Thread(target=CMTWMloop, args=(main, x))
    th6.start()

def CMTWMloop(main, CMTWM):
    for i in CMTWM.to_numpy():
        main.sgCMTWM.emit(i)




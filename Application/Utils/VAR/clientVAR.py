import threading
import traceback


import numpy as np
import datatable as dt
import time
import pandas as pd


def process(main):
    if main.CMPOCW.model.lastSerialNo !=0:

        df3 = dt.Frame(main.CMPOCW.table[:main.CMPOCW.model.lastSerialNo, [0, 14, 8]], names=['ClientID', 'MRG', 'MTM'])

        df3[1:] = dt.float64

        x = df3[:, dt.sum(dt.f[1:]), dt.by('ClientID')]
        # print(x)

        th5 = threading.Thread(target=CMCWMloop, args=(main, x))
        th5.start()


def CMCWMloop(main, CMCWM):
    for i in CMCWM.to_numpy():
        main.sgCMCWM.emit(i)




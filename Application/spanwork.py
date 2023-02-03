import numpy as np
import pandas as pd
from Application.Utils.getMasters import getMaster
from PyQt5.QtCore import QObject
from os import getcwd,path



import time
loc1 = getcwd().split('Application')
loc1 = getcwd().split('Application')
downloadLoc = path.join(loc1[0], 'Downloads','SPAN')

a=QObject()
fo_contract, eq_contract,cd_contract, contract_heads = getMaster(a,False)

rrr=time.time()

spanFile = path.join(downloadLoc, 'span.csv')
span1 = pd.read_csv(spanFile,names= ['ins','symbol','exp','strk','opt','close','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15','s16','delta'])

contract = pd.DataFrame(fo_contract[:,[2,5,3,6,7,8,12]],columns = ['Token','ins','symbol','exp','strk','opt','strk1'])
span1.iloc[:,4] = span1.iloc[:,4].fillna(' ')
span1.iloc[:,3] = span1.iloc[:,3].fillna(1.0)
span1.iloc[:,2] = span1.iloc[:,2].astype(str)


a= pd.merge(contract, span1, how='left', left_on=['symbol','exp','strk1','opt'], right_on = ['symbol','exp','strk','opt'])

print(a.columns)

rrr1=time.time()
print(rrr1-rrr)

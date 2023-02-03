import shutil
import datetime
from datetime import datetime
import traceback
import requests
from zipfile import ZipFile
import sys
import os
import lxml.etree as elementTree
import pandas as pd
import numpy as np
from Application.Utils.getMasters import *
from Application.Constants.file import *

Ymd_today = datetime.datetime.today().strftime("%d%m%Y")
loc1 = getcwd().split('Application')
downloadLoc = path.join(loc1[0], 'Downloads','VAR',Ymd_today)



def latest_var(main):
    try:

        print('new_Var')
        # Ymd_today = datetime.datetime.today().strftime("%Y%m%d")
        print("TODAY:",Ymd_today)

        # loc1 = os.getcwd().split('Application')
        # downloadLoc = os.path.join(loc1[0], 'Downloads', 'SPAN', Ymd_today)

        if (os.path.exists(downloadLoc)):
            pass
        else:
            os.makedirs(downloadLoc)

        Ymd_yesterday = main.prevDate.strftime("%d%m%Y")
        # print("YESTEDAY:",Ymd_yesterday)
        user_agent = 'Mozilla/5.0'
        headers = {'User-Agent': user_agent}
        url = VAR_FILE_URL #+ Ymd_today #+'_1.DAT'
        # take selected span type
        # spanValue = main.BOD.cbSpan.currentText()
        # print(spanValue)
        print('getting_url of VAR file and downloading..........')

        # BUILD url PATH
        url = builFileURL(main,VAR_FILE_URL,Ymd_today,Ymd_yesterday)
        #
        print("URL:", url)
        # DOWNLOAD FILE
        # lbl_spanError
        res = requests.get(url, headers=headers)
        print("status  :", res.status_code)
        if(res.status_code != 200):
            # main.BOD.lbl_spanError.setText("File not found or internal server error")
            print("File not found or internal server error")
        else:
            # DOWNLOAD ZIP FILE
            varLOC = path.join(downloadLoc, "var.csv")
            with open(varLOC, 'wb+') as f:
                f.write(res.content)
            f.close()
            print("dat nsccl downloaded.....")

            # unzipSpan(main,final_file, downloadLoc,spanLOC)
            # parseSpan_spread(main,downloadLoc)
            # parseSpan_margin(main,downloadLoc)
            # parseSpan_calSpred(main, downloadLoc)
            getVARMargin(main,downloadLoc)
    except:
        print(traceback.print_exc())



# latest_var()


def getVARMargin(main,downloadLoc):

        # loc1 = os.getcwd().split('Application')
        # downloadLoc = os.path.join(loc1[0], 'Downloads', 'SPAN',)

        # a = QObject()
        # fo_contract, eq_contract, cd_contract, contract_heads = getMaster(a, False)

        rrr = time.time()

        varfile = path.join(downloadLoc, "var.csv")
        VAR = pd.read_csv(varfile,skiprows=1,usecols=[1,2,3,9],names=[ 'Symbol', 'Series', 'ISIN', 'VARMRGrate'])

        contract = pd.DataFrame(main.eq_contract[:, [2, 3, 6]],
                                columns=['Token', 'Symbol', 'Series'])
        # VAR.iloc[:, 4] = VAR.iloc[:, 4].fillna(' ')
        # VAR.iloc[:, 3] = VAR.iloc[:, 3].fillna(0.0)
        # VAR.iloc[:, 3] = VAR.iloc[:, 3].astype(str)

        # vvv = pd.merge(VAR, contract, how='left', left_on=['Symbol', 'Series'],
        #              right_on=['Symbol', 'Series']).to_csv('d:/VAREDIT.csv')

        main.VARMargin = pd.merge(VAR, contract, how='left', left_on=['Symbol', 'Series'],
                                   right_on=['Symbol', 'Series']).to_numpy()

        # rrr1 = time.time()
        # print(rrr1 - rrr)





def builFileURL(self,url,Ymd_today,Ymd_yesterday):

    user_agent = 'Mozilla/5.0'
    headers = {'User-Agent': user_agent}

    url1 = url +Ymd_today+'_1.DAT'
    url2 = url + Ymd_yesterday + '_1.DAT'
    # print(url1)
    # print(url2)
    if (requests.get(url1, headers=headers).status_code == 200):
        print('working')
        final_file = url1


    elif (requests.get(url2, headers=headers).status_code == 200):
        print('working')
        final_file = url2
    else:
        final_file=' '


    url=final_file



    return url

def process_var(main):
    getVARMargin(main, downloadLoc)






























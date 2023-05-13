import os
import itertools
import threading
import shutil
import zipfile

import numpy as np
import json
import requests
import sys
import traceback
import logging
from Application.Utils.configReader import get_API_config,writeAPIdetails
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from Application.Utils.support import *
from Application.Utils.getMaster import getMaster


def login(main):
    try:
        print("inside API login")
#        main.login.pbLogin.setEnabled(False)
       # main.login.label.append('Logging in to Marketdata API..')
        get_API_config(main)
        User=main.login.leUsername.text()
        password=main.login.lePW.text()
        print(User,password)
        payload = {
            "username": User,
            "password": password,
            "source":"desktop"

        }
        login_url = main.FastApiURL + '/v3/login'

        # login_url = main.FastApiURL + f'/dlogin?username={User}&password={password}'
        # print("login_url:", login_url)
        # print("payload : ", payload)
        login_access = requests.post(login_url, json=payload)
        logging.info(login_access.text)

        # print(login_access.text)


        if login_access.status_code == 200:
            data = login_access.json()
            # print('hjhjkjh',data)
            # result = data['result']
            # if data['type'] == 'success':
            #     a = 'successfull'
            # result = data['result']

            token = data['Token']
            usertype= data['Type']
            Type_id = data['Type_id']
            writeAPIdetails(token, usertype,Type_id)

            if main.login.cbCmaster.isChecked():
                update_contract_FOletest(main,token)
            else:
                update_contract_FOold(main)

            main.createUserObject()


            main.SioClient.startSocket(token,main.socketIP)

            if usertype!='master':

                th56=threading.Thread(target=update_TerminalMaster,args=(main,token))
                th56.setDaemon(True)
                th56.start()

                th1 = threading.Thread(target=updatePOTW_DB, args=(main, token))
                th1.setDaemon(True)
                th1.start()

                th2 = threading.Thread(target=getTWSWM, args=(main, token))
                th2.setDaemon(True)
                th2.start()

                th3 = threading.Thread(target=getTWM, args=(main, token))
                th3.setDaemon(True)
                th3.start()

                th4 = threading.Thread(target=getCMPOTW, args=(main, token))
                th4.setDaemon(True)
                th4.start()

                th5 = threading.Thread(target=getCMTWM, args=(main, token))
                th5.setDaemon(True)
                th5.start()
            else:
                th56 = threading.Thread(target=update_TerminalMaster, args=(main, token))
                th56.setDaemon(True)
                th56.start()

                th1 = threading.Thread(target=updatePOTW_DB, args=(main, token))
                th1.setDaemon(True)
                th1.start()

                th2 = threading.Thread(target=getTWSWM, args=(main, token))
                th2.setDaemon(True)
                th2.start()

                th3 = threading.Thread(target=getTWM, args=(main, token))
                th3.setDaemon(True)
                th3.start()

                th4 = threading.Thread(target=getCMPOTW, args=(main, token))
                th4.setDaemon(True)
                th4.start()

                th5 = threading.Thread(target=getCMTWM, args=(main, token))
                th5.setDaemon(True)
                th5.start()

                th21 = threading.Thread(target=updatePOCW_DB, args=(main, token))
                th21.setDaemon(True)
                th21.start()

                th22 = threading.Thread(target=getCWSWM, args=(main, token))
                th22.setDaemon(True)
                th22.start()

                th32 = threading.Thread(target=getCWM, args=(main, token))
                th32.setDaemon(True)
                th32.start()

                th33 = threading.Thread(target=getCMPOCW, args=(main, token))
                th33.setDaemon(True)
                th33.start()

                th34 = threading.Thread(target=getCMCWM, args=(main, token))
                th34.setDaemon(True)
                th34.start()




            main.login.close()

            main.show()


            # versionCheck(main,token)

        elif login_access.status_code == 401:
            # print('kkkk')
            main.messageBox = QMessageBox()
            main.messageBox.setIcon(QMessageBox.Critical)
            main.messageBox.setWindowTitle('Error')
            main.messageBox.setWindowFlags(Qt.WindowStaysOnTopHint)
            main.messageBox.setText('UserName or Password is Invalid!')
            main.messageBox.exec_()

            # main.mb = QMessageBox()
            # main.mb.setWindowFlags(Qt.WindowStaysOnTopHint)
            # main.mb.setText('Invalid user Or password')
            # main.mb.exec()



        else:
            print(traceback.print_exc())



    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())



def versionCheck(main):
    try:
        get_API_config(main)
        payload = {
            "version": "3.0.0"

        }
        login_url = main.FastApiURL + '/v3/scanrisk-version'

        # login_url = main.FastApiURL + f'/dlogin?username={User}&password={password}'
        # print("login_url:", login_url)
        # print("payload : ", payload)
        login_access = requests.post(login_url, json=payload)
        # print(login_access.text)
        # logging.info(login_access.text)
        print("status..... code", login_access.status_code)
        if login_access.status_code == 200:
            # data = login_access.json()

            main.login.show()
            # print(data)



        # elif login_access.status_code == 401:
        else:
            main.messageBox = QMessageBox()
            # main.messageBox.setWindowIcon(QIcon('../Resources/icons/alert-circle.svg'))
            main.messageBox.setIcon(QMessageBox.Critical)
            main.messageBox.setWindowFlags(Qt.WindowStaysOnTopHint)
            main.messageBox.setText('Please Update your Version!')
            main.messageBox.setWindowTitle('Update Verion')
            main.messageBox.addButton(QPushButton('Yes'), QMessageBox.YesRole)
            main.messageBox.addButton(QPushButton('No'), QMessageBox.RejectRole)
            main.messageBox.buttonClicked.connect(main.DownloadVersionClicked)
            main.messageBox.exec_()
    except:
        # print(traceback.print_exc())
        main.messageBox = QMessageBox()
        main.messageBox.setIcon(QMessageBox.Critical)
        main.messageBox.setWindowTitle('Error')
        main.messageBox.setWindowFlags(Qt.WindowStaysOnTopHint)
        main.messageBox.setText('Server Error..!! ')
        main.messageBox.show()





def DownloadVersionClicked(main,button):
    if (button.text() == 'Yes'):
        get_API_config(main)

        login_url = main.FastApiURL + '/download'

        response = requests.post(login_url, stream=True)

        loc1 = os.getcwd().split('Application')
        defaultDir = os.path.join(loc1[0])

        save = QFileDialog.getSaveFileName(main, 'Download file', defaultDir,"ZIP (*.zip)")[0]
        with open(save, "wb") as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)

    else:
        pass


# def getPositionPOTW(main,token):
#     get_API_config(main)
#     #####GetPosition API#############################
#
#     DB_url = main.FastApiURL + '/dbpotw'
#     DBheaders = {
#         'Content-Type': 'application/json',
#         'authToken': main.token
#     }
#     req = requests.request("POST", DB_url, headers=DBheaders)
#     data = req.json()
#     # print(type(data))
#
#
#
#     st = time.time()
#     # a = eval(data)
#     # print(data['data'])
#     # data23=list(itertools.chain(*data['data']))
#     # print(data23)
#
#     df = pd.DataFrame(data['data']).to_numpy()
#
#     # df[:,12]=np.arange(df.shape[0])
#     # print(df,df.shape)
#     et = time.time()
#     main.sgopenPosPOTW.emit(df)
#     # print(df[:,13])
#
#
#     # print(df.shape)
#     print('timennn', et - st)
#
#     # Position=data['data']
#     # print('position = ',Position)
#     # print('data',Position[0])
#     # print(Position)
#
#     # for pos in data['data'][0]:
#     #     print(pos)
#
#         # main.sgopenPosPOTW.emit(pos)
#
#     # data_db=requests.get()





def update_TerminalMaster(main,token):
    url = main.FastApiURL + '/v3/terminals'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)
    for pos in data['data']:
        p=list(pos.values())
        loadTerminalMaster(main,p)
        # print('p',p)
        # main.sg_terminalData.emit(p)

    # print('TWSWMdone')



    # df = pd.DataFrame(data['data']).to_numpy()
    # df[:, 12] = np.arange(df.shape[0])
    # print(df,df.shape)
    et = time.time()

    # print(df[:,13])

    # print(df.shape)
    # print('timennn', et - st)

def getTWSWM(main,token):
    TWSWM_url = main.FastApiURL + '/v3/dbtwswm'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", TWSWM_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)
    for pos in data['data']:
        p=list(pos.values())

        main.sgDB_TWSWM.emit(p)

    # print('TWSWMdone')



    # df = pd.DataFrame(data['data']).to_numpy()
    # df[:, 12] = np.arange(df.shape[0])
    # print(df,df.shape)
    et = time.time()

    # print(df[:,13])

    # print(df.shape)
    # print('timennn', et - st)
def getCWSWM(main,token):
    CWSWM_url = main.FastApiURL + '/v3/dbcwswm'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", CWSWM_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)
    for pos in data['data']:
        p=list(pos.values())

        main.sgDB_CWSWM.emit(p)

    # print('TWSWMdone')



    # df = pd.DataFrame(data['data']).to_numpy()
    # df[:, 12] = np.arange(df.shape[0])
    # print(df,df.shape)
    et = time.time()

    # print(df[:,13])

    # print(df.shape)
    # print('timennn', et - st)


def getCMPOTW(main,token):
    CMPOTW_url = main.FastApiURL + '/v3/dbCMpotw'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", CMPOTW_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)
    for pos in data['data']:
        p = list(pos.values())

        main.sgDB_CMPOTW.emit(p)
def getCMPOCW(main,token):
    CMPOCW_url = main.FastApiURL + '/v3/dbCMpocw'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", CMPOCW_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)
    for pos in data['data']:
        p = list(pos.values())

        main.sgDB_CMPOCW.emit(p)

def getCMTWM(main,token):
    CMTWM_url = main.FastApiURL + '/v3/dbCMtwm'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", CMTWM_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)
    for pos in data['data']:
        p = list(pos.values())

        main.sgDB_CMTWM.emit(p)



def getTWM(main,token):
    TWM_url = main.FastApiURL + '/v3/dbtwm'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", TWM_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)

    for pos in data['data']:
        p = list(pos.values())

        main.sgDB_TWM.emit(p)

    print('TWMdone')
    # print('timennn', et - st)
def getCWM(main,token):
    CWM_url = main.FastApiURL + '/v3/dbcwm'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", CWM_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)

    for pos in data['data']:
        p = list(pos.values())

        main.sgDB_CWM.emit(p)

    print('CWMdone')
    # print('timennn', et - st)
def getCMCWM(main,token):
    CWM_url = main.FastApiURL + '/v3/dbCMcwm'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", CWM_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)

    for pos in data['data']:
        p = list(pos.values())

        main.sgDB_CMCWM.emit(p)

    print('CMCWMdone')
    # print('timennn', et - st)


def update_contract_FOletest(main,token):
    try:
        st=time.time()
        DB_url = main.FastApiURL + '/v1/dbcontractFO'
        # DBheaders = {
        #     'Content-Type': 'application/json',
        #     'authToken': token
        # }
        response = requests.post(DB_url, stream=True)

        loc1 = os.getcwd().split('Application')
        save = os.path.join(loc1[0],'Downloads','contract_fo.csv')
        # d = os.path.join(loc1[0],'Downloads')


        # save = QFileDialog.getSaveFileName(main, 'Download file', defaultDir, "CSV (*.csv)")[0]
        with open(save, "wb") as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)




        # main.fo_contract=np.loadtxt(save, skiprows=1, delimiter=',')
        fo_contract=pd.read_csv(save,low_memory=False,header=None,skiprows=1)


        main.fo_contract = fo_contract.to_numpy()

        et = time.time()
        print('time', et - st)

        # req = requests.request("POST", DB_url, headers=DBheaders)
        # data = req.json()
        # # print(type(data['data']))
        # a=eval(data['data'])
        #
        # # print('aaaaaaaaaaaa',a,type(a))
        #
        # main.fo_contract = pd.DataFrame(a).values
        #
        # et=time.time()
        # # data23 = list(itertools.chain(*data['data']))
        #
        # # print('thearray',len(a))
        # print('time',et-st)
        # print('thearray',main.fo_contract.shape)

        # data = {'Exchange', 'Segment', 'Token' 'symbol' 'Stock_name',
        #         'instrument_type' 'exp' 'strike_price' 'option_type',
        #         'asset_token', 'tick_size', 'lot_size', 'strike1',
        #         'Multiplier', 'FreezeQty', 'pbHigh', 'pbLow',
        #         'futureToken', 'close', 'ltp', 'bid', 'ask', 'oi',
        #         'prev_day_oi', 'iv', 'delta', 'gamma', 'theta', 'vega',
        #         'theoritical_price', 'PPR', 'moneyness', 'Volume', 'amt',
        #         'Avg1MVol', 'ATP', 'strike_diff', 'expiry_type', 'cpToken',
        #         'days2Exp', 'moneyness2', '3_last', '2_last', 'last'}

        # data23 = list(itertools.chain(*data['data']))




        # data23 = list(itertools.chain(*data['data']))
        # print(data23)
        # print(type(data23))

        # st = time.time()
        #
        # for pos in data['data']:
        #     p = list(pos.values())
        #
        #     main.sgopenPosPOTW.emit(p)
        #
        # print('POTWdone')
    except:
        print(traceback.print_exc())


def update_contract_FOold(main):
    loc1 = os.getcwd().split('Application')
    save = os.path.join(loc1[0], 'Downloads', 'contract_fo.csv')
    fo_contract = pd.read_csv(save, low_memory=False, header=None, skiprows=1)


    main.fo_contract = fo_contract.to_numpy()




def updatePOTW_DB(main,token):

    DB_url = main.FastApiURL + '/v3/dbpotw'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", DB_url, headers=DBheaders)
    data = req.json()

    DBLTP_url = main.FastApiURL + '/v3/dbLTP'
    DBheaders = {
        'Content-Type': 'application/json'
    }
    req = requests.request("POST", DBLTP_url, headers=DBheaders)
    dataLTP = req.json()

    # print(type(dataLTP),dataLTP)

    st = time.time()


    for pos in data['data']:
        p=list(pos.values())
        d=dataLTP.get(str(p[2]))
        if d:
            # print('tt')
            p[10]=d['LTP']

            # (qty * data['LTP']) + netValue
            p[11]=(p[15]*d['LTP'])+p[16]

            p[24]=d['IV']
            p[25]=d['Delta'] *p[15]
            p[26]=d['Theta']*p[15]
            p[27]=d['Gama']*p[15]
            p[28]=d['Vega']*p[15]

            if (p[3] in ['FUTIDX','FUTSTK']):
                p[21]=p[11]
            else:
                p[22]=p[11]

        main.sgopenPosPOTW.emit(p)

    print('POTWdone')



    # print(df.shape)
    # print('timennn', et - st)
def updatePOCW_DB(main,token):
    try:

        DB_url = main.FastApiURL + '/v3/dbpocw'
        DBheaders = {
            'Content-Type': 'application/json',
            'authToken': token
        }
        req = requests.request("POST", DB_url, headers=DBheaders)
        data = req.json()

        DBLTP_url = main.FastApiURL + '/v3/dbLTP'
        DBheaders = {
            'Content-Type': 'application/json'
        }
        req = requests.request("POST", DBLTP_url, headers=DBheaders)
        dataLTP = req.json()

        # print(type(dataLTP),dataLTP)


        for pos in data['data']:
            p=list(pos.values())
            d=dataLTP.get(str(p[2]))
            if d:
                # print('tt')
                p[10]=d['LTP']

                # (qty * data['LTP']) + netValue
                p[11]=(p[15]*d['LTP'])+p[16]

                p[21]=d['IV']
                p[22]=d['Delta'] *p[15]
                p[23]=d['Theta']*p[15]
                p[24]=d['Gama']*p[15]
                p[25]=d['Vega']*p[15]

                if (p[3] in ['FUTIDX','FUTSTK']):
                    p[17]=p[11]
                else:
                    p[18]=p[11]

            main.sgDB_POCW.emit(p)

        print('POCWdone')
    except:
        print(traceback.print_exc())



    # print(df.shape)
    # print('timennn', et - st)
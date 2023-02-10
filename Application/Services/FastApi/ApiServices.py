import itertools
import threading

import numpy as np
import json
import requests
import sys
import traceback
import logging
from Application.Utils.configReader import get_API_config,writeAPIdetails
import time
import pandas as pd


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
        login_url = main.FastApiURL + '/login'

        # login_url = main.FastApiURL + f'/dlogin?username={User}&password={password}'
        print("login_url:", login_url)
        print("payload : ", payload)
        login_access = requests.post(login_url, json=payload)
        logging.info(login_access.text)
        print(login_access.text)

        print("status code",login_access.status_code)
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

            th1=threading.Thread(target=updatePOTW_DB,args=(main,token))
            th1.start()

            main.SioClient.startSocket(token)
            main.login.hide()
            main.show()

            # updatePOTW_DB(main,token)

            # getPositionPOTW(main,token)
            # # getTWSWM(main,token)
            #
            #

            # main.timergetPOTW.start()








            # else:
            #     pass
            #     # main.login.pbLogin.setEnable(True)



        else:
            print(traceback.print_exc())
           # main.login.pbLogin.setEnabled(True)
           #  logging.info(str(login_access.text).replace('\n', '\t\t\t\t'))
        # main.login.hide()
        # main.show()



    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())


def getPositionPOTW(main,token):
    get_API_config(main)
    #####GetPosition API#############################

    DB_url = main.FastApiURL + '/dbpotw'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': main.token
    }
    req = requests.request("POST", DB_url, headers=DBheaders)
    data = req.json()
    # print(type(data))



    st = time.time()
    # a = eval(data)
    # print(data['data'])
    # data23=list(itertools.chain(*data['data']))
    # print(data23)

    df = pd.DataFrame(data['data']).to_numpy()

    # df[:,12]=np.arange(df.shape[0])
    # print(df,df.shape)
    et = time.time()
    main.sgopenPosPOTW.emit(df)
    # print(df[:,13])


    # print(df.shape)
    print('timennn', et - st)

    # Position=data['data']
    # print('position = ',Position)
    # print('data',Position[0])
    # print(Position)

    # for pos in data['data'][0]:
    #     print(pos)

        # main.sgopenPosPOTW.emit(pos)

    # data_db=requests.get()


def getTWSWM(main,token):
    TWSWM_url = main.FastApiURL + '/dbtwswm'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", TWSWM_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()
    # a = eval(data)
    print(data['data'])
    # data23 = list(itertools.chain(*data['data']))
    # print(data23)

    df = pd.DataFrame(data['data']).to_numpy()
    # df[:, 12] = np.arange(df.shape[0])
    # print(df,df.shape)
    et = time.time()
    main.sgDB_TWSWM.emit(df)
    # print(df[:,13])

    # print(df.shape)
    print('timennn', et - st)

def getTWM(main,token):
    TWM_url = main.FastApiURL + '/dbtwm'
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

    df = pd.DataFrame(data['data']).to_numpy()
    # df[:, 12] = np.arange(df.shape[0])
    # print(df,df.shape)
    et = time.time()
    main.sgDB_TWM.emit(df)
    # print(df[:,13])

    # print(df.shape)
    print('timennn', et - st)


def updatePOTW_DB(main,token):

    DB_url = main.FastApiURL + '/dbpotw'
    DBheaders = {
        'Content-Type': 'application/json',
        'authToken': token
    }
    req = requests.request("POST", DB_url, headers=DBheaders)
    data = req.json()
    # print(type(data))

    st = time.time()


    for pos in data['data']:
        p=list(pos.values())

        main.sgopenPosPOTW.emit(p)

    print('done')



    # print(df.shape)
    # print('timennn', et - st)
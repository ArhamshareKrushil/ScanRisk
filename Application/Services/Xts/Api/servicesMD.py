import traceback
import sys
import logging
import json
import datetime
import time
from Application.Utils.getMasters import getMaster, shareContract
import  requests

from Application.Utils.configReader import writeMD,refresh
from Application.Utils.VAR.getVarFile import latest_var
import numpy as np





def subscribeToken(self, token, seg, streamType=1501):
    try:
        segment= 0
        if (seg == 'NSEFO'):
            segment = 2
        elif (seg == 'NSECM'):
            segment = 1
        ## ****** CD PENDING
        # print('segment',segment)
        sub_url = self.URL + '/marketdata/instruments/subscription'
        payloadsub = {"instruments": [{"exchangeSegment": segment, "exchangeInstrumentID": token}],
                      "xtsMessageCode": streamType}

        payloadsubjson = json.dumps(payloadsub)

        # print(payloadsubjson)
        req = requests.request("POST", sub_url, data=payloadsubjson, headers=self.MDheaders)






        if ('subscribed successfully' in req.text or 'Already Subscribed' in req.text):
            if('subscribed successfully' in req.text):
                data = req.json()
                try:
                    data2 = json.loads(data['result']['listQuotes'][0])
                except:
                    print(traceback.print_exc())
                    # data2 = json.loads(data['result']['listQuotes'])
                print('in sub',data2)


                EXCH = data2['ExchangeSegment']
                token = data2['ExchangeInstrumentID']
                bid = data2['AskInfo']['Price']
                bidQ = data2['BidInfo']['Size']
                ask = data2['AskInfo']['Price']
                askQ = data2['BidInfo']['Size']
                LTP = data2['LastTradedPrice']
                pc1 = '0.0'
                pc = data2['PercentChange']
                OPEN = data2['Open']
                HIGH = data2['High']
                LOW = data2['Low']
                CLOSE = data2['Close']
                Volume = data2['TotalValueTraded']

                d1 = {"Exch": EXCH, "Token": int(token), "Bid": bid, "BQ": bidQ, "Ask": ask, "AQ": askQ,
                      "LTP": LTP, "%CH": pc, "OPEN": OPEN, "HIGH": HIGH, "LOW": LOW, "CLOSE": CLOSE, 'Volume': Volume}




                try:
                    self.LiveFeed.sgNPFSub.emit(d1)
                except:
                    print('error ,self.LiveFeed.sgNPFrec.emit', self)

        else:
            logging.error(req.text)

        ####################### database working passage deleted if required retrive from backup ##################
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())


def unSubscription_feed(self, token, seg, streamType=1501):
    try:
        if (seg == 'NSEFO'):
            segment = 2
        elif (seg == 'NSECM'):
            segment = 1
        ## ****** CD PENDING
        sub_url = self.URL + '/marketdata/instruments/subscription'
        payloadsub = {"instruments": [{"exchangeSegment": segment, "exchangeInstrumentID": token}],
                      "xtsMessageCode": streamType}
        payloadsubjson = json.dumps(payloadsub)
        req = requests.request("PUT", sub_url, data=payloadsubjson, headers=self.MDheaders)

        logging.info(req.text)
        print(req.text)

        if ('subscribed successfully' in req.text or 'Already Subscribed' in req.text):
            pass

        else:
            logging.error(req.text)

        ####################### database working passage deleted if required retrive from backup ##################
    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())

def login(main):
    try:
        print("inside serviceMD login")
#        main.login.pbLogin.setEnabled(False)
       # main.login.label.append('Logging in to Marketdata API..')
        refresh(main)
        payload = {
            "secretKey": main.MDSecret,
            "appKey": main.MDKey,
            "source": main.Source
        }
        login_url = main.URL + '/marketdata/auth/login'
        print("login_url:", login_url)
        print("payload : ", payload)
        login_access = requests.post(login_url, json=payload)
        logging.info(login_access.text)
        print(login_access.text)

        print("status code")
        if login_access.status_code == 200:
            data = login_access.json()
            result = data['result']
            if data['type'] == 'success':
                a = 'successfull'
                result = data['result']

                token = result['token']
                userID = result['userID']
                writeMD(token, userID)
                # main.login.updateMDstatus(data['type'])
                # main.login.label.append('MARKETDATA API Logged In.\nDownloadin contract masters...')
                # main.login.updateIAstatus(data['type'])
                main.fo_contract, main.eq_contract, main.cd_contract, main.contract_heads = getMaster(main,
                    main.BOD.cbCmaster.isChecked())

                main.contract_fo1 = main.fo_contract[np.where(main.fo_contract[:, 1] != 'x')]
                # print(fltr)
                # main.unique_symbols = np.unique(main.contract_fo1[:, 3])
                # main.timerSCN.start()

                # main.createSCN()


                shareContract(main)
                main.BOD.lbMDStatus.setText('Logged in successfully')




            else:
                pass
                # main.login.pbLogin.setEnable(True)

        else:
           # main.login.pbLogin.setEnabled(True)
            logging.info(str(login_access.text).replace('\n', '\t\t\t\t'))


    except:
        logging.error(sys.exc_info()[1])
        print(traceback.print_exc())

def getQuote(self, token, seg, streamType):
    try:
        if (seg == 'NSEFO'):
            segment = 2
        elif (seg == 'NSECM'):
            segment = 1
        quote_url = self.URL + '/marketdata/instruments/quotes'
        payload_quote = {"instruments": [{"exchangeSegment": segment,"exchangeInstrumentID": token}],"xtsMessageCode": streamType,"publishFormat": "JSON"}
        quote_json = json.dumps(payload_quote)
        data = requests.request("POST", quote_url, data=quote_json, headers=self.MDheaders)
        data1 = data.json()
        d = data1['result']['listQuotes'][0]
        data2 = json.loads(d)

        return data2

    except:
        print(sys.exc_info(),'get Quote')

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

Ymd_today = datetime.datetime.today().strftime("%Y%m%d")
loc1 = getcwd().split('Application')
downloadLoc = path.join(loc1[0], 'Downloads','SPAN',Ymd_today)

spanValueList = [".s"]
def latest_span(main):
    try:

        print('new_span')
        # Ymd_today = datetime.datetime.today().strftime("%Y%m%d")
        print("TODAY:",Ymd_today)

        # loc1 = os.getcwd().split('Application')
        # downloadLoc = os.path.join(loc1[0], 'Downloads', 'SPAN', Ymd_today)

        if (os.path.exists(downloadLoc)):
            pass
        else:
            os.makedirs(downloadLoc)

        Ymd_yesterday = main.prevDate.strftime("%Y%m%d")
        print("YESTEDAY:",Ymd_yesterday)
        user_agent = 'Mozilla/5.0'
        headers = {'User-Agent': user_agent}
        url = SPAN_FILE_URL + Ymd_today
        # take selected span type
        spanValue = main.BOD.cbSpan.currentText()
        print(spanValue)
        print('getting_url of span file and downloading..........')

        # BUILD url PATH
        url,final_file = builFileURL(main,spanValue,url,Ymd_today,Ymd_yesterday)

        print("URL:", url)
        # DOWNLOAD FILE
        # lbl_spanError
        res = requests.get(url, headers=headers)
        print("status  :", res.status_code)
        if(res.status_code != 200):
            main.BOD.lbl_spanError.setText("File not found or internal server error")
        else:
            # DOWNLOAD ZIP FILE
            spanLOC = path.join(downloadLoc, "span.zip")
            with open(spanLOC, 'wb+') as f:
                f.write(res.content)
            f.close()
            print("zipped nsccl downloaded.....")

            unzipSpan(main,final_file, downloadLoc,spanLOC)
            parseSpan_spread(main,downloadLoc)
            parseSpan_margin(main,downloadLoc)
            parseSpan_calSpred(main, downloadLoc)
            getSpanMargin(main,downloadLoc)
    except:
        print(traceback.print_exc())


def getSpanMargin(main,downloadLoc):

        # loc1 = os.getcwd().split('Application')
        # downloadLoc = os.path.join(loc1[0], 'Downloads', 'SPAN',)

        # a = QObject()
        # fo_contract, eq_contract, cd_contract, contract_heads = getMaster(a, False)

        rrr = time.time()

        spanFile = os.path.join(downloadLoc, 'span.csv')
        span1 = pd.read_csv(spanFile,
                            names=['ins', 'symbol', 'exp', 'strk', 'opt', 'close', 's1', 's2', 's3', 's4', 's5', 's6',
                                   's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 'delta'])

        contract = pd.DataFrame(main.fo_contract[:, [2, 5, 3, 6, 7, 8, 12]],
                                columns=['Token', 'ins', 'symbol', 'exp', 'strk', 'opt', 'strk1'])
        span1.iloc[:, 4] = span1.iloc[:, 4].fillna(' ')
        span1.iloc[:, 3] = span1.iloc[:, 3].fillna(0.0)
        span1.iloc[:, 2] = span1.iloc[:, 2].astype(str)

        main.spanMargin = pd.merge(contract, span1, how='left', left_on=['symbol', 'exp', 'strk1', 'opt'],
                     right_on=['symbol', 'exp', 'strk', 'opt']).to_numpy()

        # ccc= pd.merge(contract, span1, how='left', left_on=['symbol', 'exp', 'strk1', 'opt'],
        #                            right_on=['symbol', 'exp', 'strk', 'opt']).to_csv('d:/scnMRG.csv')

        # rrr1 = time.time()
        # print(rrr1 - rrr)


def builFileURL(self,spanValue,url,Ymd_today,Ymd_yesterday):
    if(spanValue == 'latest'):
        user_agent = 'Mozilla/5.0'
        headers = {'User-Agent': user_agent}
        url1 = 'https://archives.nseindia.com/archives/nsccl/span/nsccl.' + Ymd_today + '.i1.zip'
        url2 = 'https://archives.nseindia.com/archives/nsccl/span/nsccl.' + Ymd_today + '.i2.zip'
        url3 = 'https://archives.nseindia.com/archives/nsccl/span/nsccl.' + Ymd_today + '.i3.zip'
        url4 = 'https://archives.nseindia.com/archives/nsccl/span/nsccl.' + Ymd_today + '.i4.zip'
        url5 = 'https://archives.nseindia.com/archives/nsccl/span/nsccl.' + Ymd_today + '.i5.zip'
        url6 = 'https://archives.nseindia.com/archives/nsccl/span/nsccl.' + Ymd_today + '.s.zip'
        url0 = 'https://archives.nseindia.com/archives/nsccl/span/nsccl.' + Ymd_yesterday + '.s.zip'
        if (requests.get(url6+'.'+'', headers=headers).status_code == 200):

            url += '.s.zip'
            final_file = Ymd_today + '.s'
        elif (requests.get(url5, headers=headers).status_code == 200):

            url += '.i5.zip'
            final_file = Ymd_today + '.i05'
        elif (requests.get(url4, headers=headers).status_code == 200):

            url += '.i4.zip'
            final_file = Ymd_today + '.i04'
        elif (requests.get(url3, headers=headers).status_code == 200):

            url += '.i3.zip'
            final_file = Ymd_today + '.i03'
        elif (requests.get(url2, headers=headers).status_code == 200):

            url += '.i2.zip'
            final_file = Ymd_today + '.i02'
        elif (requests.get(url1, headers=headers).status_code == 200):

            url += '.i1.zip'
            final_file = Ymd_today + '.i01'
        else:
            url = SPAN_FILE_URL + Ymd_yesterday + '.s.zip'
            final_file = Ymd_yesterday + '.s'
    else:
        if (spanValue == '.s'):
            url += '.s.zip'
            final_file = Ymd_today + '.s'
        elif (spanValue == 'i5'):
            url += '.i5.zip'
            final_file = Ymd_today + '.i05'
        elif (spanValue == 'i4'):
            url += '.i4.zip'
            final_file = Ymd_today + '.i04'
        elif (spanValue == 'i3'):
            url += '.i3.zip'
            final_file = Ymd_today + '.i03'
        elif (spanValue == 'i2'):
            url += '.i2.zip'
            final_file = Ymd_today + '.i02'
        elif (spanValue == 'i1'):
            url += '.i1.zip'
            final_file = Ymd_today + '.i01'
        else:
            url = SPAN_FILE_URL + Ymd_yesterday + '.s.zip'
            final_file = Ymd_yesterday + '.s'

    return url,final_file

def unzipSpan(self,final_file, downloadLoc,spanLOC):
    try:
        Ymd_today = datetime.datetime.today().strftime("%Y%m%d")
        # Ymd_yesterday = self.yesterday.strftime("%Y%m%d").upper()

        zf = ZipFile(spanLOC, 'r')
        zf.extractall(downloadLoc)
        zf.close()
        print("unzipped nsccl success.............")

        fname = 'nsccl.' + final_file + '.spn'
        print(fname)

        if path.isfile(path.join(downloadLoc,"span.spn")):
            os.remove(path.join(downloadLoc,"span.spn"))
        print("nsccl file removed successfull..............")

        pathFile =  path.join(downloadLoc, fname)
        new_file_name = path.join(downloadLoc,'span.spn')

        #
        # print('pathFile',pathFile)
        # print('new_file_name',new_file_name)

        os.rename(pathFile, new_file_name)
        print(" nsccl Rename successfull..................")
    except:
        print(traceback.print_exc())

def parseSpan_calSpred(self,downloadLoc):
    try:

        # Ymd_today = datetime.datetime.today().strftime('%Y%m%d')
        # dmY_today = datetime.datetime.today().strftime('%d%m%Y')
        # dmY_yesterdaye = self.yesterday.strftime('%d%m%Y')
        # Ydm_yesterday = self.yesterday.strftime('%Y%m%d')


        tree = elementTree.parse (path.join(downloadLoc,"span.spn"))
        root = tree.getroot()
        spanCalSpred = path.join(downloadLoc, "calspred.csv")
        with open(spanCalSpred, 'w') as abcd:
            for decade in (root.iter("ccDef")):
                for i, year in enumerate(decade.findall("./dSpread")):
                    rb1 = str(year[0].text)
                    rb2 = str(year[2][1].text)
                    rb3 = str(year[3][0].text)
                    rb4 = str(year[3][1].text)
                    rb5 = str(year[4][1].text)

                    print(str(year[0].text), str(year[2][1].text), str(year[3][0].text), str(year[3][1].text), str(year[4][1].text))
                    abcd.write("%s,%s,%s,%s,%s\n" % (rb1, rb2, rb3, rb4, rb5))

        print("calspred created..........")
        abcd.close()
    except:
        print(traceback.print_exc())

def parseSpan_spread(self,downloadLoc):
    try:

        # Ymd_today = datetime.datetime.today().strftime('%Y%m%d')
        # dmY_today = datetime.datetime.today().strftime('%d%m%Y')
        # dmY_yesterdaye = self.yesterday.strftime('%d%m%Y')
        # Ydm_yesterday = self.yesterday.strftime('%Y%m%d')


        tree = elementTree.parse (path.join(downloadLoc,"span.spn"))
        root = tree.getroot()
        spanSomr = path.join(downloadLoc, "somr.csv")
        with open(spanSomr, 'w') as abcd:
            for decade in (root.iter("ccDef")):
                # if(i>30):
                #     continue
                aa = str(decade[0].text)
                bb = str(decade[26][0][1][1].text)
                abcd.write('%s,%s\n' % (aa, bb))
        print("somr created..........")
        abcd.close()
    except:
        print(traceback.print_exc())


def parseSpan_margin(self,downloadLoc):
    try:
        tree = elementTree.parse(path.join(downloadLoc, "span.spn"))
        root = tree.getroot()
        spanSomr = path.join(downloadLoc, "span.csv")
        with open(spanSomr, 'w') as abcd:
            for decade in root.iter("futPf"):
                name = str(decade[1].text)
                if 'NIFTY' in name:
                    IT = "FUTIDX"
                else:
                    IT = "FUTSTK"

                for year in decade.findall("./fut"):
                    # print(name)
                    exp = year[1].text
                    ra_17 = year[2].text
                    ra_1 = year[12][1].text
                    ra_2 = year[12][2].text
                    ra_3 = year[12][3].text
                    ra_4 = year[12][4].text
                    ra_5 = year[12][5].text
                    ra_6 = year[12][6].text
                    ra_7 = year[12][7].text
                    ra_8 = year[12][8].text
                    ra_9 = year[12][9].text
                    ra_10 = year[12][10].text
                    ra_11 = year[12][11].text
                    ra_12 = year[12][12].text
                    ra_13 = year[12][13].text
                    ra_14 = year[12][14].text
                    ra_15 = year[12][15].text
                    ra_16 = year[12][16].text
                    ra_18 = year[12][17].text
                    OT = ("")
                    SP = ("")
                    abcd.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                        IT, name, exp, SP, OT, ra_17, ra_1, ra_2, ra_3, ra_4, ra_5, ra_6, ra_7, ra_8, ra_9, ra_10,
                        ra_11, ra_12, ra_13, ra_14, ra_15, ra_16, ra_18))



            for dec in root.iter("oopPf"):
                name = dec[1].text

                for ser in dec.iter("series"):
                    exp = ser[0].text
                    # IT = str(ser[10].tag)
                    if 'NIFTY' in name:
                        IT = "OPTIDX"
                    else:
                        IT = "OPTSTK"

                    for opt in ser.findall("opt"):
                        OT = opt[1].text
                        OT = OT + 'E'
                        SP = opt[2].text
                        # print(name, exp,OT,SP)

                        ara_17 = opt[3].text
                        ara_1 = opt[6][1].text
                        ara_2 = opt[6][2].text
                        ara_3 = opt[6][3].text
                        ara_4 = opt[6][4].text
                        ara_5 = opt[6][5].text
                        ara_6 = opt[6][6].text
                        ara_7 = opt[6][7].text
                        ara_8 = opt[6][8].text
                        ara_9 = opt[6][9].text
                        ara_10 = opt[6][10].text
                        ara_11 = opt[6][11].text
                        ara_12 = opt[6][12].text
                        ara_13 = opt[6][13].text
                        ara_14 = opt[6][14].text
                        ara_15 = opt[6][15].text
                        ara_16 = opt[6][16].text
                        ara_18 = opt[6][17].text
                        abcd.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                            IT, name, exp, SP, OT, ara_17, ara_1, ara_2, ara_3, ara_4, ara_5, ara_6, ara_7, ara_8,
                            ara_9, ara_10, ara_11, ara_12, ara_13, ara_14, ara_15, ara_16, ara_18))

        abcd.close()
        print("span coppied sucessfully ................")
    except:
        print(traceback.print_exc())




def process_span(main):
    getSpanMargin(main, downloadLoc)






























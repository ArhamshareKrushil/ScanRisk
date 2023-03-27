import struct




def process(self,Compressed_Packet,Start_Pointof_Record,End_Pointof_Record):
    # print('slj',Start_Pointof_Record)
    IndexName,F=struct.unpack('!21sc',Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record+22])
    IndexName = IndexName.decode('utf-8').rstrip()
    if IndexName in ['Nifty Bank','Nifty 50','India VIX']:

        IndexName, FILLER1, IndexValue, HighIndexValue, LowIndexValue, OpeningIndex, \
        ClosingIndex, PercentChange, YearlyHigh, YearlyLow, NoOfUpmoves, NoOfDownmoves, \
        MarketCapitalisation, NetChangeIndicator, FILLER = struct.unpack('!21sclllllllllldcc',
                                                                         Compressed_Packet[Start_Pointof_Record:
                                                                                           End_Pointof_Record])
        # if(b"Nifty Bank" in IndexName):
        IndexValue=IndexValue/100
        IndexName=IndexName.decode('utf-8').rstrip()


        output = {'ID': 7207,'Exch':1,'IndexName': IndexName, 'IndexValue': IndexValue, 'HighIndexValue': HighIndexValue,
                  'LowIndexValue': LowIndexValue, 'OpeningIndex': OpeningIndex,
                  'ClosingIndex': ClosingIndex, 'PercentChange': PercentChange,
                  'YearlyHigh': YearlyHigh, 'YearlyLow': YearlyLow, 'NoOfUpmoves': NoOfUpmoves,
                  'NoOfDownmoves': NoOfDownmoves,
                  'MarketCapitalisation': MarketCapitalisation, 'NetChangeIndicator': NetChangeIndicator, 'FILLER': FILLER}

    else:
        output={}
    return output
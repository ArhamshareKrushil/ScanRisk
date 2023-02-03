import struct




def process(self,Decoded_Packet,Start_Pointof_Record,End_Pointof_Record):

    Token=struct.unpack('!h',Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record+2])[0]
    # print('token',Token)
    if Token in self.FinalList['NSECM']:

        Token, MarketType, FillPrice, FillVolume, MarketIndexValue \
            = struct.unpack('!hhlll',
                            Decoded_Packet[Start_Pointof_Record:
                                           End_Pointof_Record])

        ltp = FillPrice / 100.0
        output = {'ID': 7202, "EXCH": 1, 'Token': Token, 'MarketType': MarketType, 'LTP': ltp,
                  'TradedQty': FillVolume, 'fillVolume': ltp * FillVolume, 'MarketIndexValue': MarketIndexValue}


    else:
        output={}

    return output
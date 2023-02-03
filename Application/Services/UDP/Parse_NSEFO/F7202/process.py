import struct



def process(self,Decoded_Packet,Start_Pointof_Record,End_Pointof_Record):


    #
    # Token, MarketType, FillPrice, FillVolume, OpenInterest, \
    # Day_Hi_OI, Day_Lo_OI = struct.unpack('!lhlllll',
    #                                      Decoded_Packet[Start_Pointof_Record:
    #                                                     End_Pointof_Record])
    #
    # ltp = FillPrice / 100.0
    # output = {'ID': 7202, 'Exch': 2, 'Token': Token, 'MarketType': MarketType, 'LTP': round(ltp, 2),
    #           'FillVolume': FillVolume, 'OpenInterest': OpenInterest,
    #           'Day_Hi_OI': Day_Hi_OI, 'Day_Lo_OI': Day_Lo_OI}

    Token=struct.unpack('!l',Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record+4])[0]

    if Token in self.FinalList['NSEFO']:


        Token, MarketType, FillPrice, FillVolume, OpenInterest, \
        Day_Hi_OI, Day_Lo_OI = struct.unpack('!lhlllll',
                                             Decoded_Packet[Start_Pointof_Record:
                                                            End_Pointof_Record])


        ltp = FillPrice / 100.0
        output = {'ID': 7202,'Exch':2, 'Token': Token, 'MarketType': MarketType, 'LTP': round(ltp,2),
                  'FillVolume': FillVolume, 'OpenInterest': OpenInterest,
                  'Day_Hi_OI': Day_Hi_OI, 'Day_Lo_OI': Day_Lo_OI}

    else:
        output={}



    return output

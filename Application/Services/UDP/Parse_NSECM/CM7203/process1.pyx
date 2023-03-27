import struct




def process(self,Decoded_Packet,Start_Pointof_Record,End_Pointof_Record):
    Token, MarketType, FillPrice, FillVolume, MarketIndexValue \
        = struct.unpack('!hhlll',
                        Decoded_Packet[Start_Pointof_Record:
                                       End_Pointof_Record])

    ltp = FillPrice / 100.0
    output = {'ID': 7202, "EXCH": 1, 'Token': Token, 'MarketType': MarketType, 'FillPrice': ltp,
              'TradedQty': FillVolume, 'fillVolume': ltp * FillVolume, 'MarketIndexValue': MarketIndexValue}
    return output
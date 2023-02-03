import struct
import time
import traceback


def process(self,Decoded_Packet,Start_Pointof_Record,End_Pointof_Record):



        Token, MarketType, FillPrice, FillVolume, OpenInterest, \
        Day_Hi_OI, Day_Lo_OI = struct.unpack('!lhlllll',
                                             Decoded_Packet[Start_Pointof_Record:
                                                            End_Pointof_Record])
        # symbol = self.fo_contract[Token - 35000, 3]
        ltp = FillPrice / 100.0
        output = {'ID': 7202,'Exch':2, 'Token': Token, 'MarketType': MarketType, 'FillPrice': ltp,
                  'FillVolume': FillVolume, 'OpenInterest': OpenInterest,
                  'Day_Hi_OI': Day_Hi_OI, 'Day_Lo_OI': Day_Lo_OI}

        return output

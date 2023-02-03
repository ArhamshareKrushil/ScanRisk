import struct




def process(self,Compressed_Packet,Start_Pointof_Record,End_Pointof_Record):

    IndexName, IndexValue, HighIndexValue, LowIndexValue, OpeningIndex, \
    ClosingIndex, PercentChange, YearlyHigh, YearlyLow, NoOfUpmoves, NoOfDownmoves, \
    MarketCapitalisation, NetChangeIndicator, FILLER = struct.unpack('!21slllllllllldcc',
                                                                     Compressed_Packet[Start_Pointof_Record:
                                                                                       End_Pointof_Record])
    output = {'ID': 7216,'Exch':1,'IndexName': IndexName, 'IndexValue': IndexValue, 'HighIndexValue': HighIndexValue,
              'LowIndexValue': LowIndexValue, 'OpeningIndex': OpeningIndex,
              'ClosingIndex': ClosingIndex, 'PercentChange': PercentChange,
              'YearlyHigh': YearlyHigh, 'YearlyLow': YearlyLow, 'NoOfUpmoves': NoOfUpmoves,
              'NoOfDownmoves': NoOfDownmoves,
              'MarketCapitalisation': MarketCapitalisation, 'NetChangeIndicator': NetChangeIndicator, 'FILLER': FILLER}
    return output
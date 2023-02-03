import struct

def process(self,Compressed_Packet,Start_Pointof_Record):
    Token, InstrumentName, Symbol, Series, ExpiryDate, StrikePrice, OptionType, CALevel, \
    MarketType  , MessageLength,Message = struct.unpack('!l6s10s2sll2shhxxh239s',
                                             Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record + 279])



    output = {'ID': 6511,'Exch':2,'Token': Token, 'InstrumentName': InstrumentName, 'Symbol': Symbol,
              'Series': Series, 'ExpiryDate': ExpiryDate,
              'StrikePrice': StrikePrice, 'OptionType': OptionType,
              'CALevel': CALevel, 'MarketType': MarketType, 'MessageLength': MessageLength,'Message':Message}
    return output

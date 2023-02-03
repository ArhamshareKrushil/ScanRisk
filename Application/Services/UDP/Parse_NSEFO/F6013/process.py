import struct




def process(self,Compressed_Packet,Start_Pointof_Record):
    Symbol, Series, Token, OpeningPrice = struct.unpack('!2s2sll',
                                             Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record + 12])

    output = {'ID': 6013, 'Exch': 2, 'Symbol': Symbol, 'Series': Series, 'Token': Token,
              'OpeningPrice': OpeningPrice}
    return output
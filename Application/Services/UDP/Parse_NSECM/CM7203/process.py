import struct




def process(self,Decoded_Packet,Start_Pointof_Record,End_Pointof_Record):




    IndexName, IndexValue= struct.unpack('!21sl',
                        Decoded_Packet[Start_Pointof_Record:
                                       End_Pointof_Record])

    # ltp = FillPrice / 100.0
    output = {'ID': 7203, "EXCH": 1, 'IndexName': IndexName, 'IndexValue': IndexValue}




    return output
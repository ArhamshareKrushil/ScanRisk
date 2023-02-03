import struct


def process(self,Compressed_Packet,Start_Pointof_Record,End_Pointof_Record):
    # Reserved1, Reserved2, LogTime, MarketType, TransactionCode, NoOfRecords, Reserved3, TimeStamp, \
    # Reserved4, MessageLength = struct.unpack('!2s2sl2shh8sq8sh',
    #                                          Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record + 40])

    Token, CurrentOI = struct.unpack('!ll', Compressed_Packet[Start_Pointof_Record:End_Pointof_Record])



    output = {'ID': 'OI','Exch':2,'Token': Token, 'CurrentOI': CurrentOI}
    return output


    # OI=[]
    # OPEN_INTEREST_sp = Start_Pointof_Record + 40
    # for oi in range(NoOfRecords):
    #     OPEN_INTEREST_ep = OPEN_INTEREST_sp+8
    #     TokenNo, CurrentOI = struct.unpack('!ll', Compressed_Packet[OPEN_INTEREST_sp:OPEN_INTEREST_ep])
    #     OPEN_INTEREST_sp = OPEN_INTEREST_ep
    #     OPEN_INTEREST_output = {'TokenNo': TokenNo, 'CurrentOI': CurrentOI}
    #     OI.append(OPEN_INTEREST_output)
    #     # print(OPEN_INTEREST_output)
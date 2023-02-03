import struct



def process(self,Decoded_Packet,Start_Pointof_Record,End_Pointof_Record):
    Token= struct.unpack('!l',
                        Decoded_Packet[Start_Pointof_Record:
                                       Start_Pointof_Record+4])
    MKT_Info=[]

    MKT_INFO_sp = Start_Pointof_Record + 6
    for i in range(3):
        MKT_INFO_ep = MKT_INFO_sp + 24
        BuyVolume, BuyPrice, SellVolume, SellPrice,LTP,LastTradeTime = struct.unpack('!llllll', Decoded_Packet[MKT_INFO_sp:MKT_INFO_ep])
        MKT_INFO_output = {'BuyVolume': BuyVolume, 'BuyPrice': BuyPrice,
              'SellVolume': SellVolume, 'SellPrice': SellPrice, 'LTP': LTP,'LastTradeTime':LastTradeTime}
        print(MKT_INFO_output)
        MKT_Info.append(MKT_INFO_output)
        MKT_INFO_sp = MKT_INFO_ep

    Start_Pointof_Record=MKT_INFO_sp

    OpenInterest = struct.unpack('!l',
                          Decoded_Packet[Start_Pointof_Record:
                                         Start_Pointof_Record + 4])


    output = {'ID': 7201, "EXCH": 2, 'Token': Token, 'OpenInterest':OpenInterest,'Market_Info':MKT_Info}
    return output

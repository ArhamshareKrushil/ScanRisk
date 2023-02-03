import struct


def process(self,Decoded_Packet,Start_Pointof_Record):
    Token1, Token2, MbpBuy, MbpSell, LastActiveTime, TradedVolume, TotalTradedValue = struct.unpack('!llhhlld',
                                                                                                    Decoded_Packet[
                                                                                                    Start_Pointof_Record:Start_Pointof_Record + 28])
    MbpBuys=[]
    print('MBP_Buys')
    MbpBuys_sp = Start_Pointof_Record + 28
    for i in range(5):
        MbpBuys_ep = MbpBuys_sp + 10
        NoOrders, Volume, Price = struct.unpack('!hll', Decoded_Packet[MbpBuys_sp:MbpBuys_ep])
        MbpBuys_output = {'NoOrders': NoOrders, 'Volume': Volume, 'Price': Price}
        print(MbpBuys_output)
        MbpBuys_sp = MbpBuys_ep
        MbpBuys.append(MbpBuys_output)

    print('MBP_Sells')

    MbpSells = []
    MbpSells_sp = MbpBuys_sp

    for i in range(5):
        MbpSells_ep = MbpSells_sp + 10
        NoOrders, Volume, Price = struct.unpack('!hll', Decoded_Packet[MbpSells_sp:MbpSells_ep])
        MbpSells_output = {'NoOrders': NoOrders, 'Volume': Volume, 'Price': Price}
        print(MbpSells_output)
        MbpSells_sp = MbpSells_ep
        MbpSells.append(MbpSells_output)

    Start_Pointof_Record = MbpSells_ep

    Buy, Sell, OpenPriceDifference, DayHighPriceDifference, DayLowPriceDifference, \
    LTPDifference, LastUpdateTime = struct.unpack('!ddlllll',
                                                  Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record + 36])

    output = {'ID': 7211, "EXCH": 2, 'Token1': Token1, 'Token2': Token2, 'MbpBuy': MbpBuy,
              'MbpSell': MbpSell, 'LastActiveTime': LastActiveTime,
              'TradedVolume': TradedVolume, 'TotalTradedValue': TotalTradedValue,
              'Buy': Buy, 'Sell': Sell, 'OpenPriceDifference': OpenPriceDifference,
              'DayHighPriceDifference': DayHighPriceDifference, 'DayLowPriceDifference': DayLowPriceDifference,
              'LTPDifference': LTPDifference, 'LastUpdateTime': LastUpdateTime,'MbpBuys':MbpBuys,'MbpSells':MbpSells
              }
    return output

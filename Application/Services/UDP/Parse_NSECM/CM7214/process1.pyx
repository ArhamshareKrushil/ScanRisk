import struct




def process(self,Decoded_Packet,Start_Pointof_Record):

    Token, BookType, TradingStatus, Volume,IndicativeTradedQty, LTP, NetChangeIndicator, NetPriceChangeFromClosingPrice, \
                LTQ,LastTradeTime,ATP,FirstOpenPrice= \
            struct.unpack('!hhhlll2slllll', Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record + 40])

    MBP_buffer_sp = Start_Pointof_Record + 40
    for rb in range(10):
           MBP_buffer_ep=MBP_buffer_sp+12
           Quantity,Price,NumberOfOrders,BbBuySellFlag=struct.unpack('!llhh', Decoded_Packet[MBP_buffer_sp :MBP_buffer_ep])
           MBP_buffer_output={'Quantity':Quantity,'Price':Price,'NumberOfOrders':NumberOfOrders,'BbBuySellFlag':BbBuySellFlag}
           print(MBP_buffer_output)
           MBP_buffer_sp=MBP_buffer_ep

    Start_Pointof_Record = MBP_buffer_ep

    BbTotalBuyFlag, BbTotalSellFlag, TotalBuyQuantity, TotalSellQuantity = struct.unpack('!hhdd',
                                                                                         Decoded_Packet[
                                                                                         Start_Pointof_Record:Start_Pointof_Record + 20])

    #MBO_MBP_INDICATOR

    CLOSE, OPEN, HIGH, LOW = struct.unpack('!llll',Decoded_Packet[
                                                Start_Pointof_Record+20:Start_Pointof_Record + 36])

    output={'ID': 7214, 'Exch': 1, 'Token': Token, 'BookType': BookType,
              'TradingStatus': TradingStatus,
              'Volume': Volume,'IndicativeTradedQty':IndicativeTradedQty, 'LTP': LTP,
              'NetChangeIndicator': NetChangeIndicator,
              'NetPriceChangeFromClosingPrice': NetPriceChangeFromClosingPrice,
              'LTQ': LTQ, 'LastTradeTime': LastTradeTime,
              'ATP': ATP,
              'FirstOpenPrice': FirstOpenPrice,
             'BbTotalBuyFlag': BbTotalBuyFlag,
              'BbTotalSellFlag': BbTotalSellFlag, 'TotalBuyQuantity': TotalBuyQuantity,
              'TotalSellQuantity': TotalSellQuantity, 'CLOSE': CLOSE,
              'OPEN': OPEN, 'HIGH': HIGH, 'LOW': LOW}
    return output

import struct




def process(self,Decoded_Packet,Start_Pointof_Record):
    Token, BookType, TradingStatus, Volume, LTP, NetChangeIndicator, NetPriceChangeFromClosingPrice, \
    LTQ, LastTradeTime, ATP, AuctionNumber, AuctionStatus, InitiatorType, \
    InitiatorPrice, InitiatorQuantity, AuctionPrice, AuctionQuantity = \
        struct.unpack('!hhhll2sllllhhhllll', Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record + 54])

    Bids_MBO = []
    Asks_MBO = []
    Bids_MBP = []
    Asks_MBP = []

    MBO_buffer_sp = Start_Pointof_Record + 54
    for rb in range(10):
        TraderId = struct.unpack('!l', Decoded_Packet[MBO_buffer_sp:MBO_buffer_sp + 4])
        Qty = struct.unpack('!l', Decoded_Packet[MBO_buffer_sp + 4:MBO_buffer_sp + 8])
        Price = struct.unpack('!l', Decoded_Packet[MBO_buffer_sp + 8:MBO_buffer_sp + 12])
        MinFillQty = struct.unpack('!l', Decoded_Packet[MBO_buffer_sp + 14:MBO_buffer_sp + 18])

        MBO_buffer_output = {'TraderId': TraderId, 'Qty': Qty, 'Price': Price, 'MinFillQty': MinFillQty}
        print(MBO_buffer_output)
        MBO_buffer_sp = MBO_buffer_sp + 18
        if (rb < 5):
            Bids_MBO.append(MBO_buffer_output)
        else:
            Asks_MBO.append(MBO_buffer_output)

    MBP_buffer_sp = MBO_buffer_sp
    for rb in range(10):
        MBP_buffer_ep = MBP_buffer_sp + 12
        Quantity, Price, NumberOfOrders, BbBuySellFlag = struct.unpack('!llhh',
                                                                       Decoded_Packet[MBP_buffer_sp:MBP_buffer_ep])
        MBP_buffer_output = {'Quantity': Quantity, 'Price': Price, 'NumberOfOrders': NumberOfOrders,
                             'BbBuySellFlag': BbBuySellFlag}
        print(MBP_buffer_output)
        MBP_buffer_sp = MBP_buffer_ep
        if (rb < 5):
            Bids_MBP.append(MBP_buffer_output)
        else:
            Asks_MBP.append(MBP_buffer_output)

    Start_Pointof_Record = MBP_buffer_ep

    BbTotalBuyFlag, BbTotalSellFlag, TotalBuyQuantity, TotalSellQuantity, CLOSE, OPEN, HIGH, LOW = struct.unpack(
        '!hhddxxllll', Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record + 38])

    # MBO_MBP_INDICATOR

    output = {'ID': 7200,'Exch':1,'Token': Token, 'BookType': BookType, 'TradingStatus': TradingStatus,
              'Volume': Volume, 'LTP': LTP,
              'NetChangeIndicator': NetChangeIndicator,
              'NetPriceChangeFromClosingPrice': NetPriceChangeFromClosingPrice,
              'LTQ': LTQ, 'LastTradeTime': LastTradeTime, 'ATP': ATP,
              'AuctionNumber': AuctionNumber, 'AuctionStatus': AuctionStatus, 'InitiatorType': InitiatorType,
              'InitiatorPrice': InitiatorPrice,
              'InitiatorQuantity': InitiatorQuantity, 'AuctionPrice': AuctionPrice, 'AuctionQuantity': AuctionQuantity,
              'BbTotalBuyFlag': BbTotalBuyFlag, 'BbTotalSellFlag': BbTotalSellFlag,
              'TotalBuyQuantity': TotalBuyQuantity,
              'TotalSellQuantity': TotalSellQuantity, 'CLOSE': CLOSE, 'OPEN': OPEN, 'HIGH': HIGH,
              'LOW': LOW,'Bids_MBO':Bids_MBO,'Asks_MBO':Asks_MBO,'Bids_MBP':Bids_MBP,'Asks_MBP':Asks_MBP
              }
    return output

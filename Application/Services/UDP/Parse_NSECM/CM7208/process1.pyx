import struct

``


def process(self,Decoded_Packet,Start_Pointof_Record):
    Token = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record + 2])[0]
    BookType = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 2:Start_Pointof_Record + 4])[0]
    TradingStatus = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 4:Start_Pointof_Record + 6])[0]

    Volume = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 6:Start_Pointof_Record + 10])[0]
    LTP = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 10:Start_Pointof_Record + 14])[0] / 100.0
    NetChangeIndicator = struct.unpack('!2s', Decoded_Packet[Start_Pointof_Record + 14:Start_Pointof_Record + 16])[0]
    NetPriceChangeFromClosingPrice = \
    struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 16:Start_Pointof_Record + 20])[0] / 100.0
    LTQ = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 20:Start_Pointof_Record + 24])[0]
    LastTradeTime = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 24:Start_Pointof_Record + 28])
    ATP = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 28:Start_Pointof_Record + 32])[0]
    AuctionNumber = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 32:Start_Pointof_Record + 34])[0]
    AuctionStatus = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 34:Start_Pointof_Record + 36])[0]
    InitiatorType = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 36:Start_Pointof_Record + 38])[0]
    InitiatorPrice = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 38:Start_Pointof_Record + 42])[0]
    InitiatorQuantity = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 42:Start_Pointof_Record + 46])[0]
    AuctionPrice = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 46:Start_Pointof_Record + 50])[0]
    AuctionQuantity = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 50:Start_Pointof_Record + 54])[0]

    buffer_sp = Start_Pointof_Record + 54
    Bids = []
    Asks = []

    for rb in range(10):
        buffer_ep = buffer_sp + 12
        Quantity, Price, NumberOfOrders, BbBuySellFlag = struct.unpack('!llhh', Decoded_Packet[buffer_sp:buffer_ep])
        Price /= 100
        buffer_output = {'Quantity': Quantity, 'Price': Price, 'NumberOfOrders': NumberOfOrders,
                         'BbBuySellFlag': BbBuySellFlag}
        if (rb < 5):
            Bids.append(buffer_output)
        else:
            Asks.append(buffer_output)

        buffer_sp = buffer_ep

    BbTotalBuyFlag = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 174:Start_Pointof_Record + 176])[0]
    BbTotalSellFlag = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 176:Start_Pointof_Record + 178])[0]
    TotalBuyQuantity = struct.unpack('!d', Decoded_Packet[Start_Pointof_Record + 178:Start_Pointof_Record + 186])[0]
    TotalSellQuantity = struct.unpack('!d', Decoded_Packet[Start_Pointof_Record + 186:Start_Pointof_Record + 194])[0]

    # MBP_INDICATOR=

    CLOSE = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 196:Start_Pointof_Record + 200])[0] / 100.0
    OPEN = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 200:Start_Pointof_Record + 204])[0] / 100.0
    HIGH = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 204:Start_Pointof_Record + 208])[0] / 100.0
    LOW = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 208:Start_Pointof_Record + 212])[0] / 100.0

    output = {'ID': 7208,'Exch':1,'Token': Token, 'BookType': BookType, 'TradingStatus': TradingStatus,
              'Volume': Volume, 'LTP': LTP,
              'NetChangeIndicator': NetChangeIndicator,
              'NetPriceChangeFromClosingPrice': NetPriceChangeFromClosingPrice,
              'LTQ': LTQ, 'LastTradeTime': LastTradeTime, 'ATP': ATP,
              'AuctionNumber': AuctionNumber, 'AuctionStatus': AuctionStatus, 'InitiatorType': InitiatorType,
              'InitiatorPrice': InitiatorPrice,
              'InitiatorQuantity': InitiatorQuantity, 'AuctionPrice': AuctionPrice, 'AuctionQuantity': AuctionQuantity,
              'BbTotalBuyFlag': BbTotalBuyFlag,
              'BbTotalSellFlag': BbTotalSellFlag, 'TotalBuyQuantity': TotalBuyQuantity,
              'TotalSellQuantity': TotalSellQuantity, 'CLOSE': CLOSE,
              'OPEN': OPEN, 'HIGH': HIGH, 'LOW': LOW, 'Bids': {'Bid1': Bids[0], 'Bid2': Bids[1],
                                                               'Bid3': Bids[2], 'Bid4': Bids[3], 'Bid5': Bids[4]},
              'Asks': {'Ask1': Asks[0], 'Ask2': Asks[1], 'Ask3': Asks[2], 'Ask4': Asks[3], 'Ask5': Asks[4]}
              }
    return output

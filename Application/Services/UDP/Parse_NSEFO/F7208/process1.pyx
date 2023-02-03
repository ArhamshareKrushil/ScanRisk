import struct



def process(self,Decoded_Packet,Start_Pointof_Record):
    Token = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record + 4])[0]
    BookType = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 4:Start_Pointof_Record + 6])[0]
    TradingStatus = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 6:Start_Pointof_Record + 8])[0]
    Volume = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 8:Start_Pointof_Record + 12])[0]
    LTP = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 12:Start_Pointof_Record + 16])[0] / 100.0
    NetChangeIndicator = struct.unpack('!c', Decoded_Packet[Start_Pointof_Record + 16:Start_Pointof_Record + 17])[0].decode()
    NetPriceChangeFromClosingPrice =struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 18:Start_Pointof_Record + 22])[0] / 100.0
    LTQ = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 22:Start_Pointof_Record + 26])[0]
    LastTradeTime = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 26:Start_Pointof_Record + 30])
    ATP = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 30:Start_Pointof_Record + 34])[0] / 100
    AuctionNumber = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 34:Start_Pointof_Record + 36])[0]
    AuctionStatus = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 36:Start_Pointof_Record + 38])[0]
    InitiatorType = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 38:Start_Pointof_Record + 40])[0]
    InitiatorPrice = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 40:Start_Pointof_Record + 44])[0] / 100
    InitiatorQuantity = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 44:Start_Pointof_Record + 48])[0]
    AuctionPrice = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 48:Start_Pointof_Record + 52])[0] / 100
    AuctionQuantity = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 52:Start_Pointof_Record + 56])[0]

    symbol = self.fo_contract[Token - 35000, 3]

    buffer_sp = Start_Pointof_Record + 56
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

    BbTotalBuyFlag = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 176:Start_Pointof_Record + 178])[0]
    BbTotalSellFlag = struct.unpack('!h', Decoded_Packet[Start_Pointof_Record + 178:Start_Pointof_Record + 180])[0]
    TotalBuyQuantity = struct.unpack('!d', Decoded_Packet[Start_Pointof_Record + 180:Start_Pointof_Record + 188])[0]
    TotalSellQuantity = struct.unpack('!d', Decoded_Packet[Start_Pointof_Record + 188:Start_Pointof_Record + 196])[0]

    # ST_INDICATOR=

    CLOSE = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 198:Start_Pointof_Record + 202])[0] / 100.0
    OPEN = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 202:Start_Pointof_Record + 206])[0] / 100.0
    HIGH = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 206:Start_Pointof_Record + 210])[0] / 100.0
    LOW = struct.unpack('!l', Decoded_Packet[Start_Pointof_Record + 210:Start_Pointof_Record + 214])[0] / 100.0

    output = {'ID': 1502, 'Exch': 2, 'Token': Token, 'symbol': symbol, 'BookType': BookType,
              'TradingStatus': TradingStatus,
              'Volume': Volume, 'LTP': LTP,
              'NetChangeIndicator': NetChangeIndicator,
              'NetPriceChangeFromClosingPrice': NetPriceChangeFromClosingPrice,
              'LTQ': LTQ, 'LastTradeTime': LastTradeTime,
              'ATP': ATP,
              'AuctionNumber': AuctionNumber, 'AuctionStatus': AuctionStatus, 'InitiatorType': InitiatorType,
              'InitiatorPrice': InitiatorPrice,
              'InitiatorQuantity': InitiatorQuantity, 'AuctionPrice': AuctionPrice,
              'AuctionQuantity': AuctionQuantity, 'BbTotalBuyFlag': BbTotalBuyFlag,
              'BbTotalSellFlag': BbTotalSellFlag, 'TotalBuyQuantity': TotalBuyQuantity,
              'TotalSellQuantity': TotalSellQuantity, 'CLOSE': CLOSE,
              'OPEN': OPEN, 'HIGH': HIGH, 'LOW': LOW, 'Bids': {'Bid1': Bids[0], 'Bid2': Bids[1],
                                                               'Bid3': Bids[2], 'Bid4': Bids[3], 'Bid5': Bids[4]},
              'Asks': {'Ask1': Asks[0], 'Ask2': Asks[1], 'Ask3': Asks[2], 'Ask4': Asks[3], 'Ask5': Asks[4]}
              }



    output1 = {'ID': 1501, 'Exch': 2, 'Token': Token, 'symbol': symbol, 'BookType': BookType,
               'TradingStatus': TradingStatus,
               'Volume': Volume, 'LTP': LTP, 'Bid': Bids[0]['Price'], 'BQ': Bids[0]['Quantity'],
               'Ask': Asks[0]['Price'], 'AQ': Bids[0]['Quantity'],
               'NetChangeIndicator': NetChangeIndicator, '%CH': str(LTP - NetPriceChangeFromClosingPrice),
               'LTQ': LTQ, 'LTT': LastTradeTime, 'ATP': ATP, 'CLOSE': CLOSE,
               'OPEN': OPEN, 'HIGH': HIGH, 'LOW': LOW}


    return output1
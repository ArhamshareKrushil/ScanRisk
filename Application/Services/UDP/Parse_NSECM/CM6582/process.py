import struct


def process(self,Compressed_Packet,Start_Pointof_Record,):
    Token, AuctionNumber, AuctionStatus, InitiatorType, TotalBuyQty, BestBuyPrice, TotalSellQty, BestSellPrice \
        , AuctionPrice, AuctionQty, SettlementPeriod = struct.unpack('!hhhhllllllh',
                                                                     Compressed_Packet[
                                                                     Start_Pointof_Record:Start_Pointof_Record + 279])

    output = {'ID': 6582,'Exch':1,'Token': Token, 'AuctionNumber': AuctionNumber, 'AuctionStatus': AuctionStatus,
              'InitiatorType': InitiatorType,
              'TotalBuyQty': TotalBuyQty, 'BestBuyPrice': BestBuyPrice, 'TotalSellQty': TotalSellQty,
              'BestSellPrice': BestSellPrice,
              'AuctionPrice': AuctionPrice, 'AuctionQty': AuctionQty, 'SettlementPeriod': SettlementPeriod}
    return output
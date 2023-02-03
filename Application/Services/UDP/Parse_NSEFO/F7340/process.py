import struct



def process(self,Compressed_Packet,Start_Pointof_Record):
    Token, InstrumentName, Symbol, Series, ExpiryDate, StrikePrice, OptionType, CALevel, \
    PermittedToTrade, IssuedCapital, WarningQuantity, FreezeQuantity, CreditRating = struct.unpack(
        '!l6s10s2sll2shhdll12s',
        Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record + 64])

    # ST_SEC_ELIGIBILITY

    Start_Pointof_Record = Start_Pointof_Record + 64
    IssueRate, IssueStartDate, InterestPaymentDate, IssueMaturityDate, MarginPercentage, MinimumLotQuantity, BoardLotQuantity, TickSize, \
    Name, Reserved, ListingDate, ExpulsionDate, ReAdmissionDate, RecordDate, LowPriceRange, HighPriceRange, ExpiryDate1, NoDeliveryStartDate, \
    NoDeliveryEndDate = struct.unpack('!hlllllll25sclllllllll',
                                      Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record + 92])

    # ST_ELIGIBLITY_ INDICATORS
    # ST_PURPOSE
    Start_Pointof_Record = Start_Pointof_Record + 92

    BookClosureStartDate, BookClosureEndDate, ExerciseStartDate, ExerciseEndDate, OldToken, AssetInstrument, AssetName, AssetToken, IntrinsicValue, \
    ExtrinsicValue, LocalUpdateDateTime, DeleteFlag, Remark, BasePrice \
        = struct.unpack('!lllll6s10slllxxlc25sl', Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record + 84])

    output = {'ID': 7340,'Exch':2,'Token': Token, 'InstrumentName': InstrumentName, 'Symbol': Symbol, 'Series': Series,
              'ExpiryDate': ExpiryDate,
              'StrikePrice': StrikePrice, 'OptionType': OptionType,
              'CALevel': CALevel, 'PermittedToTrade': PermittedToTrade, 'IssuedCapital': IssuedCapital,
              'WarningQuantity': WarningQuantity,
              'FreezeQuantity': FreezeQuantity, 'CreditRating': CreditRating, 'IssueRate': InstrumentName,
              'IssueStartDate': IssueStartDate, 'InterestPaymentDate': InterestPaymentDate,
              'IssueMaturityDate': IssueMaturityDate, 'MarginPercentage': MarginPercentage,
              'MinimumLotQuantity': MinimumLotQuantity,
              'BoardLotQuantity': BoardLotQuantity, 'TickSize': TickSize, 'Name': Name, 'Reserved': Reserved,
              'ListingDate': ListingDate, 'ExpulsionDate': ExpulsionDate, 'ReAdmissionDate': ReAdmissionDate,
              'RecordDate': RecordDate, 'LowPriceRange': LowPriceRange, 'HighPriceRange': HighPriceRange,
              'ExpiryDate1': ExpiryDate1,
              'NoDeliveryStartDate': NoDeliveryStartDate, 'NoDeliveryEndDate': NoDeliveryEndDate,
              'BookClosureStartDate': BookClosureStartDate,
              'BookClosureEndDate': BookClosureEndDate, 'ExerciseStartDate': ExerciseStartDate,
              'ExerciseEndDate': ExerciseEndDate, 'OldToken': OldToken,
              'AssetInstrument': AssetInstrument, 'AssetName': AssetName, 'AssetToken': AssetToken,
              'IntrinsicValue': IntrinsicValue, 'ExtrinsicValue': ExtrinsicValue,
              'LocalUpdateDateTime': LocalUpdateDateTime, 'DeleteFlag': DeleteFlag,
              'Remark': Remark, 'BasePrice': BasePrice}
    return output
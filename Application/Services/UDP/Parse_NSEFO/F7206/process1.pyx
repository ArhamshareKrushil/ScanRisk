
import struct
cpdef pro(object self,object Decoded_Packet,int Start_Pointof_Record,int End_Pointof_Record):

    cdef long Token, FillPrice, FillVolume, OpenInterest, Day_Hi_OI, Day_Lo_OI
    cdef int MarketType

    Token, MarketType, FillPrice, FillVolume, OpenInterest,Day_Hi_OI, Day_Lo_OI = struct.unpack('!lhlllll',Decoded_Packet[Start_Pointof_Record:End_Pointof_Record])

    cdef double ltp = FillPrice / 100.0
    cdef dict output = {'ID': 7202,'Exch':2, 'Token': Token, 'MarketType': MarketType, 'FillPrice': ltp,'FillVolume': FillVolume, 'OpenInterest': OpenInterest,'Day_Hi_OI': Day_Hi_OI, 'Day_Lo_OI': Day_Lo_OI}
    return output

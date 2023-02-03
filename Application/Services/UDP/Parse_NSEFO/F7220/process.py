import struct



def process(self,Decoded_Packet,Start_Pointof_Record):
    MsgCount= struct.unpack('!l',Decoded_Packet[Start_Pointof_Record:Start_Pointof_Record +4 ])


    PPRD=[]
    #PRICE_PROTECTION_RANGE_DETAILS
    PPRD_sp=Start_Pointof_Record +4
    for p in range(25):
        PPRD_ep=PPRD_sp+12
        Token,HighExecBand,LowExecBand=struct.unpack('!l',Decoded_Packet[PPRD_sp:PPRD_ep])
        PPRD_output={'Token':Token,'HighExecBand':HighExecBand,'LowExecBand':LowExecBand}
        PPRD.append(PPRD_output)
        PPRD_sp=PPRD_ep

    output={'MsgCount':MsgCount,'PRICE_PROTECTION_RANGE_DETAILS':PPRD}
    return output
import struct



def process(self,Compressed_Packet,Start_Pointof_Record):
    BranchNumber, BrokerNumber, ActionCode, Reserved, BroadcastMessageLength, BroadcastMessage = struct.unpack(
        '!h5s3s4sxxh239s', Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record + 257])

    output = {'ID': 6501, 'Exch': 1, 'BranchNumber': BranchNumber, 'BrokerNumber': BrokerNumber,
              'ActionCode': ActionCode, 'Reserved': Reserved,
              'BroadcastMessageLength': BroadcastMessageLength,
              'BroadcastMessage': BroadcastMessage}

    return output

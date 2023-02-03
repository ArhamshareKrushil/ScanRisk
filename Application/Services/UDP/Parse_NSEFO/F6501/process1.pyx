import struct
import time
import traceback


def process(self,Compressed_Packet,Start_Pointof_Record):
    BranchNumber, BrokerNumber, ActionCode, Reserved, BroadcastMessageLength, BroadcastMessage = struct.unpack(
        '!h5s3sxx26sh239s', Compressed_Packet[Start_Pointof_Record:Start_Pointof_Record + 279])

    output = {'ID': 6501, 'Exch': 2, 'BranchNumber': BranchNumber, 'BrokerNumber': BrokerNumber,
              'ActionCode': ActionCode, 'Reserved': Reserved,
              'BroadcastMessageLength': BroadcastMessageLength,
              'BroadcastMessage': BroadcastMessage}

    return output

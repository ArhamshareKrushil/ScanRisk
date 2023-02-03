import struct
from Application.Services.UDP.Parse_NSECM.CM7216 import process





def getOutput(self,Compressed_Packet):
    NoOf_Records = struct.unpack('!h', Compressed_Packet[48:50])
    Start_Pointof_Record= 50
    for ik in range(NoOf_Records[0]):
        End_Pointof_Record = Start_Pointof_Record + 71

        output = process.process(self, Compressed_Packet, Start_Pointof_Record, End_Pointof_Record)



        print(output)
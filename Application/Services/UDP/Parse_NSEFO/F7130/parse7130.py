from  Application.Services.UDP.Parse_NSEFO.F7130 import process
import struct



def getOutput(self,Compressed_Packet):


    NoOf_Records = struct.unpack('!h', Compressed_Packet[20:22])
    packetLen = struct.unpack('!h', Compressed_Packet[46:48])
    print('packetLen 7130',packetLen)
    Start_Pointof_Record = 48
    for ik in range(NoOf_Records[0]):
        End_Pointof_Record = Start_Pointof_Record + 8
        output = process.process(self, Compressed_Packet, Start_Pointof_Record,End_Pointof_Record)
        print(output)
        self.sender.sendData(output)
        Start_Pointof_Record = End_Pointof_Record
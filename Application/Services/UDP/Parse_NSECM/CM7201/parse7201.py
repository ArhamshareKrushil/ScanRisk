from Application.Services.UDP.Parse_NSECM.CM7201 import process


import struct



def getOutput(self,Decoded_Packet):

    NoOf_Records = struct.unpack('!h', Decoded_Packet[48:50])
    Start_Pointof_Record= 50
    for ik in range(NoOf_Records[0]):
        End_Pointof_Record = Start_Pointof_Record + 80

        output = process.process(self, Decoded_Packet, Start_Pointof_Record, End_Pointof_Record)
        print(output)
        self.sender.sendData(output)

        Start_Pointof_Record = End_Pointof_Record


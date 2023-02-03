import struct
from Application.Services.UDP.Parse_NSEFO.F7208 import process
from Application.Services.UDP.Parse_NSEFO.F7208 import process







def getOutput(self,Decoded_Packet):

    NoOf_Records = struct.unpack('!h', Decoded_Packet[48:50])
    Start_Pointof_Record = 50

    for ik in range(NoOf_Records[0]):
        End_Pointof_Record = Start_Pointof_Record + 214

        output1 = process.process(self, Decoded_Packet, Start_Pointof_Record)
        # print(output1)

        if output1:
            # print('7208')
            self.sgData7208.emit(output1)



        # self.sender.sendData(output1)
        Start_Pointof_Record = End_Pointof_Record